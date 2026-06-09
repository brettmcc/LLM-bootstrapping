import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
STATE_PATH = BASE_DIR / "policy_labor_market_data.csv"
SPEC_PATH = BASE_DIR / "spec.json"


ACS_COLSPECS = [
    (0, 4),    # year
    (65, 67),  # statefip
    (691, 701),  # perwt
    (739, 740),  # sex
    (740, 743),  # age
    (763, 764),  # hispan
    (764, 767),  # hispand
    (767, 770),  # bpl
    (770, 775),  # bpld
    (789, 790),  # citizen
    (794, 798),  # yrimmig
    (874, 875),  # empstat
    (904, 906),  # uhrswork
]

ACS_COLS = [
    "year",
    "statefip",
    "perwt",
    "sex",
    "age",
    "hispan",
    "hispand",
    "bpl",
    "bpld",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
]


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispand == 100",
        "bpld == 20000",
        "citizen == 3",
        "16 <= age <= 40",
        "sex in (1, 2)",
        "yrimmig > 0",
    ],
    "outcome_definition": "(uhrswork >= 35).astype(int)",
    "treatment_definition": "((age + (2012 - year)).between(15, 30)) & ((age - (year - yrimmig)) <= 15) & (yrimmig <= 2007)",
    "model_specification_line": "result = smf.wls('full_time ~ treated * post + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + unemp + lfpr + driverslicenses + everify + limiteverify', data=analysis_df, weights=analysis_df['perwt']).fit(cov_type='cluster', cov_kwds={'groups': analysis_df['statefip']})",
}


def read_state_data() -> pd.DataFrame:
    state = pd.read_csv(STATE_PATH)
    state.columns = [column.lower() for column in state.columns]
    state["statefip"] = pd.to_numeric(state["state_fips"], errors="coerce").astype("Int64")
    state["year"] = pd.to_numeric(state["year"], errors="coerce").astype("Int64")
    state = state.rename(
        columns={
            "driverslicenses": "driverslicenses",
            "instatetuition": "instatetuition",
            "statefinancialaid": "statefinancialaid",
            "higheredban": "higheredban",
            "everify": "everify",
            "limiteverify": "limiteverify",
            "omnibus": "omnibus",
            "task287g": "task287g",
            "jail287g": "jail287g",
            "securecommunities": "securecommunities",
            "lfpr": "lfpr",
            "unemp": "unemp",
        }
    )
    return state[
        [
            "statefip",
            "year",
            "driverslicenses",
            "instatetuition",
            "statefinancialaid",
            "higheredban",
            "everify",
            "limiteverify",
            "omnibus",
            "task287g",
            "jail287g",
            "securecommunities",
            "lfpr",
            "unemp",
        ]
    ]


def load_acs() -> pd.DataFrame:
    frames = []
    reader = pd.read_fwf(
        ACS_PATH,
        colspecs=ACS_COLSPECS,
        names=ACS_COLS,
        header=None,
        chunksize=250_000,
    )

    for chunk in reader:
        for column in ACS_COLS:
            chunk[column] = pd.to_numeric(chunk[column], errors="coerce")
        chunk["perwt"] = chunk["perwt"] / 100.0

        mask = (
            chunk["year"].between(2006, 2016)
            & (chunk["year"] != 2012)
            & chunk["hispand"].eq(100)
            & chunk["bpld"].eq(20000)
            & chunk["citizen"].eq(3)
            & chunk["age"].between(16, 40)
            & chunk["sex"].isin([1, 2])
            & chunk["yrimmig"].gt(0)
        )

        filtered = chunk.loc[mask, ACS_COLS].copy()
        if not filtered.empty:
            frames.append(filtered)

    if not frames:
        raise RuntimeError("No ACS observations remain after filtering.")

    df = pd.concat(frames, ignore_index=True)
    df["year"] = df["year"].astype(int)
    df["statefip"] = df["statefip"].astype(int)
    df["sex"] = df["sex"].astype(int)
    df["age"] = df["age"].astype(int)
    df["citizen"] = df["citizen"].astype(int)
    df["yrimmig"] = df["yrimmig"].astype(int)
    df["post"] = (df["year"] >= 2013).astype(int)
    df["age_2012"] = df["age"] + (2012 - df["year"])
    df["age_at_arrival"] = df["age"] - (df["year"] - df["yrimmig"])
    df["treated"] = (
        df["age_2012"].between(15, 30)
        & df["age_at_arrival"].le(15)
        & df["yrimmig"].le(2007)
    ).astype(int)
    df["full_time"] = (df["uhrswork"] >= 35).astype(int)
    return df


def build_analysis_data() -> pd.DataFrame:
    acs = load_acs()
    state = read_state_data()
    analysis_df = acs.merge(state, on=["statefip", "year"], how="left", validate="m:1")
    if analysis_df[["lfpr", "unemp"]].isna().any().any():
        raise RuntimeError("State-year merge introduced missing controls.")
    if analysis_df["treated"].nunique() < 2:
        raise RuntimeError("Treatment has no variation after filtering.")
    return analysis_df


def main() -> None:
    analysis_df = build_analysis_data()
    result = smf.wls(
        "full_time ~ treated * post + age + I(age ** 2) + C(sex) + C(year) + C(statefip) + unemp + lfpr + driverslicenses + everify + limiteverify",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    spec_path = SPEC_PATH
    with spec_path.open("w", encoding="utf-8") as handle:
        json.dump(SPEC, handle, indent=2)

    output = {
        "point_estimate": float(result.params["treated:post"]),
        "standard_error": float(result.bse["treated:post"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output, separators=(",", ":")))


if __name__ == "__main__":
    main()
