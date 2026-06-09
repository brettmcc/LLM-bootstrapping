"""Recover treated-group sizes for archived runs that need bespoke logic.

The generic treated-group recovery script is intentionally conservative.  It
only accepts counts that can be inferred from an estimator input whose row count
matches the archived run's reported sample size.  A few valid runs aggregate
person-level ACS observations before estimation, or store the sample in NumPy
arrays instead of a pandas DataFrame.  For those runs, the only reliable place to
count treated observations is the original sample-construction code.

This script implements exactly that targeted recovery for three archived runs:

* run_20260505T014553Z_87dc0a
* run_20260512T181941Z_e6166c
* run_20260519T172426Z_1e8b9c

It streams the expanded ACS fixed-width extract once, applies each run's saved
sample and treatment construction, validates the reconstructed sample size
against runs_complete_expanded.csv, and optionally merges accepted counts back
into both the recovery audit CSV and runs_complete_expanded.csv.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


TARGET_RUN_IDS = (
    "run_20260505T014553Z_87dc0a",
    "run_20260512T181941Z_e6166c",
    "run_20260519T172426Z_1e8b9c",
)


@dataclass
class CountState:
    """Mutable counters for one reconstructed archived run."""

    sample_size: int = 0
    treated_group_size: int = 0


def parse_int(text: str) -> int | None:
    """Parse a fixed-width integer field, treating blanks and junk as missing."""

    value = text.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_layout_colspecs(layout_path: Path, wanted: list[str]) -> dict[str, tuple[int, int]]:
    """Read one-based IPUMS layout positions and convert them to Python slices."""

    pattern = re.compile(r"^\s*\w+\s+(?P<name>[A-Za-z0-9_]+)\s+(?P<start>\d+)-(?P<end>\d+)")
    specs: dict[str, tuple[int, int]] = {}

    with layout_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            match = pattern.match(line)
            if match is None:
                continue
            name = match.group("name")
            if name not in wanted:
                continue
            # IPUMS/Stata layouts are one-based and inclusive.  Python slices
            # are zero-based and stop-exclusive, so only the start moves down by
            # one while the end can be used directly.
            specs[name] = (int(match.group("start")) - 1, int(match.group("end")))

    missing = [name for name in wanted if name not in specs]
    if missing:
        raise RuntimeError(f"Missing layout information for: {', '.join(missing)}")
    return specs


def field(line: str, start: int, end: int) -> int | None:
    """Extract and parse one fixed-width integer field from a raw ACS line."""

    return parse_int(line[start:end])


def field_from_specs(line: str, specs: dict[str, tuple[int, int]], name: str) -> int | None:
    """Extract and parse a named field using parsed IPUMS layout positions."""

    start, end = specs[name]
    return field(line, start, end)


def update_87dc0a(line: str, state: CountState) -> None:
    """Apply run_20260505T014553Z_87dc0a sample and treatment construction."""

    year = field(line, 0, 4)
    if year is None or year < 2006 or year > 2016 or year == 2012:
        return

    hispan = field(line, 763, 764)
    bpl = field(line, 767, 770)
    citizen = field(line, 789, 790)
    age = field(line, 740, 743)
    birthyr = field(line, 747, 751)
    yrimmig = field(line, 794, 798)
    statefip = field(line, 65, 67)
    perwt_raw = field(line, 691, 701)

    if (
        hispan != 1
        or bpl != 200
        or citizen not in (3, 4, 5)
        or age is None
        or age < 15
        or age > 40
        or birthyr is None
        or birthyr < 1976
        or birthyr > 1996
        or yrimmig is None
        or yrimmig > 2007
        or statefip is None
        or perwt_raw is None
    ):
        return

    treated = (
        birthyr >= 1982
        and birthyr <= 1996
        and yrimmig <= 2007
        and ((age - (year - yrimmig)) <= 15)
    )
    state.sample_size += 1
    state.treated_group_size += int(treated)


def update_e6166c(line: str, state: CountState) -> None:
    """Apply run_20260512T181941Z_e6166c sample and treatment construction."""

    if len(line) < 906:
        return

    year = field(line, 0, 4)
    statefip = field(line, 65, 67)
    perwt = field(line, 691, 701)
    age = field(line, 740, 743)
    birthyr = field(line, 747, 751)
    hispan = field(line, 763, 764)
    bpl = field(line, 767, 770)
    citizen = field(line, 789, 790)
    yrimmig = field(line, 794, 798)
    empstat = field(line, 874, 875)
    uhrswork = field(line, 904, 906)

    if any(
        value is None
        for value in (
            year,
            statefip,
            perwt,
            age,
            birthyr,
            hispan,
            bpl,
            citizen,
            yrimmig,
            empstat,
            uhrswork,
        )
    ):
        return
    if year not in {2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016}:
        return
    if hispan != 1 or bpl != 200 or citizen not in (3, 4, 5):
        return
    if perwt <= 0 or age < 0 or age > 120 or birthyr < 1900 or yrimmig < 1900:
        return

    age_at_arrival = yrimmig - birthyr
    treated = birthyr >= 1982 and 0 <= age_at_arrival < 16 and yrimmig <= 2007
    state.sample_size += 1
    state.treated_group_size += int(treated)


def update_1e8b9c(line: str, specs: dict[str, tuple[int, int]], state: CountState) -> None:
    """Apply run_20260519T172426Z_1e8b9c sample and treatment construction."""

    year = field_from_specs(line, specs, "year")
    statefip = field_from_specs(line, specs, "statefip")
    perwt = field_from_specs(line, specs, "perwt")
    age = field_from_specs(line, specs, "age")
    birthyr = field_from_specs(line, specs, "birthyr")
    birthqtr = field_from_specs(line, specs, "birthqtr")
    hispan = field_from_specs(line, specs, "hispan")
    bpl = field_from_specs(line, specs, "bpl")
    citizen = field_from_specs(line, specs, "citizen")
    yrimmig = field_from_specs(line, specs, "yrimmig")
    empstat = field_from_specs(line, specs, "empstat")

    if (
        year is None
        or year < 2006
        or year > 2016
        or year == 2012
        or statefip is None
        or statefip < 1
        or statefip > 56
        or age is None
        or age < 16
        or age > 40
        or birthyr is None
        or birthyr < 1975
        or birthyr > 1995
        or birthqtr not in (1, 2, 3, 4)
        or hispan != 1
        or bpl != 200
        or citizen != 3
        or yrimmig is None
        or yrimmig <= 0
        or yrimmig > year
        or empstat not in (1, 2, 3)
        or perwt is None
        or perwt <= 0
    ):
        return

    treated = (
        yrimmig <= 2007
        and ((yrimmig - birthyr) <= 15)
        and (birthyr > 1981 or (birthyr == 1981 and birthqtr >= 3))
    )
    state.sample_size += 1
    state.treated_group_size += int(treated)


def retained_target_sample_sizes(runs_csv: Path) -> dict[str, int]:
    """Load the stored sample sizes used to validate the bespoke reconstruction."""

    runs = pd.read_csv(runs_csv)
    runs = runs.loc[runs["run_id"].isin(TARGET_RUN_IDS), ["run_id", "sample_size"]].copy()
    if len(runs) != len(TARGET_RUN_IDS):
        found = set(runs["run_id"])
        missing = [run_id for run_id in TARGET_RUN_IDS if run_id not in found]
        raise RuntimeError(f"Target runs missing from {runs_csv}: {', '.join(missing)}")
    runs["sample_size"] = pd.to_numeric(runs["sample_size"], errors="raise").astype(int)
    return dict(zip(runs["run_id"], runs["sample_size"], strict=True))


def write_counts(output: Path, rows: list[dict[str, object]]) -> None:
    """Write the bespoke count audit CSV in a stable column order."""

    output.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "run_id",
        "sample_size",
        "reconstructed_sample_size",
        "treated_group_size",
        "accepted",
        "method",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def merge_into_recovery_csv(recovery_csv: Path, rows: list[dict[str, object]]) -> None:
    """Merge accepted bespoke counts into the shared treated-size recovery audit."""

    accepted = pd.DataFrame(rows)
    accepted = accepted.loc[accepted["accepted"], ["run_id", "sample_size", "treated_group_size"]].copy()
    accepted["accepted"] = True

    if recovery_csv.exists():
        recovery = pd.read_csv(recovery_csv)
    else:
        recovery = pd.DataFrame(columns=["run_id", "sample_size", "treated_group_size", "accepted"])

    recovery = recovery.loc[~recovery["run_id"].isin(accepted["run_id"])].copy()
    recovery = pd.concat([recovery, accepted], ignore_index=True)
    recovery = recovery.sort_values("run_id").reset_index(drop=True)
    recovery.to_csv(recovery_csv, index=False)


def merge_into_runs_csv(runs_csv: Path, recovery_csv: Path) -> None:
    """Update runs_complete_expanded.csv with all accepted recovered treated counts."""

    runs = pd.read_csv(runs_csv)
    recovery = pd.read_csv(recovery_csv)
    accepted = recovery.loc[
        recovery["accepted"].astype(str).str.lower().eq("true"),
        ["run_id", "treated_group_size"],
    ].copy()
    accepted["treated_group_size"] = pd.to_numeric(accepted["treated_group_size"], errors="coerce")
    accepted = accepted.dropna(subset=["treated_group_size"])
    accepted = accepted.drop_duplicates(subset=["run_id"], keep="last")

    existing = pd.to_numeric(runs.get("treated_group_size"), errors="coerce")
    runs = runs.drop(columns=["treated_group_size"], errors="ignore")
    preserved = pd.DataFrame({"run_id": runs["run_id"], "treated_group_size": existing})
    preserved = preserved.dropna(subset=["treated_group_size"])

    merged_counts = pd.concat([preserved, accepted], ignore_index=True)
    merged_counts = merged_counts.drop_duplicates(subset=["run_id"], keep="last")
    runs = runs.merge(merged_counts, on="run_id", how="left")
    runs.to_csv(runs_csv, index=False)


def recover_counts(acs_path: Path, layout_path: Path) -> dict[str, CountState]:
    """Stream the ACS extract once and return counts for all bespoke target runs."""

    specs_1e8b9c = parse_layout_colspecs(
        layout_path,
        [
            "year",
            "statefip",
            "perwt",
            "age",
            "birthyr",
            "birthqtr",
            "hispan",
            "bpl",
            "citizen",
            "yrimmig",
            "empstat",
        ],
    )
    counts = {run_id: CountState() for run_id in TARGET_RUN_IDS}

    with acs_path.open("r", encoding="latin-1", newline="") as handle:
        for line in handle:
            update_87dc0a(line, counts["run_20260505T014553Z_87dc0a"])
            update_e6166c(line, counts["run_20260512T181941Z_e6166c"])
            update_1e8b9c(line, specs_1e8b9c, counts["run_20260519T172426Z_1e8b9c"])

    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-csv", type=Path, default=Path("runs_complete_expanded.csv"))
    parser.add_argument("--acs", type=Path, default=Path("replication-materials/ACS_extract_expanded.dat"))
    parser.add_argument("--layout", type=Path, default=Path("replication-materials/acs_extra_expanded.do"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("meta_analysis_expanded/bespoke_treated_group_size_recovery.csv"),
    )
    parser.add_argument(
        "--recovery-csv",
        type=Path,
        default=Path("meta_analysis_expanded/treated_group_size_recovery.csv"),
    )
    parser.add_argument(
        "--update-runs-csv",
        action="store_true",
        help="Merge accepted bespoke counts into the recovery audit and runs_complete_expanded.csv.",
    )
    parser.add_argument(
        "--merge-only",
        action="store_true",
        help="Update runs_complete_expanded.csv from the existing recovery audit without rereading the ACS file.",
    )
    args = parser.parse_args()

    if args.merge_only:
        merge_into_runs_csv(args.runs_csv, args.recovery_csv)
        print(f"Updated {args.runs_csv} from accepted counts in {args.recovery_csv}.")
        return

    expected_sample_sizes = retained_target_sample_sizes(args.runs_csv)
    counts = recover_counts(args.acs, args.layout)

    rows: list[dict[str, object]] = []
    for run_id in TARGET_RUN_IDS:
        reconstructed = counts[run_id].sample_size
        expected = expected_sample_sizes[run_id]
        accepted = reconstructed == expected and counts[run_id].treated_group_size > 0
        rows.append(
            {
                "run_id": run_id,
                "sample_size": expected,
                "reconstructed_sample_size": reconstructed,
                "treated_group_size": counts[run_id].treated_group_size if accepted else "",
                "accepted": accepted,
                "method": "bespoke_streaming_archived_sample_construction",
            }
        )

    write_counts(args.output, rows)
    if args.update_runs_csv:
        merge_into_recovery_csv(args.recovery_csv, rows)
        merge_into_runs_csv(args.runs_csv, args.recovery_csv)

    accepted_count = sum(bool(row["accepted"]) for row in rows)
    print(f"Recovered accepted bespoke treated-group sizes for {accepted_count} of {len(rows)} runs.")
    for row in rows:
        print(
            "{run_id}: reconstructed_n={reconstructed_sample_size}, "
            "expected_n={sample_size}, treated_group_size={treated_group_size}, "
            "accepted={accepted}".format(**row)
        )


if __name__ == "__main__":
    main()
