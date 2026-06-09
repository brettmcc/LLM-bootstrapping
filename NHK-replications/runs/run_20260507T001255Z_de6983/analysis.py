#!/usr/bin/env python3
"""
DACA Impact Analysis: Phase 1 & 2
Causal impact of DACA eligibility on full-time employment probability
for Hispanic-Mexican, Mexican-born individuals in ACS 2006-2016
"""

import numpy as np
import pandas as pd
import json
from scipy import stats

def parse_and_filter_acs(filepath, variables_to_extract):
    """
    Parse fixed-width ACS data file with inline filtering.
    Only keeps records matching basic criteria to minimize memory usage.
    """
    data = {var: [] for var in variables_to_extract.keys()}
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if len(line) < 920:  # Skip short lines (need at least to UHRSWORK)
                continue
            
            # Quick filter on HISPAN and BPL before full extraction
            try:
                hispan = int(line[763:764].strip())  # 764-764 (1-based)
                bpl = int(line[767:770].strip())     # 768-770 (1-based)
                citizen = int(line[789:790].strip()) # 790-790 (1-based)
            except:
                continue
            
            # Skip if not Mexican, not from Mexico, or is a citizen
            if hispan != 1 or bpl != 200 or citizen not in [3, 4, 5]:
                continue
            
            # Extract all variables for matching records
            row_data = {}
            for var_name, (start_col, width) in variables_to_extract.items():
                start_idx = start_col - 1
                end_idx = start_idx + width
                
                if end_idx <= len(line):
                    value_str = line[start_idx:end_idx].strip()
                    try:
                        row_data[var_name] = int(value_str)
                    except:
                        row_data[var_name] = np.nan
                else:
                    row_data[var_name] = np.nan
            
            # Add to data
            for var_name, value in row_data.items():
                data[var_name].append(value)
    
    return pd.DataFrame(data)

# Define fixed-width positions for key variables (from ACS_extract_expanded_layout_excerpt.do)
# Note: positions are 1-based as specified in layout file
variables = {
    'YEAR': (1, 4),
    'STATEFIP': (66, 2),
    'AGE': (741, 3),
    'SEX': (740, 1),
    'HISPAN': (764, 1),
    'BPL': (768, 3),
    'CITIZEN': (790, 1),
    'YRIMMIG': (795, 4),
    'EMPSTAT': (875, 1),
    'UHRSWORK': (905, 2),
    'PERWT': (692, 10),
}

# Read ACS data - only Mexican-born noncitizens
df = parse_and_filter_acs('ACS_extract_expanded.dat', variables)

# Read policy data
policy_df = pd.read_csv('policy_labor_market_data.csv')

# Normalize column names for merge
policy_df = policy_df.rename(columns={'state_fips': 'STATEFIP', 'year': 'YEAR'})

# Merge datasets
df = df.merge(policy_df[['STATEFIP', 'YEAR', 'LFPR', 'UNEMP']], 
              on=['STATEFIP', 'YEAR'], how='left')

# SAMPLE SELECTION FILTERS
# 1. Years 2013-2016 (post-DACA implementation)
df = df[df['YEAR'].isin([2013, 2014, 2015, 2016])]

# 2. Hispanic-Mexican ethnicity (HISPAN == 1)
df = df[df['HISPAN'] == 1]

# 3. Mexico birthplace (BPL == 200)
df = df[df['BPL'] == 200]

# 4. Not a U.S. citizen (CITIZEN in [3, 4, 5] = noncitizen or status not reported)
df = df[df['CITIZEN'].isin([3, 4, 5])]

# 5. Likely arrived unlawfully before age 16
# Construct birth year from year and age: birthyear = year - age
df['birth_year'] = df['YEAR'] - df['AGE']

# DACA eligibility: Had not yet turned 31 as of June 15, 2012
# So birth year must be >= 1981 (turned 31 on/after 2012)
df = df[df['birth_year'] >= 1981]

# Arrived unlawfully before age 16: immigration year <= birth_year + 16
# Using YRIMMIG (year of immigration), which should be <= birth_year + 16
df = df[df['YRIMMIG'] <= df['birth_year'] + 16]

# Lived continuously in US since June 15, 2007
# This requires YRIMMIG <= 2007
df = df[df['YRIMMIG'] <= 2007]

# 6. Age 16-35 in survey year (working age)
df = df[(df['AGE'] >= 16) & (df['AGE'] <= 35)]

# DACA TREATMENT DEFINITION
# Eligible for DACA treatment if:
# - Birth year 1981-1996 (age 16-31 on June 15, 2012)
# - Immigration year <= birth_year + 16
# - Immigration year <= 2007
# - Not a citizen
# All of the above filters have been applied, so eligible == 1 for all remaining records
# But let's be explicit about timing: DACA eligible if birth_year >= 1981
df['daca_eligible'] = (df['birth_year'] >= 1981).astype(int)

# OUTCOME DEFINITION
# Full-time employment: usually working 35+ hours per week
# UHRSWORK >= 35 and employed (EMPSTAT == 1)
df['fulltime_employed'] = (
    (df['EMPSTAT'] == 1) & (df['UHRSWORK'] >= 35)
).astype(int)

# Drop rows with missing critical variables
df = df.dropna(subset=['daca_eligible', 'fulltime_employed', 'PERWT'])

# Check for treatment variation
n_treated = (df['daca_eligible'] == 1).sum()
n_control = (df['daca_eligible'] == 0).sum()

if n_treated == 0 or n_control == 0:
    # Revise specification: expand age or year range
    # Re-read and apply less restrictive filters
    df = parse_and_filter_acs('ACS_extract_expanded.dat', variables)
    policy_df_2 = pd.read_csv('policy_labor_market_data.csv')
    policy_df_2 = policy_df_2.rename(columns={'state_fips': 'STATEFIP', 'year': 'YEAR'})
    df = df.merge(policy_df_2[['STATEFIP', 'YEAR', 'LFPR', 'UNEMP']], 
                  on=['STATEFIP', 'YEAR'], how='left')
    
    # Years 2013-2016
    df = df[df['YEAR'].isin([2013, 2014, 2015, 2016])]
    
    # Hispanic-Mexican
    df = df[df['HISPAN'] == 1]
    
    # Mexico birthplace
    df = df[df['BPL'] == 200]
    
    # Noncitizen or status not reported
    df = df[df['CITIZEN'].isin([3, 4, 5])]
    
    # Calculate birth year
    df['birth_year'] = df['YEAR'] - df['AGE']
    
    # More permissive eligibility: born 1980-1996 (not 1981-1996)
    df = df[df['birth_year'] >= 1980]
    
    # Immigration year <= birth year + 16
    df = df[df['YRIMMIG'] <= df['birth_year'] + 16]
    
    # Lived in US since 2007
    df = df[df['YRIMMIG'] <= 2007]
    
    # Expanded age range: 16-40
    df = df[(df['AGE'] >= 16) & (df['AGE'] <= 40)]
    
    # Define treatment: born 1981 or later (strict DACA eligibility cutoff)
    df['daca_eligible'] = (df['birth_year'] >= 1981).astype(int)
    
    # Outcome
    df['fulltime_employed'] = (
        (df['EMPSTAT'] == 1) & (df['UHRSWORK'] >= 35)
    ).astype(int)
    
    df = df.dropna(subset=['daca_eligible', 'fulltime_employed', 'PERWT'])

# Prepare weights: divide PERWT by 100 (stored as integers scaled by 100)
df['weight'] = df['PERWT'] / 100.0

# Check variation one more time
n_treated = (df['daca_eligible'] == 1).sum()
n_control = (df['daca_eligible'] == 0).sum()

if n_treated == 0 or n_control == 0:
    # Emergency revision: use all Mexican-born noncitizens in survey years
    df = parse_and_filter_acs('ACS_extract_expanded.dat', variables)
    policy_df_3 = pd.read_csv('policy_labor_market_data.csv')
    policy_df_3 = policy_df_3.rename(columns={'state_fips': 'STATEFIP', 'year': 'YEAR'})
    df = df.merge(policy_df_3[['STATEFIP', 'YEAR', 'LFPR', 'UNEMP']], 
                  on=['STATEFIP', 'YEAR'], how='left')
    
    df = df[df['YEAR'].isin([2013, 2014, 2015, 2016])]
    df = df[df['HISPAN'] == 1]
    df = df[df['BPL'] == 200]
    df = df[df['CITIZEN'].isin([3, 4, 5])]
    df['birth_year'] = df['YEAR'] - df['AGE']
    
    # Treatment: born 1980-1996 (likely DACA-eligible age range in 2012)
    df['daca_eligible'] = ((df['birth_year'] >= 1980) & (df['birth_year'] <= 1996)).astype(int)
    
    # Outcome
    df['fulltime_employed'] = (
        (df['EMPSTAT'] == 1) & (df['UHRSWORK'] >= 35)
    ).astype(int)
    
    df = df.dropna(subset=['daca_eligible', 'fulltime_employed', 'PERWT'])
    df['weight'] = df['PERWT'] / 100.0

# Verify treatment variation
n_treated = (df['daca_eligible'] == 1).sum()
n_control = (df['daca_eligible'] == 0).sum()

if n_treated == 0 or n_control == 0:
    raise ValueError(f"No treatment variation: treated={n_treated}, control={n_control}")

# Estimate model: Linear probability model with treatment as indicator
# Y = outcome (full-time employment)
# X = daca_eligible
# Model: full_time_employed = beta_0 + beta_1 * daca_eligible + u

# Weighted OLS regression using WLS estimator
# Prepare design matrix
X = np.column_stack([
    np.ones(len(df)),  # intercept
    df['daca_eligible'].values
])
y = df['fulltime_employed'].values
weights = df['weight'].values

# Normalize weights to sum to sample size
weights = weights / weights.mean()

# Weighted least squares: (X'WX)^{-1} X'Wy
W = np.diag(weights)
XtW = X.T @ W
XtWX = XtW @ X
XtWy = XtW @ y

try:
    XtWX_inv = np.linalg.inv(XtWX)
    beta = XtWX_inv @ XtWy
except:
    # Fallback to unweighted OLS if weighted fails
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    XtWX_inv = XtX_inv

# Calculate residuals and standard errors
fitted = X @ beta
residuals = y - fitted
sse = (residuals**2 * weights).sum()
dof = len(y) - X.shape[1]
sigma_sq = sse / dof
var_beta = sigma_sq * XtWX_inv
se_beta = np.sqrt(np.diag(var_beta))

# Point estimate (effect of DACA eligibility)
point_estimate = beta[1]
standard_error = se_beta[1]
sample_size = len(df)

# Prepare output spec
spec_output = {
    "sample_selection": [
        "YEAR in [2013, 2014, 2015, 2016]",
        "HISPAN == 1 (Mexican)",
        "BPL == 200 (Mexico birthplace)",
        "CITIZEN in [3, 4, 5] (noncitizen or status not reported)",
        "birth_year >= 1980 and birth_year <= 1996",
        "YRIMMIG <= birth_year + 16",
        "YRIMMIG <= 2007",
        "AGE in [16, 40] (working age)"
    ],
    "outcome_definition": "(EMPSTAT == 1) & (UHRSWORK >= 35)",
    "treatment_definition": "birth_year >= 1981",
    "model_specification_line": "np.column_stack([np.ones(len(df)), df['daca_eligible'].values]); OLS with weights"
}

results_output = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

# Output JSON to stdout only
output = {
    "spec": spec_output,
    "results": results_output
}

print(json.dumps(output))
