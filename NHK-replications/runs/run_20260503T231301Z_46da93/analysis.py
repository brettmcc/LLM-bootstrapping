"""
DACA Effect on Full-Time Employment -- Difference-in-Differences

Sample  : Hispanic-Mexican (HISPAN==1), born in Mexico (BPL==200),
          non-citizen (CITIZEN in 3,4), arrived before age 16,
          age >= 18, birth year 1975-1996.
Years   : 2008-2011 (pre-DACA) and 2013-2016 (post-DACA); 2012 excluded
          because DACA was announced/implemented mid-year.
Treatment: DACA-age-eligible = birth year >= 1982 (age <= 30 on June 15, 2012).
           Control cohort     = birth year 1975-1981 (age 31-37, just over limit).
Outcome : Full-time employed: currently employed (EMPSTAT==1) AND
          usually works >= 35 hrs/week (UHRSWORK >= 35).
Model   : WLS linear probability DiD with year FE and state FE.
          SE: HC1 heteroskedasticity-robust.
"""

import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Column specs from the Stata infix layout (1-based) converted to Python
# 0-based (start inclusive, end exclusive) for pd.read_fwf.
# ---------------------------------------------------------------------------
# Stata layout:  variable  start-end  (1-based)
# Python:        (start-1, end)
COLSPECS = [
    (0,   4),    # year        1-4
    (65,  67),   # statefip   66-67
    (691, 701),  # perwt      692-701  (raw int; divide by 100)
    (739, 740),  # sex        740-740
    (740, 743),  # age        741-743
    (747, 751),  # birthyr    748-751
    (763, 764),  # hispan     764-764
    (767, 770),  # bpl        768-770
    (789, 790),  # citizen    790-790
    (794, 798),  # yrimmig    795-798
    (859, 861),  # educ       860-861
    (874, 875),  # empstat    875-875
    (904, 906),  # uhrswork   905-906
]

COLNAMES = [
    "year", "statefip", "perwt", "sex", "age", "birthyr",
    "hispan", "bpl", "citizen", "yrimmig", "educ", "empstat", "uhrswork",
]

# Years to keep (exclude 2012 transition year)
PRE_YEARS  = {2008, 2009, 2010, 2011}
POST_YEARS = {2013, 2014, 2015, 2016}
ALL_YEARS  = PRE_YEARS | POST_YEARS

# ---------------------------------------------------------------------------
# Read fixed-width file in chunks and keep only the relevant rows early
# to stay well within memory limits.
# ---------------------------------------------------------------------------
CHUNK_SIZE = 300_000  # rows per chunk

kept_chunks = []

for chunk in pd.read_fwf(
    "ACS_extract_expanded.dat",
    colspecs=COLSPECS,
    names=COLNAMES,
    dtype="int64",      # all selected columns are integers
    header=None,
    chunksize=CHUNK_SIZE,
):
    # Early row filter -- keeps only the small subset we need
    mask = (
        (chunk["hispan"] == 1)              &   # Mexican Hispanic
        (chunk["bpl"]    == 200)            &   # Born in Mexico
        (chunk["citizen"].isin([3, 4]))     &   # Non-citizen (undocumented proxy)
        (chunk["year"].isin(ALL_YEARS))     &   # Pre- and post-DACA years
        (chunk["birthyr"] >= 1975)          &   # Relevant birth cohorts
        (chunk["birthyr"] <= 1996)          &
        (chunk["age"] >= 18)               &   # Working-age adults
        (chunk["yrimmig"] > 0)                  # Year of immigration is known
    )
    kept_chunks.append(chunk.loc[mask].copy())

df = pd.concat(kept_chunks, ignore_index=True)

# Scale person weight (2 implied decimal places stored as integer in raw data)
df["perwt"] = df["perwt"] / 100.0

# ---------------------------------------------------------------------------
# Apply remaining eligibility filters
# ---------------------------------------------------------------------------

# DACA requires arriving in the US BEFORE the 16th birthday.
# Approximate age at immigration = yrimmig - birthyr.
df = df[df["yrimmig"] < df["birthyr"] + 16].copy()

# Drop any rows with zero/missing weight
df = df[df["perwt"] > 0].copy()

# ---------------------------------------------------------------------------
# Construct treatment, time, and outcome variables
# ---------------------------------------------------------------------------

# Post-DACA period indicator
df["post"] = (df["year"] >= 2013).astype(int)

# DACA age-eligibility: born 1982 or later => age <= 30 on June 15, 2012
# (Cohorts 1975-1981 serve as the just-too-old control group.)
df["daca_eligible"] = (df["birthyr"] >= 1982).astype(int)

# DiD interaction term (the coefficient of interest)
df["treat_post"] = df["daca_eligible"] * df["post"]

# Outcome: full-time employment
# Employed (empstat==1) AND usually works >= 35 hours per week (uhrswork>=35)
df["full_time"] = (
    (df["empstat"] == 1) & (df["uhrswork"] >= 35)
).astype(int)

# ---------------------------------------------------------------------------
# Sanity check: ensure variation in treatment
# ---------------------------------------------------------------------------
assert df["daca_eligible"].nunique() == 2, \
    "No variation in DACA eligibility -- revise birth-year cutoffs."
assert len(df) >= 500, \
    f"Sample too small ({len(df)} obs) -- revise filters."

# ---------------------------------------------------------------------------
# DiD regression (linear probability model, weighted least squares)
#
# Model: full_time = a0 + a1*daca_eligible + a2*treat_post
#                   + year FE + state FE + age + sex + educ + e
#
# Note: `post` is omitted because year fixed effects (C(year)) subsume it.
# The coefficient on treat_post is the DiD estimate of the DACA effect.
# HC1 heteroskedasticity-robust standard errors.
# ---------------------------------------------------------------------------
result = smf.wls(
    "full_time ~ daca_eligible + treat_post + C(year) + C(statefip) + age + sex + educ",
    data=df,
    weights=df["perwt"],
).fit(cov_type="HC1")

point_estimate = float(result.params["treat_post"])
standard_error = float(result.bse["treat_post"])
sample_size    = int(result.nobs)

# ---------------------------------------------------------------------------
# Output ONLY the required JSON (no extra text)
# ---------------------------------------------------------------------------
print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size":    sample_size,
}))
