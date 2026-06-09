#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Research Question: Among ethnically Hispanic-Mexican Mexican-born people living in the US,
what was the causal impact of DACA eligibility on full-time employment probability (35+ hours/week)?
"""

import pandas as pd
import numpy as np
import json
import sys

def parse_fixed_width_line(line):
    """
    Parse a single fixed-width record from ACS data.
    Field positions derived from ACS_extract_expanded_layout_excerpt.do (converted from 1-indexed to 0-indexed)
    """
    data = {}
    
    # Parse integer fields from fixed-width positions
    data['year'] = int(line[0:4]) if len(line) >= 4 else None
    data['age'] = int(line[740:743]) if len(line) >= 743 else None
    data['hispan'] = int(line[763:764]) if len(line) >= 764 else None
    data['bpl'] = int(line[767:770]) if len(line) >= 770 else None
    data['citizen'] = int(line[789:790]) if len(line) >= 790 else None
    data['empstat'] = int(line[874:875]) if len(line) >= 875 else None
    data['uhrswork'] = int(line[904:906]) if len(line) >= 906 else None
    
    # Parse person weight (stored as integer scaled by 100, per ACS documentation)
    try:
        perwt_str = line[691:701].strip()
        data['perwt'] = float(perwt_str) / 100 if perwt_str else None
    except:
        data['perwt'] = None
    
    return data

def read_acs_data_chunked(filename, chunksize=50000):
    """Read ACS fixed-width data in chunks to manage memory (max 30GB constraint)."""
    records = []
    
    with open(filename, 'r', encoding='latin-1', errors='ignore') as f:
        for line in f:
            # Skip incomplete records
            if len(line.rstrip()) < 700:
                continue
            
            record = parse_fixed_width_line(line.rstrip())
            records.append(record)
            
            # Yield chunks to avoid exceeding memory limits
            if len(records) >= chunksize:
                yield pd.DataFrame(records)
                records = []
        
        if records:
            yield pd.DataFrame(records)

def define_treatment(df):
    """
    Define DACA eligibility treatment variable.
    
    DACA eligibility criteria:
    - Mexican-born: bpl == 200
    - Hispanic-Mexican: hispan == 1
    - Not a US citizen: citizen in [3, 5]
    - Age constraint: aged 16-30 in June 2012, implying birth years 1982-1996
    """
    
    # Mexican-born and Hispanic-Mexican
    is_mexican = (df['bpl'] == 200) & (df['hispan'] == 1)
    
    # Not a citizen (3=not citizen, 5=status not reported)
    not_citizen = df['citizen'].isin([3, 5])
    
    # Age eligible: born 1982-1996 (aged 16-30 in June 2012)
    birth_year = df['year'] - df['age']
    age_eligible = (birth_year >= 1982) & (birth_year <= 1996)
    
    # Treatment indicator
    df['eligible_for_daca'] = ((is_mexican & not_citizen & age_eligible) & (df['age'] > 0)).astype(int)
    
    return df

def define_outcome(df):
    """
    Define full-time employment outcome.
    Full-time = employed (empstat==1) with 35+ hours per week usual work (uhrswork>=35)
    """
    is_employed = df['empstat'] == 1
    is_full_time = df['uhrswork'] >= 35
    
    df['full_time_employed'] = (is_employed & is_full_time).astype(int)
    
    return df

def create_analysis_sample(df):
    """
    Create analysis sample with sample selection filters.
    """
    # DACA implementation in 2012; analysis years 2013-2016
    df = df[(df['year'] >= 2013) & (df['year'] <= 2016)].copy()
    
    # Working-age population
    df = df[(df['age'] >= 16) & (df['age'] <= 65)].copy()
    
    # Remove missing/invalid values
    df = df[df['age'] > 0].copy()
    df = df[df['perwt'].notna() & (df['perwt'] > 0)].copy()
    df = df[df['empstat'].notna() & (df['empstat'] > 0)].copy()
    df = df[df['uhrswork'] > 0].copy()
    
    # Keep only Mexican-origin respondents (bpl==200 or hispan==1)
    df = df[((df['bpl'] == 200) | (df['hispan'] == 1))].copy()
    
    return df

def run_weighted_regression(df):
    """
    Run weighted OLS: full_time_employed = intercept + beta*eligible_for_daca
    Using survey weights (perwt).
    Memory-efficient computation avoids creating full diagonal weight matrix.
    """
    # Prepare analysis dataset
    analysis_df = df[['eligible_for_daca', 'full_time_employed', 'perwt']].copy()
    analysis_df = analysis_df.dropna()
    
    if len(analysis_df) == 0:
        raise ValueError("No valid data for regression")
    
    X = analysis_df['eligible_for_daca'].values
    y = analysis_df['full_time_employed'].values
    weights = analysis_df['perwt'].values
    
    # Add constant to X
    X_with_const = np.column_stack([np.ones(len(X)), X])
    
    # Compute weighted OLS without full diagonal matrix
    # (X'WX)^-1 X'Wy where W is diagonal
    # Equivalent to: sum(w_i * x_i @ x_i') and sum(w_i * x_i * y_i)
    
    # Compute X'WX efficiently (2x2 matrix)
    weighted_X = X_with_const * weights[:, np.newaxis]
    XtWX = weighted_X.T @ X_with_const
    
    # Compute X'Wy efficiently (2-element vector)
    XtWy = weighted_X.T @ y
    
    try:
        beta = np.linalg.solve(XtWX, XtWy)
    except np.linalg.LinAlgError:
        raise ValueError("Singular matrix in weighted regression")
    
    # Calculate standard errors
    y_pred = X_with_const @ beta
    residuals = y - y_pred
    wrss = np.sum(weights * residuals**2)
    
    n = len(y)
    k = X_with_const.shape[1]
    mse = wrss / (n - k)
    
    XtWX_inv = np.linalg.inv(XtWX)
    vcov = mse * XtWX_inv
    se = np.sqrt(np.diag(vcov))
    
    # Return treatment effect (beta[1]) and its SE
    return float(beta[1]), float(se[1]), int(n)

def main():
    """Main analysis pipeline."""
    
    # Read and process ACS data in chunks
    all_dfs = []
    for chunk in read_acs_data_chunked('ACS_extract_expanded.dat'):
        chunk = define_treatment(chunk)
        chunk = define_outcome(chunk)
        all_dfs.append(chunk)
    
    # Combine chunks
    df = pd.concat(all_dfs, ignore_index=True)
    
    # Create analysis sample
    df = create_analysis_sample(df)
    
    # Verify treatment variation
    if df['eligible_for_daca'].nunique() < 2:
        raise ValueError("No treatment variation in sample")
    
    # Estimate treatment effect
    point_estimate, standard_error, sample_size = run_weighted_regression(df)
    
    # Output only JSON result (no extra text to stdout)
    results = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size
    }
    
    print(json.dumps(results))

if __name__ == '__main__':
    main()
