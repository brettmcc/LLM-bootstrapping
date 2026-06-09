"""
DACA effect on full-time employment – Difference-in-Differences

Research design
---------------
Outcome   : full-time employment (empstat==1 AND uhrswork>=35)
Treatment : DACA-eligible birth cohort (born >=1982, i.e. <31 on 15 Jun 2012)
Control   : Just-ineligible birth cohort (born 1972-1981, too old for DACA)
Pre-period: 2009-2011 (before DACA announcement)
Post-period: 2013-2016 (after DACA implementation; 2012 dropped as transition year)

Sample restrictions
-------------------
- Hispanic of Mexican origin (hispan == 1)
- Born in Mexico (bpl == 200)
- Non-citizen (citizen == 3; proxy for undocumented status)
- Year of immigration recorded and <= 2007 (5-year continuous US residence by June 2012)
- Arrived before 16th birthday (yrimmig - birthyr < 16)
- Birth year 1972-1996 (covers both treatment and control cohorts)
- Survey year 2009-2016, excluding 2012
- Working-age (18-40 at time of survey)

Model
-----
OLS/WLS DiD with year FEs (absorbing 'post' main effect), state FEs, age, age^2, sex.
Person weights used (perwt). Heteroskedasticity-robust (HC1) standard errors.
"""

import json
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ── Column layout from ACS_extract_expanded_layout_excerpt.do ─────────────────
# Stata positions are 1-indexed; Python colspecs are 0-indexed (start, end exclusive)
COLSPECS = [
    (0,   4),    # year      – Census year
    (65,  67),   # statefip  – State FIPS code
    (691, 701),  # perwt     – Person weight (raw value; divide by 100 per do-file)
    (739, 740),  # sex       – 1=Male, 2=Female
    (740, 743),  # age       – Age in years
    (747, 751),  # birthyr   – Year of birth
    (763, 764),  # hispan    – Hispanic origin general (1=Mexican)
    (767, 770),  # bpl       – Birthplace general (200=Mexico)
    (789, 790),  # citizen   – Citizenship (3=Not a citizen)
    (794, 798),  # yrimmig   – Year of immigration (0=N/A)
    (874, 875),  # empstat   – Employment status general (1=Employed)
    (904, 906),  # uhrswork  – Usual hours worked per week
]

COLNAMES = ['year', 'statefip', 'perwt', 'sex', 'age', 'birthyr',
            'hispan', 'bpl', 'citizen', 'yrimmig', 'empstat', 'uhrswork']

# Use compact dtypes to limit per-chunk memory; int16 safely holds all values <=32767
DTYPES = {
    'year':     'int16',
    'statefip': 'int16',
    'perwt':    'float32',   # will be divided by 100 after reading
    'sex':      'int16',
    'age':      'int16',     # can reach 140 in codebook, so int16 (not int8)
    'birthyr':  'int16',
    'hispan':   'int16',
    'bpl':      'int16',
    'citizen':  'int16',
    'yrimmig':  'int16',
    'empstat':  'int16',
    'uhrswork': 'int16',
}

# Resolve path relative to this script so it works from any working directory
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'ACS_extract_expanded.dat')

# ── Read fixed-width file in chunks to stay within ~30 GB memory budget ───────
CHUNK_SIZE = 500_000
kept_chunks = []

reader = pd.read_fwf(
    DATA_PATH,
    colspecs=COLSPECS,
    header=None,
    names=COLNAMES,
    dtype=DTYPES,
    chunksize=CHUNK_SIZE,
)

for chunk in reader:
    # Apply person-weight scaling (raw ÷ 100 per layout do-file)
    chunk['perwt'] = chunk['perwt'] / 100.0

    # ── Early row filters ────────────────────────────────────────────────────
    # Compute arrival age as integer to avoid overflow on int16 subtraction
    arrival_age = chunk['yrimmig'].astype('int32') - chunk['birthyr'].astype('int32')

    mask = (
        (chunk['hispan']  == 1)    &   # Hispanic of Mexican origin
        (chunk['bpl']     == 200)  &   # Born in Mexico
        (chunk['citizen'] == 3)    &   # Non-citizen (proxy for undocumented)
        (chunk['yrimmig'] >  0)    &   # Has a recorded immigration year
        (chunk['yrimmig'] <= 2007) &   # In US ≥5 yrs before DACA (arrived by 2007)
        (arrival_age      <  16)   &   # Arrived before 16th birthday
        (chunk['year']    >= 2009) &   # Analysis window: 2009-2016 minus 2012
        (chunk['year']    <= 2016) &
        (chunk['year']    != 2012) &   # Drop DACA implementation/transition year
        (chunk['birthyr'] >= 1972) &   # Covers control (1972-1981) + treated (1982-1996)
        (chunk['birthyr'] <= 1996) &
        (chunk['age']     >= 18)   &   # Working-age adults
        (chunk['age']     <= 40)
    )
    sub = chunk.loc[mask].copy()
    if len(sub) > 0:
        kept_chunks.append(sub)

df = pd.concat(kept_chunks, ignore_index=True)

# ── Construct analysis variables ───────────────────────────────────────────────
# Treatment indicator: DACA-eligible birth cohort (born >=1982 → age ≤30 on 15 Jun 2012)
# Control cohort: born 1972-1981 (would have been DACA-eligible except too old)
df['eligible'] = (df['birthyr'] >= 1982).astype('int8')

# Post-DACA indicator (year >= 2013)
df['post'] = (df['year'] >= 2013).astype('int8')

# Difference-in-differences interaction term
df['post_x_elig'] = df['post'] * df['eligible']

# Outcome: full-time employed = employed (empstat==1) AND usually works >=35 hrs/week
df['fulltime'] = (
    (df['empstat'] == 1) & (df['uhrswork'] >= 35)
).astype('int8')

# ── Verify treatment variation before running model ────────────────────────────
if df['eligible'].nunique() < 2:
    sys.stderr.write("ERROR: No variation in treatment indicator.\n")
    sys.exit(1)

# ── Difference-in-differences regression ──────────────────────────────────────
# Year FEs absorb the 'post' main effect.
# State FEs control for state-level fixed differences.
# Age + age^2 capture lifecycle employment patterns.
# Sex controls for gender differences in full-time work.
formula = (
    'fulltime ~ post_x_elig + eligible'
    ' + C(year) + C(statefip)'
    ' + age + I(age**2)'
    ' + C(sex)'
)

res = smf.wls(
    formula=formula,
    data=df,
    weights=df['perwt'],
).fit(cov_type='HC1')

# ── Output: ONLY the JSON object required by the prompt ───────────────────────
output = {
    'point_estimate': float(res.params['post_x_elig']),
    'standard_error': float(res.bse['post_x_elig']),
    'sample_size':    int(res.nobs),
}
print(json.dumps(output))
