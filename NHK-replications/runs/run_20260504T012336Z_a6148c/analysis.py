"""
Estimates the effect of DACA eligibility on full-time employment probability
among Hispanic-Mexican, Mexico-born, non-citizen individuals in the ACS.

Identification strategy: Difference-in-Differences (DiD)
  - Treatment: Born after June 15, 1981 (birthyr >= 1982) -- DACA-eligible by age cutoff
  - Control: Born 1975-1981 -- just aged out of DACA eligibility
  - Pre-DACA period: 2009-2011 (before DACA announcement June 2012)
  - Post-DACA period: 2013-2016 (after DACA implementation)
  - 2012 excluded as a transition year

Sample selection:
  - Hispanic-Mexican (hispan == 1) and born in Mexico (bpl == 200)
  - Non-citizen (citizen == 3) as a proxy for undocumented status
  - Arrived before their 16th birthday (yrimmig - birthyr <= 15)
  - Arrived by 2007 (yrimmig <= 2007, proxying continuous US residence since June 2007)
  - Birth year in 1975-1994 (spans control + treatment cohorts at working age)

Outcome: full-time employment = (empstat == 1) AND (uhrswork >= 35)

Model: WLS OLS with year and state fixed effects; cluster-robust SEs at state level.
Key coefficient: interaction daca_eligible:post (the DiD estimate).
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import json
import sys

# ---------------------------------------------------------------------------
# Column specifications: (0-indexed start, exclusive end) for pd.read_fwf
# Derived from the Stata infix layout (1-indexed) by subtracting 1 from start.
# ---------------------------------------------------------------------------
colspecs = [
    (0, 4),      # year       -- ACS survey year (1-4)
    (65, 67),    # statefip   -- State FIPS code (66-67)
    (747, 751),  # birthyr    -- Year of birth (748-751)
    (763, 764),  # hispan     -- Hispanic origin general version (764-764)
    (767, 770),  # bpl        -- Birthplace general version (768-770)
    (789, 790),  # citizen    -- Citizenship status (790-790)
    (794, 798),  # yrimmig    -- Year of immigration (795-798)
    (874, 875),  # empstat    -- Employment status general version (875-875)
    (904, 906),  # uhrswork   -- Usual hours worked per week (905-906)
    (691, 701),  # perwt      -- Person weight, raw integer (divide by 100 for actual)
]

colnames = [
    'year', 'statefip', 'birthyr', 'hispan', 'bpl',
    'citizen', 'yrimmig', 'empstat', 'uhrswork', 'perwt',
]

# Use compact dtypes to save memory; perwt stored as float to handle large values
dtypes = {
    'year':     'int16',
    'statefip': 'int8',
    'birthyr':  'int16',
    'hispan':   'int8',
    'bpl':      'int16',
    'citizen':  'int8',
    'yrimmig':  'int16',
    'empstat':  'int8',
    'uhrswork': 'int8',
    'perwt':    'float32',
}

# ---------------------------------------------------------------------------
# Read the fixed-width file in chunks to stay within memory limits
# ---------------------------------------------------------------------------
CHUNK_SIZE = 500_000
chunks = []

reader = pd.read_fwf(
    'ACS_extract_expanded.dat',
    colspecs=colspecs,
    names=colnames,
    dtype=dtypes,
    chunksize=CHUNK_SIZE,
    header=None,
)

for chunk in reader:
    # Apply early filters to minimize memory use before concatenation.
    # Keep only: Hispanic-Mexican, born in Mexico, non-citizen,
    # study years (2009-2016 excl. 2012), birth years in scope.
    mask = (
        (chunk['hispan'] == 1) &          # Hispanic-Mexican
        (chunk['bpl'] == 200) &            # Born in Mexico
        (chunk['citizen'] == 3) &          # Not a citizen (undocumented proxy)
        (chunk['year'] >= 2009) &
        (chunk['year'] <= 2016) &
        (chunk['year'] != 2012) &          # Exclude DACA transition year
        (chunk['yrimmig'] >= 1900) &       # Exclude N/A (0000) and "not reported" (0996)
        (chunk['yrimmig'] <= 2016) &       # Exclude future/invalid years
        (chunk['birthyr'] >= 1975) &       # Start of control group
        (chunk['birthyr'] <= 1994)         # End of treatment group
    )
    filtered = chunk[mask]
    if len(filtered) > 0:
        chunks.append(filtered)

df = pd.concat(chunks, ignore_index=True)

# ---------------------------------------------------------------------------
# Additional sample restrictions
# ---------------------------------------------------------------------------

# DACA criterion 1: arrived before 16th birthday
# (using year-level approximation; yrimmig - birthyr <= 15 means at most 15 when arrived)
df = df[df['yrimmig'] - df['birthyr'] <= 15]

# DACA criterion 2: arrived by June 2007 (continuous US residence since June 15, 2007)
df = df[df['yrimmig'] <= 2007]

# Drop any remaining rows with non-positive weights
df = df[df['perwt'] > 0]

# perwt in the raw file has 2 implied decimal places (Stata: replace perwt = perwt/100)
df['weight'] = df['perwt'] / 100.0

# ---------------------------------------------------------------------------
# Construct treatment, post, and outcome indicators
# ---------------------------------------------------------------------------

# DACA eligibility: born after June 15, 1981 -> use birthyr >= 1982 as threshold
# (those born in 1982 were at most 29.5 on June 15, 2012 -- clearly under 31)
df['daca_eligible'] = (df['birthyr'] >= 1982).astype(np.int8)

# Post-DACA indicator: 2013 onwards
df['post'] = (df['year'] >= 2013).astype(np.int8)

# Outcome: employed full-time (usual hours >= 35 while employed at work/with job)
df['fulltime'] = (
    (df['empstat'] == 1) & (df['uhrswork'] >= 35)
).astype(np.int8)

# ---------------------------------------------------------------------------
# Verify treatment variation (per prompt step 3)
# ---------------------------------------------------------------------------
n_treated = df['daca_eligible'].sum()
n_control = (df['daca_eligible'] == 0).sum()
assert n_treated > 0, "ERROR: No DACA-eligible (treated) observations found."
assert n_control > 0, "ERROR: No control-group observations found."

# ---------------------------------------------------------------------------
# DiD regression with year and state fixed effects
# Weighted least squares uses person weights; state-clustered robust SEs.
# ---------------------------------------------------------------------------
model = smf.wls(
    'fulltime ~ daca_eligible * post + C(year) + C(statefip)',
    data=df,
    weights=df['weight'],
)
result = model.fit(
    cov_type='cluster',
    cov_kwds={'groups': df['statefip']},
)

# The DiD estimate: coefficient on the interaction term daca_eligible:post
coef = float(result.params['daca_eligible:post'])
se   = float(result.bse['daca_eligible:post'])
n    = int(result.nobs)

# ---------------------------------------------------------------------------
# Output: single JSON object to STDOUT (no extra text)
# ---------------------------------------------------------------------------
output = {
    "point_estimate": round(coef, 6),
    "standard_error": round(se, 6),
    "sample_size": n,
}
print(json.dumps(output))
