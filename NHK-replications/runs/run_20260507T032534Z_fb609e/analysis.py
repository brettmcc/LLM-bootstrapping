#!/usr/bin/env python3
"""
Phase 12 Analysis: DACA Impact on Full-Time Employment
Estimates the causal effect of DACA eligibility on full-time employment
among ethnically Hispanic-Mexican, Mexican-born people in the US.
"""

import json
import pandas as pd
import numpy as np
import struct
from statsmodels.regression.linear_model import WLS

# ============================================================================
# STEP 1: READ THE FIXED-WIDTH ACS DATA
# ============================================================================

# Fixed-width field specifications from ACS_extract_expanded_layout_excerpt.do
# Format: (name, start_col, end_col) - using 1-based indexing from Stata
acs_fields = {
    'year': (1, 4),
    'statefip': (66, 67),
    'age': (741, 743),
    'hispan': (764, 764),
    'bpl': (768, 770),
    'citizen': (790, 790),
    'empstat': (875, 875),
    'uhrswork': (905, 906),
    'perwt': (692, 701),
}

def read_acs_data(filename, fields):
    """
    Read fixed-width ACS data file.
    Convert 1-based Stata column numbers to 0-based Python slicing.
    """
    data_dict = {name: [] for name in fields}
    
    with open(filename, 'r', encoding='latin-1') as f:
        for line in f:
            for name, (start, end) in fields.items():
                # Convert 1-based Stata columns to 0-based Python slicing
                value_str = line[start-1:end].strip()
                try:
                    if name in ['age', 'hispan', 'bpl', 'citizen', 'empstat', 'uhrswork']:
                        value = int(value_str) if value_str else np.nan
                    elif name == 'perwt':
                        value = float(value_str) if value_str else np.nan
                    elif name == 'year':
                        value = int(value_str) if value_str else np.nan
                    else:
                        value = value_str
                    data_dict[name].append(value)
                except (ValueError, IndexError):
                    data_dict[name].append(np.nan)
    
    return pd.DataFrame(data_dict)

# Read ACS data
print("Reading ACS data...", flush=True)
df = read_acs_data('ACS_extract_expanded.dat', acs_fields)

# ============================================================================
# STEP 2: DEFINE DACA ELIGIBILITY AND TREATMENT VARIABLES
# ============================================================================

# DACA eligibility criteria:
# 1. Ethnically Hispanic-Mexican: hispan == 1
# 2. Mexican-born: bpl == 200
# 3. Arrived unlawfully before age 16
# 4. Not yet 31 by June 15, 2012: birth_year >= 1981 (so age <= 31 in 2012)
# 5. Lived continuously since June 15, 2007: can't verify directly from ACS
# 6. Present on June 15, 2012 without lawful status: citizen in [3, 4, 5]

# For birth year: age = year - birth_year (approximately)
# If person is age A in year Y, birth year is approximately Y - A
# For DACA eligibility: born >= 1981 (so by 2012, age <= 31)

df['birth_year_approx'] = df['year'] - df['age']

# Filter for sample selection:
# 1. Hispanic-Mexican ethnicity
sample1 = df['hispan'] == 1

# 2. Mexican-born
sample2 = df['bpl'] == 200

# 3. Not a citizen (includes non-citizens: 3, 4, 5)
sample3 = df['citizen'].isin([3, 4, 5])

# 4. DACA eligibility age requirements:
#    - Born before age 16: birth year <= year - 16, or age >= 16 in the current year
#    - Not yet 31 by June 2012: birth year >= 1981
#    This means: 16 <= age <= 31 in relevant years
sample4 = (df['age'] >= 16) & (df['age'] <= 31)

# 5. Treatment variable: daca_eligible = 1 if meets criteria
daca_eligible = (sample1 & sample2 & sample3 & sample4).astype(int)

# 6. Years of analysis: 2013-2016 (post-DACA)
#    Treatment = year >= 2013
treatment_year = (df['year'] >= 2013).astype(int)

# Outcome: Full-time employment
# Employed (empstat == 1) AND working >= 35 hours per week (uhrswork >= 35)
fulltime_employed = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

# Apply sample selection
eligible_sample = daca_eligible == 1
analysis_df = df[eligible_sample].copy()
analysis_df['treatment'] = treatment_year[eligible_sample]
analysis_df['outcome'] = fulltime_employed[eligible_sample]
analysis_df['weight'] = analysis_df['perwt'] / 100  # ACS weights are scaled by 100

# ============================================================================
# STEP 3: CHECK FOR VARIATION IN TREATMENT AND OUTCOME
# ============================================================================

print(f"Sample size: {len(analysis_df)}", flush=True)
print(f"Treatment variation: {analysis_df['treatment'].nunique()} values", flush=True)
print(f"Outcome variation: {analysis_df['outcome'].nunique()} values", flush=True)
print(f"Treatment distribution:\n{analysis_df['treatment'].value_counts()}", flush=True)
print(f"Outcome distribution:\n{analysis_df['outcome'].value_counts()}", flush=True)

# Check for variation
has_treatment_variation = analysis_df['treatment'].nunique() > 1
has_outcome_variation = analysis_df['outcome'].nunique() > 1

if not (has_treatment_variation and has_outcome_variation):
    print("WARNING: Insufficient variation in treatment or outcome", flush=True)

# ============================================================================
# STEP 4: ESTIMATE TREATMENT EFFECT
# ============================================================================

# Specification: Linear probability model with weights
# outcome = beta_0 + beta_1*treatment + epsilon
# Using weighted least squares with ACS person weights

# Prepare data for WLS estimation
X = analysis_df[['treatment']].copy()
X['const'] = 1
X = X[['const', 'treatment']]  # Reorder for readability
y = analysis_df['outcome']
weights = analysis_df['weight']

# Fit WLS model
model = WLS(y, X, weights=weights)
results = model.fit()

# Extract results
point_estimate = results.params['treatment']
standard_error = results.bse['treatment']
sample_size = len(analysis_df)

# ============================================================================
# STEP 5: OUTPUT RESULTS
# ============================================================================

output = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

print(json.dumps(output))
