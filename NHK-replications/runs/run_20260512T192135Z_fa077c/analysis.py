from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


ACS_COLS = [
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

ACS_COLSPECS = [
    (0, 4),      # year
    (65, 67),    # statefip
    (691, 701),   # perwt
    (739, 740),   # sex
    (740, 743),   # age
    (747, 751),   # birthyr
    (763, 764),   # hispan
    (767, 770),   # bpl
    (789, 790),   # citizen
    (794, 798),   # yrimmig
    (874, 875),   # empstat
    (904, 906),   # uhrswork
]


def load_policy_data() -> pd.DataFrame:
    policy = pd.read_csv(POLICY_PATH)
    policy.columns = [column.lower() for column in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = pd.to_numeric(policy["statefip"], errors="coerce")
    policy["year"] = pd.to_numeric(policy["year"], errors="coerce")
    return policy


def load_acs_chunks() -> pd.DataFrame:
    frames = []

    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLS,
        header=None,
        chunksize=250_000,
        dtype=str,
    ):
        for column in ACS_COLS:
            chunk[column] = pd.to_numeric(chunk[column].str.strip(), errors="coerce")

        # The raw PERWT values are stored with two implied decimals.
        chunk["perwt"] = chunk["perwt"] / 100.0

        sample = (
            chunk["year"].between(2006, 2016)
            & chunk["statefip"].between(1, 56)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & (chunk["citizen"] == 3)
            & chunk["sex"].isin([1, 2])
            & (chunk["age"] >= 16)
            & chunk["birthyr"].between(1982, 1996)
            & chunk["yrimmig"].notna()
            & (chunk["yrimmig"] >= chunk["birthyr"])
            & (chunk["yrimmig"] <= 2016)
            & chunk["empstat"].isin([1, 2, 3])
            & (chunk["perwt"] > 0)
        )

        chunk = chunk.loc[sample, ACS_COLS].copy()
        chunk["fulltime"] = ((chunk["empstat"] == 1) & (chunk["uhrswork"] >= 35)).astype(int)
        chunk["eligible"] = (
            (chunk["birthyr"].between(1982, 1996))
            & (chunk["yrimmig"] <= 2007)
            & ((chunk["yrimmig"] - chunk["birthyr"]) < 16)
        ).astype(int)
        chunk["post"] = (chunk["year"] >= 2013).astype(int)
        chunk["eligible_post"] = chunk["eligible"] * chunk["post"]

        frames.append(chunk)

    if not frames:
        raise RuntimeError("No ACS observations were loaded.")

    return pd.concat(frames, ignore_index=True)


def build_sample(df: pd.DataFrame, citizen_values: tuple[int, ...], birthyr_min: int, birthyr_max: int) -> pd.DataFrame:
    sample = df[
        df["year"].between(2006, 2016)
        & df["statefip"].between(1, 56)
        & (df["hispan"] == 1)
        & (df["bpl"] == 200)
        & df["citizen"].isin(citizen_values)
        & df["sex"].isin([1, 2])
        & (df["age"] >= 16)
        & df["birthyr"].between(birthyr_min, birthyr_max)
        & df["yrimmig"].notna()
        & (df["yrimmig"] >= df["birthyr"])
        & (df["yrimmig"] <= 2016)
        & df["empstat"].isin([1, 2, 3])
        & (df["perwt"] > 0)
    ].copy()

    sample["fulltime"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(int)
    sample["eligible"] = (
        (sample["birthyr"].between(1982, 1996))
        & (sample["yrimmig"] <= 2007)
        & ((sample["yrimmig"] - sample["birthyr"]) < 16)
    ).astype(int)
    sample["post"] = (sample["year"] >= 2013).astype(int)
    sample["eligible_post"] = sample["eligible"] * sample["post"]
    return sample


def choose_spec(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    candidates = [
        {
            "sample_selection": [
                "2006 <= year <= 2016",
                "1 <= statefip <= 56",
                "hispan == 1",
                "bpl == 200",
                "citizen == 3",
                "sex in {1, 2}",
                "age >= 16",
                "1982 <= birthyr <= 1996",
                "yrimmig >= birthyr",
                "yrimmig <= 2016",
                "empstat in {1, 2, 3}",
                "perwt > 0",
            ],
            "citizen_values": (3,),
            "birthyr_min": 1982,
            "birthyr_max": 1996,
        },
        {
            "sample_selection": [
                "2006 <= year <= 2016",
                "1 <= statefip <= 56",
                "hispan == 1",
                "bpl == 200",
                "citizen in {3, 4, 5}",
                "sex in {1, 2}",
                "age >= 16",
                "1982 <= birthyr <= 1996",
                "yrimmig >= birthyr",
                "yrimmig <= 2016",
                "empstat in {1, 2, 3}",
                "perwt > 0",
            ],
            "citizen_values": (3, 4, 5),
            "birthyr_min": 1982,
            "birthyr_max": 1996,
        },
        {
            "sample_selection": [
                "2006 <= year <= 2016",
                "1 <= statefip <= 56",
                "hispan == 1",
                "bpl == 200",
                "citizen == 3",
                "sex in {1, 2}",
                "age >= 16",
                "1976 <= birthyr <= 1996",
                "yrimmig >= birthyr",
                "yrimmig <= 2016",
                "empstat in {1, 2, 3}",
                "perwt > 0",
            ],
            "citizen_values": (3,),
            "birthyr_min": 1976,
            "birthyr_max": 1996,
        },
    ]

    for candidate in candidates:
        sample = build_sample(
            df,
            citizen_values=candidate["citizen_values"],
            birthyr_min=candidate["birthyr_min"],
            birthyr_max=candidate["birthyr_max"],
        )
        if sample["eligible"].nunique() == 2 and 0 < sample["eligible"].sum() < len(sample):
            spec = {
                "sample_selection": candidate["sample_selection"],
                "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
                "treatment_definition": "(birthyr >= 1982) & (birthyr <= 1996) & (yrimmig <= 2007) & ((yrimmig - birthyr) < 16)",
                "model_specification_line": 'result = smf.wls("fulltime ~ eligible_post + eligible + C(year) + C(birthyr) + C(statefip) + C(sex) + lfpr + unemp", data=analysis_df, weights=analysis_df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})',
            }
            return sample, spec

    raise RuntimeError("No candidate specification produced treatment variation.")


def main() -> None:
    policy = load_policy_data()
    acs = load_acs_chunks()

    analysis_df, spec = choose_spec(acs)

    analysis_df = analysis_df.merge(
        policy[
            [
                "statefip",
                "year",
                "lfpr",
                "unemp",
            ]
        ],
        on=["statefip", "year"],
        how="left",
        validate="m:1",
    )

    if analysis_df[["lfpr", "unemp"]].isna().any().any():
        raise RuntimeError("State-year labor market controls are missing after merge.")

    # Statsmodels uses the dataframe attached to the fitted model, so we keep the analysis dataframe intact.
    result = smf.wls(
        "fulltime ~ eligible_post + eligible + C(year) + C(birthyr) + C(statefip) + C(sex) + lfpr + unemp",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    if "eligible_post" not in result.params:
        raise RuntimeError("The treatment effect coefficient was not estimated.")

    output_spec = spec
    SPEC_PATH.write_text(json.dumps(output_spec, indent=2), encoding="utf-8")

    output = {
        "point_estimate": float(result.params["eligible_post"]),
        "standard_error": float(result.bse["eligible_post"]),
        "sample_size": int(len(analysis_df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
