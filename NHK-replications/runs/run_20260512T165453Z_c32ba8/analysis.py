import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_FILE = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_FILE = BASE_DIR / "policy_labor_market_data.csv"
SPEC_FILE = BASE_DIR / "spec.json"


ACS_SLICES = {
    "year": (0, 4),
    "statefip": (65, 67),
    "perwt": (691, 701),
    "sex": (739, 740),
    "birthyr": (747, 751),
    "hispan": (763, 764),
    "bpl": (767, 770),
    "citizen": (789, 790),
    "yrimmig": (794, 798),
    "empstat": (874, 875),
    "uhrswork": (904, 906),
}


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016",
        "year != 2012",
        "hispan == 1",
        "bpl == 200",
        "citizen in [3, 4]",
        "empstat in [1, 2, 3]",
        "0 < yrimmig <= 2007",
        "1978 <= birthyr <= 1986",
        "yrimmig - birthyr <= 15",
    ],
    "outcome_definition": "((empstat == 1) & (uhrswork >= 35)).astype(float)",
    "treatment_definition": "(birthyr >= 1982).astype(float)",
    "model_specification_line": (
        "model = smf.wls(\"full_time ~ C(birthyr) + C(year) + C(statefip) + C(sex) + "
        "daca_post + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + "
        "EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP\", "
        "data=sample, weights=sample['perwt']).fit(cov_type='cluster', cov_kwds={'groups': sample['statefip']})"
    ),
}


def _parse_int(line: str, start: int, end: int):
    text = line[start:end].strip()
    if not text:
        return None
    return int(text)


def _load_acs_sample() -> pd.DataFrame:
    records = []
    with ACS_FILE.open("r", encoding="ascii", errors="ignore") as handle:
        for line in handle:
            year = _parse_int(line, *ACS_SLICES["year"])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            hispan = _parse_int(line, *ACS_SLICES["hispan"])
            bpl = _parse_int(line, *ACS_SLICES["bpl"])
            citizen = _parse_int(line, *ACS_SLICES["citizen"])
            empstat = _parse_int(line, *ACS_SLICES["empstat"])
            if (
                hispan != 1
                or bpl != 200
                or citizen not in (3, 4)
                or empstat not in (1, 2, 3)
            ):
                continue

            birthyr = _parse_int(line, *ACS_SLICES["birthyr"])
            yrimmig = _parse_int(line, *ACS_SLICES["yrimmig"])
            if (
                birthyr is None
                or yrimmig is None
                or yrimmig <= 0
                or yrimmig > 2007
                or birthyr < 1978
                or birthyr > 1986
                or (yrimmig - birthyr) > 15
            ):
                continue

            statefip = _parse_int(line, *ACS_SLICES["statefip"])
            sex = _parse_int(line, *ACS_SLICES["sex"])
            perwt_raw = _parse_int(line, *ACS_SLICES["perwt"])
            uhrswork = _parse_int(line, *ACS_SLICES["uhrswork"])
            if None in (statefip, sex, perwt_raw, uhrswork):
                continue

            records.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt_raw / 100.0,
                    "sex": sex,
                    "birthyr": birthyr,
                    "hispan": hispan,
                    "bpl": bpl,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                }
            )

    if not records:
        raise RuntimeError("No observations matched the sample filters.")

    sample = pd.DataFrame.from_records(records)
    sample["daca_eligible"] = (sample["birthyr"] >= 1982).astype(float)
    sample["post_daca"] = (sample["year"] >= 2013).astype(float)
    sample["daca_post"] = sample["daca_eligible"] * sample["post_daca"]

    if sample["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")
    if sample["post_daca"].nunique() < 2:
        raise RuntimeError("Post-DACA indicator lacks variation in the selected sample.")
    if sample["daca_post"].sum() == 0:
        raise RuntimeError("Treated post observations are missing from the selected sample.")

    sample["full_time"] = ((sample["empstat"] == 1) & (sample["uhrswork"] >= 35)).astype(float)
    return sample


def _merge_state_controls(sample: pd.DataFrame) -> pd.DataFrame:
    policy = pd.read_csv(POLICY_FILE)
    policy = policy[
        [
            "state_fips",
            "year",
            "DRIVERSLICENSES",
            "INSTATETUITION",
            "STATEFINANCIALAID",
            "HIGHEREDBAN",
            "EVERIFY",
            "LIMITEVERIFY",
            "OMNIBUS",
            "TASK287G",
            "JAIL287G",
            "SECURECOMMUNITIES",
            "LFPR",
            "UNEMP",
        ]
    ].copy()
    policy["statefip"] = policy["state_fips"].astype(int)
    policy["year"] = policy["year"].astype(int)
    policy = policy.drop(columns=["state_fips"])

    merged = sample.merge(policy, on=["statefip", "year"], how="left", validate="many_to_one")
    if merged[[
        "DRIVERSLICENSES",
        "INSTATETUITION",
        "STATEFINANCIALAID",
        "HIGHEREDBAN",
        "EVERIFY",
        "LIMITEVERIFY",
        "OMNIBUS",
        "TASK287G",
        "JAIL287G",
        "SECURECOMMUNITIES",
        "LFPR",
        "UNEMP",
    ]].isna().any().any():
        raise RuntimeError("State-level controls are missing after the merge.")
    return merged


def _estimate(sample: pd.DataFrame):
    model = smf.wls(
        "full_time ~ C(birthyr) + C(year) + C(statefip) + C(sex) + daca_post + "
        "DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + "
        "LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES + LFPR + UNEMP",
        data=sample,
        weights=sample["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": sample["statefip"]})
    return model


def main() -> None:
    SPEC_FILE.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")

    sample = _merge_state_controls(_load_acs_sample())
    model = _estimate(sample)

    output = {
        "point_estimate": float(model.params["daca_post"]),
        "standard_error": float(model.bse["daca_post"]),
        "sample_size": int(len(sample)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
