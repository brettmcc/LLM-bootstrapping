#!/usr/bin/env python3
"""
DACA Impact Analysis: Full-time Employment Effect
Specification: Difference-in-differences on full-time employment among 
Hispanic-Mexican Mexican-born noncitizens aged 18-35.
"""

import pandas as pd
import numpy as np
from scipy import stats
import json
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PART 1: DATA LOADING AND PREPARATION
# ============================================================================

# Read ACS data using fixed-width format from layout file
# Based on ACS_extract_expanded_layout_excerpt.do specifications

def read_acs_data(filename):
    """Read fixed-width ACS data file with selective column parsing."""
    
    df_list = []
    
    with open(filename, 'r') as f:
        for line in f:
            if len(line) < 950:  # Skip malformed lines
                continue
            
            row = {}
            try:
                row['year'] = int(line[0:4])
                row['statefip'] = int(line[65:67])
                row['hispan'] = int(line[763:764])
                row['bpl'] = int(line[767:770])
                row['citizen'] = int(line[789:790])
                row['yrimmig'] = int(line[794:798])
                row['age'] = int(line[740:743])
                row['uhrswork'] = int(line[804:806])
                row['perwt'] = float(line[691:701])
                row['empstat'] = int(line[874:875])
                
                df_list.append(row)
            except (ValueError, IndexError):
                continue
    
    df = pd.DataFrame(df_list)
    return df

print("Loading ACS data...")
acs = read_acs_data('ACS_extract_expanded.dat')
print(f"Loaded {len(acs)} records")

# Load policy data
print("Loading policy data...")
policy = pd.read_csv('policy_labor_market_data.csv')
policy.rename(columns={'state_fips': 'statefip'}, inplace=True)

# ============================================================================
# PART 2: SAMPLE SELECTION
# ============================================================================

print("\nApplying sample selection criteria...")

# Filter 1: Years 2006-2016 (already in data)
# We'll use 2006-2011 as pre-period and 2013-2016 as post-period
# 2012 is excluded as DACA was implemented mid-year (June 15)
acs = acs[(acs['year'] >= 2006) & (acs['year'] <= 2016) & (acs['year'] != 2012)]
print(f"After year filter: {len(acs)}")

# Filter 2: Hispanic origin = 1 (Mexican)
acs = acs[acs['hispan'] == 1]
print(f"After hispan==1 (Mexican): {len(acs)}")

# Filter 3: Birthplace = 200 (Mexico)
acs = acs[acs['bpl'] == 200]
print(f"After bpl==200 (Mexico): {len(acs)}")

# Filter 4: Noncitizen (citizen codes 3, 4, 5)
acs = acs[acs['citizen'].isin([3, 4, 5])]
print(f"After citizen status filter: {len(acs)}")

# Filter 5: Age restriction
# DACA eligible: must be <31 on June 15, 2012 and arrived before age 16
acs = acs[(acs['age'] >= 18) & (acs['age'] <= 35)]
print(f"After age filter (18-35): {len(acs)}")

# Filter 6: Valid employment and hours worked data
# uhrswork > 0 means employed and working
acs = acs[(acs['uhrswork'] > 0) & (acs['uhrswork'] < 100)]  # Valid hours (1-99)
print(f"After valid hours worked filter: {len(acs)}")

# Check if we have any data
if len(acs) == 0:
    print("ERROR: No data remaining after filters!")
    exit(1)

# ============================================================================
# PART 3: CONSTRUCT VARIABLES
# ============================================================================

print("\nConstructing analysis variables...")

# Outcome: Full-time employment (35+ hours per week)
# UHRSWORK ranges from 1 to 99, where 99 may represent "no hours reported"
acs['fulltime'] = (acs['uhrswork'] >= 35).astype(int)

# Approximate birth year based on age in survey year
acs['birth_year_approx'] = acs['year'] - acs['age']

# DACA eligibility indicator
# Eligible: born after June 15, 1981, so birth year >= 1982
acs['daca_eligible'] = (acs['birth_year_approx'] >= 1982).astype(int)

# Post-DACA indicator (implemented June 15, 2012)
acs['post'] = (acs['year'] >= 2013).astype(int)

# Treatment: Eligible * Post interaction
acs['treated'] = (acs['daca_eligible'] * acs['post']).astype(int)

# Merge with policy data for state and year controls
acs = acs.merge(policy[['statefip', 'year', 'EVERIFY', 'OMNIBUS']], 
                on=['statefip', 'year'], 
                how='left')

# Normalize weights (divide by 100 as per ACS convention)
acs['perwt_normalized'] = acs['perwt'] / 100.0

print(f"Final analysis sample: {len(acs)} observations")

# ============================================================================
# PART 4: VERIFY TREATMENT VARIATION
# ============================================================================

print("\nVerifying treatment variation...")

treatment_variation = pd.crosstab(
    acs['daca_eligible'], 
    acs['post'], 
    margins=True,
    rownames=['DACA Eligible'],
    colnames=['Post-DACA']
)
print(treatment_variation)

# Check outcome variation
print(f"\nOutcome (full-time employment) variation:")
print(f"  Mean: {acs['fulltime'].mean():.4f}")
print(f"  Std: {acs['fulltime'].std():.4f}")
print(f"  Min: {acs['fulltime'].min()}")
print(f"  Max: {acs['fulltime'].max()}")

# Check variation by treatment group
print(f"\nFull-time employment by DACA eligibility and period:")
for eligible in [0, 1]:
    for period in [0, 1]:
        subset = acs[(acs['daca_eligible'] == eligible) & (acs['post'] == period)]
        if len(subset) > 0:
            print(f"  DACA Eligible={eligible}, Post={period}: {subset['fulltime'].mean():.4f} ({len(subset)} obs)")

if acs['fulltime'].std() == 0:
    print("ERROR: No variation in outcome variable!")
    exit(1)

# ============================================================================
# PART 5: ESTIMATION
# ============================================================================

print("\nEstimating treatment effect using difference-in-differences...")

# Prepare data for estimation - ensure all data types are numeric
y = acs['fulltime'].astype(float).values
weights = acs['perwt_normalized'].astype(float).values

# Create design matrix manually to ensure numeric types
daca_eligible = acs['daca_eligible'].astype(float).values
post = acs['post'].astype(float).values
treated = acs['treated'].astype(float).values
everify = acs['EVERIFY'].fillna(0).astype(float).values
omnibus = acs['OMNIBUS'].fillna(0).astype(float).values

# Add state and year fixed effects as dummies
state_dummies = pd.get_dummies(acs['statefip'], prefix='state', drop_first=True, dtype=float)
year_dummies = pd.get_dummies(acs['year'], prefix='year', drop_first=True, dtype=float)

# Build design matrix with explicit column names and numeric dtype
X_list = [np.ones(len(y)), daca_eligible, post, treated, everify, omnibus]
X_names = ['const', 'daca_eligible', 'post', 'treated', 'everify', 'omnibus']

# Add fixed effects
for col in state_dummies.columns:
    X_list.append(state_dummies[col].astype(float).values)
    X_names.append(col)

for col in year_dummies.columns:
    X_list.append(year_dummies[col].astype(float).values)
    X_names.append(col)

# Stack into matrix
X_all = np.column_stack(X_list).astype(float)

# Use weighted least squares
from statsmodels.regression.linear_model import WLS

model = WLS(y, X_all, weights=weights)
results = model.fit()

# Extract treatment effect
# Find which column index corresponds to 'treated'
treated_idx = X_names.index('treated')
treatment_coef = results.params[treated_idx]
treatment_se = results.bse[treated_idx]

print(f"\nDifference-in-Differences Results:")
print(f"Treatment Effect (daca_eligible * post): {treatment_coef:.6f}")
print(f"Standard Error: {treatment_se:.6f}")
if treatment_se > 0:
    t_stat = treatment_coef / treatment_se
    p_val = 2 * (1 - stats.t.cdf(abs(t_stat), len(y) - X_all.shape[1]))
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_val:.6f}")

# Sample size
sample_size = len(y)

# ============================================================================
# PART 6: OUTPUT RESULTS
# ============================================================================

# Specification details
spec = {
    "sample_selection": [
        "year in [2006,2007,2008,2009,2010,2011,2013,2014,2015,2016]",
        "hispan == 1 (Mexican ethnicity)",
        "bpl == 200 (Mexico birthplace)",
        "citizen in [3,4,5] (noncitizen status)",
        "age in [18,35]",
        "uhrswork in [1,99] (employed with valid hours)"
    ],
    "outcome_definition": "(acs['uhrswork'] >= 35).astype(int)",
    "treatment_definition": "(acs['birth_year_approx'] >= 1982) * (acs['year'] >= 2013)",
    "model_specification_line": "WLS(fulltime ~ daca_eligible + post + treated + state_fe + year_fe, weights=perwt_normalized)"
}

results_dict = {
    "point_estimate": float(treatment_coef),
    "standard_error": float(treatment_se),
    "sample_size": int(sample_size)
}

output = {
    "spec": spec,
    "results": results_dict
}

# Print JSON output (STDOUT only - no extra text)
print(json.dumps(output, indent=2))

# Also save spec to spec.json
with open('spec.json', 'w') as f:
    json.dump(spec, f, indent=2)
