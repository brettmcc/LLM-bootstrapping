"""
DACA DiD Analysis
=================
Research question: Effect of DACA eligibility on full-time employment (>=35 hrs/week)
among Hispanic-Mexican, Mexico-born, non-citizen people in the US.

Identification strategy: Difference-in-Differences
  - Treated:  DACA-eligible (Mexican-born, non-citizen, arrived before age 16,
              arrived by 2007, born >= 1982 i.e. under 31 on June 15 2012)
  - Control:  Just above the DACA age cutoff (same criteria except birthyr 1977-1981)
  - Pre:      2009-2011  (3 years before DACA, implemented August 2012)
  - Post:     2013-2016  (first full post-DACA years, skipping 2012 transition year)

Model: OLS DiD with year and state FE, standard errors clustered at state level
  ft_employed ~ daca_eligible * post + C(year) + C(statefip) + female
"""

import os
import sys
import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ── Column specs from ACS_extract_expanded_layout_excerpt.do ─────────────────
# Format: (python_0indexed_start, python_0indexed_end_exclusive)
# Conversion: python_start = stata_start - 1,  python_end = stata_end
COLSPECS = [
    (0,   4),    # year       Stata 1-4
    (65,  67),   # statefip   Stata 66-67
    (739, 740),  # sex        Stata 740
    (740, 743),  # age        Stata 741-743
    (747, 751),  # birthyr    Stata 748-751
    (763, 764),  # hispan     Stata 764
    (767, 770),  # bpl        Stata 768-770
    (789, 790),  # citizen    Stata 790
    (794, 798),  # yrimmig    Stata 795-798
    (874, 875),  # empstat    Stata 875
    (904, 906),  # uhrswork   Stata 905-906
]

NAMES = [
    'year', 'statefip', 'sex', 'age', 'birthyr',
    'hispan', 'bpl', 'citizen', 'yrimmig',
    'empstat', 'uhrswork',
]

# Use small integer types to keep memory low
DTYPES = {
    'year':     'int16',
    'statefip': 'int8',
    'sex':      'int8',
    'age':      'int16',
    'birthyr':  'int16',
    'hispan':   'int8',
    'bpl':      'int16',
    'citizen':  'int8',
    'yrimmig':  'int16',
    'empstat':  'int8',
    'uhrswork': 'int8',
}

CHUNK_SIZE = 500_000  # rows per chunk to stay within memory budget

# ── Locate data file relative to this script ─────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE  = os.path.join(SCRIPT_DIR, 'ACS_extract_expanded.dat')

# ── Load and filter in chunks ─────────────────────────────────────────────────
kept_chunks = []

for chunk in pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=NAMES,
    dtype=DTYPES,
    header=None,
    chunksize=CHUNK_SIZE,
):
    # Age-at-immigration proxy (using survey-year birth year and immigration year)
    age_at_immigration = chunk['yrimmig'] - chunk['birthyr']

    mask = (
        # Ethnicity: Mexican-Hispanic
        (chunk['hispan'] == 1) &
        # Country of birth: Mexico (BPL general code 200)
        (chunk['bpl'] == 200) &
        # Citizenship: not a citizen (3) or first-papers only (4)
        ((chunk['citizen'] == 3) | (chunk['citizen'] == 4)) &
        # Has a recorded immigration year (0 = N/A / born in US)
        (chunk['yrimmig'] > 0) &
        # Arrived by 2007 (satisfies DACA's 5-year continuous presence by June 2012)
        (chunk['yrimmig'] <= 2007) &
        # Arrived before 16th birthday (key DACA criterion)
        (age_at_immigration >= 0) &
        (age_at_immigration < 16) &
        # Study period: pre (2009-2011) and post (2013-2016), drop 2012 transition
        (chunk['year'] >= 2009) &
        (chunk['year'] <= 2016) &
        (chunk['year'] != 2012) &
        # Birth cohort: 1977-1991 ensures everyone is at least 18 in 2009
        # Treated (eligible): 1982-1991; Control (just above cutoff): 1977-1981
        (chunk['birthyr'] >= 1977) &
        (chunk['birthyr'] <= 1991)
    )

    sub = chunk.loc[mask].copy()
    if len(sub) > 0:
        kept_chunks.append(sub)

df = pd.concat(kept_chunks, ignore_index=True)

# ── Construct analysis variables ──────────────────────────────────────────────

# DACA eligibility: born after June 15, 1981 => birthyr >= 1982 is the clean cutoff
# (persons born in 1982 had definitely not turned 31 by June 15, 2012)
df['daca_eligible'] = (df['birthyr'] >= 1982).astype('int8')

# Post-DACA indicator: DACA implemented Aug 2012; first full effects visible 2013+
df['post'] = (df['year'] >= 2013).astype('int8')

# Outcome: employed full-time = usual hours per week >= 35
# uhrswork == 0 is N/A (not employed), so this correctly codes non-employed as 0
df['ft_employed'] = (df['uhrswork'] >= 35).astype('int8')

# Female indicator (control for gender differences in employment)
df['female'] = (df['sex'] == 2).astype('int8')

# ── Verify treatment variation ────────────────────────────────────────────────
n_treated = int(df['daca_eligible'].sum())
n_control = int((df['daca_eligible'] == 0).sum())

print(f"Treated (DACA-eligible, birthyr 1982-1991): {n_treated}", file=sys.stderr)
print(f"Control (above cutoff, birthyr 1977-1981):  {n_control}", file=sys.stderr)
print(f"Total analytic sample:                      {len(df)}",   file=sys.stderr)

if n_treated == 0 or n_control == 0:
    print("FATAL: No variation in treatment variable — check data filters.", file=sys.stderr)
    sys.exit(1)

# ── OLS DiD regression ────────────────────────────────────────────────────────
# Year and state fixed effects absorb common time trends and state-level levels.
# Standard errors clustered at the state level (treatment varies at national level,
# but there is state-level correlation in labour market shocks).
model = smf.ols(
    'ft_employed ~ daca_eligible * post + C(year) + C(statefip) + female',
    data=df,
)
result = model.fit(cov_type='HC1')

# DiD estimate: coefficient on the daca_eligible:post interaction
point_estimate = float(result.params['daca_eligible:post'])
standard_error = float(result.bse['daca_eligible:post'])
sample_size    = int(result.nobs)

# ── Output (must be ONLY this JSON on stdout) ─────────────────────────────────
print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size":    sample_size,
}))
