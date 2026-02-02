import json
from pathlib import Path

import pandas as pd
import statsmodels.api as sm

BASE_PATH = Path("usa_00042.dat")

LAYOUT = {
    "year": (0, 4),
    "sample": (4, 10),
    "serial": (10, 18),
    "cbserial": (18, 31),
    "hhwt": (31, 41),
    "cluster": (41, 54),
    "statefip": (54, 56),
    "metarea": (56, 59),
    "metaread": (59, 63),
    "strata": (63, 75),
    "gq": (75, 76),
    "nfams": (76, 78),
    "nsubfam": (78, 79),
    "ncouples": (79, 80),
    "nmothers": (80, 81),
    "nfathers": (81, 82),
    "multgen": (82, 83),
    "multgend": (83, 85),
    "pernum": (85, 89),
    "perwt": (89, 99),
    "famsize": (99, 101),
    "nchild": (101, 102),
    "sex": (102, 103),
    "age": (103, 106),
    "birthqtr": (106, 107),
    "marst": (107, 108),
    "birthyr": (108, 112),
    "race": (112, 113),
    "raced": (113, 116),
    "hispan": (116, 117),
    "hispand": (117, 120),
    "bpl": (120, 123),
    "bpld": (123, 128),
    "citizen": (128, 129),
    "yrimmig": (129, 133),
    "language": (133, 135),
    "languaged": (135, 139),
    "speakeng": (139, 140),
    "school": (140, 141),
    "educ": (141, 143),
    "educd": (143, 146),
    "gradeatt": (146, 147),
    "gradeattd": (147, 149),
    "schltype": (149, 150),
    "empstat": (150, 151),
    "empstatd": (151, 153),
    "labforce": (153, 154),
    "wkswork2": (154, 155),
    "uhrswork": (155, 157),
}

SELECT = ["year", "hispand", "bpl", "labforce", "age", "uhrswork", "birthyr", "yrimmig"]


def read_data(chunksize: int = 200_000):
    colspecs = [(LAYOUT[name][0], LAYOUT[name][1]) for name in SELECT]
    dtype = {
        "year": "int16",
        "hispand": "int16",
        "bpl": "int16",
        "labforce": "int8",
        "age": "int16",
        "uhrswork": "int8",
        "birthyr": "int16",
        "yrimmig": "int16",
    }
    return pd.read_fwf(
        BASE_PATH,
        colspecs=colspecs,
        names=SELECT,
        dtype=dtype,
        chunksize=chunksize,
    )


def eligible_mask(subset: pd.DataFrame) -> pd.Series:
    arrival_age = subset["yrimmig"] - subset["birthyr"]
    age_2012 = 2012 - subset["birthyr"]
    return (
        (arrival_age < 16)
        & (subset["yrimmig"] <= 2007)
        & (age_2012 >= 16)
        & (age_2012 <= 30)
    )


def main():
    df_pieces = []
    for chunk in read_data():
        mask = (
            (chunk["year"] >= 2013)
            & (chunk["year"] <= 2016)
            & (chunk["labforce"] == 1)
            & (chunk["hispand"] == 107)
            & (chunk["bpl"] == 200)
            & (chunk["age"] >= 16)
            & (chunk["age"] <= 35)
            & (chunk["birthyr"] > 0)
            & (chunk["yrimmig"] > 0)
        )
        subset = chunk.loc[mask]
        if subset.empty:
            continue
        subset = subset.assign(
            treatment=eligible_mask(subset).astype(int),
            outcome=(subset["uhrswork"] >= 35).astype(int),
        )
        df_pieces.append(subset[["treatment", "outcome"]])
    if not df_pieces:
        raise SystemExit("No filtered rows")
    df = pd.concat(df_pieces, ignore_index=True)
    if df["treatment"].nunique() < 2:
        raise SystemExit("No variation in treatment")
    model = sm.OLS(df["outcome"], sm.add_constant(df[["treatment"]]))
    result = model.fit()
    output = {
        "point_estimate": float(result.params["treatment"]),
        "standard_error": float(result.bse["treatment"]),
        "sample_size": int(df.shape[0]),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
