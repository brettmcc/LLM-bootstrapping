#!/usr/bin/env python3
"""
DACA Eligibility and Full-Time Employment Analysis
Estimates the effect of DACA eligibility on full-time employment for Hispanic-Mexican immigrants
"""

import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

# Fixed-width column specifications (1-based positions converted to 0-based)
column_specs = {
    'year': (0, 4),           # columns 1-4
    'perwt': (691, 701),      # columns 692-701
    'age': (740, 743),        # columns 741-743
    'hispan': (763, 764),     # columns 764-764
    'bpl': (767, 770),        # columns 768-770
    'citizen': (789, 790),    # columns 790-790
    'empstat': (874, 875),    # columns 875-875
    'uhrswork': (904, 906),   # columns 905-906
}

# Read fixed-width file in chunks to manage memory efficiently
df_list = []
chunk_size = 100000
try:
    for chunk in pd.read_fwf('ACS_extract_expanded.dat', 
                              colspecs=list(column_specs.values()), 
                              names=list(column_specs.keys()), 
                              header=None,
                              chunksize=chunk_size):
        df_list.append(chunk)
    df = pd.concat(df_list, ignore_index=True)
except Exception as e:
    # If read_fwf fails, try alternative approach
    with open('ACS_extract_expanded.dat', 'r') as f:
        rows = []
        for line in f:
            row = {}
            for col_name, (start, end) in column_specs.items():
                try:
                    row[col_name] = line[start:end].strip()
                except:
                    row[col_name] = None
            rows.append(row)
    df = pd.DataFrame(rows)

# Convert to numeric types
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Sample Selection Filters:
# 1. Ethnically Hispanic-Mexican (hispan == 1)
# 2. Mexico-born (bpl == 200)
# 3. Non-citizen (citizen in [3, 4, 5]: not a citizen, received first papers, or status not reported)
# 4. Survey years 2013-2016 (when DACA effects would be observable)
sample_df = df[
    (df['hispan'] == 1) &
    (df['bpl'] == 200) &
    (df['citizen'].isin([3, 4, 5])) &
    (df['year'].isin([2013, 2014, 2015, 2016]))
].copy()

# Outcome: Full-time employment defined as employed AND usually working 35+ hours per week
# empstat: 1=Employed, 2=Unemployed, 3=Not in labor force
# uhrswork: usual hours worked per week
sample_df['outcome_fulltime'] = (
    (sample_df['empstat'] == 1) & 
    (sample_df['uhrswork'] >= 35)
).astype(int)

# Treatment: DACA Eligibility
# DACA eligibility criteria (as of June 15, 2012):
# - Had not yet had their 31st birthday as of June 15, 2012 (born after June 15, 1981)
# - Would arrive unlawfully before their 16th birthday (born before June 15, 1996)
# Combined: born between June 16, 1981 and June 15, 1996
# We approximate birth year as: survey_year - age
sample_df['birth_year_approx'] = sample_df['year'] - sample_df['age']
sample_df['treatment_daca_eligible'] = (
    (sample_df['birth_year_approx'] >= 1981) & 
    (sample_df['birth_year_approx'] <= 1996)
).astype(int)

# Drop rows with missing values in key variables
sample_df = sample_df.dropna(subset=[
    'age', 'hispan', 'bpl', 'citizen', 'empstat', 'uhrswork', 
    'perwt', 'outcome_fulltime', 'treatment_daca_eligible'
])

# Verify treatment variation
n_treated = (sample_df['treatment_daca_eligible'] == 1).sum()
n_control = (sample_df['treatment_daca_eligible'] == 0).sum()

if n_treated == 0 or n_control == 0:
    raise ValueError("Treatment has no variation in the sample")

# Sample size
sample_size = len(sample_df)

# Estimation: Weighted difference-in-means (difference in proportions)
# Using person weights (perwt) - note that perwt is already divided by 100 per the Stata code
treated = sample_df[sample_df['treatment_daca_eligible'] == 1]
control = sample_df[sample_df['treatment_daca_eligible'] == 0]

# Calculate weighted means for outcome
treated_outcome_sum = (treated['outcome_fulltime'] * treated['perwt']).sum()
treated_weight_sum = treated['perwt'].sum()
treated_mean = treated_outcome_sum / treated_weight_sum

control_outcome_sum = (control['outcome_fulltime'] * control['perwt']).sum()
control_weight_sum = control['perwt'].sum()
control_mean = control_outcome_sum / control_weight_sum

# Point estimate: difference in weighted means
point_estimate = treated_mean - control_mean

# Standard error calculation for weighted difference-in-means
# Var(Y) = E[w^2 * (y - E[y])^2] / (sum(w))^2
treated_resid_sq = (treated['outcome_fulltime'] - treated_mean) ** 2
control_resid_sq = (control['outcome_fulltime'] - control_mean) ** 2

treated_var_weighted = (treated['perwt'] ** 2 * treated_resid_sq).sum() / (treated_weight_sum ** 2)
control_var_weighted = (control['perwt'] ** 2 * control_resid_sq).sum() / (control_weight_sum ** 2)

standard_error = np.sqrt(treated_var_weighted + control_var_weighted)

# Prepare output JSON
output_json = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

# Print ONLY the JSON object
print(json.dumps(output_json))
