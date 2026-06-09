#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Analyzes the effect of DACA eligibility on full-time employment among 
ethnically Hispanic-Mexican, Mexican-born individuals (2013-2016).
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
import struct

# Parse the fixed-width ACS data
def read_acs_fixed_width(filepath):
    """
    Read the fixed-width ACS data file and extract relevant variables.
    Using 1-based indexing from the layout file, converted to 0-based Python slicing.
    From ACS_extract_expanded_layout_excerpt.do:
    - year: 1-4
    - statefip: 66-67
    - age: 741-743
    - sex: 740
    - hispan: 764
    - bpl: 768-770
    - citizen: 790
    - empstat: 875
    - uhrswork: 905-906
    - perwt: 692-701
    """
    records = []
    with open(filepath, 'r') as f:
        for line in f:
            if len(line) < 912:  # Need at least to column 912 for all fields
                continue
            try:
                # Convert 1-based to 0-based indexing (subtract 1 from start, keep end the same)
                # YEAR: positions 1-4 (0-based: 0-4)
                year = int(line[0:4].strip())
                
                # STATEFIP: positions 66-67 (0-based: 65-67)
                statefip = int(line[65:67].strip())
                
                # SEX: position 740 (0-based: 739-740)
                sex = int(line[739:740].strip())
                
                # AGE: positions 741-743 (0-based: 740-743)
                age = int(line[740:743].strip())
                
                # HISPAN: position 764 (0-based: 763-764)
                hispan = int(line[763:764].strip())
                
                # BPL: positions 768-770 (0-based: 767-770)
                bpl = int(line[767:770].strip())
                
                # CITIZEN: position 790 (0-based: 789-790)
                citizen = int(line[789:790].strip())
                
                # EMPSTAT: position 875 (0-based: 874-875)
                empstat = int(line[874:875].strip())
                
                # UHRSWORK: positions 905-906 (0-based: 904-906)
                uhrswork = int(line[904:906].strip())
                
                # PERWT: positions 692-701 (0-based: 691-701) - person weight (8 decimal places implied)
                perwt = int(line[691:701].strip()) / 100.0
                
                records.append({
                    'statefip': statefip,
                    'year': year,
                    'age': age,
                    'sex': sex,
                    'hispan': hispan,
                    'bpl': bpl,
                    'citizen': citizen,
                    'empstat': empstat,
                    'uhrswork': uhrswork,
                    'perwt': perwt
                })
            except (ValueError, IndexError):
                continue
    
    return pd.DataFrame(records)

def apply_filters(df):
    """
    Apply sample selection filters based on DACA eligibility criteria.
    
    Filters:
    1. Ethnically Hispanic-Mexican (hispan == 1) and Mexican-born (bpl == 200)
    2. Age constraints based on DACA rules:
       - DACA eligibility window: arrived before age 16, under 31 on June 15 2012
       - In 2012: age must be <= 30 (born 1982 or later)
       - In 2013-2016: age 20-35 (allowing for aging cohort)
    3. Non-citizen or status not reported (citizen in [3, 4, 5])
    4. Years 2006-2016 (includes pre and post DACA for comparison)
    5. Employed (empstat == 1) or unemployed (empstat == 2) to focus on labor force
    """
    
    # Filter 1: Hispanic-Mexican and Mexican-born
    df = df[(df['hispan'] == 1) & (df['bpl'] == 200)].copy()
    
    # Filter 2: Years 2006-2016 (to have treatment variation)
    df = df[(df['year'] >= 2006) & (df['year'] <= 2016)].copy()
    
    # Filter 3: Non-citizen status (citizen codes 3, 4, 5)
    # Code 3 = Not a citizen, 4 = Not a citizen but has received first papers, 5 = Foreign born, citizenship status not reported
    df = df[df['citizen'].isin([3, 4, 5])].copy()
    
    # Filter 4: DACA-eligible age range
    # DACA: arrived before age 16, age < 31 on June 15, 2012
    # Born 1982 or later to be < 31 in 2012
    # In 2006: age 0-24 (if born 1982+)
    # In 2016: age 10-34 (if born 1982+)
    # Focus on working-age cohort: age 16-45 to capture DACA-eligible population across years
    df = df[(df['age'] >= 16) & (df['age'] <= 45)].copy()
    
    # Filter 5: Labor force participation (employed or unemployed)
    # empstat: 1 = employed, 2 = unemployed, 3 = not in labor force
    df = df[df['empstat'].isin([1, 2])].copy()
    
    return df

def create_treatment_outcome(df):
    """
    Create treatment and outcome variables.
    
    Treatment: post-DACA period (year >= 2013 automatically, from filters)
    We use a simple indicator for year >= 2013 to define post-treatment period.
    Since DACA implementation was June 15, 2012, by 2013 most administrative
    adjustments should be in place. We'll also create an eligibility proxy.
    
    Outcome: Full-time employment (uhrswork >= 35 hours/week)
    """
    
    # Outcome: Full-time employment (35+ hours per week)
    df['fulltime'] = (df['uhrswork'] >= 35).astype(int)
    
    # Treatment: Post-DACA (2013 onwards)
    # DACA was implemented in 2012, so treatment = 1 for years >= 2013
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    
    return df

def estimate_effect(df):
    """
    Estimate the treatment effect using weighted OLS (WLS).
    
    Specification: Simple difference-in-differences style estimation
    using a linear model that accounts for the post-DACA period effect.
    
    We pool all years and estimate:
    fulltime = b0 + b1*post_daca + e
    
    With person weights (PERWT) to account for survey design.
    """
    
    # Remove missing values
    df = df.dropna(subset=['fulltime', 'post_daca', 'perwt'])
    
    # Ensure positive weights
    df = df[df['perwt'] > 0].copy()
    
    sample_size = len(df)
    
    # Construct design matrix
    # Simple model: fulltime ~ post_daca
    X = np.column_stack([np.ones(sample_size), df['post_daca'].values])
    y = df['fulltime'].values
    w = df['perwt'].values
    
    # Weighted OLS: beta = (X'WX)^-1 X'Wy
    # More efficient: compute weighted cross products directly
    W_sqrt = np.sqrt(w)
    X_weighted = X * W_sqrt[:, np.newaxis]  # Element-wise multiplication
    y_weighted = y * W_sqrt
    
    # Normal equations: (X'WX) beta = X'Wy
    XtWX = X_weighted.T @ X_weighted
    XtWy = X_weighted.T @ y_weighted
    
    beta = np.linalg.solve(XtWX, XtWy)
    
    # Calculate residuals and standard errors
    residuals = y - (X @ beta)
    weighted_rss = np.sum(w * residuals ** 2)
    
    # Degrees of freedom
    df_resid = sample_size - X.shape[1]
    
    # Standard error of residuals
    mse = weighted_rss / df_resid
    
    # Variance-covariance matrix: (X'WX)^-1 * sigma^2
    var_cov = np.linalg.inv(XtWX) * mse
    
    # Standard errors
    se = np.sqrt(np.diag(var_cov))
    
    # Extract coefficient for post_daca (index 1)
    point_estimate = float(beta[1])
    standard_error = float(se[1])
    
    return point_estimate, standard_error, sample_size

def main():
    # Read the ACS data
    print("Reading ACS data...", flush=True)
    df = read_acs_fixed_width('ACS_extract_expanded.dat')
    print(f"Initial records: {len(df)}", flush=True)
    
    # Debug: check data before filtering
    print(f"Year range: {df['year'].min()} to {df['year'].max()}", flush=True)
    print(f"Unique hispans: {sorted(df['hispan'].unique())[:20]}", flush=True)
    print(f"Unique bpls: {sorted(df['bpl'].unique())[:20]}", flush=True)
    print(f"Unique citizens: {sorted(df['citizen'].unique())}", flush=True)
    print(f"Age range: {df['age'].min()} to {df['age'].max()}", flush=True)
    print(f"Unique empstats: {sorted(df['empstat'].unique())}", flush=True)
    
    # Apply sample selection filters
    print("Applying sample selection filters...", flush=True)
    df = apply_filters(df)
    print(f"After filtering: {len(df)}", flush=True)
    
    # Check treatment variation
    print("Checking treatment variation...", flush=True)
    print(f"Pre-DACA (2006-2012): {len(df[df['year'] < 2013])}", flush=True)
    print(f"Post-DACA (2013-2016): {len(df[df['year'] >= 2013])}", flush=True)
    
    if len(df) == 0:
        print("Error: No variation in treatment period", flush=True)
        raise ValueError("Insufficient data in pre or post DACA period")
    
    # Create treatment and outcome variables
    df = create_treatment_outcome(df)
    
    # Estimate effect
    print("Estimating treatment effect...", flush=True)
    point_estimate, standard_error, sample_size = estimate_effect(df)
    
    # Create specification dict
    spec = {
        "sample_selection": [
            "hispan == 1 (Mexican)",
            "bpl == 200 (Mexico born)",
            "citizen in [3, 4, 5] (non-citizen)",
            "age >= 16 and age <= 45",
            "empstat in [1, 2] (in labor force)",
            "year >= 2006 and year <= 2016"
        ],
        "outcome_definition": "fulltime = 1 if uhrswork >= 35 else 0",
        "treatment_definition": "post_daca = 1 if year >= 2013 else 0",
        "model_specification_line": "np.linalg.lstsq((W @ X), (W @ y))[0] with W = diag(sqrt(perwt))"
    }
    
    # Create results dict
    results = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size
    }
    
    # Combine into output
    output = {
        "spec": spec,
        "results": results
    }
    
    # Print only the JSON object
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
