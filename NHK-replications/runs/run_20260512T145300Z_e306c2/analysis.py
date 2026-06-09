import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
POLICY_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"

SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen == 3",
        "15 <= age <= 40",
        "birthyr > 0 and yrimmig > 0 and yrimmig <= year",
        "empstat in {1, 2, 3}",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(int)",
    "treatment_definition": "((birthyr >= 1982) & (yrimmig <= 2007) & ((yrimmig - birthyr) <= 15))",
    "model_specification_line": "result = smf.wls(\"full_time ~ eligible + eligible:post + C(statefip) + C(year) + C(age) + lfpr + unemp\", data=analysis_df, weights=analysis_df[\"perwt\"]).fit(cov_type=\"cluster\", cov_kwds={\"groups\": analysis_df[\"statefip\"]})",
}


ACS_COLS = {
    "year": (0, 4),
    "statefip": (65, 67),
    "perwt": (691, 701),
    "age": (740, 743),
    "birthyr": (747, 751),
    "hispan": (763, 764),
    "bpl": (767, 770),
    "citizen": (789, 790),
    "yrimmig": (794, 798),
    "empstat": (874, 875),
    "uhrswork": (904, 906),
}


def _parse_int(field: bytes):
    field = field.strip()
    if not field:
        return None
    return int(field)


def _parse_float(field: bytes):
    field = field.strip()
    if not field:
        return None
    return float(field)


def load_policy_controls(path: Path) -> dict[tuple[int, int], dict[str, float]]:
    policy = pd.read_csv(path)
    policy.columns = [col.lower() for col in policy.columns]
    policy = policy.rename(columns={"state_fips": "statefip"})
    policy["statefip"] = policy["statefip"].astype(int)
    policy["year"] = policy["year"].astype(int)
    policy["lfpr"] = pd.to_numeric(policy["lfpr"], errors="coerce")
    policy["unemp"] = pd.to_numeric(policy["unemp"], errors="coerce")

    controls = {}
    for row in policy[["statefip", "year", "lfpr", "unemp"]].itertuples(index=False):
        controls[(int(row.statefip), int(row.year))] = {
            "lfpr": float(row.lfpr),
            "unemp": float(row.unemp),
        }
    return controls


def load_acs_sample(path: Path, policy_controls: dict[tuple[int, int], dict[str, float]]) -> pd.DataFrame:
    records = []
    with path.open("rb") as fh:
        for line in fh:
            year = _parse_int(line[ACS_COLS["year"][0] : ACS_COLS["year"][1]])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = _parse_int(line[ACS_COLS["hispan"][0] : ACS_COLS["hispan"][1]])
            if hispan != 1:
                continue

            bpl = _parse_int(line[ACS_COLS["bpl"][0] : ACS_COLS["bpl"][1]])
            if bpl != 200:
                continue

            citizen = _parse_int(line[ACS_COLS["citizen"][0] : ACS_COLS["citizen"][1]])
            if citizen != 3:
                continue

            age = _parse_int(line[ACS_COLS["age"][0] : ACS_COLS["age"][1]])
            if age is None or age < 15 or age > 40:
                continue

            birthyr = _parse_int(line[ACS_COLS["birthyr"][0] : ACS_COLS["birthyr"][1]])
            yrimmig = _parse_int(line[ACS_COLS["yrimmig"][0] : ACS_COLS["yrimmig"][1]])
            if birthyr is None or birthyr <= 0 or yrimmig is None or yrimmig <= 0 or yrimmig > year:
                continue

            empstat = _parse_int(line[ACS_COLS["empstat"][0] : ACS_COLS["empstat"][1]])
            if empstat not in (1, 2, 3):
                continue

            statefip = _parse_int(line[ACS_COLS["statefip"][0] : ACS_COLS["statefip"][1]])
            perwt = _parse_float(line[ACS_COLS["perwt"][0] : ACS_COLS["perwt"][1]])
            uhrswork = _parse_int(line[ACS_COLS["uhrswork"][0] : ACS_COLS["uhrswork"][1]])
            if statefip is None or perwt is None:
                continue

            controls = policy_controls.get((statefip, year))
            if controls is None:
                continue

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "age": age,
                    "birthyr": birthyr,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork if uhrswork is not None else float("nan"),
                    "perwt": perwt / 100.0,
                    "lfpr": controls["lfpr"],
                    "unemp": controls["unemp"],
                }
            )

    return pd.DataFrame.from_records(records)


def build_analysis_frame() -> pd.DataFrame:
    policy_controls = load_policy_controls(POLICY_PATH)
    analysis_df = load_acs_sample(ACS_PATH, policy_controls)

    if analysis_df.empty:
        raise RuntimeError("No observations matched the requested sample.")

    analysis_df["full_time"] = ((analysis_df["empstat"] == 1) & (analysis_df["uhrswork"] >= 35)).astype(int)
    analysis_df["eligible"] = (
        (analysis_df["birthyr"] >= 1982)
        & (analysis_df["yrimmig"] <= 2007)
        & ((analysis_df["yrimmig"] - analysis_df["birthyr"]) <= 15)
    ).astype(int)
    analysis_df["post"] = (analysis_df["year"] >= 2013).astype(int)

    analysis_df = analysis_df.dropna(subset=["full_time", "eligible", "post", "lfpr", "unemp", "perwt"])

    if analysis_df["eligible"].nunique() < 2:
        raise RuntimeError("Treatment has no variation under the current sample definition.")

    return analysis_df


def fit_model(analysis_df: pd.DataFrame):
    result = smf.wls(
        "full_time ~ eligible + eligible:post + C(statefip) + C(year) + C(age) + lfpr + unemp",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})
    return result


def main() -> None:
    with SPEC_PATH.open("w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=2)
        fh.write("\n")

    analysis_df = build_analysis_frame()
    result = fit_model(analysis_df)

    output = {
        "point_estimate": float(result.params["eligible:post"]),
        "standard_error": float(result.bse["eligible:post"]),
        "sample_size": int(result.nobs),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
