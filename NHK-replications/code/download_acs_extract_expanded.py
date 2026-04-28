"""Create and download an expanded IPUMS USA extract for NHK Task 1.

This script does four things in one reproducible flow:

1. It scans the Task 1 submitted replication bundles and collects the union of
   IPUMS USA variables that researchers explicitly extracted or referenced in
   code.
2. It constrains the extract to the one-year ACS samples from 2006 through 2016,
   which matches the instructions for the least-information task.
3. It submits the resulting extract definition to the IPUMS API and waits for
   the IPUMS servers to finish building the extract.
4. It downloads the completed extract files into replication-materials using the
   filename stem ACS_extract_expanded.

The implementation intentionally uses only the Python standard library so that
it can run in the project environment without adding new dependencies.
"""

from __future__ import annotations

import json
import gzip
import re
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib import error, request


# These are the only samples allowed by the attached task instructions:
# one-year ACS files from 2006 through 2016, and no PRCS / 3-year / 5-year files.
USA_ONE_YEAR_ACS_SAMPLES = [f"us{year}a" for year in range(2006, 2017)]

# The API documentation shows that microdata extracts are created by calling the
# shared extracts endpoint with the collection name in the query string.
IPUMS_API_BASE_URL = "https://api.ipums.org"
IPUMS_API_COLLECTION = "usa"
IPUMS_API_VERSION = "2"

# Polling every minute is slow enough to be polite to the API while still giving
# useful progress updates during what can be a long extract build.
POLL_SECONDS = 60

# The download links returned by IPUMS use semantic keys rather than the final
# filenames we want in replication-materials. This mapping lets us save the files
# with the requested ACS_extract_expanded filename stem.
DOWNLOAD_KEY_TO_SUFFIX = {
    "data": ".dat.gz",
    "ddiCodebook": ".xml",
    "basicCodebook": ".cbk",
    "stataCommandFile": ".do",
    "rCommandFile": ".R",
    "sasCommandFile": ".sas",
    "spssCommandFile": ".sps",
}

# A small number of researcher-observed mnemonics are not directly requestable in
# the current USA API even though they point to a nearby valid harmonized
# variable. We map those to the current requestable equivalent.
VARIABLE_ALIAS_MAP = {
    "MIGTYPE1": "MIGTYPED5",
}

# IPUMS USA quality flags are not requested as standalone variables in the API.
# Instead, they are requested by turning on dataQualityFlags for the underlying
# parent variable(s). These mappings cover the quality-flag mnemonics observed in
# the submitted Task 1 replications.
QUALITY_FLAG_PARENT_VARIABLES = {
    "QAGE": ["AGE"],
    "QBPL": ["BPL"],
    "QCITIZEN": ["CITIZEN"],
    "QEDUC": ["EDUC"],
    "QEMPSTAT": ["EMPSTAT"],
    "QHISPAN": ["HISPAN"],
    "QLANGUAG": ["LANGUAGE", "SPEAKENG"],
    "QMARST": ["MARST"],
    "QMIGRAT1": ["MIGRATE1"],
    "QOCC": ["OCC"],
    "QRACE": ["RACE"],
    "QRELATE": ["RELATE"],
    "QSCHOOL": ["SCHOOL"],
    "QSEX": ["SEX"],
    "QSPEAKEN": ["SPEAKENG"],
    "QUHRSWOR": ["UHRSWORK"],
    "QWKSWORK2": ["WKSWORK2"],
    "QWORKEDY": ["WORKEDYR"],
    "QYRIMM": ["YRIMMIG"],
    "QYRNATUR": ["YRNATUR"],
}

REVERSE_VARIABLE_ALIAS_MAP = {
    target: source for source, target in VARIABLE_ALIAS_MAP.items()
}

PARENT_TO_QUALITY_FLAGS: dict[str, set[str]] = defaultdict(set)
for quality_flag, parents in QUALITY_FLAG_PARENT_VARIABLES.items():
    for parent_variable in parents:
        PARENT_TO_QUALITY_FLAGS[parent_variable].add(quality_flag)


def repo_root() -> Path:
    """Return the NHK-replications repository root.

    This script lives in NHK-replications/code, so walking up one directory from
    the script file yields the repository root in a stable, machine-independent
    way.
    """

    return Path(__file__).resolve().parents[1]


def replication_materials_dir() -> Path:
    """Return the replication-materials directory used by the task."""

    return repo_root() / "replication-materials"


def submitted_replications_dir() -> Path:
    """Return the directory containing the submitted replication bundles."""

    return repo_root() / "meta_analysis" / "Submitted Replications"


def local_extract_layout_path() -> Path:
    """Return the existing Task 1 ACS layout file.

    We use the current layout file as a starting lexicon of known-good IPUMS USA
    variable names so that code-token matching later on only admits actual IPUMS
    mnemonics rather than arbitrary words that happen to appear in scripts.
    """

    return replication_materials_dir() / "usa_00042.do"


def api_key_env_path() -> Path:
    """Return the path to the secrets file that stores the IPUMS API key."""

    return Path.home() / ".apikeys" / "keys.env"


def output_stem_path() -> Path:
    """Return the requested filename stem for the downloaded extract files."""

    return replication_materials_dir() / "ACS_extract_expanded"


def load_ipums_api_key(env_path: Path) -> str:
    """Read IPUMS_API_KEY from the user's key file.

    The instructions explicitly say to use the key stored in ~/.apikeys/keys.env.
    We parse the file ourselves here so the script does not depend on dotenv.
    """

    if not env_path.exists():
        raise FileNotFoundError(f"API key file not found: {env_path}")

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "IPUMS_API_KEY":
            value = value.strip().strip('"').strip("'")
            if value:
                return value

    raise RuntimeError(f"IPUMS_API_KEY was not found in {env_path}")


def read_text(path: Path) -> str | None:
    """Read a text-like file using a forgiving UTF-8 decode.

    We only need plain-text access for the submitted code files and IPUMS DDI / do
    files. If a file cannot be decoded cleanly, returning None is safer than
    failing the entire extract-building workflow.
    """

    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def parse_infix_variables(stata_text: str) -> set[str]:
    """Extract variable names from an IPUMS Stata infix layout file.

    IPUMS Stata command files declare each variable with a type, mnemonic, and
    fixed-width position. We only want the mnemonic.
    """

    if "infix" not in stata_text.lower():
        return set()

    variable_pattern = re.compile(
        r"^\s*(?:byte|int|long|double|float|str\d*|strl?|str)\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)\s+\d+-\d+",
        re.IGNORECASE | re.MULTILINE,
    )
    return {match.lower() for match in variable_pattern.findall(stata_text)}


def parse_ddi_variables(xml_text: str) -> set[str]:
    """Extract variable names from an IPUMS DDI codebook file."""

    variable_pattern = re.compile(
        r'<var\b[^>]*\bname="([A-Za-z0-9_]+)"',
        re.IGNORECASE,
    )
    return {match.lower() for match in variable_pattern.findall(xml_text)}


def collect_observed_variables() -> list[str]:
    """Build the observed variable superset from Task 1 submitted materials.

    The logic mirrors the manual comparison work already done in this repository:

    - First collect variables that appear in explicit IPUMS extract files
      (Stata .do loaders and DDI .xml codebooks).
    - Then scan code files for tokens that match the known IPUMS variable lexicon.

    Using the lexicon guard keeps us from accidentally treating ordinary English
    words as variables while still allowing code-only variables to be included.
    """

    root = submitted_replications_dir()
    task1_dirs = [
        path / "Replication Task 1"
        for path in root.iterdir()
        if path.is_dir() and path.name.isdigit() and (path / "Replication Task 1").exists()
    ]

    explicit_extract_vars: set[str] = set()
    code_tokens_by_task: dict[Path, set[str]] = defaultdict(set)

    # Seed the lexicon with the variables already present in the current extract.
    # This allows code-only references to already-known IPUMS variables to pass
    # the token filter even if no researcher bundled an explicit DDI or .do file.
    lexicon = parse_infix_variables(
        local_extract_layout_path().read_text(encoding="utf-8", errors="ignore")
    )

    token_pattern = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)\b")
    extract_suffixes = {".do", ".xml"}
    code_suffixes = {".do", ".r", ".rmd", ".py", ".ipynb", ".ado"}

    for task1_dir in task1_dirs:
        for path in task1_dir.rglob("*"):
            if not path.is_file():
                continue

            suffix = path.suffix.lower()
            relative_path = str(path.relative_to(root)).lower()

            if suffix in extract_suffixes:
                text = read_text(path)
                if not text:
                    continue

                variables = set()
                if suffix == ".do":
                    variables |= parse_infix_variables(text)
                elif suffix == ".xml":
                    variables |= parse_ddi_variables(text)

                # We only want ACS / IPUMS extract metadata, not arbitrary .xml or
                # .do files that happen to sit in the same bundle.
                if variables and re.search(r"usa_\d+|ipums|acs", relative_path):
                    explicit_extract_vars |= variables
                    lexicon |= variables

            if suffix in code_suffixes:
                text = read_text(path)
                if not text:
                    continue
                code_tokens_by_task[task1_dir] |= {
                    token.lower() for token in token_pattern.findall(text)
                }

    observed_vars = set(explicit_extract_vars)
    for token_set in code_tokens_by_task.values():
        observed_vars |= token_set & lexicon

    if not observed_vars:
        raise RuntimeError("No observed IPUMS variables were found in Submitted Replications.")

    return sorted(variable.upper() for variable in observed_vars)


def build_request_variables(
    observed_variables: list[str],
) -> tuple[dict[str, dict[str, Any]], dict[str, str], list[str]]:
    """Translate observed mnemonics into a valid USA API variable payload.

    This handles two request-construction details that the raw observed mnemonic
    list does not capture:

    - aliases such as MIGTYPE1 -> MIGTYPED5
    - quality flags requested via dataQualityFlags on parent variables rather than
      as standalone Q* variables
    """

    request_variables: dict[str, dict[str, Any]] = {}
    alias_notes: dict[str, str] = {}
    requested_quality_flags: list[str] = []

    for observed_variable in sorted(set(observed_variables)):
        if observed_variable in QUALITY_FLAG_PARENT_VARIABLES:
            requested_quality_flags.append(observed_variable)
            for parent_variable in QUALITY_FLAG_PARENT_VARIABLES[observed_variable]:
                request_variables.setdefault(parent_variable, {})["dataQualityFlags"] = True
            continue

        request_variable = VARIABLE_ALIAS_MAP.get(observed_variable, observed_variable)
        if request_variable != observed_variable:
            alias_notes[observed_variable] = request_variable

        request_variables.setdefault(request_variable, {})

    return request_variables, alias_notes, requested_quality_flags


def build_extract_request(variables: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Construct the IPUMS USA extract request payload."""

    return {
        "description": (
            "ACS_extract_expanded: one-year ACS 2006-2016, superset of Task 1 "
            "researcher-observed IPUMS USA variable choices"
        ),
        "dataStructure": {"rectangular": {"on": "P"}},
        "dataFormat": "fixed_width",
        "samples": {sample: {} for sample in USA_ONE_YEAR_ACS_SAMPLES},
        "variables": variables,
    }


def extract_invalid_variables_from_error(error_message: str) -> list[str]:
    """Parse rejected variable mnemonics out of an IPUMS validation error.

    The API returns messages like "Invalid variable name: EDUC_MOM" and
    "Invalid mnemonic: QAGE" inside the error detail payload. It also returns
    sample-availability messages such as "MIGTYPED5: This variable is not
    available in any of the samples currently selected." Pulling those back out
    lets us retry automatically with the requestable subset instead of forcing the
    user to manually prune the variable list.
    """

    invalid_patterns = [
        re.compile(
            r"Invalid (?:variable name|mnemonic):\s*([A-Z0-9_]+)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\b([A-Z0-9_]+):\s*This variable is not available in any of the samples currently selected",
            re.IGNORECASE,
        ),
    ]
    invalid_variables: list[str] = []
    for invalid_pattern in invalid_patterns:
        invalid_variables.extend(match.upper() for match in invalid_pattern.findall(error_message))

    # Preserve first-seen order so the audit file remains easy to read.
    return list(dict.fromkeys(invalid_variables))


def ipums_api_request(
    method: str,
    url: str,
    api_key: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Send an authenticated request to the IPUMS API and decode the JSON body."""

    body = None
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    http_request = request.Request(url=url, data=body, headers=headers, method=method)

    try:
        with request.urlopen(http_request) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"IPUMS API request failed with status {exc.code} for {url}: {details}"
        ) from exc


def download_file(url: str, destination: Path, api_key: str) -> None:
    """Download one completed extract artifact to disk."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    http_request = request.Request(url=url, headers={"Authorization": api_key})

    try:
        with request.urlopen(http_request) as response, destination.open("wb") as handle:
            shutil.copyfileobj(response, handle, length=1024 * 1024)
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"Download failed with status {exc.code} for {url}: {details}"
        ) from exc


def save_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON with stable formatting for reproducibility."""

    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def output_path_for_download(download_key: str, download_url: str) -> Path:
    """Translate an IPUMS download link into the requested local filename.

    Known artifact types are saved as ACS_extract_expanded plus their usual file
    extension. Unknown artifacts still get saved, but with the download key folded
    into the filename so nothing is silently dropped.
    """

    stem = output_stem_path()
    if download_key in DOWNLOAD_KEY_TO_SUFFIX:
        return stem.with_name(stem.name + DOWNLOAD_KEY_TO_SUFFIX[download_key])

    # Fall back to the extension used in the original URL so uncommon file types
    # still remain identifiable.
    suffix = ""
    download_name = download_url.rstrip("/").rsplit("/", 1)[-1]
    if "." in download_name:
        suffix = "." + download_name.split(".", 1)[1]
    return stem.with_name(f"{stem.name}_{download_key}{suffix}")


def original_extract_stem(status_response: dict[str, Any]) -> str:
    """Recover the original IPUMS filename stem from the download links.

    IPUMS names files with a request number such as usa_00044.dat.gz. We rename
    the files on disk, so we also need the original stem in order to rewrite the
    internal references in the downloaded command files.
    """

    download_links = status_response.get("downloadLinks", {})
    data_link = download_links.get("data")
    if not data_link:
        raise RuntimeError("Completed extract response did not include the data download link.")

    download_name = data_link["url"].rstrip("/").rsplit("/", 1)[-1]
    # Remove all suffixes so usa_00044.dat.gz becomes usa_00044.
    stem = download_name
    while "." in stem:
        stem = stem.rsplit(".", 1)[0]
    return stem


def gunzip_data_file(compressed_path: Path, uncompressed_path: Path) -> None:
    """Expand the downloaded .dat.gz file into a plain .dat file."""

    with gzip.open(compressed_path, "rb") as source, uncompressed_path.open("wb") as target:
        shutil.copyfileobj(source, target, length=1024 * 1024)


def rewrite_text_file(path: Path, old_text: str, new_text: str) -> None:
    """Replace text inside a downloaded command file if needed."""

    if not path.exists():
        return

    text = path.read_text(encoding="utf-8", errors="ignore")
    updated_text = text.replace(old_text, new_text)
    if updated_text != text:
        path.write_text(updated_text, encoding="utf-8")


def normalize_downloaded_artifacts(status_response: dict[str, Any]) -> None:
    """Make the renamed extract artifacts internally consistent.

    The downloaded command files still refer to the original IPUMS stem such as
    usa_00044. After renaming the files to ACS_extract_expanded.*, we also want:

    - an uncompressed ACS_extract_expanded.dat file for command-file workflows
    - internal references in .do / .R / .sas / .sps updated to the new stem
    """

    stem = output_stem_path()
    compressed_data_path = stem.with_name(stem.name + ".dat.gz")
    uncompressed_data_path = stem.with_name(stem.name + ".dat")
    if compressed_data_path.exists():
        print(f"Expanding {compressed_data_path.name} -> {uncompressed_data_path.name}")
        gunzip_data_file(compressed_data_path, uncompressed_data_path)

    old_stem = original_extract_stem(status_response)
    new_stem = stem.name
    for suffix in [".do", ".R", ".sas", ".sps"]:
        rewrite_text_file(stem.with_name(stem.name + suffix), old_stem, new_stem)


def submit_extract(api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Submit the IPUMS USA extract request and return the API response."""

    url = (
        f"{IPUMS_API_BASE_URL}/extracts?collection={IPUMS_API_COLLECTION}"
        f"&version={IPUMS_API_VERSION}"
    )
    return ipums_api_request("POST", url, api_key, payload)


def submit_extract_with_validation_retry(
    api_key: str,
    observed_variables: list[str],
) -> tuple[dict[str, Any], list[str], list[str]]:
    """Submit the extract, automatically pruning only API-invalid variables.

    The task instructions constrain us to a harmonized, spec-compliant USA extract.
    Some mnemonics observed in the submitted replications are not valid under those
    constraints in the current IPUMS API. When the API explicitly rejects such
    mnemonics, we drop only the rejected names and immediately resubmit.
    """

    remaining_variables = list(observed_variables)
    excluded_variables: list[str] = []

    while True:
        request_variables, _, _ = build_request_variables(remaining_variables)
        payload = build_extract_request(request_variables)
        try:
            response = submit_extract(api_key, payload)
            return response, remaining_variables, excluded_variables
        except RuntimeError as exc:
            invalid_variables = extract_invalid_variables_from_error(str(exc))
            if not invalid_variables:
                raise

            remaining_set = set(remaining_variables)
            new_invalid_variables: list[str] = []
            for invalid_variable in invalid_variables:
                if invalid_variable in remaining_set:
                    new_invalid_variables.append(invalid_variable)

                aliased_source = REVERSE_VARIABLE_ALIAS_MAP.get(invalid_variable)
                if aliased_source and aliased_source in remaining_set:
                    new_invalid_variables.append(aliased_source)

                for quality_flag in PARENT_TO_QUALITY_FLAGS.get(invalid_variable, set()):
                    if quality_flag in remaining_set:
                        new_invalid_variables.append(quality_flag)

            # Preserve order for readability in the exclusion audit file.
            new_invalid_variables = list(dict.fromkeys(new_invalid_variables))
            if not new_invalid_variables:
                raise

            print(
                "IPUMS rejected the following variables for this USA extract: "
                + ", ".join(new_invalid_variables)
            )

            excluded_variables.extend(new_invalid_variables)
            remaining_variables = [
                variable
                for variable in remaining_variables
                if variable not in set(new_invalid_variables)
            ]

            if not remaining_variables:
                raise RuntimeError(
                    "All observed variables were rejected by the IPUMS API after validation retries."
                ) from exc


def fetch_extract_status(api_key: str, extract_number: int) -> dict[str, Any]:
    """Fetch the current status for one submitted extract."""

    url = (
        f"{IPUMS_API_BASE_URL}/extracts/{extract_number}?collection={IPUMS_API_COLLECTION}"
        f"&version={IPUMS_API_VERSION}"
    )
    return ipums_api_request("GET", url, api_key)


def wait_for_completion(api_key: str, extract_number: int) -> dict[str, Any]:
    """Poll the IPUMS API until the extract finishes or fails."""

    last_status = None
    while True:
        status_response = fetch_extract_status(api_key, extract_number)
        status = status_response.get("status", "unknown")

        if status != last_status:
            print(f"Extract {extract_number} status: {status}")
            last_status = status

        download_links = status_response.get("downloadLinks", {})
        if status in {"completed", "produced"} and download_links:
            return status_response

        if status in {"failed", "canceled"}:
            raise RuntimeError(
                f"IPUMS extract {extract_number} ended with status {status}: "
                f"{json.dumps(status_response, indent=2)}"
            )

        time.sleep(POLL_SECONDS)


def download_extract_files(api_key: str, status_response: dict[str, Any]) -> None:
    """Download all available artifacts for the completed extract."""

    download_links = status_response.get("downloadLinks", {})
    if not download_links:
        raise RuntimeError("Completed extract response did not include any download links.")

    for download_key, link_info in sorted(download_links.items()):
        download_url = link_info["url"]
        destination = output_path_for_download(download_key, download_url)
        print(f"Downloading {download_key} -> {destination.name}")
        download_file(download_url, destination, api_key)

    normalize_downloaded_artifacts(status_response)


def main() -> int:
    """Run the full extract creation workflow.

    The script saves a few helper artifacts alongside the downloaded extract so the
    job can be audited later without rerunning the API calls:

    - ACS_extract_expanded_variables.txt: the final sorted variable list
    - ACS_extract_expanded_request.json: the exact submitted API request
    - ACS_extract_expanded_extract_response.json: the final completed API response
    """

    materials_dir = replication_materials_dir()
    materials_dir.mkdir(parents=True, exist_ok=True)

    print("Collecting observed IPUMS USA variables from Task 1 submitted replications...")
    observed_variables = collect_observed_variables()
    print(f"Observed variable count: {len(observed_variables)}")

    observed_variables_path = materials_dir / "ACS_extract_expanded_variables_observed.txt"
    observed_variables_path.write_text(
        "\n".join(observed_variables) + "\n",
        encoding="utf-8",
    )

    api_key = load_ipums_api_key(api_key_env_path())

    print("Submitting IPUMS USA extract request...")
    submission_response, requested_variables, excluded_variables = submit_extract_with_validation_retry(
        api_key,
        observed_variables,
    )

    request_variables, alias_notes, requested_quality_flags = build_request_variables(
        requested_variables,
    )

    variables_path = materials_dir / "ACS_extract_expanded_variables.txt"
    variables_path.write_text(
        "\n".join(sorted(request_variables)) + "\n",
        encoding="utf-8",
    )

    excluded_variables_path = materials_dir / "ACS_extract_expanded_excluded_variables.txt"
    excluded_variables_path.write_text(
        "\n".join(excluded_variables) + ("\n" if excluded_variables else ""),
        encoding="utf-8",
    )

    quality_flags_path = materials_dir / "ACS_extract_expanded_quality_flags_requested.txt"
    quality_flags_path.write_text(
        "\n".join(requested_quality_flags) + ("\n" if requested_quality_flags else ""),
        encoding="utf-8",
    )

    aliases_path = materials_dir / "ACS_extract_expanded_variable_aliases.json"
    save_json(aliases_path, alias_notes)

    request_path = materials_dir / "ACS_extract_expanded_request.json"
    save_json(request_path, build_extract_request(request_variables))

    extract_number = int(submission_response["number"])
    print(f"Submitted extract number: {extract_number}")

    final_status = wait_for_completion(api_key, extract_number)

    response_path = materials_dir / "ACS_extract_expanded_extract_response.json"
    save_json(response_path, final_status)

    print("Downloading completed extract artifacts...")
    download_extract_files(api_key, final_status)

    print("Finished downloading ACS_extract_expanded artifacts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())