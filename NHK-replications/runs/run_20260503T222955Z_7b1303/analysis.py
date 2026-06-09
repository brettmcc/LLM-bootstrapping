"""
Estimation of DACA eligibility effect on full-time employment.

Design: Difference-in-Differences (DiD) around the DACA age cutoff.
  - Treatment group : Mexican-born non-citizens born 1982-1996
    (born after June 15 1981 → under 31 on DACA announcement date)
  - Control group   : Same population born 1976-1981
    (just above the age cutoff, ineligible by age)
  - Pre-DACA period : 2006-2011
  - Post-DACA period: 2013-2016  (2012 excluded: DACA announced mid-year)

Additional eligibility proxies applied to both groups:
  - Arrived before age 16 (yrimmig - birthyr < 16)
  - Arrived before June 15 2007 (yrimmig <= 2007)
    [continuous US residence requirement]

Outcome : full_time = 1 if employed (empstat==1) AND uhrswork >= 35
Model   : WLS linear probability model with state FE, year FE, age
          polynomial, sex control, and state unemployment rate.
          Standard errors clustered at the state level.
"""

import json
import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# File paths (always relative to this script so the code runs on any machine)
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE   = os.path.join(SCRIPT_DIR, "ACS_extract_expanded.dat")
POLICY_FILE = os.path.join(SCRIPT_DIR, "policy_labor_market_data.csv")

# ---------------------------------------------------------------------------
# Column specifications derived from ACS_extract_expanded_layout_excerpt.do
#
# Stata layout uses 1-based column indices.
# Python's pd.read_fwf uses 0-based, end-exclusive colspecs:
#   Stata col A-B  →  Python (A-1, B)
# ---------------------------------------------------------------------------
COLSPECS = [
    (0,   4),    # year      cols   1-4
    (65,  67),   # statefip  cols  66-67
    (691, 701),  # perwt     cols 692-701  (raw int; .do divides by 100)
    (739, 740),  # sex       col  740
    (740, 743),  # age       cols 741-743
    (747, 751),  # birthyr   cols 748-751
    (763, 764),  # hispan    col  764
    (767, 770),  # bpl       cols 768-770
    (789, 790),  # citizen   col  790
    (794, 798),  # yrimmig   cols 795-798
    (874, 875),  # empstat   col  875
    (904, 906),  # uhrswork  cols 905-906
]

NAMES = [
    "year", "statefip", "perwt_raw", "sex", "age", "birthyr",
    "hispan", "bpl", "citizen", "yrimmig", "empstat", "uhrswork",
]

# Explicit dtypes minimise memory per chunk.
# int8 holds -128..127; int16 holds up to 32767; int64 for perwt_raw safety.
DTYPE = {
    "year":      "int16",
    "statefip":  "int8",
    "perwt_raw": "int64",   # stored as integer × 100 in the .dat file
    "sex":       "int8",
    "age":       "int16",
    "birthyr":   "int16",
    "hispan":    "int8",
    "bpl":       "int16",
    "citizen":   "int8",
    "yrimmig":   "int16",
    "empstat":   "int8",
    "uhrswork":  "int8",
}

# ---------------------------------------------------------------------------
# Read the fixed-width ACS file in chunks to stay well under the 30 GB cap
# ---------------------------------------------------------------------------
CHUNKSIZE = 500_000   # rows to read at once

chunks = []

reader = pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=NAMES,
    dtype=DTYPE,
    chunksize=CHUNKSIZE,
    header=None,          # raw data file has no header row
)

for chunk in reader:
    # Apply the perwt scaling documented in the .do file (perwt = perwt / 100)
    chunk["perwt"] = chunk["perwt_raw"].astype("float32") / 100.0
    chunk.drop(columns=["perwt_raw"], inplace=True)

    # ------------------------------------------------------------------
    # Per-chunk sample filters (applied early to minimise peak memory):
    #
    #  1. bpl == 200        : born in Mexico
    #  2. hispan == 1       : Hispanic of Mexican ethnicity
    #  3. citizen == 3      : not a citizen (proxy for undocumented status)
    #  4. year in list      : pre-DACA (2006-2011) or post-DACA (2013-2016)
    #                         — 2012 excluded (DACA announced mid-year)
    #  5. birthyr 1976-1996 : control group (1976-1981) + treatment (1982-1996)
    #  6. yrimmig > 0       : immigration year is recorded
    #  7. yrimmig >= birthyr: sanity check (arrived after birth)
    #  8. yrimmig-birthyr<16: arrived before 16th birthday (DACA requirement)
    #  9. yrimmig <= 2007   : arrived before continuous-residence threshold
    # 10. age >= 16         : working-age population only
    # ------------------------------------------------------------------
    PRE_POST_YEARS = [2006, 2007, 2008, 2009, 2010, 2011,
                      2013, 2014, 2015, 2016]
    mask = (
        (chunk["bpl"]    == 200) &
        (chunk["hispan"] == 1)   &
        (chunk["citizen"] == 3)  &
        (chunk["year"].isin(PRE_POST_YEARS)) &
        (chunk["birthyr"] >= 1976) &
        (chunk["birthyr"] <= 1996) &
        (chunk["yrimmig"]  > 0)  &
        (chunk["yrimmig"] >= chunk["birthyr"]) &
        ((chunk["yrimmig"] - chunk["birthyr"]) < 16) &
        (chunk["yrimmig"] <= 2007) &
        (chunk["age"] >= 16)
    )
    filtered = chunk[mask].copy()
    if len(filtered) > 0:
        chunks.append(filtered)

# Combine all filtered chunks into one DataFrame
df = pd.concat(chunks, ignore_index=True)

# ---------------------------------------------------------------------------
# Merge state-level unemployment rate (time-varying control)
# ---------------------------------------------------------------------------
policy = pd.read_csv(POLICY_FILE, usecols=["state_fips", "year", "UNEMP"])

# policy_labor_market_data.csv uses 'state_fips'; ACS uses 'statefip'
df = df.merge(
    policy,
    left_on=["statefip", "year"],
    right_on=["state_fips", "year"],
    how="left",
)
df.drop(columns=["state_fips"], inplace=True)

# ---------------------------------------------------------------------------
# Construct outcome, treatment, and control variables
# ---------------------------------------------------------------------------

# Outcome: currently employed full-time (employed AND usual hours >= 35/wk)
df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype("int8")

# Treatment: DACA-eligible by the age cutoff
#   DACA required < 31 years old on June 15 2012 → born after June 15 1981
#   Annual approximation: eligible if birthyr >= 1982
df["eligible"] = (df["birthyr"] >= 1982).astype("int8")

# Post-DACA period indicator (DACA became operational in August 2012;
# first full post-year is 2013)
df["post"] = (df["year"] >= 2013).astype("int8")

# DiD interaction — this coefficient is the causal estimate of interest
df["eligible_post"] = df["eligible"] * df["post"]

# Age polynomial for lifecycle employment profile controls
df["age_f"]  = df["age"].astype("float32")
df["age_sq"] = df["age_f"] ** 2

# Male indicator (sex == 1 in ACS codebook)
df["male"] = (df["sex"] == 1).astype("int8")

# ---------------------------------------------------------------------------
# Verify treatment variation across all four DiD cells before regression
# ---------------------------------------------------------------------------
cell_counts = df.groupby(["eligible", "post"]).size()
assert (cell_counts > 0).all(), (
    f"One or more DiD cells are empty — revise specification.\n{cell_counts}"
)

# ---------------------------------------------------------------------------
# Difference-in-Differences regression
#
#   LPM: full_time = β0
#          + β1·eligible + β2·post + β3·(eligible×post)   ← DiD terms
#          + β4·age + β5·age²                              ← lifecycle
#          + β6·male                                        ← composition
#          + β7·UNEMP                                       ← state LM cycle
#          + state FE + year FE                             ← common trends
#          + ε
#
#   β3 (eligible_post) is the causal estimate: the change in full-time
#   employment probability attributable to DACA eligibility.
#
#   Estimator : WLS with ACS person weights (perwt) for population inference
#   Std errors: clustered at the state level
# ---------------------------------------------------------------------------
model = smf.wls(
    (
        "full_time ~ eligible_post + eligible + post"
        " + age_f + age_sq + male + UNEMP"
        " + C(statefip) + C(year)"
    ),
    data=df,
    weights=df["perwt"],
)

result = model.fit(
    cov_type="cluster",
    cov_kwds={"groups": df["statefip"]},
)

# ---------------------------------------------------------------------------
# Print ONLY the JSON result to stdout (no other output)
# ---------------------------------------------------------------------------
output = {
    "point_estimate": round(float(result.params["eligible_post"]), 6),
    "standard_error": round(float(result.bse["eligible_post"]),    6),
    "sample_size":    int(result.nobs),
}

print(json.dumps(output))
