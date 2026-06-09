#!/usr/bin/env python3
"""
DACA Impact on Full-Time Employment Analysis

Analysis of the causal impact of DACA eligibility on full-time employment probability
among Hispanic-Mexican, Mexican-born individuals in the United States, 2013-2016.

Key Research Question:
Among ethnically Hispanic-Mexican Mexican-born people, what was the causal impact of DACA
eligibility on the probability of full-time employment (35+ hours per week)?

Identification Strategy:
Use variation in DACA eligibility based on:
1. Birth cohort (born 1981 or later vs earlier - those under 31 on June 15, 2012)
2. Arrival cohort (arrived before 2007 - continuous residence requirement)
3. Arrival age (arrived before age 16)
4. Geographic/state variation as controls

Model: Weighted linear regression with state and year fixed effects
Treatment: DACA eligibility indicator (1 if born 1981 or later, 0 otherwise)
Outcome: Full-time employment (working 35+ hours per week)
Sample: Hispanic-Mexican, Mexico-born, non-citizen, age 16-65, arrived before 2007 before age 16
"""

import pandas as pd
import numpy as np
import sys
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. READ AND PARSE THE FIXED-WIDTH ACS DATA
# ============================================================================

# Define fixed-width file column positions (based on ACS_extract_expanded_layout_excerpt.do)
# Note: positions are 1-indexed in .do file, 0-indexed in Python
acs_positions = {
    'year': (0, 4),           # positions 1-4
    'statefip': (65, 67),     # positions 66-67
    'pernum': (687, 691),     # positions 688-691
    'perwt': (691, 701),      # positions 692-701 (has 2 implied decimals)
    'age': (740, 743),        # positions 741-743
    'hispan': (763, 764),     # positions 764-764
    'bpl': (767, 770),        # positions 768-770
    'citizen': (789, 790),    # positions 790-790
    'yrimmig': (794, 798),    # positions 795-798
    'empstat': (874, 875),    # positions 875-875
    'uhrswork': (904, 906),   # positions 905-906
}

print("Reading ACS fixed-width data...", file=sys.stderr, flush=True)

chunks = []
chunk_size = 50000
chunk_count = 0

try:
    with open('ACS_extract_expanded.dat', 'r', encoding='latin-1') as f:
        chunk = []
        for line_num, line in enumerate(f):
            try:
                # Ensure line is long enough
                if len(line) < 906:
                    continue
                
                # Extract fields based on fixed-width positions
                record = {}
                record['year'] = int(line[acs_positions['year'][0]:acs_positions['year'][1]].strip() or '0')
                record['statefip'] = int(line[acs_positions['statefip'][0]:acs_positions['statefip'][1]].strip() or '0')
                record['pernum'] = int(line[acs_positions['pernum'][0]:acs_positions['pernum'][1]].strip() or '0')
                
                # Weight has 2 implied decimals
                perwt_str = line[acs_positions['perwt'][0]:acs_positions['perwt'][1]].strip()
                record['perwt'] = float(perwt_str) / 100.0 if perwt_str and perwt_str != '0' else np.nan
                
                record['age'] = int(line[acs_positions['age'][0]:acs_positions['age'][1]].strip() or '0')
                record['hispan'] = int(line[acs_positions['hispan'][0]:acs_positions['hispan'][1]].strip() or '0')
                record['bpl'] = int(line[acs_positions['bpl'][0]:acs_positions['bpl'][1]].strip() or '0')
                record['citizen'] = int(line[acs_positions['citizen'][0]:acs_positions['citizen'][1]].strip() or '0')
                
                yrimmig_str = line[acs_positions['yrimmig'][0]:acs_positions['yrimmig'][1]].strip()
                if yrimmig_str and yrimmig_str != '0000':
                    record['yrimmig'] = int(yrimmig_str)
                else:
                    record['yrimmig'] = np.nan
                
                record['empstat'] = int(line[acs_positions['empstat'][0]:acs_positions['empstat'][1]].strip() or '0')
                
                uhrswork_str = line[acs_positions['uhrswork'][0]:acs_positions['uhrswork'][1]].strip()
                record['uhrswork'] = int(uhrswork_str) if uhrswork_str else np.nan
                
                chunk.append(record)
                
                # Create chunks to manage memory
                if len(chunk) >= chunk_size:
                    chunks.append(pd.DataFrame(chunk))
                    chunk_count += 1
                    print(f"  Processed chunk {chunk_count}...", file=sys.stderr, flush=True)
                    chunk = []
                    
            except (ValueError, IndexError):
                # Skip malformed records silently
                continue
        
        # Add final chunk
        if chunk:
            chunks.append(pd.DataFrame(chunk))
            chunk_count += 1

    # Combine all chunks
    df = pd.concat(chunks, ignore_index=True)
    print(f"Loaded {len(df):,} total records", file=sys.stderr, flush=True)

except Exception as e:
    print(f"ERROR reading ACS data: {e}", file=sys.stderr, flush=True)
    sys.exit(1)

# ============================================================================
# 2. LOAD STATE-LEVEL POLICY DATA
# ============================================================================

try:
    policy_df = pd.read_csv('policy_labor_market_data.csv')
    # Normalize column names to lowercase
    policy_df.columns = policy_df.columns.str.lower()
    print(f"Loaded {len(policy_df):,} state-year observations", file=sys.stderr, flush=True)
except Exception as e:
    print(f"ERROR reading policy data: {e}", file=sys.stderr, flush=True)
    sys.exit(1)

# ============================================================================
# 3. MERGE ACS WITH POLICY DATA
# ============================================================================

df = df.merge(
    policy_df,
    left_on=['year', 'statefip'],
    right_on=['year', 'state_fips'],
    how='left'
)

# ============================================================================
# 4. SAMPLE SELECTION CRITERIA
# ============================================================================

print("\nApplying sample selection criteria...", file=sys.stderr, flush=True)

# Filter 1: Hispanic Mexican origin
df_sample = df[(df['hispan'] == 1) & (df['bpl'] == 200)].copy()
print(f"  Hispanic Mexican, Mexico-born: {len(df_sample):,}", file=sys.stderr, flush=True)

# Filter 2: Non-citizens (DACA eligible must lack legal status)
# Citizen codes: 3=Not citizen, 4=First papers, 5=Status not reported
df_sample = df_sample[df_sample['citizen'].isin([3, 4, 5])].copy()
print(f"  Non-citizen: {len(df_sample):,}", file=sys.stderr, flush=True)

# Filter 3: Years 2013-2016 (post-DACA)
df_sample = df_sample[df_sample['year'].isin([2013, 2014, 2015, 2016])].copy()
print(f"  Years 2013-2016: {len(df_sample):,}", file=sys.stderr, flush=True)

# Filter 4: Age 16-65 (working age)
df_sample = df_sample[(df_sample['age'] >= 16) & (df_sample['age'] <= 65)].copy()
print(f"  Age 16-65: {len(df_sample):,}", file=sys.stderr, flush=True)

# Filter 5: Arrived by 2007 (continuous residence requirement)
df_sample = df_sample[df_sample['yrimmig'] <= 2007].copy()
print(f"  Arrived by 2007: {len(df_sample):,}", file=sys.stderr, flush=True)

# Filter 6: Arrived before age 16
df_sample['arrival_age'] = df_sample['age'] - (df_sample['year'] - df_sample['yrimmig'])
df_sample = df_sample[df_sample['arrival_age'] < 16].copy()
print(f"  Arrived before age 16: {len(df_sample):,}", file=sys.stderr, flush=True)

# ============================================================================
# 5. TREATMENT AND OUTCOME VARIABLES
# ============================================================================

# Treatment: DACA eligible = born 1981 or later (under 31 on June 15, 2012)
df_sample['birth_year'] = df_sample['year'] - df_sample['age']
df_sample['daca_eligible'] = (df_sample['birth_year'] >= 1981).astype(int)

# Outcome: Full-time employed = employed AND 35+ hours per week
df_sample['full_time'] = (
    (df_sample['empstat'] == 1) & 
    (df_sample['uhrswork'] >= 35)
).astype(int)

# Check variation
n_eligible = df_sample['daca_eligible'].sum()
n_ineligible = len(df_sample) - n_eligible
n_ft = df_sample['full_time'].sum()

print(f"\nTreatment variation:", file=sys.stderr, flush=True)
print(f"  DACA eligible (1981+): {n_eligible:,}", file=sys.stderr, flush=True)
print(f"  Not eligible (<1981): {n_ineligible:,}", file=sys.stderr, flush=True)
print(f"  Full-time employed: {n_ft:,}", file=sys.stderr, flush=True)

if n_eligible == 0 or n_ineligible == 0:
    print("ERROR: No treatment variation!", file=sys.stderr, flush=True)
    sys.exit(1)

# ============================================================================
# 6. PREPARE FOR REGRESSION
# ============================================================================

# Create control variables
df_sample['year_2014'] = (df_sample['year'] == 2014).astype(int)
df_sample['year_2015'] = (df_sample['year'] == 2015).astype(int)
df_sample['year_2016'] = (df_sample['year'] == 2016).astype(int)

# State fixed effects for top 10 states (to avoid multicollinearity)
top_states = df_sample['statefip'].value_counts().head(10).index.tolist()
for state in top_states[1:]:  # Exclude first state as baseline
    df_sample[f'state_{state}'] = (df_sample['statefip'] == state).astype(int)

# Prepare data for regression
feature_cols = ['daca_eligible', 'year_2014', 'year_2015', 'year_2016']
feature_cols.extend([col for col in df_sample.columns if col.startswith('state_')])

# Add policy controls if available
if 'unemp' in df_sample.columns:
    feature_cols.append('unemp')
if 'lfpr' in df_sample.columns:
    feature_cols.append('lfpr')

# Drop rows with missing values
df_reg = df_sample[feature_cols + ['full_time', 'perwt']].dropna().copy()

print(f"Final regression sample: {len(df_reg):,}", file=sys.stderr, flush=True)

# ============================================================================
# 7. WEIGHTED LINEAR REGRESSION
# ============================================================================

from sklearn.linear_model import LinearRegression

# Prepare X and y
X = df_reg[feature_cols].values
y = df_reg['full_time'].values
weights = df_reg['perwt'].values.astype(float)

# Normalize weights
weights = weights / weights.mean()

# Fit weighted OLS
reg = LinearRegression()
reg.fit(X, y, sample_weight=weights)

# Extract treatment coefficient
treatment_effect = reg.coef_[0]

# Calculate standard error using heteroskedasticity-robust sandwich estimator
predicted = reg.predict(X)
residuals = y - predicted

# Bread: (X'WX)^-1
XtX = X.T @ np.diag(weights) @ X
bread = np.linalg.inv(XtX)

# Meat: X'W * residuals^2 * W X
meat = X.T @ np.diag(weights * (residuals ** 2)) @ X

# Variance-covariance matrix
vcov = bread @ meat @ bread

# Standard error of treatment coefficient
se = np.sqrt(np.diag(vcov))[0]

# ============================================================================
# 8. OUTPUT RESULTS
# ============================================================================

sample_size = len(df_reg)

results_dict = {
    "point_estimate": float(treatment_effect),
    "standard_error": float(se),
    "sample_size": int(sample_size)
}

# Print ONLY JSON to stdout
import json
print(json.dumps(results_dict))
