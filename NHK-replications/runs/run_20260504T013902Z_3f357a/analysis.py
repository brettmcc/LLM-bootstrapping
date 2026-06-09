"""
Estimates the effect of DACA eligibility on full-time employment (35+ hrs/week)
for Hispanic-Mexican, Mexico-born, non-citizen individuals in ACS 2009-2016.

Strategy: Difference-in-Differences (DiD) using the DACA age cutoff (born before
vs. after June 15, 1981) as the treatment variation, with pre-period (2009-2011)
and post-period (2013-2016) comparison. Excludes 2012 (transition year).

Treatment group: birth_year >= 1982 (not yet 31 as of June 15, 2012 — DACA-eligible)
Control group:   birth_year in [1977, 1981] (just over the age cutoff — ineligible)

Outputs a single JSON object with point_estimate, standard_error, sample_size.
"""

import json
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Column specs for the fixed-width ACS data file.
# Stata positions are 1-indexed; Python colspecs are 0-indexed half-open [start, stop).
# Source: ACS_extract_expanded_layout_excerpt.do
# ---------------------------------------------------------------------------
COLSPECS = [
    (0,   4),    # year      — survey year
    (65,  67),   # statefip  — state FIPS code
    (691, 701),  # perwt     — person weight (double, 10 chars; 2 implied decimals)
    (740, 743),  # age       — age in years
    (763, 764),  # hispan    — Hispanic origin: 1=Mexican
    (770, 775),  # bpld      — detailed birthplace: 20000=Mexico
    (789, 790),  # citizen   — citizenship: 3=not a citizen, 4=not citizen/first papers
    (794, 798),  # yrimmig   — year of immigration
    (904, 906),  # uhrswork  — usual hours worked per week (0=N/A)
]

COLNAMES = ["year", "statefip", "perwt", "age", "hispan", "bpld",
            "citizen", "yrimmig", "uhrswork"]

# Survey years to use: pre-period 2009-2011, post-period 2013-2016 (exclude 2012)
KEEP_YEARS = {2009, 2010, 2011, 2013, 2014, 2015, 2016}

# Birth-year bandwidth around the 1981/1982 DACA age cutoff
BY_LOW  = 1977   # control group lower bound (just over the age cutoff)
BY_HIGH = 1986   # treatment group upper bound

# ---------------------------------------------------------------------------
# Read the fixed-width data file in chunks for memory efficiency.
# Early-filter each chunk before concatenation.
# ---------------------------------------------------------------------------
CHUNK_SIZE = 500_000

chunks = []

reader = pd.read_fwf(
    "ACS_extract_expanded.dat",
    colspecs=COLSPECS,
    names=COLNAMES,
    dtype=str,          # read as strings first; parse below to handle whitespace
    chunksize=CHUNK_SIZE,
)

for chunk in reader:
    # Convert all columns to numeric, coercing errors to NaN
    for col in COLNAMES:
        chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

    # --- Early filters to reduce memory before concatenation ---

    # Keep only survey years of interest
    chunk = chunk[chunk["year"].isin(KEEP_YEARS)]
    if chunk.empty:
        continue

    # Keep only Hispanic-Mexican (hispan==1) born in Mexico (bpld==20000)
    chunk = chunk[(chunk["hispan"] == 1) & (chunk["bpld"] == 20000)]
    if chunk.empty:
        continue

    # Keep only non-citizens (citizen 3=not a citizen, 4=first papers only)
    chunk = chunk[chunk["citizen"].isin([3, 4])]
    if chunk.empty:
        continue

    # Require a valid year of immigration
    chunk = chunk[(chunk["yrimmig"] > 0) & (chunk["yrimmig"].notna())]
    if chunk.empty:
        continue

    # Approximate birth year and apply bandwidth filter early
    chunk["birth_year"] = chunk["year"] - chunk["age"]
    chunk = chunk[chunk["birth_year"].between(BY_LOW, BY_HIGH)]
    if chunk.empty:
        continue

    chunks.append(chunk)

if not chunks:
    sys.exit("ERROR: No observations passed initial filters.")

df = pd.concat(chunks, ignore_index=True)

# ---------------------------------------------------------------------------
# Derive analysis variables
# ---------------------------------------------------------------------------

# birth_year already computed above; recompute cleanly on the merged frame
df["birth_year"] = df["year"] - df["age"]

# Continuous US residence since at least 2007 (DACA requirement)
# Arrived before 16th birthday (DACA requirement: arrived before June 15, 1996,
# i.e., before 16th birthday AND before June 2012 minus 15 years)
# Approximation: yrimmig <= birth_year + 15  AND  yrimmig <= 2007
df = df[
    (df["yrimmig"] <= df["birth_year"] + 15) &  # arrived before 16th birthday
    (df["yrimmig"] <= 2007)                      # resident since 2007 (DACA req.)
]

# Apply birth-year bandwidth (already applied in chunk loop, but enforce cleanly)
df = df[df["birth_year"].between(BY_LOW, BY_HIGH)]

# Reasonable working-age filter
df = df[df["age"].between(18, 40)]

# Drop any rows with missing key variables
df = df.dropna(subset=["year", "statefip", "perwt", "age",
                        "birth_year", "yrimmig", "uhrswork", "citizen"])

# ---------------------------------------------------------------------------
# Outcome: full-time employment (uhrswork >= 35)
# uhrswork == 0 means N/A (not employed), which maps to full_time = 0.
# ---------------------------------------------------------------------------
df["full_time"] = (df["uhrswork"] >= 35).astype(int)

# ---------------------------------------------------------------------------
# Treatment and post indicators
# ---------------------------------------------------------------------------

# DACA-eligible if birth_year >= 1982 (not yet 31 as of June 15, 2012)
df["daca_eligible"] = (df["birth_year"] >= 1982).astype(int)

# Post-DACA period (DACA implemented June 2012; post = survey years 2013-2016)
df["post"] = (df["year"] >= 2013).astype(int)

# Quadratic age control (captures lifecycle employment pattern)
df["age_sq"] = df["age"] ** 2

# Verify treatment variation exists
n_treated     = df["daca_eligible"].sum()
n_control     = (df["daca_eligible"] == 0).sum()
n_post        = df["post"].sum()
n_pre         = (df["post"] == 0).sum()
n_treated_post = ((df["daca_eligible"] == 1) & (df["post"] == 1)).sum()

if n_treated == 0 or n_control == 0 or n_post == 0 or n_pre == 0:
    sys.exit(
        f"ERROR: Insufficient variation. treated={n_treated}, control={n_control}, "
        f"post={n_post}, pre={n_pre}"
    )

# ---------------------------------------------------------------------------
# Difference-in-Differences regression
# Model: full_time ~ daca_eligible * post + year FE + state FE + age + age²
# Weighted by survey person weight; HC1 heteroskedasticity-robust SEs.
# The coefficient on daca_eligible:post is the DiD estimate.
# ---------------------------------------------------------------------------
result = smf.wls(
    "full_time ~ daca_eligible * post + C(year) + C(statefip) + age + age_sq",
    data=df,
    weights=df["perwt"],
).fit(cov_type="HC1")

# Extract DiD estimate (interaction term)
did_coef = float(result.params["daca_eligible:post"])
did_se   = float(result.bse["daca_eligible:post"])
n_obs    = int(result.nobs)

# ---------------------------------------------------------------------------
# Output: single JSON object to STDOUT (no extra text)
# ---------------------------------------------------------------------------
output = {
    "point_estimate": round(did_coef, 6),
    "standard_error": round(did_se,   6),
    "sample_size":    n_obs,
}

print(json.dumps(output))
