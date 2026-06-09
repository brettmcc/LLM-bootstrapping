#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Analyzes the causal effect of DACA eligibility on full-time employment probability
for ethnically Hispanic-Mexican, Mexican-born individuals living in the United States
using ACS data from 2013-2016.
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

def parse_acs_fixed_width(filename, year_min=2013, year_max=2016):
    """
    Parse the fixed-width ACS data file, filtering for relevant individuals and years.
    Only loads specified columns to manage memory usage.
    """
    # Field positions for fixed-width parsing (1-based in Stata, 0-based in Python)
    # Based on ACS_extract_expanded_layout_excerpt.do
    field_specs = {
        'year': (0, 4),      # columns 1-4
        'age': (740, 743),   # columns 741-743
        'birthyr': (747, 751), # columns 748-751
        'hispan': (763, 764),  # column 764 (1-based), so 763-764 (0-based)
        'bpl': (767, 770),   # columns 768-770
        'citizen': (789, 790), # column 790
        'yrimmig': (794, 798), # columns 795-798
        'empstat': (874, 875), # column 875
        'uhrswork': (904, 906), # columns 905-906
        'perwt': (691, 701),   # columns 692-701 (person weight)
    }
    
    # Read the fixed-width file
    # Read all rows initially
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    records = []
    for line_idx, line in enumerate(lines):
        if len(line) < 906:  # Skip lines that are too short
            continue
        
        try:
            # Extract year first to filter early
            year_str = line[field_specs['year'][0]:field_specs['year'][1]].strip()
            year = int(year_str) if year_str else 0
            
            # Filter years early
            if year < year_min or year > year_max:
                continue
            
            # Extract key fields
            age_str = line[field_specs['age'][0]:field_specs['age'][1]].strip()
            age = int(age_str) if age_str else -1
            
            hispan_str = line[field_specs['hispan'][0]:field_specs['hispan'][1]].strip()
            hispan = int(hispan_str) if hispan_str else 0
            
            bpl_str = line[field_specs['bpl'][0]:field_specs['bpl'][1]].strip()
            bpl = int(bpl_str) if bpl_str else 0
            
            citizen_str = line[field_specs['citizen'][0]:field_specs['citizen'][1]].strip()
            citizen = int(citizen_str) if citizen_str else 0
            
            yrimmig_str = line[field_specs['yrimmig'][0]:field_specs['yrimmig'][1]].strip()
            yrimmig = int(yrimmig_str) if yrimmig_str else 0
            
            empstat_str = line[field_specs['empstat'][0]:field_specs['empstat'][1]].strip()
            empstat = int(empstat_str) if empstat_str else 0
            
            uhrswork_str = line[field_specs['uhrswork'][0]:field_specs['uhrswork'][1]].strip()
            uhrswork = int(uhrswork_str) if uhrswork_str else 0
            
            perwt_str = line[field_specs['perwt'][0]:field_specs['perwt'][1]].strip()
            perwt = float(perwt_str) if perwt_str else 0
            
            # Filter for Hispanic-Mexican birthplace
            # hispan==1 is Mexican, bpl==200 is Mexico
            if hispan != 1 or bpl != 200:
                continue
            
            records.append({
                'year': year,
                'age': age,
                'birthyr': int(line[field_specs['birthyr'][0]:field_specs['birthyr'][1]].strip()) if line[field_specs['birthyr'][0]:field_specs['birthyr'][1]].strip() else 0,
                'hispan': hispan,
                'bpl': bpl,
                'citizen': citizen,
                'yrimmig': yrimmig,
                'empstat': empstat,
                'uhrswork': uhrswork,
                'perwt': perwt / 100.0,  # ACS weights are scaled by 100; divide to get actual weight
            })
        except (ValueError, IndexError):
            continue
    
    df = pd.DataFrame(records)
    return df

def define_daca_eligibility(df):
    """
    Define DACA eligibility based on the criteria:
    - Arrived unlawfully before age 16
    - Had not yet turned 31 as of June 15, 2012
    - Lived continuously in US since June 15, 2007
    - Were not a citizen or legal resident (citizen != 2)
    
    Since we don't have explicit data on unlawful entry or continuous residence,
    we use proxies:
    - Age and year of immigration to infer arrival age
    - Citizenship status to check for legal status
    """
    # DACA eligibility cutoff dates
    # Born before June 15, 1981 (would be 31 on June 15, 2012)
    # Arrived in US before June 15, 2007, before age 16
    
    # We approximate:
    # - Birth year based on age and year of survey
    # - Age at arrival based on yrimmig (year of immigration)
    
    df['birth_year_approx'] = df['year'] - df['age']
    
    # Not yet turned 31 as of June 15, 2012 means birth year >= 1981
    df['age_cutoff_eligible'] = df['birth_year_approx'] >= 1981
    
    # Arrived before age 16 (yrimmig before birth_year + 16)
    df['arrival_age_approx'] = df['yrimmig'] - df['birth_year_approx']
    df['arrival_age_eligible'] = (df['arrival_age_approx'] < 16) & (df['yrimmig'] > 0)
    
    # Not a citizen (citizen == 3 means "not a citizen", 0 is N/A)
    # For DACA eligibility, must not be a citizen or legal resident
    df['legal_status_eligible'] = df['citizen'].isin([3, 4, 5])  # 3=not citizen, 4=first papers, 5=status not reported
    
    # Define DACA treatment variable: eligible if meets all criteria
    df['daca_eligible'] = (
        df['age_cutoff_eligible'] & 
        df['arrival_age_eligible'] & 
        df['legal_status_eligible']
    )
    
    return df

def define_outcome(df):
    """
    Define full-time employment outcome: usually working 35 hours per week or more.
    Uses uhrswork variable (usual hours worked per week).
    """
    df['fulltime'] = df['uhrswork'] >= 35
    return df

def run_analysis(df):
    """
    Estimate the causal effect of DACA eligibility on full-time employment
    using weighted least squares regression.
    
    Model: fulltime = alpha + beta*treatment + gamma*post_daca + 
                      delta*(treatment * post_daca) + year_FE
    
    The interaction term (delta) captures the treatment effect.
    """
    
    # Ensure valid observations
    df = df[(df['uhrswork'] > 0) & (df['empstat'] == 1) & (df['age'] > 0)].copy()
    
    if len(df) == 0:
        return None
    
    # Define treatment indicator: DACA eligibility
    df['treatment'] = df['daca_eligible'].astype(int)
    
    # Define post-DACA period indicator
    # DACA was announced June 15, 2012, applications started Aug 15, 2012
    # Observable effects likely in 2013 onwards
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    
    # Create interaction term
    df['treatment_x_post'] = df['treatment'] * df['post_daca']
    
    # Outcome variable
    df['outcome'] = df['fulltime'].astype(int)
    
    # Get weights and normalize them
    weights = df['perwt'].values
    weights = weights / weights.mean()  # Normalize for numerical stability
    
    # Features for regression
    X = df[['treatment', 'post_daca', 'treatment_x_post']].values
    y = df['outcome'].values
    
    # Add year fixed effects (dummy variables for years 2013-2016)
    year_dummies = pd.get_dummies(df['year'], prefix='year', drop_first=True)
    X = np.column_stack([X, year_dummies.values])
    
    # Add constant
    X = np.column_stack([np.ones(len(X)), X])
    
    # Weighted least squares using matrix algebra without creating diagonal matrix
    # Normal equations: (X'WX)b = X'Wy
    # where W is the weight matrix
    
    # Compute X'WX and X'Wy efficiently
    W_X = X * weights[:, np.newaxis]  # Element-wise multiplication for each row
    XtWX = W_X.T @ X
    Xtwy = W_X.T @ y
    
    try:
        # Solve the normal equations
        beta = np.linalg.solve(XtWX, Xtwy)
    except np.linalg.LinAlgError:
        # If singular, use least squares
        beta, _, _, _ = np.linalg.lstsq(XtWX, Xtwy, rcond=None)
    
    # Extract the treatment effect coefficient
    # Position: 0=constant, 1=treatment, 2=post_daca, 3=treatment_x_post
    treatment_effect = beta[3]
    
    # Calculate standard errors
    predictions = X @ beta
    residuals = y - predictions
    weighted_residuals = residuals * np.sqrt(weights)
    residual_sum_squares = np.sum(weighted_residuals ** 2)
    
    n = len(y)
    k = X.shape[1]
    
    # Variance of residuals
    var_residual = residual_sum_squares / (n - k)
    
    # Variance-covariance matrix
    try:
        XtWX_inv = np.linalg.inv(XtWX)
        var_coef = var_residual * XtWX_inv
        se_treatment_effect = np.sqrt(var_coef[3, 3])
    except:
        se_treatment_effect = np.sqrt(var_residual / n)
    
    # Sample size
    sample_size = len(df)
    
    return {
        'point_estimate': float(treatment_effect),
        'standard_error': float(se_treatment_effect),
        'sample_size': int(sample_size),
        'n_eligible': int(df['treatment'].sum()),
        'n_outcome_1': int(df['outcome'].sum()),
    }

def main():
    # Parse ACS data
    print("Loading ACS data...", flush=True)
    df = parse_acs_fixed_width('ACS_extract_expanded.dat', year_min=2013, year_max=2016)
    
    print(f"Initial sample size: {len(df)}", flush=True)
    
    # Define DACA eligibility
    df = define_daca_eligibility(df)
    
    # Define outcome
    df = define_outcome(df)
    
    print(f"After parsing: {len(df)}", flush=True)
    print(f"DACA eligible in sample: {df['daca_eligible'].sum()}", flush=True)
    print(f"Full-time employed in sample: {df['fulltime'].sum()}", flush=True)
    
    # Check variation in treatment
    treatment_variation = df['daca_eligible'].var()
    if treatment_variation == 0:
        print("ERROR: No variation in treatment variable. Revising specification...", flush=True)
        # Need to revise - this shouldn't happen with proper data
        raise ValueError("No treatment variation")
    
    # Run analysis
    results = run_analysis(df)
    
    if results is None:
        print("ERROR: Analysis failed", flush=True)
        return None
    
    # Define specification JSON
    spec = {
        "sample_selection": [
            "hispan == 1 (Mexican)",
            "bpl == 200 (Mexico)",
            "year >= 2013 and year <= 2016",
            "age > 0 and uhrswork > 0 and empstat == 1",
            "birth_year_approx >= 1981 (not yet 31 as of June 15, 2012)",
            "arrival_age < 16 and yrimmig > 0 (arrived before age 16)",
            "citizen in [3, 4, 5] (not a citizen or status uncertain)"
        ],
        "outcome_definition": "fulltime = (uhrswork >= 35)",
        "treatment_definition": "daca_eligible = (age_cutoff_eligible AND arrival_age_eligible AND legal_status_eligible)",
        "model_specification_line": "model.fit(X_weighted, y_weighted)  # WLS with treatment, post_daca, interaction, and year FE"
    }
    
    output = {
        "spec": spec,
        "results": {
            "point_estimate": results['point_estimate'],
            "standard_error": results['standard_error'],
            "sample_size": results['sample_size']
        }
    }
    
    # Print only JSON to stdout
    print(json.dumps(output))

if __name__ == '__main__':
    main()
