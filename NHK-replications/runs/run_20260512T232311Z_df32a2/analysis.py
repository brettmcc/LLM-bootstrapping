from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


COLS = [
    ("year", (0, 4)),
    ("statefip", (65, 67)),
    ("perwt", (691, 701)),
    ("sex", (739, 740)),
    ("age", (740, 743)),
    ("birthyr", (747, 751)),
    ("hispan", (763, 764)),
    ("bpl", (767, 770)),
    ("citizen", (789, 790)),
    ("yrimmig", (794, 798)),
    ("empstat", (874, 875)),
    ("uhrswork", (904, 906)),
]


SAMPLE_SELECTION = [
    "hispan == 1 (Mexican Hispanic origin)",
    "bpl == 200 (born in Mexico)",
    "citizen == 3 (not a US citizen)",
    "age >= 18 and age <= 45 (working-age adults)",
    "year in [2009, 2010, 2011, 2013, 2014, 2015, 2016] (pre-DACA: 2009-2011, post-DACA: 2013-2016; 2012 excluded as transition year)",
    "arrival_age = yrimmig - birthyr, restricted to 0 <= arrival_age < 16 (arrived in US before age 16, matching DACA criterion)",
    "birthyr in 1982-1986 (treated) or 1977-1981 (control), symmetric 5-year bandwidth around the age-31 DACA eligibility cutoff",
]


def read_sample() -> pd.DataFrame:
    """Stream the ACS extract and keep only rows relevant to the design."""
    cols = [name for name, _ in COLS]
    specs = [spec for _, spec in COLS]

    chunks: list[pd.DataFrame] = []
    year_keep = {2009, 2010, 2011, 2013, 2014, 2015, 2016}

    for chunk in pd.read_fwf(
        DATA_PATH,
        colspecs=specs,
        names=cols,
        dtype=str,
        chunksize=250_000,
    ):
        for col in cols:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        arrival_age = chunk["yrimmig"] - chunk["birthyr"]
        mask = (
            chunk["hispan"].eq(1)
            & chunk["bpl"].eq(200)
            & chunk["citizen"].eq(3)
            & chunk["age"].between(18, 45, inclusive="both")
            & chunk["year"].isin(year_keep)
            & arrival_age.ge(0)
            & arrival_age.lt(16)
            & chunk["birthyr"].between(1977, 1986, inclusive="both")
        )

        filtered = chunk.loc[mask, cols].copy()
        if not filtered.empty:
            chunks.append(filtered)

    if not chunks:
        raise RuntimeError("No observations matched the requested sample.")

    df = pd.concat(chunks, ignore_index=True)
    df["treated"] = df["birthyr"].between(1982, 1986, inclusive="both").astype(int)
    df["post"] = df["year"].isin({2013, 2014, 2015, 2016}).astype(int)
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)

    return df


def estimate(df: pd.DataFrame) -> tuple[float, float, int]:
    """Estimate the DACA cohort DiD and return the requested summary stats."""
    if df["treated"].nunique() < 2:
        raise RuntimeError("Treatment has no variation in the filtered sample.")
    if df["post"].nunique() < 2:
        raise RuntimeError("Post indicator has no variation in the filtered sample.")

    result = smf.ols(
        "full_time ~ treated * post + C(year) + C(statefip) + age + I(age ** 2) + C(sex)",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"].astype(int)})

    return (
        float(result.params["treated:post"]),
        float(result.bse["treated:post"]),
        int(result.nobs),
    )


def main() -> None:
    df = read_sample()
    point_estimate, standard_error, sample_size = estimate(df)

    spec = {
        "sample_selection": SAMPLE_SELECTION,
        "outcome_definition": "(df['empstat'] == 1) & (df['uhrswork'] >= 35)",
        "treatment_definition": "(df['birthyr'] >= 1982).astype(int)",
        "model_specification_line": "result = smf.ols('full_time ~ treated * post + C(year) + C(statefip) + age + I(age ** 2) + C(sex)', data=df).fit(cov_type='cluster', cov_kwds={'groups': df['statefip'].astype(int)})",
    }

    SPEC_PATH.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    output = {
        "spec": spec,
        "results": {
            "point_estimate": point_estimate,
            "standard_error": standard_error,
            "sample_size": sample_size,
        },
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
