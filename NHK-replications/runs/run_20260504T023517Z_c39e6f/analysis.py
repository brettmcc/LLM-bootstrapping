"""
DACA Difference-in-Differences Analysis
Research Question:
  Among ethnically Hispanic-Mexican, Mexican-born people in the US, what was the
  causal impact of DACA eligibility on the probability of full-time employment
  (usually >= 35 hrs/wk), estimated for 2013-2016 using a DiD design?

Identification strategy:
  DACA's age cutoff (must be < 31 as of June 15, 2012) creates a sharp discontinuity.
  We compare Mexican-born, non-citizen immigrants who arrived before age 16 and by 2007:
    - Treated: birth year >= 1982 (age < 31 at June 2012; DACA-eligible)
    - Control:  birth year 1972-1981 (age 31-40 at June 2012; just above cutoff)
  Estimator: OLS DiD with state and year fixed effects, SEs clustered by state.
"""

import json       # for serializing output
import sys        # for redirecting diagnostic messages to stderr
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# ---------------------------------------------------------------------------
# Fixed-width column layout (0-based start, exclusive end)
# Source: ACS_extract_expanded_layout_excerpt.do (Stata 1-based positions)
# ---------------------------------------------------------------------------
COLSPECS = [
    (0,   4),    # year:     survey year
    (65,  67),   # statefip: state FIPS code
    (691, 701),  # perwt:    person weight (stored * 100, divide below)
    (740, 743),  # age:      age at survey
    (747, 751),  # birthyr:  birth year
    (763, 764),  # hispan:   Hispanic origin, general (1 = Mexican)
    (767, 770),  # bpl:      birthplace, general (200 = Mexico)
    (789, 790),  # citizen:  citizenship status (3 = not a citizen)
    (794, 798),  # yrimmig:  year of immigration (0 = N/A)
    (874, 875),  # empstat:  employment status (1 = employed)
    (904, 906),  # uhrswork: usual hours worked per week
]

COLNAMES = [
    'year', 'statefip', 'perwt', 'age', 'birthyr',
    'hispan', 'bpl', 'citizen', 'yrimmig', 'empstat', 'uhrswork',
]

DATA_FILE = 'ACS_extract_expanded.dat'

# ---------------------------------------------------------------------------
# Read data in chunks to stay well within the 30 GB memory limit.
# We apply sample filters inside the loop so we only keep relevant rows.
# ---------------------------------------------------------------------------
CHUNK_SIZE = 400_000  # rows per chunk; adjust down if RAM is tight

# Survey years: pre-DACA (2009-2011) and post-DACA (2013-2016).
# 2012 is excluded because DACA was announced mid-year, making it ambiguous.
KEEP_YEARS = {2009, 2010, 2011, 2013, 2014, 2015, 2016}

chunks = []

print("Reading data file in chunks...", file=sys.stderr)

with pd.read_fwf(
    DATA_FILE,
    colspecs=COLSPECS,
    names=COLNAMES,
    dtype=str,          # read everything as string first; convert below
    chunksize=CHUNK_SIZE,
    header=None,
) as reader:
    for i, chunk in enumerate(reader):
        # --- Convert all columns to numeric; coerce invalid entries to NaN ---
        for col in COLNAMES:
            chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

        # Drop rows with any missing value in our key variables
        chunk = chunk.dropna(subset=COLNAMES)

        # Scale perwt: stored as integer*100 in the fixed-width file
        chunk['perwt'] = chunk['perwt'] / 100.0

        # ---- Sample filters (applied early to minimize memory usage) --------

        # 1. Ethnically Hispanic-Mexican: hispan == 1
        chunk = chunk[chunk['hispan'] == 1]

        # 2. Born in Mexico: BPL general code 200
        chunk = chunk[chunk['bpl'] == 200]

        # 3. Non-citizen: proxy for lacking lawful status (citizen == 3)
        chunk = chunk[chunk['citizen'] == 3]

        # 4. Survey years of interest only (exclude 2012)
        chunk = chunk[chunk['year'].isin(KEEP_YEARS)]

        # 5. Birth year range defining both comparison groups:
        #      Treated (DACA-eligible):  birthyr 1982-1997 → age <  31 at June 2012
        #      Control (just over cutoff): birthyr 1972-1981 → age 31-40 at June 2012
        chunk = chunk[(chunk['birthyr'] >= 1972) & (chunk['birthyr'] <= 1997)]

        # 6. Must have immigrated (yrimmig > 0 means the person was actually recorded
        #    as having arrived; 0 = N/A, typically used for US-born)
        chunk = chunk[chunk['yrimmig'] > 0]

        # 7. Arrived by June 2007: proxy for the DACA requirement of continuous
        #    residence in the US since June 15, 2007
        chunk = chunk[chunk['yrimmig'] <= 2007]

        # 8. Arrived before age 16: key DACA eligibility requirement.
        #    We approximate age at arrival as (yrimmig - birthyr).
        chunk['age_at_arr'] = chunk['yrimmig'] - chunk['birthyr']
        chunk = chunk[(chunk['age_at_arr'] >= 0) & (chunk['age_at_arr'] < 16)]

        # 9. At least 18 years old at survey time (focus on adults in labor market)
        chunk = chunk[chunk['age'] >= 18]

        # Store the filtered chunk (drop helper column to save memory)
        chunks.append(chunk.drop(columns=['age_at_arr']))

        if i % 10 == 0:
            print(f"  ... processed chunk {i}", file=sys.stderr)

print(f"Finished reading. Concatenating {len(chunks)} chunks...", file=sys.stderr)
df = pd.concat(chunks, ignore_index=True)
print(f"  Sample size after filters: {len(df):,}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Define treatment, post, and outcome variables
# ---------------------------------------------------------------------------

# Treatment indicator: DACA-eligible age cohort
#   birthyr >= 1982  →  age < 31 as of June 15, 2012  →  treated = 1
#   birthyr 1972-1981 →  age 31-40 at June 2012        →  treated = 0
df['treated'] = (df['birthyr'] >= 1982).astype(np.float64)

# Post-DACA indicator: survey year >= 2013
df['post'] = (df['year'] >= 2013).astype(np.float64)

# Outcome: full-time employment
#   employed (empstat == 1) AND usually works >= 35 hours per week (uhrswork >= 35)
df['employed_ft'] = (
    (df['empstat'] == 1) & (df['uhrswork'] >= 35)
).astype(np.float64)

# Explicit DiD interaction term (needed for double-demeaning step below)
df['post_treated'] = df['post'] * df['treated']

# Cast grouping variables to int
df['statefip'] = df['statefip'].astype(int)
df['year']     = df['year'].astype(int)

# ---------------------------------------------------------------------------
# Verify treatment variation (required by the prompt)
# ---------------------------------------------------------------------------
treat_counts = df['treated'].value_counts()
print(f"Treatment variation:\n{treat_counts}", file=sys.stderr)

if treat_counts.get(0.0, 0) == 0 or treat_counts.get(1.0, 0) == 0:
    raise ValueError("No variation in treatment variable. Revise specification.")

post_counts = df['post'].value_counts()
print(f"Post variation:\n{post_counts}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Frisch-Waugh-Lovell (FWL) two-way fixed-effects approach
#
# Problem: running OLS with explicit state dummies creates K ≈ 64 parameters
# but only G = 51 state clusters, making the cluster-robust sandwich matrix
# rank-deficient and yielding nonsensical SEs.
#
# Solution (FWL theorem): partial out state and year fixed effects from all
# variables of interest via iterative double-demeaning, then run OLS on the
# residuals.  The resulting model has only K = 4 parameters, so G = 51 >> K
# and the clustered covariance estimator is well-defined.
#
# The coefficient on `post_treated_dm` in OLS(employed_ft_dm ~ ...)
# is numerically equivalent to the coefficient on `post:treated` in the
# full model with explicit FE dummies.
# ---------------------------------------------------------------------------

def double_demean(df, var, entity_col, time_col, max_iter=200, tol=1e-10):
    """
    Partial out two-way fixed effects (entity + time) via alternating projections
    (Gauss-Seidel iteration on entity and time means).

    Parameters
    ----------
    df          : DataFrame with entity_col and time_col as columns
    var         : name of the column to demean
    entity_col  : column name for the entity (state) grouping variable
    time_col    : column name for the time (year) grouping variable
    max_iter    : maximum number of alternating-projection iterations
    tol         : convergence tolerance (max absolute change in residuals)

    Returns
    -------
    pandas Series with the within-entity-time residuals
    """
    # Start with the raw values as a float Series (same index as df)
    v = df[var].astype(float).copy()

    entity = df[entity_col]   # Series used for groupby alignment
    time   = df[time_col]     # Series used for groupby alignment

    for _ in range(max_iter):
        v_prev = v.values.copy()

        # Subtract entity (state) conditional means
        v = v - v.groupby(entity).transform('mean')

        # Subtract time (year) conditional means
        v = v - v.groupby(time).transform('mean')

        # Check convergence: stop when max residual change is below tolerance
        if np.max(np.abs(v.values - v_prev)) < tol:
            break

    return v


print("Double-demeaning variables to partial out state and year FEs...", file=sys.stderr)

# Demean all four variables involved in the DiD interaction model
for var in ['employed_ft', 'post', 'treated', 'post_treated']:
    df[var + '_dm'] = double_demean(df, var, 'statefip', 'year')
    print(f"  demeaned {var}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Difference-in-Differences regression on double-demeaned variables
#
#   employed_ft_dm = α + β1·post_dm + β2·treated_dm + β3·post_treated_dm + ε
#
#   β3 is the DiD estimator (identical to the full-model coefficient by FWL).
#   With K = 4 parameters and G = 51 state clusters, the clustered sandwich
#   estimator is well-identified (G >> K).
# ---------------------------------------------------------------------------
print("Running DiD regression on demeaned variables...", file=sys.stderr)

model = smf.ols(
    'employed_ft_dm ~ post_dm + treated_dm + post_treated_dm',
    data=df,
).fit(
    cov_type='cluster',
    cov_kwds={'groups': df['statefip']},
)

print(f"  R-squared: {model.rsquared:.4f}", file=sys.stderr)
print(f"  DiD coef (post_treated_dm): {model.params['post_treated_dm']:.6f}", file=sys.stderr)
print(f"  Clustered SE:               {model.bse['post_treated_dm']:.6f}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Output: ONLY a single JSON object to STDOUT (no extra text)
# ---------------------------------------------------------------------------
result = {
    'point_estimate': float(model.params['post_treated_dm']),
    'standard_error': float(model.bse['post_treated_dm']),
    'sample_size':    int(len(df)),
}

print(json.dumps(result))
