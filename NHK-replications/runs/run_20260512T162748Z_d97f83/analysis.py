from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


# Fixed-width slices from the layout excerpt, converted to 0-based half-open ranges.
ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (747, 751),  # birthyr
    (794, 798),  # yrimmig
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]
ACS_NAMES = [
    "year",
    "statefip",
    "perwt",
    "birthyr",
    "yrimmig",
    "hispan",
    "bpl",
    "citizen",
    "empstat",
    "uhrswork",
]


def load_acs_sample() -> pd.DataFrame:
    """Read only the ACS columns we need and apply the sample restrictions early."""
    chunks = []
    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_NAMES,
        chunksize=200_000,
    ):
        # Convert the selected columns to numeric values before filtering.
        for name in ACS_NAMES:
            chunk[name] = pd.to_numeric(chunk[name], errors="coerce")

        chunk = chunk.dropna(subset=ACS_NAMES)
        chunk = chunk.astype(
            {
                "year": "int64",
                "statefip": "int64",
                "perwt": "float64",
                "birthyr": "int64",
                "yrimmig": "int64",
                "hispan": "int64",
                "bpl": "int64",
                "citizen": "int64",
                "empstat": "int64",
                "uhrswork": "int64",
            }
        )

        # Keep the sample centered on Mexican-born Hispanic noncitizens in the DACA birth-year window.
        chunk = chunk[
            (chunk["year"].between(2006, 2016))
            & (chunk["year"] != 2012)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & (chunk["birthyr"].between(1982, 1996))
            & (chunk["yrimmig"] > 0)
        ].copy()

        if chunk.empty:
            continue

        # Approximate DACA eligibility using birth year and year of immigration.
        chunk["eligible"] = (
            (chunk["yrimmig"] <= 2007)
            & (chunk["yrimmig"] <= chunk["birthyr"] + 15)
        ).astype(int)

        # 2013-2016 are the post-DACA years; 2006-2011 are the pre-period.
        chunk["post"] = (chunk["year"] >= 2013).astype(int)

        # Full-time employment means employed and usually working at least 35 hours per week.
        chunk["full_time"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)

        # Weight scale in the ACS extract uses two implied decimals.
        chunk["perwt"] = chunk["perwt"] / 100.0

        chunks.append(
            chunk[["statefip", "year", "perwt", "eligible", "post", "full_time"]]
        )

    if not chunks:
        raise RuntimeError("No ACS observations matched the sample restrictions.")

    return pd.concat(chunks, ignore_index=True)


def load_policy_controls() -> pd.DataFrame:
    """Load the state-year policy file and keep the controls used in the regression."""
    policy = pd.read_csv(POLICY_PATH)
    policy["state_fips"] = pd.to_numeric(policy["state_fips"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    policy = policy.dropna(subset=["state_fips", "year"]).copy()
    policy["statefip"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)

    keep_cols = [
        "statefip",
        "year",
        "DRIVERSLICENSES",
        "INSTATETUITION",
        "STATEFINANCIALAID",
        "HIGHEREDBAN",
        "EVERIFY",
        "LIMITEVERIFY",
        "OMNIBUS",
        "JAIL287G",
        "LFPR",
        "UNEMP",
    ]
    return policy[keep_cols].copy()


def main() -> None:
    acs = load_acs_sample()
    policy = load_policy_controls()

    merged = acs.merge(policy, on=["statefip", "year"], how="inner", validate="many_to_one")

    if merged["eligible"].nunique() < 2:
        raise RuntimeError("Treatment does not vary in the analysis sample.")
    if merged["post"].nunique() < 2:
        raise RuntimeError("Post indicator does not vary in the analysis sample.")

    formula = (
        "full_time ~ eligible + eligible:post + C(statefip) + C(year) + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + "
        "EVERIFY + LIMITEVERIFY + OMNIBUS + JAIL287G + LFPR + UNEMP"
    )

    fit = smf.wls(
        formula,
        data=merged,
        weights=merged["perwt"],
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": merged["statefip"]},
    )

    point_estimate = float(fit.params["eligible:post"])
    standard_error = float(fit.bse["eligible:post"])
    sample_size = int(len(merged))

    spec = {
        "sample_selection": [
            "year >= 2006 and year <= 2016 and year != 2012",
            "hispan == 1",
            "bpl == 200",
            "citizen in {3, 4, 5}",
            "birthyr >= 1982 and birthyr <= 1996",
            "yrimmig > 0",
        ],
        "outcome_definition": "int(empstat == 1 and uhrswork >= 35)",
        "treatment_definition": "int((yrimmig <= 2007) and (yrimmig <= birthyr + 15))",
        "model_specification_line": (
            'fit = smf.wls("full_time ~ eligible + eligible:post + C(statefip) + C(year) + '
            'DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + '
            'LIMITEVERIFY + OMNIBUS + JAIL287G + LFPR + UNEMP", data=merged, weights=merged["perwt"]).fit('
            'cov_type="cluster", cov_kwds={"groups": merged["statefip"]})'
        ),
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    result = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size,
    }
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
