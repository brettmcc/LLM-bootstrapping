"""
Difference-in-Differences (DiD) analysis of DACA's effect on full-time employment
among Mexican-born, Mexican-Hispanic, non-citizen adults in the United States.

IDENTIFICATION STRATEGY:
  DACA was announced June 15, 2012, with applications opening August 15, 2012.
  Eligibility required (among other things) not yet having turned 31 as of
  June 15, 2012 (i.e., born after June 15, 1981).

  We exploit this age cutoff as our treatment/control split:
    - Treatment group: birthyr >= 1982  (under-31 on DACA date => potentially eligible)
    - Control group:   birthyr <= 1980  (over-31 on DACA date => age-ineligible)
    - birthyr == 1981 is excluded (ambiguous without birth month)

  Both groups must satisfy the other non-age DACA criteria:
    - Arrived in the US before their 16th birthday (arrival_age <= 15)
    - Immigrated by 2007 (yrimmig <= 2007, satisfying the 5-year presence requirement)
    - Not a US citizen

  DiD equation:
    full_time = alpha + beta1*treat + beta2*post + beta3*(treat x post)
                + year FEs + state FEs + age FEs + sex + educ + state_unemp + e

  beta3 is the DiD estimator of DACA's effect on the probability of full-time employment.

PRE/POST PERIODS:
  Pre:  2009-2011 (post-recession baseline, prior to DACA)
  Post: 2013-2016 (after DACA implementation)
  Year 2012 is excluded as the transition year.

OUTPUT: prints a single JSON object to STDOUT with keys:
  "point_estimate", "standard_error", "sample_size"
"""

import json
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ──────────────────────────────────────────────────────────────────────────────
# FILE PATHS (all relative to the script's directory)
# ──────────────────────────────────────────────────────────────────────────────
DATA_DIR    = os.path.dirname(os.path.abspath(__file__))
ACS_FILE    = os.path.join(DATA_DIR, "ACS_extract_expanded.dat")
POLICY_FILE = os.path.join(DATA_DIR, "policy_labor_market_data.csv")

# ──────────────────────────────────────────────────────────────────────────────
# FIXED-WIDTH COLUMN SPECIFICATIONS
# Source: ACS_extract_expanded_layout_excerpt.do
# Format: (start-1, end) in 0-indexed Python half-open intervals
# e.g., Stata position 66-67  =>  Python colspec (65, 67)
# ──────────────────────────────────────────────────────────────────────────────
COLSPECS = [
    (0,   4),    # year      1-4       : survey year
    (65,  67),   # statefip  66-67     : state FIPS code
    (138, 139),  # gq        139-139   : group quarters type
    (691, 701),  # perwt     692-701   : person weight (raw; divide by 100)
    (739, 740),  # sex       740-740   : sex (1=male, 2=female)
    (740, 743),  # age       741-743   : age in years
    (747, 751),  # birthyr   748-751   : year of birth
    (763, 764),  # hispan    764-764   : Hispanic origin (1=Mexican)
    (767, 770),  # bpl       768-770   : birthplace (200=Mexico)
    (789, 790),  # citizen   790-790   : citizenship (3=non-citizen, 4=1st papers)
    (794, 798),  # yrimmig   795-798   : year of immigration (0=N/A, 996=not reported)
    (859, 861),  # educ      860-861   : educational attainment code
    (874, 875),  # empstat   875-875   : employment status (1=employed)
    (904, 906),  # uhrswork  905-906   : usual hours worked per week
]

COLNAMES = [
    "year", "statefip", "gq", "perwt", "sex", "age", "birthyr",
    "hispan", "bpl", "citizen", "yrimmig", "educ", "empstat", "uhrswork",
]

# Compact dtypes to reduce memory footprint while reading
DTYPES = {
    "year":     "int16",
    "statefip": "int16",   # int8 max is 127; some FIPS codes are fine, but int16 is safer
    "gq":       "int8",
    "perwt":    "float64", # read as float; will divide by 100
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

# Survey years to include (DACA enacted mid-2012; exclude 2012 entirely)
VALID_YEARS = {2009, 2010, 2011, 2013, 2014, 2015, 2016}

# ──────────────────────────────────────────────────────────────────────────────
# READ ACS DATA IN CHUNKS (to stay well within 30 GB memory budget)
# ──────────────────────────────────────────────────────────────────────────────
CHUNKSIZE = 500_000   # rows per chunk; adjust down if memory is tight

chunks = []
for chunk in pd.read_fwf(
    ACS_FILE,
    colspecs=COLSPECS,
    names=COLNAMES,
    dtype=DTYPES,
    chunksize=CHUNKSIZE,
    header=None,           # no header row in .dat file
):
    # ── Rescale person weight: raw field has 2 implied decimal places ──────
    chunk["perwt"] = chunk["perwt"] / 100.0

    # ── Early row filters (applied before storing, to minimize memory) ─────

    # 1. Keep only study years
    chunk = chunk[chunk["year"].isin(VALID_YEARS)]

    # 2. Keep Mexican-Hispanic individuals (HISPAN=1) born in Mexico (BPL=200)
    chunk = chunk[(chunk["hispan"] == 1) & (chunk["bpl"] == 200)]

    # 3. Keep non-citizens only (CITIZEN=3 not a citizen; CITIZEN=4 has first papers)
    chunk = chunk[chunk["citizen"].isin([3, 4])]

    # 4. Exclude institutional group quarters (prisons, nursing homes: GQ=3)
    chunk = chunk[chunk["gq"] != 3]

    # 5. Keep only rows with a valid immigration year
    #    0    = N/A (US-born, not applicable)
    #    996  = Not reported
    chunk = chunk[(chunk["yrimmig"] > 0) & (chunk["yrimmig"] != 996)]

    # 6. Keep working-age adults (restricts birth years to plausible range)
    chunk = chunk[(chunk["age"] >= 18) & (chunk["age"] <= 45)]

    if len(chunk) > 0:
        chunks.append(chunk)

# Combine all filtered chunks into a single DataFrame
df = pd.concat(chunks, ignore_index=True)

# ──────────────────────────────────────────────────────────────────────────────
# APPLY DACA ELIGIBILITY CRITERIA
# ──────────────────────────────────────────────────────────────────────────────

# Age at arrival in the US: year of immigration minus birth year
# (yrimmig is calendar year, birthyr is calendar year => integer age approximation)
df["arrival_age"] = (df["yrimmig"] - df["birthyr"]).astype("int16")

# DACA Criterion: arrived before 16th birthday
df = df[df["arrival_age"] <= 15]

# DACA Criterion: lived continuously in US since June 15, 2007 => immigrated by 2007
df = df[df["yrimmig"] <= 2007]

# DACA Age Cutoff: not yet 31 years old on June 15, 2012
#   => born AFTER June 15, 1981
#   => using birth year only (no birth month): birthyr >= 1982 treated as eligible
#                                              birthyr <= 1980 treated as ineligible
#   => birthyr == 1981 is ambiguous (could be before or after June 15) => exclude
df = df[df["birthyr"] != 1981]

# Binary treatment indicator: 1 = DACA age-eligible, 0 = age-ineligible
df["treat"] = (df["birthyr"] >= 1982).astype("int8")

# Binary post-period indicator: 1 = 2013-2016 (post-DACA), 0 = 2009-2011 (pre-DACA)
df["post"] = (df["year"] >= 2013).astype("int8")

# ──────────────────────────────────────────────────────────────────────────────
# OUTCOME VARIABLE: Full-time employment
# Definition: employed (EMPSTAT=1) AND usually works >= 35 hours per week
# UHRSWORK=0 means N/A (not in labor force / unemployed) => full_time=0 for those
# ──────────────────────────────────────────────────────────────────────────────
df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype("int8")

# ──────────────────────────────────────────────────────────────────────────────
# MERGE STATE-LEVEL CONTROLS (state unemployment rate as labor market control)
# ──────────────────────────────────────────────────────────────────────────────
policy = pd.read_csv(POLICY_FILE)

# Keep only the state identifier, year, and labor market variables
policy = policy[["state_fips", "year", "UNEMP", "LFPR"]].copy()
policy.rename(columns={"state_fips": "statefip",
                        "UNEMP": "state_unemp",
                        "LFPR":  "state_lfpr"}, inplace=True)
policy["statefip"] = policy["statefip"].astype("int16")
policy["year"]     = policy["year"].astype("int16")

# Left join: every ACS row stays; rows without a matching state-year get NaN
df = df.merge(policy, on=["statefip", "year"], how="left")

# Drop rows where state unemployment is missing (should be very few or none)
df = df.dropna(subset=["state_unemp"])

# ──────────────────────────────────────────────────────────────────────────────
# VERIFY THAT THERE IS VARIATION IN THE TREATMENT
# ──────────────────────────────────────────────────────────────────────────────
n_treat   = int((df["treat"] == 1).sum())
n_control = int((df["treat"] == 0).sum())

if n_treat == 0 or n_control == 0:
    # If no variation, something is wrong with the sample construction
    sys.stderr.write(
        f"ERROR: No treatment variation. treat=1: {n_treat}, treat=0: {n_control}\n"
    )
    sys.exit(1)

# ──────────────────────────────────────────────────────────────────────────────
# DIFFERENCE-IN-DIFFERENCES REGRESSION
# Linear Probability Model (WLS with person weights)
#
# Outcome:    full_time  (1 = employed full-time, 0 = otherwise)
# Key term:   treat:post (DiD coefficient = causal effect of DACA eligibility
#                         on probability of full-time employment)
# Fixed effects: year, state (FIPS), age in years
# Additional controls: sex, education code, state unemployment rate
# Standard errors: clustered at the state level
# ──────────────────────────────────────────────────────────────────────────────
model_formula = (
    "full_time ~ treat * post"
    " + C(year) + C(statefip) + C(age)"
    " + sex + educ + state_unemp"
)

result = smf.wls(
    model_formula,
    data=df,
    weights=df["perwt"],
).fit(
    cov_type="cluster",
    cov_kwds={"groups": df["statefip"]},
)

# ──────────────────────────────────────────────────────────────────────────────
# OUTPUT: single JSON object to STDOUT (no other output)
# ──────────────────────────────────────────────────────────────────────────────
output = {
    "point_estimate": round(float(result.params["treat:post"]), 6),
    "standard_error": round(float(result.bse["treat:post"]),   6),
    "sample_size":    int(result.nobs),
}

print(json.dumps(output))
