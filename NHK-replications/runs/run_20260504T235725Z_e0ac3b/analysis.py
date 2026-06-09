import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
STATE_FILE = BASE_DIR / "policy_labor_market_data.csv"


# Only the columns needed for the DACA design are parsed from the fixed-width ACS file.
ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
    (747, 751),  # birthyr
    (763, 764),  # hispan
    (767, 770),  # bpl
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

ACS_COLUMNS = [
    "year",
    "statefip",
    "perwt",
    "sex",
    "age",
    "birthyr",
    "hispan",
    "bpl",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]


def load_acs_sample() -> pd.DataFrame:
    """Read the ACS file in chunks and keep only the rows needed for the design."""
    kept_chunks = []

    reader = pd.read_fwf(
        ACS_FILE,
        colspecs=ACS_COLSPECS,
        names=ACS_COLUMNS,
        chunksize=250_000,
        iterator=True,
    )

    for chunk in reader:
        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"].isin([3, 4, 5]))
            & chunk["age"].between(16, 40)
            & chunk["birthyr"].between(1972, 1996)
            & chunk["yrimmig"].between(1, 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) <= 15)
            & (chunk["perwt"] > 0)
        )

        if mask.any():
            kept_chunks.append(chunk.loc[mask, ACS_COLUMNS].copy())

    if not kept_chunks:
        raise RuntimeError("No observations remained after applying the ACS sample filters.")

    df = pd.concat(kept_chunks, ignore_index=True)
    df = df.astype(
        {
            "year": "int16",
            "statefip": "int16",
            "perwt": "float64",
            "sex": "int8",
            "age": "int16",
            "birthyr": "int16",
            "hispan": "int8",
            "bpl": "int16",
            "citizen": "int8",
            "yrimmig": "int16",
            "empstat": "int8",
            "uhrswork": "float64",
        }
    )
    return df


def load_state_controls() -> pd.DataFrame:
    """Read the state-year labor market controls and standardize the merge keys."""
    controls = pd.read_csv(
        STATE_FILE,
        usecols=["state_fips", "year", "LFPR", "UNEMP"],
    )
    controls = controls.rename(columns={"state_fips": "statefip"})
    controls["statefip"] = pd.to_numeric(controls["statefip"], errors="raise").astype("int16")
    controls["year"] = controls["year"].astype("int16")
    return controls


def build_analysis_frame() -> pd.DataFrame:
    """Merge ACS microdata with the state-year control file and create analysis variables."""
    acs = load_acs_sample()
    controls = load_state_controls()
    merged = acs.merge(controls, on=["statefip", "year"], how="inner", validate="many_to_one")

    merged["full_time"] = ((merged["empstat"] == 1) & (merged["uhrswork"] >= 35)).astype(float)
    merged["post"] = (merged["year"] >= 2013).astype(int)
    merged["daca_eligible"] = (merged["birthyr"] >= 1982).astype(int)

    if merged["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility has no variation after applying the sample restrictions.")

    return merged


def estimate_effect(df: pd.DataFrame):
    """Fit the weighted least-squares specification with state-clustered standard errors."""
    model = smf.wls(
        "full_time ~ daca_eligible * post + age + I(age ** 2) + year + I(year ** 2) + C(sex) + C(statefip) + UNEMP + LFPR",
        data=df,
        weights=df["perwt"] / 100.0,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})
    return model


def main() -> None:
    df = build_analysis_frame()
    model = estimate_effect(df)
    output = {
        "point_estimate": float(model.params["daca_eligible:post"]),
        "standard_error": float(model.bse["daca_eligible:post"]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
