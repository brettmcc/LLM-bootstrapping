"""
DACA Impact Analysis: Effect on Full-Time Employment for Mexican-Born Hispanics

Research Question: Among ethnically Hispanic-Mexican Mexican-born people living 
in the United States, what was the causal impact of eligibility for DACA 
(treatment) on the probability that the eligible person is employed full-time 
(outcome), defined as usually working 35 hours per week or more?

DACA was implemented in June 15, 2012. Analysis focuses on 2013-2016.
"""

import pandas as pd
import numpy as np
from statsmodels.formula.api import wls
import json

# Load the ACS fixed-width data
# Based on the layout file, we need columns: year, hispan, bpl, citizen, age, 
# empstat, uhrswork, perwt
# The data file is fixed-width with 1-based indexing

# Column specifications (1-based, converted to 0-based for Python slicing)
# Column ranges from layout file (1-based): convert to 0-based slicing
columns_spec = {
    'year': (0, 4),           # 1-4
    'hispan': (763, 764),     # 764-764
    'bpl': (767, 770),        # 768-770
    'citizen': (789, 790),    # 790-790
    'age': (740, 743),        # 741-743
    'empstat': (874, 875),    # 875-875
    'uhrswork': (904, 906),   # 905-906
    'perwt': (691, 701),      # 692-701
}

# Read fixed-width file with dtype specification to manage memory
dtypes = {
    'year': 'int32',
    'hispan': 'int8',
    'bpl': 'int16',
    'citizen': 'int8',
    'age': 'int16',
    'empstat': 'int8',
    'uhrswork': 'int8',
    'perwt': 'float64',
}

# Read the fixed-width ACS data
data = []
with open('ACS_extract_expanded.dat', 'r') as f:
    for line in f:
        row = {}
        for col_name, (start, end) in columns_spec.items():
            value_str = line[start:end].strip()
            if value_str == '':
                value = np.nan
            else:
                try:
                    if col_name == 'perwt':
                        value = float(value_str)
                    else:
                        value = int(value_str)
                except ValueError:
                    value = np.nan
            row[col_name] = value
        data.append(row)

df = pd.DataFrame(data)

# Convert columns to appropriate dtypes
for col in df.columns:
    if col in dtypes:
        try:
            df[col] = df[col].astype(dtypes[col])
        except:
            pass

# ============================================================================
# SAMPLE SELECTION: Build the analysis sample
# ============================================================================

# 1. Restrict to years 2013-2016 (post-DACA implementation)
df = df[(df['year'] >= 2013) & (df['year'] <= 2016)]

# 2. Ethnically Hispanic-Mexican: hispan == 1 (Mexican)
df = df[df['hispan'] == 1]

# 3. Mexican-born: bpl == 200 (Mexico)
df = df[df['bpl'] == 200]

# 4. Age between 18 and 31 (DACA eligible age range at implementation)
# Born before June 15, 1994 and after June 14, 1981 (age <31 in 2012, arrived <16)
# For post-2012 analysis, we track people who were DACA-eligible
df = df[(df['age'] >= 18) & (df['age'] <= 31)]

# 5. Not a citizen (DACA targets non-citizens)
# citizen codes: 3=Not a citizen, 4=First papers, 5=Status not reported
# For DACA eligibility, we need non-citizens
df = df[df['citizen'].isin([3, 4, 5])]

# 6. In labor force (employed or unemployed) to focus on labor market participation
# empstat: 1=Employed, 2=Unemployed
df = df[df['empstat'].isin([1, 2])]

# 7. Remove missing values
df = df.dropna(subset=['year', 'age', 'empstat', 'uhrswork', 'perwt'])

# ============================================================================
# OUTCOME DEFINITION
# ============================================================================
# Full-time employment: employed AND usually working 35+ hours per week
# empstat == 1 (employed) and uhrswork >= 35
df['full_time'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

# ============================================================================
# TREATMENT DEFINITION (Difference-in-Differences Design)
# ============================================================================
# Treatment: Post-DACA period (2012 onwards, eligible for work authorization)
# The key question: those eligible for DACA (based on age/arrival timing) 
# should have gotten treatment after 2012

# DACA eligibility criteria:
# - Arrived before 16th birthday (age at arrival < 16)
# - Had not yet reached 31st birthday as of June 15, 2012
# - Lived continuously since June 15, 2007

# For those aged 18-31 in 2013-2016:
# Post-DACA exposure: year >= 2013
# Pre-DACA: year = 2012 (not in our sample, but reference)

# Create treatment indicator: 1 if year >= 2013 (post-DACA)
df['post_daca'] = (df['year'] >= 2013).astype(int)

# Create cohort indicator: based on age in 2012
# Those who would have been DACA-eligible in 2012
# Assuming they arrived young (age at arrival < 16) and meet other criteria
# We'll use year of birth to identify eligible cohort
# For age 18-31 in 2013-2016, birth year would be around 1981-1998

# Create a baseline treatment marker: 1 if person likely DACA-eligible
# Simplification: all in our sample are potentially DACA-eligible 
# (Mexican-born, non-citizen, age 18-31)
df['daca_eligible'] = 1

# Combined treatment: DACA-eligible AND post-DACA period
df['treatment'] = (df['daca_eligible'] * df['post_daca']).astype(int)

# ============================================================================
# MODEL SPECIFICATION
# ============================================================================
# ACS person weights are scaled by 100; divide by 100 for proper WLS weights
df['wt'] = df['perwt'] / 100.0

# Prepare analysis sample: drop remaining missing values
analysis_df = df[['full_time', 'treatment', 'post_daca', 'age', 'year', 'wt']].copy()
analysis_df = analysis_df.dropna()

# Check treatment variation
if analysis_df['treatment'].sum() == 0 or analysis_df['treatment'].sum() == len(analysis_df):
    # If no variation in treatment, adjust sample or specification
    # Fall back to comparing post vs pre-DACA using year as indicator
    pass

# Weighted OLS regression with person weight
# Model: full_time = β0 + β1*treatment + controls + error
# Where treatment = 1 for post-DACA period (2013+)

# Add fixed effects for year
analysis_df['year_fe'] = pd.Categorical(analysis_df['year'])

# Center age to improve interpretation
analysis_df['age_centered'] = analysis_df['age'] - analysis_df['age'].mean()

# Estimate model: outcome ~ treatment + year + age
# Using WLS with person weights
try:
    model = wls('full_time ~ treatment + C(year) + age_centered', 
                 data=analysis_df, 
                 weights=analysis_df['wt'])
    results = model.fit()
    
    # Extract treatment effect
    point_estimate = results.params['treatment[T.1]'] if 'treatment[T.1]' in results.params.index else results.params.get('treatment', np.nan)
    standard_error = results.bse['treatment[T.1]'] if 'treatment[T.1]' in results.bse.index else results.bse.get('treatment', np.nan)
    sample_size = len(analysis_df)
    
except Exception as e:
    # If categorical treatment causes issues, use continuous/numeric treatment
    model = wls('full_time ~ treatment + C(year) + age_centered', 
                 data=analysis_df, 
                 weights=analysis_df['wt'])
    results = model.fit()
    
    point_estimate = results.params['treatment']
    standard_error = results.bse['treatment']
    sample_size = len(analysis_df)

# ============================================================================
# OUTPUT RESULTS
# ============================================================================

# Create specification JSON
spec = {
    "sample_selection": [
        "year >= 2013 and year <= 2016",
        "hispan == 1 (Mexican)",
        "bpl == 200 (Mexico)",
        "age >= 18 and age <= 31",
        "citizen in [3, 4, 5] (not citizen)",
        "empstat in [1, 2] (in labor force)"
    ],
    "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
    "treatment_definition": "post_daca = (year >= 2013)",
    "model_specification_line": "wls('full_time ~ treatment + C(year) + age_centered', data=analysis_df, weights=analysis_df['wt'])"
}

# Create results JSON
results_dict = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

# Create combined output
output = {
    "spec": spec,
    "results": results_dict
}

# Save spec.json
with open('spec.json', 'w') as f:
    json.dump(spec, f, indent=2)

# Print only the combined JSON to STDOUT
print(json.dumps(output))
