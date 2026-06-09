#!/usr/bin/env python3
"""
DACA Impact Analysis: Full-Time Employment for Mexican-Born Immigrants
Analyze the causal impact of DACA eligibility on full-time employment probability.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path

# Define working directory (current directory where the script is run)
work_dir = Path.cwd()

print("Loading ACS data...", flush=True)

# Column specifications using pandas read_fwf (1-based positions, needs to be 0-based for colspecs)
# From ACS_extract_expanded_layout_excerpt.do:
# year        1-4
# age         741-743
# hispan      764-764
# bpl         768-770
# citizen     790-790
# yrimmig     795-798
# perwt       692-701
# empstat     875-875
# uhrswork    905-906

# For pandas read_fwf, positions are 0-based (subtract 1 from Stata's 1-based positions)
colspecs = [
    (0, 4),       # year (1-4 in Stata = 0-3 in Python, but 0-4 for up to position 4)
    (740, 743),   # age (741-743)
    (763, 764),   # hispan (764)
    (767, 770),   # bpl (768-770)
    (789, 790),   # citizen (790)
    (794, 798),   # yrimmig (795-798)
    (691, 701),   # perwt (692-701)
    (874, 875),   # empstat (875)
    (904, 906),   # uhrswork (905-906)
]

colnames = ['year', 'age', 'hispan', 'bpl', 'citizen', 'yrimmig', 'perwt', 'empstat', 'uhrswork']

# Read the fixed-width file using pandas with chunking
chunk_size = 50000  # Process 50k records at a time
chunks = []

try:
    reader = pd.read_fwf(
        work_dir / 'ACS_extract_expanded.dat',
        colspecs=colspecs,
        names=colnames,
        header=None,
        dtype={
            'year': 'int32',
            'age': 'int32',
            'hispan': 'int32',
            'bpl': 'int32',
            'citizen': 'int32',
            'yrimmig': 'int32',
            'perwt': 'float64',
            'empstat': 'int32',
            'uhrswork': 'int32',
        },
        chunksize=chunk_size
    )
    
    # Process chunks
    records_processed = 0
    for chunk_idx, chunk in enumerate(reader):
        records_processed += len(chunk)
        if (chunk_idx + 1) % 10 == 0:
            print(f"  Processed {records_processed} records...", flush=True)
        
        # Apply initial filters to reduce memory
        chunk = chunk[
            (chunk['year'].between(2006, 2016)) &
            (chunk['age'].between(18, 35)) &
            (chunk['empstat'] > 0) &
            (chunk['yrimmig'] > 0) &
            (chunk['yrimmig'] <= chunk['year'])
        ].copy()
        
        if len(chunk) > 0:
            chunks.append(chunk)
    
    # Concatenate all chunks
    df = pd.concat(chunks, ignore_index=True)
    print(f"Data loaded: {len(df)} records", flush=True)
    
except Exception as e:
    print(f"ERROR reading data: {str(e)}", flush=True)
    import traceback
    traceback.print_exc()
    import sys
    sys.exit(1)

if len(df) == 0:
    print("ERROR: No records loaded from file!", flush=True)
    import sys
    sys.exit(1)

# Apply sample selection
print("Applying sample selection...", flush=True)

# Create birth year from survey year and age
df['birth_year'] = df['year'] - df['age']

# DACA eligibility criteria
df['is_mexican'] = ((df['hispan'] == 1) | (df['bpl'] == 200)).astype(int)
df['is_noncitizen'] = df['citizen'].isin([3, 4, 5]).astype(int)
df['age_at_immigration'] = df['yrimmig'] - df['birth_year']
df['arrived_before_age_16'] = (df['age_at_immigration'] < 16).astype(int)
df['arrived_by_2007'] = (df['yrimmig'] <= 2007).astype(int)
df['age_on_june_2012'] = 2012 - df['birth_year']
df['eligible_age_2012'] = ((df['age_on_june_2012'] >= 0) & (df['age_on_june_2012'] <= 30)).astype(int)

# DACA eligibility flag (all conditions must be met)
df['daca_eligible'] = (
    (df['is_mexican'] == 1) &
    (df['is_noncitizen'] == 1) &
    (df['arrived_by_2007'] == 1) &
    (df['arrived_before_age_16'] == 1) &
    (df['eligible_age_2012'] == 1)
).astype(int)

print(f"DACA-eligible records: {df['daca_eligible'].sum()}", flush=True)

# Apply the sample selection: DACA-eligible individuals
df = df[df['daca_eligible'] == 1].copy()

print(f"Sample size after selection: {len(df)}", flush=True)

if len(df) == 0:
    print("ERROR: No records match the sample selection criteria!", flush=True)
    import sys
    sys.exit(1)

# Check for variation in treatment
print("Checking treatment variation...", flush=True)

# Create outcome variable: full-time employment (empstat == 1 AND uhrswork >= 35)
df['full_time_employed'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

# Create post-DACA indicator
df['post_daca'] = (df['year'] >= 2013).astype(int)

# Check for variation in key variables
print(f"Full-time employment rate: {df['full_time_employed'].mean():.4f}", flush=True)
print(f"Post-DACA period share: {df['post_daca'].mean():.4f}", flush=True)

# Check variation
if df['post_daca'].std() == 0:
    print("ERROR: No variation in post_daca treatment variable!", flush=True)
    import sys
    sys.exit(1)

# Normalize person weights (divide by 100 as per ACS documentation)
df['perwt_normalized'] = df['perwt'] / 100.0

# Create outcome and treatment variables
outcome = df['full_time_employed'].values
treatment = df['post_daca'].values
weights = df['perwt_normalized'].values

# Weighted OLS regression: full_time_employed ~ post_daca + constant
X = np.column_stack([np.ones(len(df)), treatment])

# Weighted least squares: WLS minimizes sum of (w_i * (y_i - x_i'*b)^2)
# This is equivalent to OLS on weighted variables
try:
    # Transform for weighted least squares
    sqrt_weights = np.sqrt(weights)
    weighted_X = X * sqrt_weights[:, np.newaxis]
    weighted_y = outcome * sqrt_weights
    
    # Calculate OLS on weighted variables: beta = (X'X)^{-1} X'y
    XtX = weighted_X.T @ weighted_X
    Xty = weighted_X.T @ weighted_y
    
    # Solve for coefficients
    beta = np.linalg.solve(XtX, Xty)
    
    # Calculate residuals
    residuals = outcome - X @ beta
    
    # Calculate standard errors
    n = len(df)
    k = X.shape[1]  # number of parameters
    
    # For WLS, sigma^2 estimate is sum of (w_i * e_i^2) / (n - k)
    weighted_residuals_sq = weights * (residuals ** 2)
    sigma_squared = weighted_residuals_sq.sum() / (n - k)
    
    # Variance-covariance matrix: sigma^2 * (X'WX)^{-1}
    XtWX = weighted_X.T @ weighted_X
    var_covar = sigma_squared * np.linalg.inv(XtWX)
    se = np.sqrt(np.diag(var_covar))
    
    # Extract results
    point_estimate = float(beta[1])  # Coefficient on post_daca
    standard_error = float(se[1])
    sample_size = int(len(df))
    
    print(f"Point estimate: {point_estimate:.6f}", flush=True)
    print(f"Standard error: {standard_error:.6f}", flush=True)
    print(f"Sample size: {sample_size}", flush=True)
    
except Exception as e:
    print(f"ERROR: Regression failed: {str(e)}", flush=True)
    import traceback
    traceback.print_exc()
    import sys
    sys.exit(1)

# Output specification JSON
spec = {
    "sample_selection": [
        "hispan == 1 OR bpl == 200",
        "citizen IN [3, 4, 5]",
        "yrimmig <= 2007",
        "yrimmig - (year - age) < 16",
        "2012 - (year - age) >= 0 AND 2012 - (year - age) <= 30",
        "year BETWEEN 2006 AND 2016",
        "age BETWEEN 18 AND 35",
        "empstat > 0",
        "yrimmig > 0 AND yrimmig <= year"
    ],
    "outcome_definition": "empstat == 1 AND uhrswork >= 35",
    "treatment_definition": "year >= 2013",
    "model_specification_line": "WLS(full_time_employed, [1, post_daca], weights=perwt/100)"
}

# Save spec.json
spec_path = work_dir / 'spec.json'
with open(spec_path, 'w') as f:
    json.dump(spec, f, indent=2)

print(f"Specification saved to {spec_path}", flush=True)

# Output results JSON only (as required by prompt)
results = {
    "spec": spec,
    "results": {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size
    }
}

print(json.dumps(results))
