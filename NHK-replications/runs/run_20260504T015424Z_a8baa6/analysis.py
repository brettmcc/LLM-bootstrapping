"""
analysis.py
===========
Research Question:
    Among Hispanic-Mexican, Mexico-born people in the US, what was the causal
    impact of DACA eligibility on the probability of full-time employment
    (usually working >= 35 hours/week) in 2013-2016?

Identification Strategy: Difference-in-Differences (DiD)
    - Treatment group: DACA-eligible
        * Born in or after 1982 (< 31 years old on June 15, 2012)
        * Arrived in the US before their 16th birthday (yrimmig <= birthyr + 15)
        * Arrived by 2007 (proxy for continuous US presence since June 15, 2007)
        * Not a citizen (proxy for unlawful status)
    - Control group: Age-ineligible immigrants
        * Born 1972-1981 (31-40 years old in 2012, just over the age cutoff)
        * Same arrival restrictions (before age 16, by 2007)
        * Same citizenship and ethnicity/birthplace filters
    - Pre-period:  2009-2011 (before DACA)
    - Post-period: 2013-2016 (after DACA; 2012 excluded as transition year)
    - Outcome: full_time = (empstat == 1) & (uhrswork >= 35)
    - Model: weighted OLS (linear probability model) with year + state FEs,
             standard errors clustered at the state level

STDOUT: prints ONLY a single JSON object with keys
        "point_estimate", "standard_error", "sample_size"
"""

import os
import json
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ============================================================
# Column positions for the fixed-width ACS data file.
# The .do layout file uses 1-indexed inclusive Stata notation.
# For Python's read_fwf: colspec = (stata_start - 1, stata_end)
#   where start is inclusive (0-indexed) and end is exclusive.
# ============================================================
COL_SPECS = [
    (0,   4),    # year       Stata cols 1-4
    (65,  67),   # statefip   Stata cols 66-67
    (691, 701),  # perwt      Stata cols 692-701 (raw value / 100 = actual weight)
    (739, 740),  # sex        Stata col  740
    (740, 743),  # age        Stata cols 741-743
    (747, 751),  # birthyr    Stata cols 748-751
    (763, 764),  # hispan     Stata col  764  (1 = Mexican)
    (767, 770),  # bpl        Stata cols 768-770 (200 = Mexico)
    (789, 790),  # citizen    Stata col  790  (3 = Not a citizen)
    (794, 798),  # yrimmig    Stata cols 795-798 (0000 = N/A)
    (874, 875),  # empstat    Stata col  875  (1 = Employed)
    (904, 906),  # uhrswork   Stata cols 905-906 (usual hrs/week; 0 = N/A)
]

COL_NAMES = [
    'year', 'statefip', 'perwt',
    'sex', 'age', 'birthyr',
    'hispan', 'bpl', 'citizen', 'yrimmig',
    'empstat', 'uhrswork',
]

# Years included in the analysis (excludes 2012, the DACA transition year)
STUDY_YEARS = {2009, 2010, 2011, 2013, 2014, 2015, 2016}

# ============================================================
# Read the fixed-width file in chunks to manage memory.
# The file is large; we filter aggressively on each chunk.
# ============================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file  = os.path.join(script_dir, 'ACS_extract_expanded.dat')

CHUNK_SIZE = 300_000  # rows per chunk; tune if memory is tight

collected = []  # list of filtered DataFrames, one per chunk

reader = pd.read_fwf(
    data_file,
    colspecs=COL_SPECS,
    names=COL_NAMES,
    dtype=str,          # read everything as string first to avoid parse errors
    header=None,        # no header row in the .dat file
    chunksize=CHUNK_SIZE,
)

for chunk in reader:
    # Convert all columns to numeric; non-numeric values become NaN
    chunk = chunk.apply(pd.to_numeric, errors='coerce')

    # --- Filter 1: restrict to study years (drop 2012 and out-of-range years) ---
    chunk = chunk[chunk['year'].isin(STUDY_YEARS)]
    if chunk.empty:
        continue

    # --- Filter 2: Hispanic of Mexican origin (hispan == 1) ---
    chunk = chunk[chunk['hispan'] == 1]
    if chunk.empty:
        continue

    # --- Filter 3: born in Mexico (bpl == 200) ---
    chunk = chunk[chunk['bpl'] == 200]
    if chunk.empty:
        continue

    # --- Filter 4: non-citizen (proxy for undocumented; citizen == 3) ---
    chunk = chunk[chunk['citizen'] == 3]
    if chunk.empty:
        continue

    # --- Filter 5: valid immigration year and arrived by 2007 ---
    # yrimmig == 0 means N/A (typically native-born or not applicable)
    chunk = chunk[(chunk['yrimmig'] > 0) & (chunk['yrimmig'] <= 2007)]
    if chunk.empty:
        continue

    # --- Filter 6: birth cohorts that define treatment + control groups ---
    # Treatment: birthyr 1982-1996 (under 31 in 2012)
    # Control:   birthyr 1972-1981 (31-40 in 2012)
    chunk = chunk[(chunk['birthyr'] >= 1972) & (chunk['birthyr'] <= 1996)]
    if chunk.empty:
        continue

    # --- Filter 7: working-age adults in the survey year ---
    chunk = chunk[(chunk['age'] >= 18) & (chunk['age'] <= 45)]
    if chunk.empty:
        continue

    collected.append(chunk)

# Concatenate all filtered chunks into a single DataFrame
df = pd.concat(collected, ignore_index=True)

# ============================================================
# Variable construction
# ============================================================

# PERWT: the raw file stores weights with 2 implied decimal places
# (e.g., raw value 010461 represents 104.61)
df['perwt'] = df['perwt'] / 100.0

# Indicator: person arrived in the US BEFORE their 16th birthday.
# If born in year B and arrived in year Y, they arrived at age ~(Y - B).
# "Before 16th birthday" means Y <= B + 15  (i.e., arrived at age 0-15).
df['arrived_as_child'] = (df['yrimmig'] <= df['birthyr'] + 15).astype(int)

# Treatment: DACA-eligible cohort
#   - Born in 1982 or later  -> had not yet turned 31 as of June 15, 2012
#   - Arrived before age 16  -> brought to the US as a child (a key DACA criterion)
#   - Arrived by 2007        -> already filtered above (proxy for 5-yr continuous presence)
#   - Non-citizen            -> already filtered above (proxy for unlawful status)
df['daca_eligible'] = (
    (df['birthyr'] >= 1982) &
    (df['arrived_as_child'] == 1)
).astype(int)

# Control: age-ineligible immigrants (just above the DACA age cutoff)
#   - Born 1972-1981 (31-40 years old in 2012; missed the under-31 cutoff)
#   - Same arrival restrictions as the treatment group for comparability
df['control_group'] = (
    (df['birthyr'] >= 1972) &
    (df['birthyr'] <= 1981) &
    (df['arrived_as_child'] == 1)
).astype(int)

# Keep only observations in the treatment or control group
df = df[(df['daca_eligible'] == 1) | (df['control_group'] == 1)].copy()

# Post-DACA indicator (2013 onward; pre = 2009-2011)
df['post'] = (df['year'] >= 2013).astype(int)

# Outcome: full-time employment
#   empstat == 1   -> currently employed
#   uhrswork >= 35 -> usually works 35+ hours per week (full-time threshold)
# If a person is not employed or hours are N/A (uhrswork == 0), full_time = 0.
df['full_time'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

# Drop any rows with NaN in regression variables
reg_vars = ['full_time', 'daca_eligible', 'post', 'age', 'sex', 'year', 'statefip', 'perwt']
df = df.dropna(subset=reg_vars)

# Ensure categorical variables are integers for the formula interface
for v in ['sex', 'year', 'statefip']:
    df[v] = df[v].astype(int)

# ============================================================
# Verify treatment variation (required by the task specification)
# ============================================================
assert df['daca_eligible'].nunique() == 2, \
    "ERROR: No variation in treatment variable (daca_eligible). Revise specification."
assert df['post'].nunique() == 2, \
    "ERROR: No variation in post indicator. Check year filters."

# ============================================================
# Difference-in-Differences regression
#
# Outcome:   full_time  (binary indicator, estimated via linear probability model)
# Treatment: daca_eligible  (1 = DACA-eligible cohort)
# DiD term:  daca_eligible:post  (treatment x post interaction = the causal estimate)
# Controls:
#   - C(year)     : year fixed effects (absorb common time trends; also absorbs "post")
#   - C(statefip) : state fixed effects (absorb time-invariant state heterogeneity)
#   - age, age^2  : flexible age polynomial (birth-year cohorts have different ages)
#   - C(sex)      : gender indicator
# Weights: perwt  (ACS person weights)
# SEs:     clustered at the state level (accounts for within-state correlation)
# ============================================================
model = smf.wls(
    'full_time ~ daca_eligible + daca_eligible:post '
    '+ age + I(age**2) + C(sex) + C(year) + C(statefip)',
    data=df,
    weights=df['perwt'],
).fit(
    cov_type='cluster',
    cov_kwds={'groups': df['statefip']},
)

# Extract the DiD estimate (coefficient on the daca_eligible x post interaction)
did_estimate = float(model.params['daca_eligible:post'])
did_se       = float(model.bse['daca_eligible:post'])
sample_n     = int(model.nobs)

# ============================================================
# Write spec.json to the same directory as this script
# ============================================================
spec = {
    "sample_selection": [
        "hispan == 1 (Mexican Hispanic origin)",
        "bpl == 200 (Born in Mexico)",
        "citizen == 3 (Not a citizen; proxy for undocumented status)",
        "yrimmig > 0 and yrimmig <= 2007 (immigrated by 2007; proxy for 5-yr continuous US presence)",
        "arrived_as_child: yrimmig <= birthyr + 15 (arrived before 16th birthday)",
        "birthyr in 1972-1996 (defines treatment and control birth cohorts)",
        "age >= 18 and age <= 45 in survey year (working-age adults)",
        "year in {2009, 2010, 2011, 2013, 2014, 2015, 2016} (excludes 2012 transition year)",
        "treatment group: birthyr >= 1982 and arrived_as_child == 1",
        "control group:   birthyr in 1972-1981 and arrived_as_child == 1",
    ],
    "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
    "treatment_definition": "(birthyr >= 1982) & (yrimmig <= birthyr + 15)",
    "model_specification_line": (
        "smf.wls('full_time ~ daca_eligible + daca_eligible:post "
        "+ age + I(age**2) + C(sex) + C(year) + C(statefip)', "
        "data=df, weights=df['perwt']).fit("
        "cov_type='cluster', cov_kwds={'groups': df['statefip']})"
    ),
}

spec_path = os.path.join(script_dir, 'spec.json')
with open(spec_path, 'w') as f:
    json.dump(spec, f, indent=2)

# ============================================================
# Print ONLY the results JSON to STDOUT (no other text)
# ============================================================
output = {
    "point_estimate": round(did_estimate, 6),
    "standard_error": round(did_se, 6),
    "sample_size":    sample_n,
}
print(json.dumps(output))
