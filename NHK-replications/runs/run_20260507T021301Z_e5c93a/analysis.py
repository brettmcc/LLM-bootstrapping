#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Estimates the causal impact of DACA eligibility on full-time employment
for ethnically Hispanic-Mexican, Mexico-born individuals.
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# STEP 1: PARSE FIXED-WIDTH ACS DATA
# ============================================================================

def parse_acs_fixed_width(filepath):
    """
    Parse the fixed-width ACS extract file.
    Based on ACS_extract_expanded_layout_excerpt.do variable positions.
    """
    # Define fixed-width column positions from the .do file (1-based Stata to 0-based Python)
    col_specs = [
        ('PERNUM', 688, 691),      # person number
        ('PERWT', 692, 701),       # person weight
        ('YEAR', 1, 4),            # need to add year from beginning
        ('SEX', 740, 740),
        ('AGE', 741, 743),
        ('HISPAN', 764, 764),
        ('BPL', 768, 770),
        ('CITIZEN', 790, 790),
        ('YRIMMIG', 795, 798),
        ('EMPSTAT', 875, 875),
        ('EMPSTATD', 876, 877),
        ('UHRSWORK', 905, 906),
    ]
    
    # Convert to 0-based positions for read_fwf
    colspecs = [(spec[1]-1, spec[2]) for spec in col_specs]
    names = [spec[0] for spec in col_specs]
    
    # Read the file
    df = pd.read_fwf(
        filepath,
        colspecs=colspecs,
        names=names,
        dtype={
            'YEAR': 'int32',
            'SEX': 'int32',
            'AGE': 'int32',
            'HISPAN': 'int32',
            'BPL': 'int32',
            'CITIZEN': 'int32',
            'YRIMMIG': 'int32',
            'EMPSTAT': 'int32',
            'EMPSTATD': 'int32',
            'UHRSWORK': 'int32',
            'PERNUM': 'int32',
            'PERWT': 'float32'
        }
    )
    
    return df



# ============================================================================
# STEP 2: PREPARE DATA AND APPLY SAMPLE SELECTION CRITERIA
# ============================================================================

def prepare_sample():
    """
    Load ACS data, apply sample selection criteria, and create analysis variables.
    """
    # Read ACS data
    print("Reading ACS data...", flush=True)
    df = parse_acs_fixed_width('ACS_extract_expanded.dat')
    
    print(f"Total records: {len(df)}", flush=True)
    print(f"HISPAN values: {df['HISPAN'].value_counts().head()}", flush=True)
    print(f"BPL values for Mexico: {(df['BPL'] == 200).sum()}", flush=True)
    print(f"CITIZEN values: {df['CITIZEN'].value_counts().head()}", flush=True)
    print(f"YEAR values: {df['YEAR'].value_counts().sort_index()}", flush=True)
    
    # Apply sample selection filters
    print("Applying sample selection...", flush=True)
    
    # 1. Ethnically Hispanic-Mexican (HISPAN == 1 in general version means Mexican)
    df = df[df['HISPAN'] == 1].copy()
    print(f"After HISPAN filter: {len(df)}", flush=True)
    
    # 2. Mexico-born (BPL == 200)
    df = df[df['BPL'] == 200].copy()
    print(f"After BPL filter: {len(df)}", flush=True)
    
    # 3. Not a citizen (CITIZEN codes: 0=N/A, 1=Born abroad of US parents, 2=Naturalized, 3=Not citizen, 4=First papers, 5=Status not reported)
    # Include non-citizens and status unknown
    df = df[df['CITIZEN'].isin([3, 4, 5])].copy()
    print(f"After CITIZEN filter: {len(df)}", flush=True)
    
    # 4. Years 2013-2016 (post-DACA implementation, June 15 2012)
    df = df[df['YEAR'].isin([2013, 2014, 2015, 2016])].copy()
    print(f"After YEAR filter: {len(df)}", flush=True)
    
    if len(df) == 0:
        print("ERROR: No records after filtering", flush=True)
        return df
    
    # 5. Age-eligible for DACA at baseline and throughout period
    # DACA criteria: arrived before 16, under 31 on 6/15/2012, arrived by 6/15/2007
    
    df['birth_year'] = df['YEAR'] - df['AGE']
    df['age_at_immigration'] = df['YRIMMIG'] - df['birth_year']
    
    print(f"Age at immigration - min: {df['age_at_immigration'].min()}, max: {df['age_at_immigration'].max()}", flush=True)
    print(f"Birth year - min: {df['birth_year'].min()}, max: {df['birth_year'].max()}", flush=True)
    
    # Arrived before 16th birthday
    df = df[df['age_at_immigration'] < 16].copy()
    print(f"After age_at_immigration < 16: {len(df)}", flush=True)
    
    # Arrived by June 15, 2007
    df = df[df['YRIMMIG'] <= 2007].copy()
    print(f"After YRIMMIG <= 2007: {len(df)}", flush=True)
    
    # Born after 1981 (to be under 31 on June 15 2012)
    df = df[df['birth_year'] > 1981].copy()
    print(f"After birth_year > 1981: {len(df)}", flush=True)
    
    # Born before 1996 (reasonable upper bound for this sample)
    df = df[df['birth_year'] < 1996].copy()
    print(f"After birth_year < 1996: {len(df)}", flush=True)
    
    # 6. Employment data available
    print(f"EMPSTAT values: {df['EMPSTAT'].value_counts().head()}", flush=True)
    print(f"UHRSWORK values - min: {df['UHRSWORK'].min()}, max: {df['UHRSWORK'].max()}", flush=True)
    
    df = df[df['EMPSTAT'].isin([1, 2, 3])].copy()
    print(f"After EMPSTAT filter: {len(df)}", flush=True)
    
    df = df[df['UHRSWORK'] > 0].copy()
    print(f"After UHRSWORK > 0: {len(df)}", flush=True)
    
    if len(df) == 0:
        print("ERROR: Empty sample after selection", flush=True)
        return df
    
    # Create outcome variable: Full-time employment (35+ hours/week AND employed)
    df['fultime_employed'] = ((df['UHRSWORK'] >= 35) & (df['EMPSTAT'] == 1)).astype(int)
    
    # Create treatment: variation based on arrival cohort
    df['years_until_daca'] = 2012 - df['YRIMMIG']
    df['high_exposure'] = ((df['YRIMMIG'] >= 1997) & (df['YRIMMIG'] <= 2002)).astype(int)
    
    # Normalize person weights
    df['weight'] = df['PERWT'] / 100.0
    
    # Check sample variation
    print(f"Sample size: {len(df)}", flush=True)
    print(f"Full-time employed: {df['fultime_employed'].sum()}/{len(df)} "
          f"({100*df['fultime_employed'].mean():.1f}%)", flush=True)
    print(f"High exposure: {df['high_exposure'].sum()}/{len(df)}", flush=True)
    
    return df

# ============================================================================
# STEP 3: ESTIMATE TREATMENT EFFECT
# ============================================================================

def estimate_treatment_effect(df):
    """
    Estimate the treatment effect using a weighted regression.
    Since all are post-DACA and DACA-eligible, we estimate the
    difference between those who would most benefit (earlier arrivals)
    vs those who would benefit less (later arrivals, but still pre-2008).
    """
    
    # Create a treatment intensity variable based on arrival cohort
    # Earlier arrivals had more time to benefit from DACA work authorization
    # Use interaction: years between arrival and DACA implementation
    df['years_until_daca'] = 2012 - df['YRIMMIG']
    
    # Create treatment: High vs Low exposure to DACA benefits
    # High exposure: arrived 1997-2002 (10-15 years before DACA, more work history to leverage)
    # Low exposure: arrived 2003-2007 (5-9 years before DACA, less work history)
    df['high_exposure'] = ((df['YRIMMIG'] >= 1997) & (df['YRIMMIG'] <= 2002)).astype(int)
    
    # Estimate using weighted OLS
    # Model: full_time_employed = β0 + β1*high_exposure + ε
    
    # Create design matrix
    X = df[['high_exposure']].values
    X = np.column_stack([np.ones(len(X)), X])  # Add intercept
    y = df['fultime_employed'].values
    w = df['weight'].values
    
    # Weighted least squares
    W = np.diag(w)
    XtWX = X.T @ W @ X
    XtWy = X.T @ W @ y
    
    # Solve for coefficients
    try:
        beta = np.linalg.solve(XtWX, XtWy)
        point_estimate = beta[1]
        
        # Calculate standard error
        residuals = y - X @ beta
        weighted_residuals = np.sqrt(w) * residuals
        mse = np.sum(weighted_residuals**2) / (len(y) - 2)
        var_beta = mse * np.linalg.inv(XtWX)
        se = np.sqrt(var_beta[1, 1])
        
    except np.linalg.LinAlgError:
        # Fallback to simple calculation if matrix is singular
        treated = df[df['high_exposure'] == 1]
        control = df[df['high_exposure'] == 0]
        
        mean_treated = (treated['fultime_employed'] * treated['weight']).sum() / treated['weight'].sum()
        mean_control = (control['fultime_employed'] * control['weight']).sum() / control['weight'].sum()
        
        point_estimate = mean_treated - mean_control
        
        # Calculate standard error as difference in means
        n_treated = treated['weight'].sum()
        n_control = control['weight'].sum()
        
        var_treated = ((treated['fultime_employed'] - mean_treated)**2 * treated['weight']).sum() / n_treated
        var_control = ((control['fultime_employed'] - mean_control)**2 * control['weight']).sum() / n_control
        
        se = np.sqrt(var_treated / n_treated + var_control / n_control)
    
    sample_size = len(df)
    
    return {
        'point_estimate': float(point_estimate),
        'standard_error': float(se),
        'sample_size': int(sample_size)
    }

# ============================================================================
# STEP 4: MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    # Prepare sample
    df = prepare_sample()
    
    # Check treatment variation
    if len(df) > 0 and (df['high_exposure'].sum() == 0 or df['high_exposure'].sum() == len(df)):
        print("WARNING: No variation in treatment indicator", flush=True)
    
    # Estimate treatment effect
    if len(df) > 0:
        results = estimate_treatment_effect(df)
    else:
        results = {
            'point_estimate': None,
            'standard_error': None,
            'sample_size': 0
        }
    
    # Create specification
    spec = {
        "sample_selection": [
            "Ethnically Hispanic-Mexican (HISPAN == 1)",
            "Mexico-born (BPL == 200)",
            "Non-citizen (CITIZEN in [3, 4, 5])",
            "Survey years 2013-2016 (post-DACA implementation)",
            "Age at immigration < 16 years",
            "Year of immigration <= 2007",
            "Birth year > 1981 (under 31 on June 15, 2012)",
            "Birth year < 1996 (at least 17 in 2013)",
            "Employment status data available (EMPSTAT in [1, 2, 3])",
            "Non-zero usual hours worked (UHRSWORK > 0)"
        ],
        "outcome_definition": "(UHRSWORK >= 35) & (EMPSTAT == 1)",
        "treatment_definition": "(YRIMMIG >= 1997) & (YRIMMIG <= 2002)",
        "model_specification_line": "np.linalg.solve(X.T @ np.diag(PERWT/100) @ X, X.T @ np.diag(PERWT/100) @ y) for y = fultime_employed, X = [1, high_exposure]"
    }
    
    # Output ONLY the JSON with spec and results
    output = {
        'spec': spec,
        'results': {
            'point_estimate': results['point_estimate'],
            'standard_error': results['standard_error'],
            'sample_size': results['sample_size']
        }
    }
    
    print(json.dumps(output))
