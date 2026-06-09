"""
DiD estimate of DACA on full-time employment.

Sample  : Hispanic-Mexican, Mexico-born, non-citizen immigrants
          who arrived by 2007 and before age 16.
          Cohort window: birthyr 1975-1996 (±7 yrs around the DACA age cutoff of 1982).
Pre-DACA: 2009-2011; Post-DACA: 2013-2016 (2012 excluded as transition year).
Treated : born 1982-1996 (age < 31 as of June 15, 2012 → DACA-eligible by age).
Control : born 1975-1981 (just above the age threshold, similar characteristics).
Outcome : full_time = 1 if UHRSWORK >= 35 (employed full-time), 0 otherwise.
Model   : WLS DiD with HC1 SEs, controlling for sex, education, state FE.
"""

import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Column specs (0-based, half-open) from the Stata fixed-width infix layout.
# Only read the columns we need to keep peak memory low.
# ---------------------------------------------------------------------------
COLSPECS = [
    (0,   4),    # year        : cols  1- 4
    (65,  67),   # statefip    : cols 66-67
    (691, 701),  # perwt       : cols 692-701  (raw int; divide by 100)
    (739, 740),  # sex         : col  740
    (740, 743),  # age         : cols 741-743
    (747, 751),  # birthyr     : cols 748-751
    (763, 764),  # hispan      : col  764
    (767, 770),  # bpl         : cols 768-770
    (789, 790),  # citizen     : col  790
    (794, 798),  # yrimmig     : cols 795-798
    (859, 861),  # educ        : cols 860-861
    (874, 875),  # empstat     : col  875
    (904, 906),  # uhrswork    : cols 905-906
]
COLNAMES = [
    "year", "statefip", "perwt", "sex", "age", "birthyr",
    "hispan", "bpl", "citizen", "yrimmig", "educ", "empstat", "uhrswork",
]

# Use compact dtypes to minimise memory footprint.
DTYPES = {
    "year":     "int16",
    "statefip": "int8",
    "perwt":    "float32",
    "sex":      "int8",
    "age":      "int16",
    "birthyr":  "int16",
    "hispan":   "int8",
    "bpl":      "int16",
    "citizen":  "int8",
    "yrimmig":  "int16",
    "educ":     "int8",
    "empstat":  "int8",
    "uhrswork": "int8",
}

# ---------------------------------------------------------------------------
# Read in chunks, pre-filtering aggressively to keep the in-memory frame small.
# ---------------------------------------------------------------------------
CHUNKSIZE = 500_000
DATA_FILE  = "ACS_extract_expanded.dat"

chunks = []
for chunk in pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=COLNAMES,
    header=None,
    dtype=DTYPES,
    chunksize=CHUNKSIZE,
):
    # perwt is stored as integer with two implied decimals (e.g. 010461 → 104.61)
    chunk["perwt"] = chunk["perwt"] / 100.0

    # Keep only observations that could possibly belong to our analysis sample.
    # Broad pre-filter (strict filters applied after concatenation).
    mask = (
        (
            chunk["year"].between(2009, 2011) |   # pre-DACA period
            chunk["year"].between(2013, 2016)      # post-DACA period
        ) &
        (chunk["hispan"] == 1) &                   # Mexican-Hispanic
        (chunk["bpl"]    == 200) &                 # born in Mexico
        (chunk["citizen"] == 3) &                  # not a citizen (undocumented proxy)
        (chunk["yrimmig"] > 0) &                   # immigration year reported
        (chunk["yrimmig"] <= 2007) &               # continuous US residence since 2007
        (chunk["birthyr"].between(1975, 1996)) &   # cohort window around DACA age cutoff
        (chunk["age"] >= 16)                        # working-age respondents only
    )
    sub = chunk[mask].copy()
    if len(sub):
        chunks.append(sub)

df = pd.concat(chunks, ignore_index=True)

# ---------------------------------------------------------------------------
# Strict sample filters applied to the combined frame.
# ---------------------------------------------------------------------------

# Arrived before 16th birthday: immigration year <= birth year + 15
df = df[df["yrimmig"] <= df["birthyr"] + 15]

# Remove any rows with missing / implausible perwt
df = df[df["perwt"] > 0]

# ---------------------------------------------------------------------------
# Construct treatment, post, and outcome variables.
# ---------------------------------------------------------------------------

# Treated = 1 for the DACA-eligible cohort (born 1982–1996, age < 31 on 15 Jun 2012).
# Control = 0 for just-too-old cohort (born 1975–1981, age 31–37 on 15 Jun 2012).
df["treated"] = (df["birthyr"] >= 1982).astype("int8")

# Post = 1 for post-DACA years (2013–2016).
df["post"] = (df["year"] >= 2013).astype("int8")

# Outcome: usually works 35+ hours/week.
# UHRSWORK == 0 means N/A (not employed), so the indicator is naturally 0 for non-workers.
df["full_time"] = (df["uhrswork"] >= 35).astype("int8")

# Verify that both treatment arms are present, with variation pre and post.
variation = df.groupby(["treated", "post"])["full_time"].count()
assert variation.shape[0] == 4, "Missing treatment×period cells – revise specification."

# ---------------------------------------------------------------------------
# DiD regression: Linear Probability Model (WLS) with HC1 robust SEs.
# Controls: sex indicator, education level, state fixed effects.
# ---------------------------------------------------------------------------
formula = "full_time ~ treated + post + treated:post + C(sex) + educ + C(statefip)"

model = smf.wls(
    formula,
    data=df,
    weights=df["perwt"],
).fit(cov_type="HC1")

# Extract DiD coefficient and its standard error.
point_estimate = float(model.params["treated:post"])
standard_error = float(model.bse["treated:post"])
sample_size    = int(model.nobs)

# ---------------------------------------------------------------------------
# Output: exactly one JSON object to STDOUT.
# ---------------------------------------------------------------------------
print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size":    sample_size,
}))
