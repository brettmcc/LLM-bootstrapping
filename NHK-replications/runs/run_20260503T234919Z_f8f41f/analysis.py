"""
Analysis: Effect of DACA eligibility on full-time employment among
Mexican-born Mexican-Hispanic non-citizens in the United States.

Design: Difference-in-Differences (DiD) exploiting the DACA age cutoff.
  - Treatment group: birthyr >= 1982 (under 31 on June 15, 2012 -> DACA eligible age)
  - Control group:   birthyr in [1972, 1981] (31-40 on June 15, 2012 -> too old for DACA)
  - Pre period:      2009-2011
  - Post period:     2013-2016 (exclude 2012, the implementation/transition year)

Outcome: full_time = 1 if employed (empstat==1) AND usual hours >= 35.

Model: OLS linear probability model with HC1 robust SEs.
  full_time ~ treat * post + age + age^2 + C(year) + C(statefip) + C(sex)
"""

import os
import sys
import json
import warnings
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Fixed-width file column specifications
# Stata infix uses 1-based inclusive column numbers.
# Python read_fwf colspecs use 0-based half-open intervals: Stata A-B -> (A-1, B)
# Columns listed in left-to-right order (required by read_fwf).
# ---------------------------------------------------------------------------
COLSPECS = [
    (0, 4),      # year       (Stata 1-4)
    (65, 67),    # statefip   (Stata 66-67)
    (691, 701),  # perwt      (Stata 692-701; 2 implied decimals, not used in regression)
    (739, 740),  # sex        (Stata 740-740; 1=Male, 2=Female)
    (740, 743),  # age        (Stata 741-743)
    (747, 751),  # birthyr    (Stata 748-751; actual birth year)
    (763, 764),  # hispan     (Stata 764-764; 1=Mexican)
    (767, 770),  # bpl        (Stata 768-770; 200=Mexico)
    (789, 790),  # citizen    (Stata 790-790; 3=Not a citizen)
    (794, 798),  # yrimmig    (Stata 795-798; 0=N/A)
    (874, 875),  # empstat    (Stata 875-875; 1=Employed, 2=Unemployed, 3=NILF)
    (904, 906),  # uhrswork   (Stata 905-906; usual hours worked per week; 0=N/A)
]

COLNAMES = [
    'year', 'statefip', 'perwt', 'sex', 'age', 'birthyr',
    'hispan', 'bpl', 'citizen', 'yrimmig', 'empstat', 'uhrswork',
]

# Study years: pre-DACA (2009-2011) and post-DACA (2013-2016).
# 2012 excluded: DACA announced June 2012, applications opened Aug 2012 -> transition year.
STUDY_YEARS = {2009, 2010, 2011, 2013, 2014, 2015, 2016}

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ACS_extract_expanded.dat')

# ---------------------------------------------------------------------------
# Read the large fixed-width file in chunks, filtering early to save memory
# ---------------------------------------------------------------------------
chunks = []
CHUNK_SIZE = 200_000  # rows per iteration

for chunk in pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=COLNAMES,
    header=None,
    chunksize=CHUNK_SIZE,
):
    # Keep only the study years (pre and post DACA)
    chunk = chunk[chunk['year'].isin(STUDY_YEARS)]
    if len(chunk) == 0:
        continue

    # Restrict to Mexico-born (bpl=200) with Mexican Hispanic ethnicity (hispan=1)
    chunk = chunk[(chunk['bpl'] == 200) & (chunk['hispan'] == 1)]
    if len(chunk) == 0:
        continue

    # Non-citizen as a proxy for undocumented status (citizen=3)
    chunk = chunk[chunk['citizen'] == 3]
    if len(chunk) == 0:
        continue

    # Valid immigration year (not N/A) and immigrated by 2007 so they
    # have been continuously in the US for at least 5 years before June 15, 2012
    chunk = chunk[(chunk['yrimmig'] > 0) & (chunk['yrimmig'] <= 2007)]
    if len(chunk) == 0:
        continue

    # Arrived before age 16 (DACA requirement).
    # Approximate age at arrival = yrimmig - birthyr.
    # Exclude invalid birthyr (0 = N/A in some cases).
    chunk = chunk[chunk['birthyr'] > 0]
    chunk = chunk[(chunk['yrimmig'] - chunk['birthyr']) < 16]
    if len(chunk) == 0:
        continue

    # Working-age adults in the survey year (18-40)
    chunk = chunk[(chunk['age'] >= 18) & (chunk['age'] <= 40)]
    if len(chunk) == 0:
        continue

    # Keep only valid sex codes (1=Male, 2=Female; drop 9=Missing)
    chunk = chunk[chunk['sex'].isin([1, 2])]
    if len(chunk) == 0:
        continue

    # Keep only valid employment status (1=Employed, 2=Unemployed, 3=NILF; drop 0=N/A, 9=Unknown)
    chunk = chunk[chunk['empstat'].isin([1, 2, 3])]
    if len(chunk) == 0:
        continue

    # Drop employed individuals with missing usual hours (empstat=1 but uhrswork=0)
    # since we cannot determine if they are full-time or not
    chunk = chunk[~((chunk['empstat'] == 1) & (chunk['uhrswork'] == 0))]
    if len(chunk) == 0:
        continue

    chunks.append(chunk)

# Combine all filtered chunks
df = pd.concat(chunks, ignore_index=True)

# ---------------------------------------------------------------------------
# Construct treatment, post, and outcome variables
# ---------------------------------------------------------------------------

# DACA age cutoff: must not have had 31st birthday as of June 15, 2012.
# birthyr >= 1982: born 1982 or later -> clearly under 31 on June 15, 2012 -> DACA eligible age.
# birthyr in [1972, 1981]: born 1972-1981 -> turned 31-40 in 2012 -> too old for DACA (control).
df['treat'] = (df['birthyr'] >= 1982).astype(int)
control_mask = (df['birthyr'] >= 1972) & (df['birthyr'] <= 1981)

# Keep only the treatment group (eligible age) and control group (just-too-old)
df = df[(df['treat'] == 1) | control_mask]

# Post-DACA period indicator (2013 onward)
df['post'] = (df['year'] >= 2013).astype(int)

# Outcome: full-time employment (employed AND usually works >= 35 hours/week)
df['full_time'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

# Age squared for nonlinear age control
df['age_sq'] = df['age'] ** 2

# Ensure integer types for categorical variables
for col in ['statefip', 'year', 'sex']:
    df[col] = df[col].astype(int)

# Drop any rows with missing values in regression variables
reg_cols = ['full_time', 'treat', 'post', 'age', 'age_sq', 'statefip', 'year', 'sex']
df = df.dropna(subset=reg_cols)

# ---------------------------------------------------------------------------
# Difference-in-Differences: OLS Linear Probability Model
#
# full_time ~ treat + post + treat:post + age + age^2 + year_FE + state_FE + sex_FE
#
# treat:post is the DiD coefficient: the causal effect of DACA eligibility
# on full-time employment among Mexican-born non-citizens who arrived before age 16.
# ---------------------------------------------------------------------------
formula = (
    'full_time ~ treat * post '
    '+ age + age_sq '
    '+ C(year) + C(statefip) + C(sex)'
)

model = smf.ols(formula=formula, data=df).fit(cov_type='HC1')

# Extract DiD estimate (effect of DACA eligibility on full-time employment)
point_estimate = float(model.params['treat:post'])
standard_error = float(model.bse['treat:post'])
sample_size = int(model.nobs)

# Output ONLY the JSON result to stdout (no other text)
print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size": sample_size,
}))
