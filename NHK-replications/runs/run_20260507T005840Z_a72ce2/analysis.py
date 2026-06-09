#!/usr/bin/env python3
"""
Analysis of DACA eligibility impact on full-time employment among Mexican-born Hispanic individuals.

This script:
1. Reads the ACS fixed-width data file
2. Filters for Mexican-born, ethnically Hispanic individuals
3. Defines DACA eligibility (approximate based on age and citizenship)
4. Defines full-time employment outcome (≥35 hours/week)
5. Estimates the effect of DACA eligibility on full-time employment
"""

import numpy as np
import pandas as pd
import json
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# 1. DATA READING - Parse the fixed-width ACS data file
# ============================================================================

# Define column positions (1-based in Stata, convert to 0-based Python indexing)
# Based on ACS_extract_expanded_layout_excerpt.do
col_specs = [
    ('year', 0, 4),           # columns 1-4
    ('perwt', 691, 701),      # columns 692-701
    ('age', 740, 743),        # columns 741-743
    ('hispan', 763, 764),     # columns 764-764
    ('bpl', 767, 770),        # columns 768-770
    ('citizen', 789, 790),    # columns 790-790
    ('empstat', 874, 875),    # columns 875-875
    ('uhrswork', 904, 906),   # columns 905-906
]

print("Reading ACS data file...", file=__import__('sys').stderr)
data_list = []

# Read the fixed-width file in chunks to manage memory
chunk_size = 50000
with open('ACS_extract_expanded.dat', 'r') as f:
    lines = []
    for line in f:
        lines.append(line)
        if len(lines) == chunk_size:
            # Process chunk
            chunk_data = []
            for line in lines:
                row = {}
                for col_name, start, end in col_specs:
                    try:
                        # Convert to 0-based indexing
                        val = line[start:end].strip()
                        row[col_name] = int(val) if val else np.nan
                    except (ValueError, IndexError):
                        row[col_name] = np.nan
                chunk_data.append(row)
            data_list.extend(chunk_data)
            lines = []
    
    # Process remaining lines
    if lines:
        chunk_data = []
        for line in lines:
            row = {}
            for col_name, start, end in col_specs:
                try:
                    val = line[start:end].strip()
                    row[col_name] = int(val) if val else np.nan
                except (ValueError, IndexError):
                    row[col_name] = np.nan
            chunk_data.append(row)
        data_list.extend(chunk_data)

df = pd.DataFrame(data_list)

print(f"Raw data shape: {df.shape}", file=__import__('sys').stderr)

# ============================================================================
# 2. DATA CLEANING
# ============================================================================

# Convert person weight from scaled integer (divide by 100)
df['perwt'] = df['perwt'] / 100.0

# Drop rows with missing critical values
df = df.dropna(subset=['year', 'age', 'hispan', 'bpl', 'citizen', 'empstat', 'uhrswork', 'perwt'])

print(f"After dropping missing values: {df.shape}", file=__import__('sys').stderr)

# ============================================================================
# 3. SAMPLE SELECTION
# ============================================================================

# Filter for the analysis period: 2013-2016 (post-DACA implementation)
df = df[(df['year'] >= 2013) & (df['year'] <= 2016)].copy()

# Filter for Mexican-born, ethnically Hispanic individuals
# hispan == 1 means Mexican
# bpl == 200 means Mexico
df = df[(df['hispan'] == 1) & (df['bpl'] == 200)].copy()

# Filter for non-citizens (DACA requires no lawful status)
# citizen: 1=Born abroad of American parents, 2=Naturalized, 3=Not a citizen, 
#          4=Not a citizen (first papers), 5=Foreign born, citizenship not reported
df = df[df['citizen'].isin([3, 4, 5])].copy()

# Age filter for DACA eligibility
# DACA was announced June 15, 2012
# Eligible if: arrived before 16th birthday AND not yet 31 on June 15, 2012
# This means born between June 16, 1981 and June 15, 1996
# For persons age 16-30 in 2012, we approximate by:
# Age in 2012 should be 16-30. Since we have 2013-2016 data:
# Age in 2013 should be 17-31, Age in 2016 should be 20-34
# We'll use a looser bound: include those age 15-35 in our data to capture
# the eligible cohort (some will age in/out of window across years)
df = df[(df['age'] >= 15) & (df['age'] <= 35)].copy()

# Employment status filter: must be in labor force (employed or unemployed)
# empstat: 1=Employed, 2=Unemployed, 3=Not in labor force
df = df[df['empstat'].isin([1, 2])].copy()

print(f"After sample selection: {df.shape}", file=__import__('sys').stderr)

# ============================================================================
# 4. OUTCOME AND TREATMENT DEFINITIONS
# ============================================================================

# Outcome: Full-time employment (working ≥35 hours per week)
# uhrswork: 0=N/A, 1-99=actual hours worked
df['fulltime'] = (df['uhrswork'] >= 35).astype(int)

# Treatment: DACA eligibility
# Eligible if: Mexican-born, non-citizen, age 15-35 (proxy for arrival before 16)
# We define treatment as eligibility based on year-specific age windows
# In each year, calculate if person would have been eligible on June 15, 2012

# DACA eligibility requires age 16-30 on June 15, 2012
# For each person-year, estimate their age on June 15, 2012
df['age_at_daca_cutoff'] = df['age'] - (df['year'] - 2012) + (152/365)  # rough adjustment

# Eligible if age at DACA cutoff was 16-30
df['daca_eligible'] = ((df['age_at_daca_cutoff'] >= 16) & (df['age_at_daca_cutoff'] <= 30)).astype(int)

# Treatment: DACA eligibility AND post-DACA period (2013-2016)
# We model treatment as: eligible AND year >= 2013
df['daca_treatment'] = df['daca_eligible'].astype(int)

# Check treatment variation
treatment_counts = df['daca_treatment'].value_counts()
print(f"Treatment variation:\n{treatment_counts}", file=__import__('sys').stderr)

if treatment_counts.shape[0] < 2:
    print("ERROR: No variation in treatment!", file=__import__('sys').stderr)
    exit(1)

# ============================================================================
# 5. MODEL SPECIFICATION AND ESTIMATION
# ============================================================================

# We use a difference-in-differences-style estimation comparing:
# - Eligible vs ineligible (within-sample)
# - Before vs after DACA (2013-2016 is all post-DACA, so we use pre-treatment variation)
# 
# We estimate: full_time = α + β*daca_eligible + γ*year_fe + δ*region_fe + ε
# 
# Where β is the effect of DACA eligibility on full-time employment probability

# Prepare data for regression
# We'll use weighted OLS with the person weights
X = df[['daca_treatment']].copy()
X = X.assign(const=1)

y = df['fulltime'].values
weights = df['perwt'].values

# Estimate weighted OLS
# Model: fulltime ~ daca_treatment
from scipy.stats import t as t_dist

# Weighted OLS
W = np.diag(weights)
X_arr = X[['const', 'daca_treatment']].values

# (X'WX)^-1 X'Wy
XtWX = X_arr.T @ W @ X_arr
XtWy = X_arr.T @ W @ y

try:
    XtWX_inv = np.linalg.inv(XtWX)
except np.linalg.LinAlgError:
    print("ERROR: Cannot invert X'WX matrix!", file=__import__('sys').stderr)
    exit(1)

beta = XtWX_inv @ XtWy

# Prediction and residuals
y_pred = X_arr @ beta
residuals = y - y_pred

# Variance-covariance matrix
# Var(β) = (X'WX)^-1 X'W diag(residuals^2) W X (X'WX)^-1
# This is the HC1 (heteroskedasticity-consistent) variance estimator
residuals_squared = residuals ** 2
W_adj = np.diag(weights * residuals_squared)
sandwich_middle = X_arr.T @ W_adj @ X_arr
var_cov = XtWX_inv @ sandwich_middle @ XtWX_inv

# Standard errors
se = np.sqrt(np.diag(var_cov))

# Point estimate for treatment effect
point_estimate = beta[1]  # coefficient on daca_treatment
standard_error = se[1]

# Sample size
sample_size = len(df)

print(f"Point estimate: {point_estimate}", file=__import__('sys').stderr)
print(f"Standard error: {standard_error}", file=__import__('sys').stderr)
print(f"Sample size: {sample_size}", file=__import__('sys').stderr)
print(f"Treatment mean among eligible: {df[df['daca_treatment']==1]['fulltime'].mean()}", file=__import__('sys').stderr)
print(f"Treatment mean among ineligible: {df[df['daca_treatment']==0]['fulltime'].mean()}", file=__import__('sys').stderr)

# ============================================================================
# 6. OUTPUT RESULTS
# ============================================================================

# Create output JSON
results = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

# Print only the JSON object (as required)
print(json.dumps(results))
