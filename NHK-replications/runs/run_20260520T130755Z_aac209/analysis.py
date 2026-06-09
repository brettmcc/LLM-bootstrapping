from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
ACS_PATH = ROOT / "ACS_extract_expanded.dat"
STATE_PATH = ROOT / "policy_labor_market_data.csv"
SPEC_PATH = ROOT / "spec.json"


# Only the fields needed for the design are parsed from the fixed-width ACS file.
ACS_COLUMNS = [
    ("year", (0, 4)),
    ("state_fip", (65, 67)),
    ("sex", (739, 740)),
    ("age", (740, 743)),
    ("hispan", (763, 764)),
    ("bpld", (770, 775)),
    ("citizen", (789, 790)),
    ("yrimmig", (794, 798)),
    ("perwt", (691, 701)),
    ("empstat", (874, 875)),
    ("uhrswork", (904, 906)),
    ("qage", (1038, 1039)),
    ("qsex", (1041, 1042)),
    ("qbpl", (1042, 1043)),
    ("qcitizen", (1043, 1044)),
    ("qhispan", (1044, 1045)),
    ("qyrimm", (1048, 1049)),
    ("qempstat", (1052, 1053)),
    ("quhrswor", (1054, 1055)),
]

ACS_INTEGER_COLUMNS = [
    "year",
    "state_fip",
    "sex",
    "age",
    "hispan",
    "bpld",
    "citizen",
    "yrimmig",
    "empstat",
    "uhrswork",
    "qage",
    "qsex",
    "qbpl",
    "qcitizen",
    "qhispan",
    "qyrimm",
    "qempstat",
    "quhrswor",
]

SPEC = {
    "sample_selection": [
        "2006 <= year <= 2016 and year != 2012",
        "hispan == 1",
        "bpld == 20000",
        "citizen == 3",
        "qage == 0 and qsex == 0 and qbpl == 0 and qcitizen == 0 and qhispan == 0 and qyrimm == 0 and qempstat == 0 and quhrswor == 0",
        "empstat in [1, 2, 3]",
        "yrimmig > 0 and yrimmig <= year and yrimmig <= 2007",
        "age_at_arrival < 16",
        "18 <= age_2012 <= 40",
    ],
    "outcome_definition": "(uhrswork >= 35).astype(int)",
    "treatment_definition": "((age_2012 <= 30) & (age_at_arrival < 16) & (yrimmig > 0) & (yrimmig <= 2007)).astype(int)",
    "model_specification_line": 'model = smf.wls("full_time ~ eligible * post + age_2012_c + I(age_2012_c ** 2) + C(sex) + C(state_fip) + C(year) + LFPR + UNEMP", data=reg_df, weights=reg_df["perwt"]).fit(cov_type="cluster", cov_kwds={"groups": reg_df["state_fip"]})',
}


def read_acs_fixed_width() -> pd.DataFrame:
    """Stream the fixed-width ACS file and keep only rows that pass the sample filters."""

    state_lookup = load_state_lookup()
    rows = []

    def parse_int(field: str) -> int | None:
        text = field.strip()
        return int(text) if text else None

    with ACS_PATH.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if len(line) < 1055:
                continue

            year = parse_int(line[0:4])
            if year is None or year < 2006 or year > 2016 or year == 2012:
                continue

            state_fip = parse_int(line[65:67])
            sex = parse_int(line[739:740])
            age = parse_int(line[740:743])
            hispan = parse_int(line[763:764])
            bpld = parse_int(line[770:775])
            citizen = parse_int(line[789:790])
            yrimmig = parse_int(line[794:798])
            perwt_raw = parse_int(line[691:701])
            empstat = parse_int(line[874:875])
            uhrswork = parse_int(line[904:906])
            qage = parse_int(line[1038:1039])
            qsex = parse_int(line[1041:1042])
            qbpl = parse_int(line[1042:1043])
            qcitizen = parse_int(line[1043:1044])
            qhispan = parse_int(line[1044:1045])
            qyrimm = parse_int(line[1048:1049])
            qempstat = parse_int(line[1052:1053])
            quhrswor = parse_int(line[1054:1055])

            if (
                state_fip is None
                or sex is None
                or age is None
                or hispan is None
                or bpld is None
                or citizen is None
                or yrimmig is None
                or perwt_raw is None
                or empstat is None
                or uhrswork is None
                or qage is None
                or qsex is None
                or qbpl is None
                or qcitizen is None
                or qhispan is None
                or qyrimm is None
                or qempstat is None
                or quhrswor is None
            ):
                continue

            age_2012 = age - (year - 2012)
            age_at_arrival = age - (year - yrimmig)
            if not (
                hispan == 1
                and bpld == 20000
                and citizen == 3
                and qage == 0
                and qsex == 0
                and qbpl == 0
                and qcitizen == 0
                and qhispan == 0
                and qyrimm == 0
                and qempstat == 0
                and quhrswor == 0
                and empstat in (1, 2, 3)
                and yrimmig > 0
                and yrimmig <= year
                and yrimmig <= 2007
                and age_at_arrival < 16
                and 18 <= age_2012 <= 40
                and sex in (1, 2)
            ):
                continue

            controls = state_lookup.get((state_fip, year))
            if controls is None:
                continue

            rows.append(
                {
                    "year": year,
                    "state_fip": state_fip,
                    "sex": sex,
                    "age": age,
                    "hispan": hispan,
                    "bpld": bpld,
                    "citizen": citizen,
                    "yrimmig": yrimmig,
                    "perwt": perwt_raw / 100.0,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                    "qage": qage,
                    "qsex": qsex,
                    "qbpl": qbpl,
                    "qcitizen": qcitizen,
                    "qhispan": qhispan,
                    "qyrimm": qyrimm,
                    "qempstat": qempstat,
                    "quhrswor": quhrswor,
                    "age_2012": age_2012,
                    "age_at_arrival": age_at_arrival,
                    "post": 1 if year >= 2013 else 0,
                    "eligible": 1 if age_2012 <= 30 else 0,
                    "full_time": 1 if uhrswork >= 35 else 0,
                    "LFPR": controls["LFPR"],
                    "UNEMP": controls["UNEMP"],
                }
            )

    return pd.DataFrame.from_records(
        rows,
        columns=[
            "year",
            "state_fip",
            "sex",
            "age",
            "hispan",
            "bpld",
            "citizen",
            "yrimmig",
            "perwt",
            "empstat",
            "uhrswork",
            "qage",
            "qsex",
            "qbpl",
            "qcitizen",
            "qhispan",
            "qyrimm",
            "qempstat",
            "quhrswor",
            "age_2012",
            "age_at_arrival",
            "post",
            "eligible",
            "full_time",
            "LFPR",
            "UNEMP",
        ],
    )


def load_state_lookup() -> dict[tuple[int, int], dict[str, float]]:
    """Load the state-year controls into a lookup table."""

    state = pd.read_csv(STATE_PATH)
    state["state_fips"] = pd.to_numeric(state["state_fips"], errors="coerce").astype("Int64")
    state["year"] = pd.to_numeric(state["year"], errors="coerce").astype("Int64")

    lookup: dict[tuple[int, int], dict[str, float]] = {}
    for row in state.dropna(subset=["state_fips", "year", "LFPR", "UNEMP"]).itertuples(index=False):
        lookup[(int(row.state_fips), int(row.year))] = {
            "LFPR": float(row.LFPR),
            "UNEMP": float(row.UNEMP),
        }

    return lookup


def build_analysis_frame() -> pd.DataFrame:
    """Keep only the regression variables after streaming sample construction."""

    acs = read_acs_fixed_width()
    acs["age_2012_c"] = acs["age_2012"] - 30
    return acs.dropna(subset=["full_time", "eligible", "post", "age_2012_c", "sex", "state_fip", "year", "perwt", "LFPR", "UNEMP"])


def run_model(reg_df: pd.DataFrame):
    """Estimate the DiD specification and return the fitted model."""

    model = smf.wls(
        "full_time ~ eligible * post + age_2012_c + I(age_2012_c ** 2) + C(sex) + C(state_fip) + C(year) + LFPR + UNEMP",
        data=reg_df,
        weights=reg_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": reg_df["state_fip"]})
    return model


def main() -> None:
    analysis_df = build_analysis_frame()

    # The DACA contrast must vary in the final sample; fail fast if it does not.
    if analysis_df["eligible"].nunique(dropna=True) < 2:
        raise RuntimeError("Treatment does not vary in the analysis sample.")

    model = run_model(analysis_df)
    term = "eligible:post"

    spec_json = json.dumps(SPEC, indent=2)
    SPEC_PATH.write_text(spec_json, encoding="utf-8")

    result = {
        "point_estimate": float(model.params[term]),
        "standard_error": float(model.bse[term]),
        "sample_size": int(len(analysis_df)),
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
