"""
DACA Effect on Full-Time Employment: Difference-in-Differences

Research question: causal impact of DACA eligibility on probability of
full-time employment (>=35 hrs/week) among Hispanic-Mexican, Mexican-born,
non-citizen individuals in the United States, 2013-2016.

Identification strategy: DiD exploiting the DACA age-31 cutoff.
  - Treatment group: arrived-before-16, arrived-by-2007, age <=30 in June 2012
    (born after June 15 1981 -> DACA-eligible by age)
  - Control group:  arrived-before-16, arrived-by-2007, age 31-40 in June 2012
    (born before June 15 1981 -> DACA-ineligible by age)
  - Pre period: 2006-2011; Post period: 2013-2016 (exclude transition year 2012)

Model: Weighted LPM DiD with state FE, year FE, age polynomial,
       clustered SE at state level.
Key coefficient: daca_eligible:post_daca (DiD interaction term).
"""

import sys
import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---- Column positions in fixed-width file ------------------------------------
# Source: ACS_extract_expanded_layout_excerpt.do (Stata 1-indexed, inclusive)
# Converted to Python 0-indexed, end-exclusive for pandas read_fwf.
COLSPECS = [
    (0, 4),       # year       (Stata cols 1-4)
    (65, 67),     # statefip   (66-67)
    (138, 139),   # gq         (139-139)
    (691, 701),   # perwt      (692-701) -- double, 2 implied decimal places
    (740, 743),   # age        (741-743)
    (763, 764),   # hispan     (764-764)
    (767, 770),   # bpl        (768-770)
    (789, 790),   # citizen    (790-790)
    (794, 798),   # yrimmig    (795-798)
    (874, 875),   # empstat    (875-875)
    (904, 906),   # uhrswork   (905-906)
]
COL_NAMES = [
    'year', 'statefip', 'gq', 'perwt',
    'age', 'hispan', 'bpl', 'citizen', 'yrimmig',
    'empstat', 'uhrswork',
]

DATA_FILE = 'ACS_extract_expanded.dat'
CHUNK_SIZE = 500_000   # rows per chunk; keeps memory well under 30 GB

# ---- Step 1: Read data in chunks, filtering early ----------------------------
chunks = []
for chunk in pd.read_fwf(
        DATA_FILE,
        colspecs=COLSPECS,
        names=COL_NAMES,
        chunksize=CHUNK_SIZE,
        header=None,
        dtype=str):          # read as strings first; convert below

    # Convert every column to numeric; non-parseable values -> NaN
    for col in COL_NAMES:
        chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

    # Early filter: retain only the relevant population to save memory.
    # hispan=1 -> Mexican Hispanic; bpl=200 -> born in Mexico;
    # citizen=3 -> non-citizen (proxy for undocumented status);
    # gq in {1,2,5} -> non-institutional household;
    # yrimmig>0 -> has a known immigration year (not N/A);
    # year 2006-2016, excluding 2012 (transition / implementation year);
    # age 15-55 to capture all relevant cohorts.
    mask = (
        (chunk['hispan'] == 1) &
        (chunk['bpl'] == 200) &
        (chunk['citizen'] == 3) &
        (chunk['gq'].isin([1, 2, 5])) &
        (chunk['yrimmig'] > 0) &
        (chunk['year'] >= 2006) &
        (chunk['year'] <= 2016) &
        (chunk['year'] != 2012) &
        (chunk['age'].between(15, 55))
    )
    chunks.append(chunk.loc[mask].copy())

df = pd.concat(chunks, ignore_index=True)

# ---- Step 2: Adjust PERWT (codebook: 2 implied decimal places) ---------------
# Example from codebook: stored value 010461 -> actual weight 104.61.
# Check magnitude: if values are clearly large integers, divide by 100.
if df['perwt'].dropna().max() > 1000:
    df['perwt'] = df['perwt'] / 100.0

# ---- Step 3: Derive DACA-relevant variables ----------------------------------
# Approximate birth year (integer; off by at most 1 due to survey timing)
df['birth_year'] = df['year'] - df['age']

# Age at immigration: year of arrival minus approximate birth year
df['age_at_immig'] = df['yrimmig'] - df['birth_year']

# Age as of June 15, 2012 (DACA announcement date)
# formula: age_in_2012 = age - (survey_year - 2012)
df['age_in_2012'] = df['age'] - (df['year'] - 2012)

# ---- Step 4: Sample selection filters ----------------------------------------
# (a) Arrived before 16th birthday -- core DACA requirement
df = df[(df['age_at_immig'] >= 0) & (df['age_at_immig'] < 16)]

# (b) Arrived by 2007 -- proxy for >=5 years continuous US residence before DACA
df = df[df['yrimmig'] <= 2007]

# (c) Cohort window: treatment (age <=30 in 2012) + control (age 31-40 in 2012)
df = df[df['age_in_2012'].between(15, 40)]

# (d) Working age at survey time (18+)
df = df[df['age'] >= 18]

# (e) Drop rows with missing values on outcome or key regression variables
df = df.dropna(subset=['empstat', 'uhrswork', 'perwt', 'statefip'])

# (f) Remove observations with zero or negative survey weights
df = df[df['perwt'] > 0]

# Ensure integer types for state and year FE
df['statefip'] = df['statefip'].astype(int)
df['year'] = df['year'].astype(int)

# ---- Step 5: Construct outcome and treatment indicators ----------------------
# Outcome: full-time employment = employed (empstat=1) AND usual hours >= 35/wk
# (empstat=0 is N/A -- children etc.; uhrswork=0 is N/A for non-employed)
df['full_time_emp'] = (
    (df['empstat'] == 1) & (df['uhrswork'] >= 35)
).astype(int)

# Treatment: DACA-eligible by the age-31 cutoff on June 15, 2012.
# Born AFTER June 15, 1981 -> had not yet turned 31 -> age_in_2012 <= 30.
df['daca_eligible'] = (df['age_in_2012'] <= 30).astype(int)

# Post-DACA period indicator (2013-2016 vs 2006-2011)
df['post_daca'] = (df['year'] >= 2013).astype(int)

# ---- Step 6: Verify treatment variation before running regression -------------
variation = (
    df.groupby(['daca_eligible', 'post_daca'])['full_time_emp']
    .agg(n='count', mean='mean')
)
print("Treatment variation check:\n", variation, file=sys.stderr)

if variation['n'].min() == 0:
    print("ERROR: No variation in treatment -- aborting.", file=sys.stderr)
    sys.exit(1)

# ---- Step 7: DiD regression (LPM) -------------------------------------------
# Weighted OLS with state FE, year FE, age polynomial.
# Interactions of daca_eligible x post_daca:
#   - daca_eligible        : time-invariant treatment-group indicator
#   - post_daca            : absorbed into C(year) FE (redundant but harmless)
#   - daca_eligible:post_daca : DiD coefficient -- causal estimate of DACA effect
# Standard errors clustered at the state level.
formula = (
    'full_time_emp ~ daca_eligible * post_daca + '
    'C(year) + C(statefip) + age + I(age**2)'
)
model = smf.wls(
    formula,
    data=df,
    weights=df['perwt']
).fit(cov_type='cluster', cov_kwds={'groups': df['statefip']})

print(model.summary(), file=sys.stderr)

# ---- Step 8: Extract and print results ---------------------------------------
point_estimate = float(model.params['daca_eligible:post_daca'])
standard_error = float(model.bse['daca_eligible:post_daca'])
sample_size = int(len(df))

# ONLY the JSON object is written to stdout (as required)
print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size": sample_size,
}))
