"""
DACA Effect on Full-Time Employment: Difference-in-Differences
Sample: Hispanic-Mexican, Mexico-born, non-citizen adults
Treatment: DACA-eligible by age criterion (born 1982-1997, arrived before age 16)
Control: Slightly older cohort (born 1972-1981) meeting same immigration criteria
Outcome: Employed full-time (empstat==1 AND uhrswork>=35)
Period: 2009-2011 (pre) vs 2013-2016 (post), excluding 2012 (transition year)
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import json
import sys

# ---------------------------------------------------------------------------
# Column specifications for the fixed-width ACS data file
# Positions are 1-indexed (from the Stata .do file); converted to 0-indexed
# for pandas read_fwf: (start-1, end) since end is exclusive in pandas.
# ---------------------------------------------------------------------------
COLSPECS_RAW = [
    # (variable_name, stata_start, stata_end)
    ('year',     1,   4),
    ('statefip', 66,  67),
    ('perwt',    692, 701),   # person weight; has 2 implied decimals -> divide by 100
    ('age',      741, 743),
    ('birthyr',  748, 751),
    ('hispan',   764, 764),   # 1 = Mexican
    ('bpl',      768, 770),   # 200 = Mexico
    ('citizen',  790, 790),   # 3 = Not a citizen
    ('yrimmig',  795, 798),   # Year of immigration; 0=N/A, 996=not reported
    ('empstat',  875, 875),   # 1=employed, 2=unemployed, 3=NILF
    ('uhrswork', 905, 906),   # Usual hours worked/week; 0=N/A
]

# Convert to 0-indexed (start-1, end) tuples for pandas
COLSPECS = [(s - 1, e) for (_, s, e) in COLSPECS_RAW]
NAMES    = [n for (n, _, _) in COLSPECS_RAW]

# Dtypes chosen to minimize memory usage while covering all valid values
DTYPES = {
    'year':     'int16',
    'statefip': 'int16',
    'perwt':    'float64',    # raw integer with 2 implied decimals
    'age':      'int16',
    'birthyr':  'int16',
    'hispan':   'int8',
    'bpl':      'int16',
    'citizen':  'int8',
    'yrimmig':  'int16',
    'empstat':  'int8',
    'uhrswork': 'int8',
}

DATA_FILE = 'ACS_extract_expanded.dat'
CHUNK_SIZE = 500_000  # rows per chunk; tune if memory is tight

# ---------------------------------------------------------------------------
# Read the data in chunks, applying filters immediately to reduce memory use
# ---------------------------------------------------------------------------
print("Reading data in chunks...", file=sys.stderr)

chunks = []
for chunk in pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=NAMES,
    dtype=DTYPES,
    chunksize=CHUNK_SIZE,
    header=None,       # no header row in the fixed-width file
):
    # Apply early filters to keep only the relevant subsample
    mask = (
        (chunk['hispan'] == 1) &          # Mexican Hispanic origin
        (chunk['bpl']    == 200) &        # Born in Mexico
        (chunk['citizen']== 3) &          # Not a citizen (undocumented proxy)
        (chunk['year'].between(2009, 2016)) &  # Study window
        (chunk['year'] != 2012) &         # Exclude transition year
        (chunk['age'].between(15, 40)) &  # Relevant working-age range
        (chunk['yrimmig'] >= 1900) &      # Valid immigration year (not N/A or "not reported")
        (chunk['yrimmig'] <= 2007)        # In US continuously since 2007 (DACA criterion)
    )
    sub = chunk[mask].copy()
    if len(sub) > 0:
        chunks.append(sub)

df = pd.concat(chunks, ignore_index=True)
print(f"  Rows after initial filters: {len(df):,}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Construct key variables
# ---------------------------------------------------------------------------

# Person weight: 2 implied decimals in the raw file
df['perwt'] = df['perwt'] / 100.0

# Approximate birth year: use birthyr if it looks valid, else impute from age
# (birthyr = 0 or 9999 indicates missing in IPUMS)
df['birthyr_use'] = np.where(
    (df['birthyr'] > 1900) & (df['birthyr'] < 2010),
    df['birthyr'],
    df['year'] - df['age']  # fallback imputation
)

# Arrived-before-16 criterion (DACA requirement)
# age_at_arrival = yrimmig - birth_year; must be < 16
df['age_at_arrival'] = df['yrimmig'] - df['birthyr_use']
df = df[df['age_at_arrival'] < 16].copy()
print(f"  Rows after arrived-before-16 filter: {len(df):,}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Define treatment and control groups by birth cohort
# ---------------------------------------------------------------------------
# DACA eligibility requires not yet having turned 31 by June 15, 2012
#   => born after June 15, 1981  => birthyr >= 1982 (approximate)
# We use birthyr 1982-1997 as the treated cohort (age 15-30 as of June 2012)
# Control cohort: birthyr 1972-1981 (age 31-40 as of June 2012)
df['treat']        = ((df['birthyr_use'] >= 1982) & (df['birthyr_use'] <= 1997)).astype(int)
df['control_flag'] = ((df['birthyr_use'] >= 1972) & (df['birthyr_use'] <= 1981)).astype(int)

# Restrict to treatment or control cohort
df = df[(df['treat'] == 1) | (df['control_flag'] == 1)].copy()
print(f"  Rows after cohort restriction: {len(df):,}", file=sys.stderr)

# Check that there is variation in the treatment variable
treat_counts = df['treat'].value_counts()
print(f"  Treat=0: {treat_counts.get(0, 0):,}  Treat=1: {treat_counts.get(1, 0):,}", file=sys.stderr)
if treat_counts.get(0, 0) == 0 or treat_counts.get(1, 0) == 0:
    raise ValueError("No variation in treatment variable. Revise sample selection.")

# ---------------------------------------------------------------------------
# Post-DACA indicator
# DACA announced June 2012; applications accepted Aug 2012.
# Post = 2013-2016; Pre = 2009-2011 (2012 excluded).
# ---------------------------------------------------------------------------
df['post'] = (df['year'] >= 2013).astype(int)

# ---------------------------------------------------------------------------
# Outcome: full-time employment
# Employed (empstat==1) AND usually works 35+ hours/week
# ---------------------------------------------------------------------------
df['empstat_ft'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

# Summary statistics for verification
print("  Cell means (empstat_ft by treat x post):", file=sys.stderr)
print(df.groupby(['treat', 'post'])['empstat_ft'].agg(['mean', 'count']).round(4), file=sys.stderr)

# ---------------------------------------------------------------------------
# Difference-in-Differences regression (linear probability model)
# empstat_ft = alpha + beta1*treat + beta2*post + beta3*(treat x post)
#              + state FE + year FE + epsilon
#
# beta3 is the DiD estimate of DACA's effect on full-time employment.
# Weighted by person weights (perwt) for population representativeness.
# Standard errors clustered at the state level.
# ---------------------------------------------------------------------------
model = smf.wls(
    'empstat_ft ~ treat * post + C(statefip) + C(year)',
    data=df,
    weights=df['perwt']
).fit(cov_type='cluster', cov_kwds={'groups': df['statefip']})

# The interaction coefficient treat:post is the DiD treatment effect
point_estimate = float(model.params['treat:post'])
standard_error = float(model.bse['treat:post'])
sample_size    = int(len(df))

# ---------------------------------------------------------------------------
# Output ONLY the JSON result to stdout
# ---------------------------------------------------------------------------
result = {
    'point_estimate': round(point_estimate, 6),
    'standard_error': round(standard_error, 6),
    'sample_size':    sample_size
}
print(json.dumps(result))
