#!/usr/bin/env python3
"""
DACA effect on full-time employment: Difference-in-Differences.

Sample: Mexican-born, Hispanic-Mexican, non-citizen individuals in ACS 2009-2011
        and 2013-2016 (2012 excluded as DACA transition year) who arrived in the
        US before their 16th birthday and by 2007.

Treatment: DACA-eligible birth cohort (born 1982–1997; under 31 on June 15, 2012).
Control  : Just-too-old cohort (born 1972–1981; 31+ on June 15, 2012).
Outcome  : Full-time employment (EMPSTAT=1 AND UHRSWORK>=35).
Model    : Weighted OLS DiD with state and year fixed effects.
"""

import sys
import json
import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE  = os.path.join(SCRIPT_DIR, "ACS_extract_expanded.dat")

# ---------------------------------------------------------------------------
# Fixed-width column specs
# Stata infix positions are 1-indexed inclusive → Python colspecs are (start-1, end)
# ---------------------------------------------------------------------------
COLSPECS = [
    (0,   4),    # year     : survey year
    (65,  67),   # statefip : state FIPS
    (138, 139),  # gq       : group-quarters status
    (691, 701),  # perwt    : person weight (2 implied decimal places)
    (740, 743),  # age      : age
    (747, 751),  # birthyr  : year of birth
    (763, 764),  # hispan   : Hispanic origin general (1=Mexican)
    (767, 770),  # bpl      : birthplace (200=Mexico)
    (789, 790),  # citizen  : citizenship (3=not citizen, 4=first papers)
    (794, 798),  # yrimmig  : year of immigration
    (874, 875),  # empstat  : employment status (1=employed)
    (904, 906),  # uhrswork : usual hours worked per week
]
COLNAMES = [
    "year", "statefip", "gq", "perwt", "age", "birthyr",
    "hispan", "bpl", "citizen", "yrimmig", "empstat", "uhrswork",
]

VALID_YEARS = {2009, 2010, 2011, 2013, 2014, 2015, 2016}
CHUNKSIZE   = 200_000

# ---------------------------------------------------------------------------
# Read and filter in chunks (memory-efficient)
# ---------------------------------------------------------------------------
chunks = []
for chunk in pd.read_fwf(
        DATA_FILE,
        colspecs=COLSPECS,
        names=COLNAMES,
        header=None,
        dtype=str,          # read as strings; convert after
        chunksize=CHUNKSIZE):

    # Convert to numeric; coerce non-numeric strings to NaN
    for col in COLNAMES:
        chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

    # PERWT has 2 implied decimal places (e.g. stored as 10461 → 104.61)
    chunk["perwt"] = chunk["perwt"] / 100.0

    # --- Early row-level filters to reduce memory footprint ---
    # 1. Keep only the relevant survey years
    chunk = chunk[chunk["year"].isin(VALID_YEARS)]
    if chunk.empty:
        continue

    # 2. Born in Mexico (BPL = 200)
    chunk = chunk[chunk["bpl"] == 200]
    if chunk.empty:
        continue

    # 3. Hispanic-Mexican ethnicity (HISPAN = 1)
    chunk = chunk[chunk["hispan"] == 1]
    if chunk.empty:
        continue

    # 4. Non-citizen (CITIZEN = 3 or 4) – proxy for undocumented status
    chunk = chunk[chunk["citizen"].isin([3, 4])]
    if chunk.empty:
        continue

    # 5. Living in a household, not group quarters (GQ = 1 or 2)
    chunk = chunk[chunk["gq"].isin([1, 2])]
    if chunk.empty:
        continue

    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)
del chunks  # free memory

# ---------------------------------------------------------------------------
# Drop rows with missing values in key variables
# ---------------------------------------------------------------------------
df = df.dropna(subset=["birthyr", "yrimmig", "empstat", "uhrswork", "statefip"])

# Cast to memory-efficient types
df["year"]     = df["year"].astype("int16")
df["statefip"] = df["statefip"].astype("int16")
df["gq"]       = df["gq"].astype("int8")
df["perwt"]    = df["perwt"].astype("float32")
df["age"]      = df["age"].astype("int16")
df["birthyr"]  = df["birthyr"].astype("int16")
df["hispan"]   = df["hispan"].astype("int8")
df["bpl"]      = df["bpl"].astype("int16")
df["citizen"]  = df["citizen"].astype("int8")
df["yrimmig"]  = df["yrimmig"].astype("int16")
df["empstat"]  = df["empstat"].astype("int8")
df["uhrswork"] = df["uhrswork"].astype("int8")

# ---------------------------------------------------------------------------
# Apply DACA structural eligibility filters
# ---------------------------------------------------------------------------
# Exclude invalid immigration year (0 = N/A)
df = df[df["yrimmig"] > 0]

# Must have arrived before their 16th birthday: yrimmig <= birthyr + 15
df = df[df["yrimmig"] <= df["birthyr"] + 15]

# Must have been in the US continuously since June 15, 2007: yrimmig <= 2007
df = df[df["yrimmig"] <= 2007]

# Restrict to relevant birth cohorts:
#   Treatment (DACA eligible)  : born 1982–1997  (under 31 as of June 15, 2012)
#   Control   (just too old)   : born 1972–1981  (31–40 as of June 15, 2012)
df = df[(df["birthyr"] >= 1972) & (df["birthyr"] <= 1997)]

# ---------------------------------------------------------------------------
# Construct analysis variables
# ---------------------------------------------------------------------------
# Treatment indicator: DACA-eligible birth cohort (birthyr >= 1982)
df["daca_eligible"] = (df["birthyr"] >= 1982).astype("int8")

# Post-DACA period (2013 onward; 2012 excluded)
df["post"] = (df["year"] >= 2013).astype("int8")

# DiD interaction term: treatment × post
df["daca_x_post"] = df["daca_eligible"] * df["post"]

# Outcome: full-time employment (employed AND usually works ≥35 hours/week)
df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype("int8")

# ---------------------------------------------------------------------------
# Check for treatment variation (required before regression)
# ---------------------------------------------------------------------------
treat_counts = df["daca_eligible"].value_counts()
print(f"[INFO] daca_eligible counts: {treat_counts.to_dict()}", file=sys.stderr)
print(f"[INFO] total sample: {len(df):,}", file=sys.stderr)
print(f"[INFO] full_time mean: {df['full_time'].mean():.4f}", file=sys.stderr)

if df["daca_eligible"].nunique() < 2:
    print("[ERROR] No variation in treatment variable. Exiting.", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# DiD regression: weighted OLS with state and year fixed effects
# Cluster-robust SEs at the state level (standard for DiD)
# ---------------------------------------------------------------------------
model = smf.wls(
    # daca_eligible  : level difference between treated & control (pre-period)
    # daca_x_post    : DiD coefficient = causal effect of DACA (our target)
    # C(statefip)    : state fixed effects
    # C(year)        : year fixed effects (absorbs the 'post' main effect)
    formula="full_time ~ daca_eligible + daca_x_post + C(statefip) + C(year)",
    data=df,
    weights=df["perwt"],
)
result = model.fit(
    cov_type="cluster",
    cov_kwds={"groups": df["statefip"]},
)

# ---------------------------------------------------------------------------
# Extract and output results
# ---------------------------------------------------------------------------
point_estimate = float(result.params["daca_x_post"])
standard_error = float(result.bse["daca_x_post"])
sample_size    = int(len(df))

print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size":    sample_size,
}))
