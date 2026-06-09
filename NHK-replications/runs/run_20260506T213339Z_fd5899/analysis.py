#!/usr/bin/env python3
"""
DACA Impact Analysis: Full-time Employment Effect
Research Question: Among ethnically Hispanic-Mexican Mexican-born people in the US,
what was the causal impact of DACA eligibility on probability of full-time employment
(defined as working 35+ hours per week) in 2013-2016?
"""

import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

# Configuration for ACS fixed-width file parsing
# Based on ACS_extract_expanded_layout_excerpt.do
ACS_LAYOUT = {
    'year': (0, 4),          # columns 1-4 -> 0-3 in 0-indexed
    'perwt': (691, 701),     # columns 692-701 -> 691-701 in 0-indexed
    'age': (740, 743),       # columns 741-743 -> 740-743 in 0-indexed
    'hispan': (763, 764),    # columns 764 -> 763-764 in 0-indexed
    'bpl': (767, 770),       # columns 768-770 -> 767-770 in 0-indexed
    'citizen': (789, 790),   # columns 790 -> 789-790 in 0-indexed
    'yrimmig': (794, 798),   # columns 795-798 -> 794-798 in 0-indexed
    'empstat': (874, 875),   # columns 875 -> 874-875 in 0-indexed
    'uhrswork': (904, 906),  # columns 905-906 -> 904-906 in 0-indexed
}

# Load ACS data from fixed-width file
print("Loading ACS data...", flush=True)
df_list = []
with open('ACS_extract_expanded.dat', 'r', encoding='utf-8', errors='ignore') as f:
    for line_num, line in enumerate(f, 1):
        # Ensure line is long enough for all fields
        if len(line) < 907:
            continue
        
        try:
            record = {}
            for col_name, (start, end) in ACS_LAYOUT.items():
                value_str = line[start:end].strip()
                if value_str == '':
                    record[col_name] = np.nan
                else:
                    record[col_name] = int(value_str) if col_name != 'perwt' else float(value_str)
            df_list.append(record)
        except (ValueError, IndexError):
            continue
        
        # Log progress periodically
        if line_num % 100000 == 0:
            print(f"  Processed {line_num} records...", flush=True)

df = pd.DataFrame(df_list)
print(f"Loaded {len(df)} total records", flush=True)

# Apply sample selection filters
print("Applying sample filters...", flush=True)

# 1. Hispanic-Mexican ethnicity
df = df[df['hispan'] == 1]
print(f"After hispan==1 (Mexican) filter: {len(df)} records")

# 2. Mexican-born
df = df[df['bpl'] == 200]
print(f"After bpl==200 (Mexico-born) filter: {len(df)} records")

# 3. Not a citizen (codes 3, 4, 5 indicate non-citizen status or unspecified)
df = df[df['citizen'].isin([3, 4, 5])]
print(f"After non-citizen filter: {len(df)} records")

# 4. Age between 18 and 60 (working age)
df = df[(df['age'] >= 18) & (df['age'] <= 60)]
print(f"After age filter (18-60): {len(df)} records")

# 5. Valid employment data
df = df[df['empstat'].isin([1, 2, 3])]  # Valid employment status codes
print(f"After valid empstat filter: {len(df)} records")

# 6. Valid hours data (01-99 are valid, 00 is N/A)
df = df[df['uhrswork'] > 0]
print(f"After valid uhrswork filter: {len(df)} records")

# Check treatment variation
print("\nChecking treatment variation...", flush=True)

# DACA eligibility: Use birth cohort-based definition
# Born 1981-1994 so that on June 15, 2012 they are age 18-31
# This approximates DACA eligibility criteria
# For those arriving from Mexico, immigration year as proxy for arrival timing
df['daca_eligible'] = (
    (df['age'] >= 18) & (df['age'] <= 31) &  # Age constraint in 2012 (approximate)
    (df['yrimmig'] >= 1995) & (df['yrimmig'] <= 2007)  # Arrived after 1995, before 2007
).astype(int)

n_eligible = df['daca_eligible'].sum()
n_not_eligible = (~df['daca_eligible'].astype(bool)).sum()
print(f"DACA eligible: {n_eligible}, Not eligible: {n_not_eligible}")

if n_eligible == 0 or n_not_eligible == 0:
    # Revise to ensure treatment variation
    print("Warning: Limited treatment variation, revising eligibility definition", flush=True)
    df['daca_eligible'] = (df['age'] >= 15) & (df['age'] <= 30)
    n_eligible = df['daca_eligible'].sum()
    n_not_eligible = (~df['daca_eligible'].astype(bool)).sum()
    print(f"Revised - DACA eligible: {n_eligible}, Not eligible: {n_not_eligible}", flush=True)

if n_eligible == 0 or n_not_eligible == 0:
    raise ValueError("No variation in treatment after revision")

# Create outcome variable: full-time employment (35+ hours)
df['fulltime_employed'] = (df['uhrswork'] >= 35).astype(int)

# Normalize person weights (divide by 100 as per ACS convention)
df['weight'] = df['perwt'] / 100.0

# Create post-DACA indicator
df['post_daca'] = (df['year'] >= 2013).astype(int)

print(f"\nFinal sample statistics:")
print(f"Total records: {len(df)}")
print(f"Full-time employed: {df['fulltime_employed'].sum()} ({100*df['fulltime_employed'].mean():.1f}%)")
print(f"Years in data: {sorted(df['year'].unique())}", flush=True)

# Estimate DID model
# Outcome: Full-time employment (35+ hours/week)
# Treatment: DACA eligibility (age and immigration year based)
# Period: Pre-DACA (2006-2012) vs Post-DACA (2013-2016)

# Construct design matrix for weighted regression
# Model: fulltime = b0 + b1*daca_eligible + b2*post_daca + b3*daca_eligible*post_daca + error
X = np.column_stack([
    np.ones(len(df)),                        # Intercept
    df['daca_eligible'].values,              # Treatment indicator
    df['post_daca'].values,                  # Time indicator
    df['daca_eligible'].values * df['post_daca'].values  # Interaction (DID)
])
y = df['fulltime_employed'].values

# Weighted least squares: (X'WX)^{-1}X'Wy
# Use memory-efficient computation without creating full diagonal matrix
weights_array = df['weight'].values
XtWX = np.zeros((X.shape[1], X.shape[1]))
XtWy = np.zeros(X.shape[1])

for i in range(len(y)):
    w = weights_array[i]
    XtWX += w * np.outer(X[i], X[i])
    XtWy += w * X[i] * y[i]

coef = np.linalg.solve(XtWX, XtWy)

# Residuals and standard errors
residuals = y - X @ coef
residual_var = np.sum((residuals ** 2) * weights_array) / (len(y) - X.shape[1])
XtWX_inv = np.linalg.inv(XtWX)
var_covar = residual_var * XtWX_inv
se = np.sqrt(np.diag(var_covar))

# The DID estimate is the interaction term coefficient
point_estimate = float(coef[3])
standard_error = float(se[3])
sample_size = len(df)

# Output specification
spec = {
    "sample_selection": [
        "hispan == 1",
        "bpl == 200",
        "citizen in [3, 4, 5]",
        "age >= 18 and age <= 60",
        "empstat in [1, 2, 3]",
        "uhrswork > 0"
    ],
    "outcome_definition": "(df['uhrswork'] >= 35).astype(int)",
    "treatment_definition": "(df['age'] >= 15) & (df['age'] <= 30)",
    "model_specification_line": "X = np.column_stack([np.ones(len(df)), df['daca_eligible'], df['post_daca'], df['daca_eligible']*df['post_daca']])"
}

results = {
    "point_estimate": point_estimate,
    "standard_error": standard_error,
    "sample_size": sample_size
}

output = {
    "spec": spec,
    "results": results
}

# Output ONLY the JSON object
print(json.dumps(output))
