"""
Research Question:
    Effect of DACA eligibility on full-time employment (usual hours >= 35/week)
    among Hispanic-Mexican, Mexico-born, non-citizen immigrants in the US.

Identification Strategy: Difference-in-Differences (DiD)
    - Treatment group: Arrived in the US before age 16 AND under 31 on June 15, 2012
      → DACA-eligible by age-at-arrival and age-on-DACA-date criteria
    - Control group: Arrived at age 16-21 (same birthplace, ethnicity, citizenship)
      → Not DACA-eligible because arrived at 16 or older
    - Pre-period: 2009-2011 (pre-DACA)
    - Post-period: 2013-2016 (post-DACA implementation)
    - DiD coefficient on daca_eligible:post = causal effect of DACA eligibility

Output: single JSON to stdout with keys point_estimate, standard_error, sample_size
"""

import json
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Column specs from ACS_extract_expanded_layout_excerpt.do
# Stata uses 1-based inclusive positions; Python colspecs are (start, end)
# where start is 0-based inclusive and end is 0-based exclusive.
# Formula: Stata col N → Python start = N-1; Stata end col M → Python end = M
# ---------------------------------------------------------------------------
COLSPECS = [
    (0, 4),      # year:     Census year (2006-2016)
    (65, 67),    # statefip: State FIPS code
    (740, 743),  # age:      Age in years at survey date
    (747, 751),  # birthyr:  Year of birth
    (763, 764),  # hispan:   Hispanic origin general (1 = Mexican)
    (767, 770),  # bpl:      Birthplace general (200 = Mexico)
    (789, 790),  # citizen:  Citizenship status (3 = not a citizen)
    (794, 798),  # yrimmig:  Year of immigration (0 = N/A, born in US)
    (874, 875),  # empstat:  Employment status general (1 = employed)
    (904, 906),  # uhrswork: Usual hours worked per week (0 = N/A)
]
COLNAMES = [
    'year', 'statefip', 'age', 'birthyr',
    'hispan', 'bpl', 'citizen', 'yrimmig',
    'empstat', 'uhrswork',
]
# Use narrow integer types to minimise RAM usage during chunked reading
DTYPES = {
    'year':     'int16',
    'statefip': 'int8',
    'age':      'int16',
    'birthyr':  'int16',
    'hispan':   'int8',
    'bpl':      'int16',
    'citizen':  'int8',
    'yrimmig':  'int16',
    'empstat':  'int8',
    'uhrswork': 'int8',
}

# Survey years: 2009-2011 are pre-DACA; 2013-2016 are post-DACA (skip 2012)
STUDY_YEARS = [2009, 2010, 2011, 2013, 2014, 2015, 2016]

# Path to the large fixed-width data file (same directory as this script)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'ACS_extract_expanded.dat')

# ---------------------------------------------------------------------------
# Read the fixed-width file in chunks to stay within memory limits
# ---------------------------------------------------------------------------
print("Reading data in chunks...", file=sys.stderr)
chunks = []
for chunk in pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=COLNAMES,
    dtype=DTYPES,
    chunksize=200_000,   # rows per chunk; tune down if RAM is tight
    header=None,
):
    # --- Apply filters early so un-needed rows are discarded immediately ---

    # Keep only pre- and post-DACA study years
    chunk = chunk[chunk['year'].isin(STUDY_YEARS)]
    if chunk.empty:
        continue

    # Hispanic of Mexican origin (hispan == 1)
    chunk = chunk[chunk['hispan'] == 1]
    if chunk.empty:
        continue

    # Born in Mexico (bpl == 200)
    chunk = chunk[chunk['bpl'] == 200]
    if chunk.empty:
        continue

    # Not a US citizen (citizen == 3); proxy for undocumented status
    chunk = chunk[chunk['citizen'] == 3]
    if chunk.empty:
        continue

    # Valid immigration year: arrived 1970-2007
    # yrimmig == 0 means born in the US (N/A); yrimmig > 2007 fails 5-yr
    # continuous-presence requirement (arrived by June 15, 2007)
    chunk = chunk[(chunk['yrimmig'] >= 1970) & (chunk['yrimmig'] <= 2007)]
    if chunk.empty:
        continue

    # Working-age restriction at survey time (18-35 years old)
    chunk = chunk[(chunk['age'] >= 18) & (chunk['age'] <= 35)]
    if chunk.empty:
        continue

    chunks.append(chunk)

# Combine all passing rows into one DataFrame
df = pd.concat(chunks, ignore_index=True)
print(f"Rows after initial filters: {len(df):,}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Derived variables
# ---------------------------------------------------------------------------

# Age at arrival = year immigrated minus birth year (calendar-year approximation)
df['age_at_arrival'] = (df['yrimmig'] - df['birthyr']).astype('int16')

# Restrict to plausible arrival ages: 0-21
# Treatment group (DACA-eligible by arrival criterion): arrived before age 16
# Control group (DACA-ineligible by arrival criterion): arrived at age 16-21
df = df[(df['age_at_arrival'] >= 0) & (df['age_at_arrival'] <= 21)]

# DACA age-on-date criterion: must be under 31 as of June 15, 2012
# Arrived before 16 AND born on/after June 16, 1981 → birthyr >= 1982 (conservative)
df = df[df['birthyr'] >= 1982]

# Treatment indicator: 1 if arrived before age 16 (DACA-eligible by arrival age)
df['daca_eligible'] = (df['age_at_arrival'] <= 15).astype('int8')

# Verify treatment has variation before proceeding
treat_counts = df['daca_eligible'].value_counts()
print(f"Treatment variation:\n{treat_counts}", file=sys.stderr)
if treat_counts.shape[0] < 2:
    raise ValueError("No variation in daca_eligible — revise specification.")

# Outcome: full-time employment = currently employed AND usual hours >= 35
# empstat == 1 means employed; uhrswork == 0 means N/A (not employed)
df['full_time'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype('int8')

# Post-DACA indicator: 1 for years 2013-2016, 0 for 2009-2011
df['post'] = (df['year'] >= 2013).astype('int8')

# Drop any rows with nulls in variables entering the regression
reg_vars = ['full_time', 'daca_eligible', 'post', 'age', 'statefip', 'year']
df = df.dropna(subset=reg_vars)

print(f"Final sample size: {len(df):,}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Difference-in-Differences regression (linear probability model)
#
# Model: full_time ~ daca_eligible * post + C(statefip) + C(year) + age
#   - C(statefip): state fixed effects absorb permanent cross-state differences
#   - C(year):     year fixed effects absorb common year-specific shocks
#   - age:         linear age control for age differences within groups
#   - daca_eligible * post: DiD interaction; its coefficient is the ATT of
#     DACA eligibility on the probability of full-time employment
# HC1 heteroskedasticity-robust standard errors
# ---------------------------------------------------------------------------
model = smf.ols(
    "full_time ~ daca_eligible * post + C(statefip) + C(year) + age",
    data=df,
).fit(cov_type='HC1')

# DiD coefficient of interest
coef_name = 'daca_eligible:post'
point_estimate = float(model.params[coef_name])
std_error      = float(model.bse[coef_name])
sample_size    = int(model.nobs)

# Print ONLY the JSON result to stdout (no extra text)
print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(std_error, 6),
    "sample_size":    sample_size,
}))
