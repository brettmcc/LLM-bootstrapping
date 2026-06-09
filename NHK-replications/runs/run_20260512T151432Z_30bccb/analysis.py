import json
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ACS_extract_expanded.dat"


def _parse_int(text: str):
    text = text.strip()
    if not text:
        return None
    return int(text)


def load_sample() -> pd.DataFrame:
    rows = []
    with DATA_FILE.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            year = _parse_int(line[0:4])
            if year is None or not (2006 <= year <= 2016):
                continue

            hispan = _parse_int(line[763:764])
            bpl = _parse_int(line[767:770])
            citizen = _parse_int(line[789:790])
            age = _parse_int(line[740:743])
            birthyr = _parse_int(line[747:751])
            yrimmig = _parse_int(line[794:798])
            statefip = _parse_int(line[65:67])
            perwt = _parse_int(line[691:701])
            sex = _parse_int(line[739:740])
            empstat = _parse_int(line[874:875])
            uhrswork = _parse_int(line[904:906])

            if (
                hispan != 1
                or bpl != 200
                or citizen != 3
                or age is None
                or not (18 <= age <= 34)
                or birthyr is None
                or yrimmig is None
                or birthyr < 1982
                or yrimmig <= 0
                or yrimmig > 2007
                or yrimmig < birthyr
                or perwt is None
                or statefip is None
                or sex is None
            ):
                continue

            rows.append(
                {
                    "year": year,
                    "statefip": statefip,
                    "perwt": perwt,
                    "sex": sex,
                    "age": age,
                    "birthyr": birthyr,
                    "yrimmig": yrimmig,
                    "empstat": empstat,
                    "uhrswork": uhrswork,
                }
            )

    if not rows:
        raise RuntimeError("No observations remain after applying the sample filters.")

    df = pd.DataFrame.from_records(rows)
    df["perwt"] = df["perwt"] / 100.0
    df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    df["daca_eligible"] = (
        (df["birthyr"] >= 1982)
        & (df["yrimmig"] <= 2007)
        & ((df["yrimmig"] - df["birthyr"]) <= 15)
    ).astype(int)
    df["post_daca"] = (df["year"] >= 2013).astype(int)
    df["sex_female"] = (df["sex"] == 2).astype(int)

    if df["daca_eligible"].nunique() < 2:
        raise RuntimeError("DACA eligibility lacks variation in the selected sample.")
    if df["post_daca"].nunique() < 2:
        raise RuntimeError("Post-DACA indicator lacks variation in the selected sample.")

    return df


def fit_model(df: pd.DataFrame):
    # Keep the model compact so it runs reliably in the constrained environment.
    formula = "full_time ~ daca_eligible * post_daca + age + sex_female + C(year)"
    model = smf.wls(formula, data=df, weights=df["perwt"]).fit(
        cov_type="cluster",
        cov_kwds={"groups": df["statefip"]},
    )
    return model


def main() -> None:
    df = load_sample()
    model = fit_model(df)
    interaction_name = "daca_eligible:post_daca"
    output = {
        "point_estimate": float(model.params[interaction_name]),
        "standard_error": float(model.bse[interaction_name]),
        "sample_size": int(len(df)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
