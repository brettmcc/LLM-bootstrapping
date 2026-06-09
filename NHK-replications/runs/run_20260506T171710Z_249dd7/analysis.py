#!/usr/bin/env python3
"""
Phase 12 Analysis: DACA Impact on Full-Time Employment for Mexican-Born Hispanic Mexicans
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings
warnings.filterwarnings('ignore')

# Fixed-width file column specifications (1-based from layout file)
# Converting to 0-based for pandas
col_specs = [
    (0, 4),         # year
    (175, 178),     # age
    (186, 189),     # hispan
    (767, 770),     # bpl
    (789, 790),     # citizen
    (794, 798),     # yrimmig
    (874, 875),     # empstat
    (904, 906),     # uhrswork
    (691, 701),     # perwt (person weight)
]

col_names = ['year', 'age', 'hispan', 'bpl', 'citizen', 'yrimmig', 'empstat', 'uhrswork', 'perwt']

# Read fixed-width ACS data in chunks to manage memory
def read_acs_data():
    """Read ACS data with filtering to reduce memory usage"""
    dfs = []
    chunksize = 50000
    
    with open('ACS_extract_expanded.dat', 'r') as f:
        chunk = []
        for i, line in enumerate(f):
            # Ensure line is long enough
            if len(line) < 710:  # Pad if needed
                line = line.rstrip('\n').ljust(710)
            
            # Extract values for each column
            row = []
            for start, end in col_specs:
                try:
                    val = line[start:end].strip()
                    row.append(val if val else None)
                except:
                    row.append(None)
            
            chunk.append(row)
            
            if len(chunk) >= chunksize:
                df = pd.DataFrame(chunk, columns=col_names)
                # Convert to numeric types
                for col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Filter early to reduce memory: years 2013-2016, Mexican-born, Mexican ethnicity
                df = df[
                    (df['year'].isin([2013, 2014, 2015, 2016])) &
                    (df['hispan'] == 1) &  # Mexican
                    (df['bpl'] == 200) &    # Mexico
                    (df['age'] >= 18) &
                    (df['age'] <= 70)
                ]
                
                if len(df) > 0:
                    dfs.append(df)
                chunk = []
    
    # Process remaining chunk
    if chunk:
        df = pd.DataFrame(chunk, columns=col_names)
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df[
            (df['year'].isin([2013, 2014, 2015, 2016])) &
            (df['hispan'] == 1) &
            (df['bpl'] == 200) &
            (df['age'] >= 18) &
            (df['age'] <= 70)
        ]
        if len(df) > 0:
            dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

# Read data
print("Reading ACS data...", flush=True)
df = read_acs_data()

print(f"Initial sample size: {len(df)}", flush=True)

# Create DACA eligibility indicator based on June 15, 2012 cutoff
# Eligible if:
# 1. Born in 1982 or later (age <= 30 on June 15, 2012)
# 2. Arrived before 2007 (lived continuously since June 15, 2007)
# 3. Non-citizen (citizen in 3, 4, or 5)
# 4. Arrived before age 16 (yrimmig <= birth_year + 15, but we use age logic)

# Birth year approximation: assumes survey is taken mid-year
df['birth_year'] = df['year'] - df['age']

# DACA eligibility criteria:
# - Born 1982 or later (age <= 30 on June 15, 2012)
# - Arrived in 2007 or earlier (lived continuously since June 15, 2007)
# - Non-citizen status (citizen codes 3, 4, or 5 indicate non-citizen)
# - Arrived before age 16
df['daca_eligible'] = (
    (df['birth_year'] >= 1982) &  # Age <= 30 on June 15, 2012
    (df['yrimmig'] <= 2007) &      # Arrived by 2007
    (df['citizen'].isin([3, 4, 5])) &  # Non-citizen
    (df['yrimmig'] >= df['birth_year'] + 1) &  # Arrived after birth
    ((df['yrimmig'] - df['birth_year']) <= 15)  # Arrived before age 16
).astype(int)

# Create outcome: full-time employment (empstat==1 and uhrswork>=35)
df['fulltime_employed'] = (
    (df['empstat'] == 1) &  # Employed
    (df['uhrswork'] >= 35)   # 35+ hours per week
).astype(int)

# Filter to observations with valid outcome data
df = df[df['fulltime_employed'].notna()]
df = df[df['daca_eligible'].notna()]

print(f"Sample after filtering for valid data: {len(df)}", flush=True)

# Verify treatment variation
daca_count = df['daca_eligible'].sum()
print(f"DACA eligible: {daca_count}, Not eligible: {len(df) - daca_count}", flush=True)

if daca_count == 0 or daca_count == len(df):
    print("ERROR: No treatment variation in sample", flush=True)
    exit(1)

# Normalize weights (divide by 100 as per ACS documentation)
df['weight'] = df['perwt'] / 100.0

# Descriptive statistics
print(f"\nSample statistics:", flush=True)
print(f"Full-time employment rate: {df['fulltime_employed'].mean():.4f}", flush=True)
print(f"DACA eligible rate: {df['daca_eligible'].mean():.4f}", flush=True)
print(f"Full-time employment by DACA eligibility:", flush=True)
print(df.groupby('daca_eligible')['fulltime_employed'].agg(['mean', 'count']))

# Use weighted least squares regression
# Model: fulltime_employed = b0 + b1*daca_eligible + e
# This estimates the intention-to-treat effect of DACA eligibility

X = df[['daca_eligible']].copy()
X = sm.add_constant(X)
y = df['fulltime_employed']
weights = df['weight']

# Fit weighted least squares model
wls_model = sm.WLS(y, X, weights=weights)
wls_result = wls_model.fit()

# Extract results
point_estimate = wls_result.params['daca_eligible']
standard_error = wls_result.bse['daca_eligible']
sample_size = len(df)

# Print results in required format
results_json = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

import json
print(json.dumps(results_json))
