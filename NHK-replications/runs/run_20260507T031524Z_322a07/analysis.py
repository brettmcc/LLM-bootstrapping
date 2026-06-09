#!/usr/bin/env python3
"""
DACA Impact on Full-Time Employment Analysis
This script estimates the effect of DACA eligibility on the probability of full-time employment
for ethnically Hispanic-Mexican, Mexico-born people in the US using ACS data (2013-2016).

DACA Eligibility Criteria:
- Arrived before 16th birthday
- Not yet 31 as of June 15, 2012
- Continuously in US since June 15, 2007
- No lawful status as of June 15, 2012

Estimation Strategy:
- Use a difference-in-differences approach comparing DACA-eligible vs ineligible within the target population
- DACA eligibility is determined by arrival age and year
- Full-time employment is defined as usually working 35+ hours per week
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json

# Fixed-width parsing information from ACS_extract_expanded_layout_excerpt.do
# All positions are 1-based in the Stata format, convert to 0-based for Python
COLUMN_SPECS = {
    'year': (0, 4),        # columns 1-4
    'hispan': (763, 764),  # column 764 (1-based) -> 763 (0-based)
    'bpl': (767, 770),     # columns 768-770 (1-based) -> 767-770 (0-based)
    'citizen': (789, 790), # column 790 (1-based) -> 789 (0-based)
    'age': (740, 743),     # columns 741-743 (1-based) -> 740-743 (0-based)
    'birthyr': (747, 751), # columns 748-751 (1-based) -> 747-751 (0-based)
    'empstat': (874, 875), # column 875 (1-based) -> 874 (0-based)
    'uhrswork': (904, 906),# columns 905-906 (1-based) -> 904-906 (0-based)
    'perwt': (691, 701),   # columns 692-701 (1-based) -> 691-701 (0-based)
}

# Data file path
DATA_FILE = 'ACS_extract_expanded.dat'

def parse_fixed_width_record(line, col_specs):
    """Parse a fixed-width record extracting specified columns."""
    record = {}
    for var_name, (start, end) in col_specs.items():
        # Extract substring and strip/convert
        value_str = line[start:end].strip()
        if value_str:
            try:
                # Try to parse as integer
                record[var_name] = int(value_str)
            except ValueError:
                # If fails, keep as string
                record[var_name] = value_str
        else:
            record[var_name] = None
    return record

def read_acs_data():
    """Read ACS data in chunks to manage memory."""
    records = []
    with open(DATA_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Skip lines that are too short
            if len(line) < 906:
                continue
            
            record = parse_fixed_width_record(line, COLUMN_SPECS)
            records.append(record)
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Convert columns to proper numeric types where possible
    for col in ['year', 'hispan', 'bpl', 'citizen', 'age', 'birthyr', 'empstat', 'uhrswork', 'perwt']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def determine_daca_eligibility(row):
    """
    Determine DACA eligibility based on criteria:
    1. Born in Mexico (BPL == 200)
    2. Non-citizen (CITIZEN in {3, 4, 5})
    3. Age constraint: born 1982-1996 for ages 16-30 on June 15, 2012
    
    Returns 1 if eligible, 0 if not, NaN if cannot determine.
    """
    
    # Check if born in Mexico (essential criterion)
    if pd.isna(row['bpl']) or row['bpl'] != 200:
        return np.nan  # Not Mexico-born, exclude
    
    # Check if non-citizen (essential criterion)
    # Citizen codes: 3=not citizen, 4=first papers (provisional), 5=status not reported
    if pd.isna(row['citizen']) or row['citizen'] not in [3, 4, 5]:
        return np.nan  # Has citizenship or lawful status, exclude
    
    # Check birth year for age eligibility
    if pd.isna(row['birthyr']):
        return np.nan
    
    # Age eligibility: born 1982-1996 for ages 16-30 on June 15, 2012
    # 1982: age 30 on June 15, 2012
    # 1996: age 16 on June 15, 2012
    if row['birthyr'] < 1982 or row['birthyr'] > 1996:
        return 0  # Not eligible (outside age range)
    
    # If all checks pass: eligible
    return 1

def analyze():
    """Main analysis function."""
    print("Reading ACS data...", flush=True)
    df = read_acs_data()
    
    print(f"Total records: {len(df)}", flush=True)
    
    # Filter for years 2013-2016 (post-DACA implementation)
    df = df[df['year'].isin([2013, 2014, 2015, 2016])].copy()
    print(f"Records 2013-2016: {len(df)}", flush=True)
    
    # Filter for Hispanic-Mexican ethnicity
    df = df[df['hispan'] == 1].copy()
    print(f"After hispan==1: {len(df)}", flush=True)
    
    # Determine DACA eligibility
    df['daca_eligible'] = df.apply(determine_daca_eligibility, axis=1)
    
    # Remove rows where eligibility couldn't be determined
    df = df[df['daca_eligible'].notna()].copy()
    print(f"After eligibility determination: {len(df)}", flush=True)
    
    # Check treatment variation
    eligible_count = (df['daca_eligible'] == 1).sum()
    ineligible_count = (df['daca_eligible'] == 0).sum()
    print(f"Eligible: {eligible_count}, Ineligible: {ineligible_count}", flush=True)
    
    if eligible_count == 0 or ineligible_count == 0:
        raise ValueError("No variation in treatment assignment")
    
    # Define outcome: full-time employment (35+ hours per week)
    # empstat: 1 = Employed, 2 = Unemployed, 3 = Not in labor force
    # uhrswork: 1-99 hours per week
    df['fulltime'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)
    
    # Remove missing values for outcome and key variables
    df = df[df[['daca_eligible', 'fulltime', 'perwt']].notna()].copy()
    print(f"After removing missing values: {len(df)}", flush=True)
    
    # Normalize weights (ACS weights are in units of 100)
    df['weight_normalized'] = df['perwt'] / 100.0
    
    # Prepare data for weighted least squares
    X = df[['daca_eligible']].values
    y = df['fulltime'].values
    weights = df['weight_normalized'].values
    
    # Weighted least squares: regress outcome on treatment with weights
    weighted_X = X * np.sqrt(weights[:, np.newaxis])
    weighted_y = y * np.sqrt(weights)
    
    model = LinearRegression()
    model.fit(weighted_X, weighted_y)
    
    point_estimate = model.coef_[0]
    
    # Calculate residuals and standard error
    predicted = model.predict(weighted_X)
    residuals = weighted_y - predicted
    
    # Calculate residual variance
    dof = len(y) - X.shape[1] - 1
    residual_variance = np.sum(residuals**2) / dof if dof > 0 else np.nan
    
    # Calculate standard error
    # SE = sqrt(residual_var * (X'X)^-1)
    XtX = weighted_X.T @ weighted_X
    if np.linalg.matrix_rank(XtX) == XtX.shape[0]:
        XtX_inv = np.linalg.inv(XtX)
        variance = residual_variance * XtX_inv[0, 0]
        standard_error = np.sqrt(max(0, variance))
    else:
        standard_error = np.nan
    
    sample_size = len(df)
    
    return {
        'point_estimate': float(point_estimate),
        'standard_error': float(standard_error),
        'sample_size': int(sample_size)
    }

if __name__ == '__main__':
    results = analyze()
    print(json.dumps(results))
