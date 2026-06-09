"""
DACA effect on full-time employment among Hispanic-Mexican Mexico-born immigrants.

Design: Difference-in-Differences (DiD)
  - Treated : born >= 1982 (at most 30 on June 15, 2012 → DACA age-eligible)
  - Control : born 1977-1981 (31-35 on June 15, 2012 → just missed age cutoff)
  - Pre-period  : 2009-2011
  - Post-period : 2013-2016 (2012 excluded as transition year)
Outcome : full_time = 1 if usual hours worked >= 35/week, else 0
Estimator: WLS OLS with state + year FE, clustered SEs at state level
"""

import os
import sys
import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Fixed-width column layout (0-indexed start, exclusive end)
# Source: ACS_extract_expanded_layout_excerpt.do  (Stata 1-indexed → subtract 1)
# ---------------------------------------------------------------------------
COLS = {
    "year":     (0,   4),    # 1-4
    "statefip": (65,  67),   # 66-67
    "gq":       (138, 139),  # 139-139
    "perwt":    (691, 701),  # 692-701  (2 implied decimals → divide by 100)
    "sex":      (739, 740),  # 740-740
    "age":      (740, 743),  # 741-743
    "birthyr":  (747, 751),  # 748-751
    "hispan":   (763, 764),  # 764-764
    "bpl":      (767, 770),  # 768-770
    "citizen":  (789, 790),  # 790-790
    "yrimmig":  (794, 798),  # 795-798
    "uhrswork": (904, 906),  # 905-906
}

# ---------------------------------------------------------------------------
# Read fixed-width file in chunks to limit peak memory usage
# ---------------------------------------------------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
dat_file   = os.path.join(script_dir, "ACS_extract_expanded.dat")

colspecs = list(COLS.values())
col_names = list(COLS.keys())

CHUNK_SIZE = 500_000
chunks = []

for chunk in pd.read_fwf(
    dat_file,
    colspecs=colspecs,
    names=col_names,
    header=None,
    chunksize=CHUNK_SIZE,
):
    # Coerce all columns to numeric (non-parseable → NaN)
    for c in col_names:
        chunk[c] = pd.to_numeric(chunk[c], errors="coerce")

    # Early filter to reduce data volume:
    #   Mexican Hispanic (hispan=1) + born in Mexico (bpl=200)
    #   + non-citizen (3=not a citizen, 4=not a citizen / first papers)
    #   + has an immigration year + arrived by 2007
    #   + not in institutional group quarters
    mask = (
        (chunk["hispan"] == 1)           &  # Mexican-Hispanic identity
        (chunk["bpl"]    == 200)         &  # born in Mexico
        (chunk["citizen"].isin([3, 4]))  &  # non-citizen
        (chunk["yrimmig"] > 0)           &  # immigration year known
        (chunk["yrimmig"] <= 2007)       &  # in US continuously since 2007
        (chunk["gq"].isin([1, 2]))          # non-institutional household
    )
    chunks.append(chunk[mask])

df = pd.concat(chunks, ignore_index=True)

# ---------------------------------------------------------------------------
# Type-cast and clean
# ---------------------------------------------------------------------------
df = df.dropna(subset=col_names)

int_cols   = ["year", "statefip", "gq", "sex", "age", "birthyr",
              "hispan", "bpl", "citizen", "yrimmig", "uhrswork"]
float_cols = ["perwt"]

df = df.astype({c: int   for c in int_cols})
df = df.astype({c: float for c in float_cols})

# perwt has 2 implied decimal digits in the raw file
df["perwt"] = df["perwt"] / 100.0

# Age at immigration (approximate; used to check arrived-before-16 criterion)
df["arrival_age"] = df["yrimmig"] - df["birthyr"]

# ---------------------------------------------------------------------------
# Apply sample filters
# ---------------------------------------------------------------------------
df = df[
    (df["arrival_age"] < 16)                                         &  # arrived before age 16
    (df["year"].isin([2009, 2010, 2011, 2013, 2014, 2015, 2016]))   &  # pre/post DACA years
    (df["age"].between(18, 40))                                      &  # working-age adults
    (df["birthyr"].between(1977, 1996))                                 # DiD age comparison window
].copy()

# ---------------------------------------------------------------------------
# Treatment, post-period, and interaction indicator
# ---------------------------------------------------------------------------
# Treated  : born >= 1982  →  at most 30 on June 15, 2012 (DACA age-eligible)
# Control  : born 1977-1981 →  31-35 on June 15, 2012 (missed the age cutoff)
df["treated"]      = (df["birthyr"] >= 1982).astype(int)
df["post"]         = (df["year"]    >= 2013).astype(int)
df["treated_post"] = df["treated"] * df["post"]

# ---------------------------------------------------------------------------
# Outcome: full-time employment (usual hours >= 35/week)
# uhrswork == 0 means N/A (not working) → full_time = 0 for non-workers
# ---------------------------------------------------------------------------
df["full_time"] = (df["uhrswork"] >= 35).astype(int)

# ---------------------------------------------------------------------------
# Additional controls
# ---------------------------------------------------------------------------
df["age2"]  = df["age"] ** 2
df["state"] = df["statefip"].astype(str).str.zfill(2)   # state FE string
df["yr"]    = df["year"].astype(str)                     # year FE string

# ---------------------------------------------------------------------------
# Verify treatment variation
# ---------------------------------------------------------------------------
if df["treated"].nunique() < 2:
    sys.stderr.write("ERROR: No variation in treatment variable.\n")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Weighted DiD OLS with state + year fixed effects
# Clustered standard errors at the state level
# ---------------------------------------------------------------------------
formula = (
    "full_time ~ treated_post + treated + post"
    " + age + age2 + C(sex) + C(state) + C(yr)"
)

result = smf.wls(
    formula,
    data=df,
    weights=df["perwt"],
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["state"]},
)

# ---------------------------------------------------------------------------
# Output JSON to STDOUT (only)
# ---------------------------------------------------------------------------
output = {
    "point_estimate": round(float(result.params["treated_post"]), 6),
    "standard_error": round(float(result.bse["treated_post"]),    6),
    "sample_size":    int(result.nobs),
}

print(json.dumps(output))
