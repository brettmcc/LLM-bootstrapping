"""
Effect of DACA eligibility on full-time employment among
Mexican-born Hispanic non-citizens in the United States.

Identification: Difference-in-Differences (DiD) using the DACA age
eligibility cutoff as the source of exogenous variation.

  Treatment:  born 1982-1986 → not yet 31 on June 15, 2012 (DACA-eligible)
  Control:    born 1977-1981 → already 31-35 on June 15, 2012 (age-ineligible)
  Both groups: arrived in US before age 16, non-citizen, Mexican-born Hispanic.

  Pre period:  2009-2011  (post = 0)
  Post period: 2013-2016  (post = 1)
  2012 excluded (transition year; DACA announced June, accepting apps August).

Outcome: full_time = 1 if uhrswork >= 35, else 0.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import json
import sys

# ---------------------------------------------------------------------------
# Column specifications
# Stata infix: 1-indexed inclusive.  Python colspecs: (start-1, end) exclusive.
# ---------------------------------------------------------------------------
COLSPECS = [
    (0, 4),      # year        Stata: 1-4
    (65, 67),    # statefip    Stata: 66-67
    (739, 740),  # sex         Stata: 740-740
    (740, 743),  # age         Stata: 741-743
    (747, 751),  # birthyr     Stata: 748-751
    (763, 764),  # hispan      Stata: 764-764
    (767, 770),  # bpl         Stata: 768-770
    (789, 790),  # citizen     Stata: 790-790
    (794, 798),  # yrimmig     Stata: 795-798
    (904, 906),  # uhrswork    Stata: 905-906
]

COL_NAMES = [
    'year', 'statefip', 'sex', 'age', 'birthyr',
    'hispan', 'bpl', 'citizen', 'yrimmig', 'uhrswork'
]

# Pre-DACA years (2009-2011) and post-DACA years (2013-2016)
YEARS = [2009, 2010, 2011, 2013, 2014, 2015, 2016]

DATA_FILE = 'ACS_extract_expanded.dat'
CHUNK_SIZE = 500_000

# ---------------------------------------------------------------------------
# Read data in chunks; apply early filters to keep memory well under 30 GB
# ---------------------------------------------------------------------------
chunks = []

print("Loading data in chunks...", file=sys.stderr)

for i, chunk in enumerate(pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=COL_NAMES,
    dtype=str,       # read as string first for safe conversion
    chunksize=CHUNK_SIZE,
    header=None,
)):
    # Convert every column to numeric; invalid/missing become NaN
    for col in COL_NAMES:
        chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

    # Keep only Mexican-born Hispanic non-citizens in the relevant years
    mask = (
        (chunk['hispan'] == 1) &        # Mexican Hispanic origin
        (chunk['bpl'] == 200) &         # Born in Mexico
        (chunk['citizen'] == 3) &       # Not a US citizen (undocumented proxy)
        (chunk['yrimmig'] > 0) &        # Has a valid year of immigration
        (chunk['birthyr'] >= 1960) &    # Plausible birth year lower bound
        (chunk['birthyr'] <= 2000) &    # Plausible birth year upper bound
        (chunk['age'] >= 18) &          # Working-age adults
        (chunk['age'] <= 45) &
        (chunk['year'].isin(YEARS))     # Pre- or post-DACA years only
    )
    filtered = chunk[mask].copy()
    if len(filtered) > 0:
        chunks.append(filtered)

    if i % 20 == 0:
        total = sum(len(c) for c in chunks)
        print(f"  chunk {i:4d}, accumulated rows: {total:,}", file=sys.stderr)

df = pd.concat(chunks, ignore_index=True)
print(f"Base sample after initial filters: {len(df):,} rows", file=sys.stderr)

# ---------------------------------------------------------------------------
# Construct variables
# ---------------------------------------------------------------------------

# Approximate age at arrival (year of immigration minus birth year).
# Standard approximation used in the DACA literature; exact birth/arrival
# dates are not available in the ACS.
df['arrival_age'] = df['yrimmig'] - df['birthyr']

# Restrict to individuals who arrived before their 16th birthday —
# one of the core DACA criteria — applied to BOTH groups for comparability.
df = df[(df['arrival_age'] >= 0) & (df['arrival_age'] < 16)]
print(f"After arrival-age < 16 filter: {len(df):,} rows", file=sys.stderr)

# ---------------------------------------------------------------------------
# Define treatment and control cohorts — narrow bandwidth around the cutoff
# ---------------------------------------------------------------------------
# Treatment: born 1982-1986 → not yet 31 on June 15, 2012 (DACA-eligible).
# Control:   born 1977-1981 → already 31-35 on June 15, 2012 (age-ineligible).
#
# Using a ±5-year window around the 1981/1982 cutoff keeps the two groups
# close in age (treated: 23-34 in 2009-2016; control: 28-39), avoiding the
# composition bias that arises from very young cohorts (born 1990-1995) who
# only enter the sample in the post-period once they turn 18, which would
# drag down the treated/post mean and bias the DiD estimate.
df = df[
    ((df['birthyr'] >= 1982) & (df['birthyr'] <= 1986)) |
    ((df['birthyr'] >= 1977) & (df['birthyr'] <= 1981))
]
print(f"After birth-year cohort filter: {len(df):,} rows", file=sys.stderr)

# Indicator = 1 for DACA-eligible birth cohort
df['treated'] = (df['birthyr'] >= 1982).astype(int)

# Indicator = 1 for post-DACA period (2013-2016)
df['post'] = (df['year'] >= 2013).astype(int)

# Outcome: full-time employment, defined as usually working >= 35 hrs/week.
# uhrswork == 0 means N/A (not employed), so the indicator is 0 for non-workers.
df['full_time'] = (df['uhrswork'] >= 35).astype(int)

# Drop any remaining rows with missing values in regression variables
df = df.dropna(subset=['full_time', 'treated', 'post', 'age', 'sex', 'year', 'statefip'])

# ---------------------------------------------------------------------------
# Verify variation exists in the treatment variable (required by spec)
# ---------------------------------------------------------------------------
treat_counts = df['treated'].value_counts().to_dict()
print(f"\nTreated distribution: {treat_counts}", file=sys.stderr)
if len(treat_counts) < 2:
    print("ERROR: no variation in treatment variable. Halting.", file=sys.stderr)
    sys.exit(1)

# Descriptive 2x2 table
for grp, lbl in [(1, "treated"), (0, "control")]:
    for prd, plbl in [(0, "pre"), (1, "post")]:
        rate = df.loc[(df['treated'] == grp) & (df['post'] == prd), 'full_time'].mean()
        n    = df.loc[(df['treated'] == grp) & (df['post'] == prd)].shape[0]
        print(f"  full_time mean ({lbl}/{plbl}): {rate:.4f}  n={n:,}", file=sys.stderr)

# ---------------------------------------------------------------------------
# DiD OLS regression with year and state fixed effects
# ---------------------------------------------------------------------------
# Model:
#   full_time = α + β·treated + γ·post + δ·(treated×post)
#             + C(year) + C(statefip) + age + age² + C(sex) + ε
#
# δ is the DiD estimate of DACA eligibility on full-time employment probability.
model_formula = (
    'full_time ~ treated * post + C(year) + C(statefip) + '
    'age + I(age**2) + C(sex)'
)

print(f"\nFitting model...", file=sys.stderr)

result = smf.ols(model_formula, data=df).fit(
    cov_type='cluster',
    cov_kwds={'groups': df['statefip'].astype(int)}
)

# ---------------------------------------------------------------------------
# Extract results and write to stdout (JSON only)
# ---------------------------------------------------------------------------
point_estimate = float(result.params['treated:post'])
standard_error = float(result.bse['treated:post'])
sample_size    = int(result.nobs)

print(f"  treated:post coeff = {point_estimate:.6f}", file=sys.stderr)
print(f"  clustered SE       = {standard_error:.6f}", file=sys.stderr)
print(f"  N                  = {sample_size:,}",      file=sys.stderr)

output = {
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size":    sample_size,
}

print(json.dumps(output))
