#!/usr/bin/env python3
"""
DACA Employment Impact Analysis
Analyzes the causal impact of DACA eligibility on full-time employment for Mexican-born non-citizens
"""

import pandas as pd
import numpy as np
import json
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# 1. READ THE FIXED-WIDTH ACS DATA
# ============================================================================

# Define column specifications based on ACS_extract_expanded_layout_excerpt.do
# We'll read only the columns we need to reduce memory usage
col_specs = [
    (0, 4, 'year'),          # positions 1-4
    (692-1, 701, 'perwt'),   # positions 692-701 (adjust for 0-indexing)
    (741-1, 743, 'age'),     # positions 741-743
    (764-1, 764, 'hispan'),  # position 764
    (768-1, 770, 'bpl'),     # positions 768-770
    (790-1, 790, 'citizen'), # position 790
    (875-1, 875, 'empstat'), # position 875
    (905-1, 906, 'uhrswork'), # positions 905-906
    (67-1, 67, 'statefip'),  # position 67 (for state identifier)
]

# More precise column definitions (1-indexed from Stata becomes 0-indexed)
dtypes = {
    'year': int,
    'perwt': float,
    'age': int,
    'hispan': int,
    'bpl': int,
    'citizen': int,
    'empstat': int,
    'uhrswork': int,
    'statefip': int,
}

# Read fixed-width file with targeted columns
# Since we're reading specific columns, we'll read in chunks to manage memory
acs_data = []
chunk_size = 100000

with open('ACS_extract_expanded.dat', 'r') as f:
    lines_read = 0
    for line in f:
        if len(line) < 906:  # Skip incomplete lines
            continue
            
        # Extract fields based on 1-based positions (convert to 0-based indexing)
        try:
            year = int(line[0:4].strip() or -1)
            statefip = int(line[66:68].strip() or -1)
            perwt = float(line[691:701].strip() or -1) / 100.0  # Divide by 100 for implied decimals
            age = int(line[740:743].strip() or -1)
            hispan = int(line[763:764].strip() or -1)
            bpl = int(line[767:770].strip() or -1)
            citizen = int(line[789:790].strip() or -1)
            empstat = int(line[874:875].strip() or -1)
            uhrswork = int(line[904:906].strip() or -1)
            
            acs_data.append({
                'year': year,
                'statefip': statefip,
                'perwt': perwt,
                'age': age,
                'hispan': hispan,
                'bpl': bpl,
                'citizen': citizen,
                'empstat': empstat,
                'uhrswork': uhrswork,
            })
            
            lines_read += 1
            if lines_read % 500000 == 0:
                print(f"Processed {lines_read} lines...", flush=True)
        except (ValueError, IndexError):
            continue

df = pd.DataFrame(acs_data)

# ============================================================================
# 2. DEFINE SAMPLE SELECTION AND VARIABLES
# ============================================================================

# DACA Eligibility Criteria:
# - Mexican-born (BPL == 200)
# - Non-citizen (CITIZEN in {3, 4, 5}: 3=Not a citizen, 4=Not citizen but has first papers, 5=Foreign born status not reported)
# - Age: Must have been <16 when arriving before 6/15/2007 and <31 on 6/15/2012
#   Implies birth year 1981-1996, so age 16-31 in 2012
#   For our analysis years (2013-2016), we look at ages 17-35
# - Years: Focus on 2013-2016 for post-DACA period, 2006-2011 for pre-period

# Filter for Mexican-born, non-citizen
daca_sample = df[
    (df['bpl'] == 200) &  # Born in Mexico
    (df['citizen'].isin([3, 4, 5])) &  # Non-citizen or status not reported
    (df['age'] >= 16) &  # Age at least 16
    (df['age'] <= 35) &  # Age at most 35 (reasonable upper bound for eligible cohorts)
    (df['year'] >= 2006) &  # Years 2006-2016
    (df['year'] <= 2016) &
    (df['perwt'] > 0) &  # Valid weight
    (df['empstat'] > 0) &  # Valid employment status
    (df['statefip'] > 0)  # Valid state code
].copy()

# Create treatment indicator: post-DACA period (2013+)
daca_sample['post_daca'] = (daca_sample['year'] >= 2013).astype(int)

# Create outcome: Full-time employment (35+ hours per week)
# EMPSTAT: 1=Employed, 2=Unemployed, 3=Not in labor force
# UHRSWORK: usual hours worked per week (00-99)
daca_sample['fulltime_employed'] = (
    (daca_sample['empstat'] == 1) &  # Employed
    (daca_sample['uhrswork'] >= 35)  # 35+ hours per week
).astype(int)

# ============================================================================
# 3. VERIFY TREATMENT VARIATION
# ============================================================================

# Check if there's variation in the treatment and outcome
pre_fulltime = daca_sample[daca_sample['post_daca'] == 0]['fulltime_employed'].mean()
post_fulltime = daca_sample[daca_sample['post_daca'] == 1]['fulltime_employed'].mean()

if pre_fulltime == post_fulltime:
    # If no variation, we need to modify the sample or specification
    print(f"Warning: No variation in post-period effect (pre={pre_fulltime}, post={post_fulltime})", flush=True)

# ============================================================================
# 4. ESTIMATE TREATMENT EFFECT
# ============================================================================

# Prepare data for regression: WLS with person weights
# Model: outcome = b0 + b1*post_daca + b2*age + b3*post_daca*age + state_FE + year_FE + error

# Create state and year fixed effects
daca_sample['state_id'] = pd.factorize(daca_sample['statefip'])[0]
daca_sample['year_id'] = pd.factorize(daca_sample['year'])[0]

# Also create demeaned interaction terms for DiD
daca_sample['age_centered'] = daca_sample['age'] - daca_sample['age'].mean()
daca_sample['interaction'] = daca_sample['post_daca'] * daca_sample['age_centered']

# Drop any rows with missing values
daca_sample_clean = daca_sample.dropna(subset=['fulltime_employed', 'perwt', 'post_daca', 'age'])

# For computational efficiency, use a sample if data is very large
if len(daca_sample_clean) > 1000000:
    # Use stratified sampling to maintain treatment/control balance
    daca_sample_clean = daca_sample_clean.groupby('post_daca', group_keys=False).apply(
        lambda x: x.sample(n=min(500000, len(x)), weights='perwt', replace=True)
    ).reset_index(drop=True)

# Prepare design matrix for simple DiD model
# outcome = b0 + b1*post_daca + b2*age_centered + state_FE + year_FE

y = daca_sample_clean['fulltime_employed'].values.astype(float)
weights = daca_sample_clean['perwt'].values.astype(float)

# Normalize weights for WLS
weights = weights / weights.mean()

# Build design matrix with categorical variables
post_daca = daca_sample_clean['post_daca'].values.astype(float)
age_centered = daca_sample_clean['age_centered'].values.astype(float)
state_id = daca_sample_clean['state_id'].values.astype(int)
year_id = daca_sample_clean['year_id'].values.astype(int)

# Create dummy variables explicitly and ensure float type
n_states = state_id.max() + 1
n_years = year_id.max() + 1

# For memory efficiency, use one-hot encoding manually
state_dummies = np.zeros((len(state_id), n_states - 1), dtype=float)
year_dummies = np.zeros((len(year_id), n_years - 1), dtype=float)

for i in range(n_states - 1):
    state_dummies[:, i] = (state_id == i).astype(float)
    
for i in range(n_years - 1):
    year_dummies[:, i] = (year_id == i).astype(float)

# Build X matrix with explicit float type
X = np.column_stack([
    np.ones(len(y), dtype=float),
    post_daca,
    age_centered,
    state_dummies,
    year_dummies
]).astype(float)

# Scale by sqrt(weights) for memory-efficient WLS
sqrt_weights = np.sqrt(weights)
X_weighted = X * sqrt_weights[:, np.newaxis]
y_weighted = y * sqrt_weights

# Normal OLS on weighted data: (X'X)^-1 X'y
XtX = X_weighted.T @ X_weighted
Xty = X_weighted.T @ y_weighted

try:
    beta = np.linalg.solve(XtX, Xty)
except np.linalg.LinAlgError:
    # If singular, use pseudoinverse
    beta = np.linalg.pinv(XtX) @ Xty

# Calculate residuals and standard errors
y_pred = X @ beta
residuals = y - y_pred
rss = np.sum(weights * residuals**2)
df_residual = len(y) - X.shape[1]
sigma_sq = rss / df_residual
var_beta = sigma_sq * np.linalg.pinv(XtX).diagonal()
se_beta = np.sqrt(var_beta)

# Extract treatment coefficient (post_daca effect)
treatment_idx = 1  # Index of post_daca in design matrix
point_estimate = beta[treatment_idx]
se = se_beta[treatment_idx]

# ============================================================================
# 5. PREPARE SPECIFICATION AND RESULTS
# ============================================================================

sample_size = len(daca_sample_clean)

# Specification description
spec_dict = {
    "sample_selection": [
        "Country of birth: Mexico (BPL == 200)",
        "Citizenship status: Non-citizen (CITIZEN in [3, 4, 5])",
        "Age: 16-35 years old",
        "Valid person weight (perwt > 0)",
        "Valid employment status (empstat > 0)",
        "Years: 2006-2016"
    ],
    "outcome_definition": "(df['empstat'] == 1) & (df['uhrswork'] >= 35)",
    "treatment_definition": "post_daca = (year >= 2013)",
    "model_specification_line": "outcome = post_daca + age_centered + state_FE + year_FE, weighted by perwt"
}

results_dict = {
    "point_estimate": float(point_estimate),
    "standard_error": float(se),
    "sample_size": int(sample_size)
}

output_dict = {
    "spec": spec_dict,
    "results": results_dict
}

# ============================================================================
# 6. OUTPUT RESULTS
# ============================================================================

# Print only the JSON output to stdout
print(json.dumps(output_dict))

# Also save spec to file as required
with open('spec.json', 'w') as f:
    json.dump(spec_dict, f, indent=2)
