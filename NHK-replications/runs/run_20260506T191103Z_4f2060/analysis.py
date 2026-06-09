#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Research Question: Among ethnically Hispanic-Mexican, Mexican-born people living 
in the US, what was the causal impact of DACA eligibility on full-time employment 
probability (35+ hours per week) in 2013-2016?
"""

import pandas as pd
import numpy as np
import json
from scipy import stats

def parse_acs_fixed_width():
    """
    Parse the fixed-width ACS data file.
    Uses 1-based indexing from the layout file.
    """
    # Define key columns based on ACS_extract_expanded_layout_excerpt.do
    col_specs = {
        'year': (0, 4),           # 1-4 (0-3 in 0-based)
        'pernum': (687, 691),     # 688-691 (687-690 in 0-based)
        'perwt': (691, 701),      # 692-701 (691-700 in 0-based)
        'statefip': (65, 67),     # 66-67 (65-66 in 0-based)
        'sex': (739, 740),        # 740 (739 in 0-based)
        'age': (740, 743),        # 741-743 (740-742 in 0-based)
        'birthqtr': (745, 746),   # 746 (745 in 0-based)
        'birthyr': (747, 751),    # 748-751 (747-750 in 0-based)
        'hispan': (763, 764),     # 764 (763 in 0-based)
        'bpl': (767, 770),        # 768-770 (767-769 in 0-based)
        'citizen': (789, 790),    # 790 (789 in 0-based)
        'yrimmig': (794, 798),    # 795-798 (794-797 in 0-based)
        'empstat': (874, 875),    # 875 (874 in 0-based)
        'labforce': (877, 878),   # 878 (877 in 0-based)
        'uhrswork': (904, 906),   # 905-906 (904-905 in 0-based)
    }
    
    # Read fixed-width file
    print("Reading ACS data file...", flush=True)
    df = pd.read_fwf(
        'ACS_extract_expanded.dat',
        colspecs=list(col_specs.values()),
        names=list(col_specs.keys()),
        dtype={
            'year': 'int16',
            'pernum': 'int16',
            'perwt': 'float64',
            'statefip': 'int8',
            'sex': 'int8',
            'age': 'int16',
            'birthqtr': 'int8',
            'birthyr': 'int16',
            'hispan': 'int8',
            'bpl': 'int16',
            'citizen': 'int8',
            'yrimmig': 'int16',
            'empstat': 'int8',
            'labforce': 'int8',
            'uhrswork': 'int8',
        }
    )
    
    return df

def load_policy_data():
    """Load state-level policy data."""
    print("Loading policy data...", flush=True)
    policy = pd.read_csv('policy_labor_market_data.csv')
    # Normalize column names to lowercase
    policy.columns = policy.columns.str.lower()
    return policy

def create_daca_treatment(row):
    """
    Create DACA treatment indicator.
    
    DACA eligibility criteria (as of June 15, 2012):
    1. Arrived unlawfully before 16th birthday
    2. Not yet 31 years old (born after June 15, 1981)
    3. Lived continuously in US since June 15, 2007
    4. Present in US on June 15, 2012 without lawful status
    
    Operationalized from ACS data:
    - Birth year: born after 1981 (so age < 31 on June 15, 2012)
    - Birthplace: BPL == 200 (Mexico) indicates likely unlawful arrival
    - Citizenship: citizen == 3 (not a citizen) at survey time
    - Immigration year: yrimmig <= 2007 (arrived by June 2007)
    """
    # Age condition: not yet 31 on June 15, 2012
    # If born in 1982 or later, would be <= 30 on June 15, 2012
    if row['birthyr'] <= 1981:
        return 0
    
    # Birthplace: Mexico (code 200)
    if row['bpl'] != 200:
        return 0
    
    # Citizenship: not a citizen (code 3) or status not reported (code 5)
    if row['citizen'] not in [3, 5]:
        return 0
    
    # Continuous residence: immigration year <= 2007
    if row['yrimmig'] > 2007 or row['yrimmig'] == 0:
        return 0
    
    return 1

def create_fulltime_outcome(row):
    """
    Create full-time employment outcome.
    Full-time: 35+ hours per week.
    """
    # uhrswork values: 00 (N/A), 01-99 (hours)
    # Valid employment hours: 1-99
    if row['uhrswork'] >= 35 and row['uhrswork'] <= 99:
        return 1
    return 0

def main():
    # Load data
    acs = parse_acs_fixed_width()
    policy = load_policy_data()
    
    print(f"Loaded ACS data: {len(acs)} rows", flush=True)
    print(f"Loaded policy data: {len(policy)} rows", flush=True)
    
    # Filter to years 2013-2016 (post-DACA implementation)
    acs = acs[acs['year'].isin([2013, 2014, 2015, 2016])]
    print(f"After year filter (2013-2016): {len(acs)} rows", flush=True)
    
    # Sample selection filters:
    # 1. Hispanic ethnicity (hispan == 1)
    acs = acs[acs['hispan'] == 1]
    print(f"After Hispanic filter: {len(acs)} rows", flush=True)
    
    # 2. Mexican-born (bpl == 200)
    acs = acs[acs['bpl'] == 200]
    print(f"After Mexican-born filter: {len(acs)} rows", flush=True)
    
    # 3. Age constraints: born 1968-1996 to be DACA-eligible
    # (born before June 15, 1996 AND not yet 31 on June 15, 2012)
    acs = acs[(acs['birthyr'] >= 1968) & (acs['birthyr'] <= 1996)]
    print(f"After age filter: {len(acs)} rows", flush=True)
    
    # 4. In labor force or employed
    acs = acs[acs['labforce'].isin([2])]  # Yes, in labor force
    print(f"After labor force filter: {len(acs)} rows", flush=True)
    
    # 5. Non-missing employment hours
    acs = acs[(acs['uhrswork'] > 0) & (acs['uhrswork'] <= 99)]
    print(f"After non-missing hours filter: {len(acs)} rows", flush=True)
    
    # Create treatment variable (DACA eligibility)
    acs['daca_eligible'] = acs.apply(create_daca_treatment, axis=1)
    print(f"DACA eligible count: {acs['daca_eligible'].sum()}", flush=True)
    
    # Check treatment variation
    if acs['daca_eligible'].sum() == 0 or acs['daca_eligible'].sum() == len(acs):
        print("ERROR: No treatment variation", flush=True)
        return None
    
    # Create outcome variable (full-time employment)
    acs['fulltime'] = acs.apply(create_fulltime_outcome, axis=1)
    print(f"Full-time employed count: {acs['fulltime'].sum()}", flush=True)
    
    # Merge with policy data
    acs = acs.merge(
        policy[['state_fips', 'year']],
        left_on=['statefip', 'year'],
        right_on=['state_fips', 'year'],
        how='left'
    )
    
    # Remove any with missing merge
    acs = acs.dropna(subset=['state_fips'])
    print(f"After policy merge: {len(acs)} rows", flush=True)
    
    # Create interaction for DiD
    acs['post'] = (acs['year'] >= 2012).astype(int)  # Post-DACA implementation
    
    # Prepare for regression
    # Use weighted least squares (WLS) with person weights
    # Model: fulltime = b0 + b1*daca_eligible + b2*post + b3*daca_eligible*post + weights
    
    # Create design matrix with explicit column construction
    daca_eligible = acs['daca_eligible'].values.astype(float)
    post = acs['post'].values.astype(float)
    interaction = daca_eligible * post
    const = np.ones(len(acs))
    
    X = np.column_stack([const, daca_eligible, post, interaction])
    y = acs['fulltime'].values.astype(float)
    weights = acs['perwt'].values / 100.0  # ACS weights are scaled by 100
    
    # Weighted regression using statsmodels
    try:
        import statsmodels.api as sm
        
        # Use statsmodels WLS
        wls_model = sm.WLS(y, X, weights=weights)
        results = wls_model.fit()
        
        # Extract coefficients and standard errors
        beta = results.params
        std_errors = results.bse
        
        point_estimate = beta[3]  # interaction coefficient
        standard_error = std_errors[3]
        sample_size = len(y)
        
    except Exception as e:
        print(f"Statsmodels WLS failed: {e}, using manual WLS", flush=True)
        
        # Manual WLS calculation with better numerical stability
        from numpy.linalg import lstsq
        
        # Construct weighted X and y: sqrt(w) * X and sqrt(w) * y
        sqrt_weights = np.sqrt(weights)
        X_weighted = X * sqrt_weights[:, np.newaxis]
        y_weighted = y * sqrt_weights
        
        # Use least squares
        beta, residuals_sum, rank, s = lstsq(X_weighted, y_weighted, rcond=None)
        
        # Calculate residuals
        y_pred = X @ beta
        residuals = y - y_pred
        
        # Weighted residual sum of squares
        rss = np.sum(weights * residuals**2)
        
        # Degrees of freedom
        n = len(y)
        k = X.shape[1]
        dof = n - k
        
        # Mean squared error
        mse = rss / dof
        
        # For standard errors, use the design matrix approach
        from numpy.linalg import inv
        X_t = X.T
        W = np.diag(weights)
        
        # Weighted cross product with better conditioning
        XtWX = X_t @ W @ X
        
        # Use lstsq to solve instead of explicit inversion
        var_cov_inv = np.linalg.lstsq(np.eye(len(XtWX)), XtWX, rcond=None)[0]
        
        # More stable calculation of standard errors
        # For WLS: var(beta) = mse * (X'WX)^-1
        try:
            from scipy.linalg import inv as scipy_inv
            var_cov = mse * scipy_inv(XtWX)
            std_errors = np.sqrt(np.diag(var_cov))
        except:
            # If inversion fails, use generalized inverse
            var_cov = mse * np.linalg.pinv(XtWX)
            std_errors = np.sqrt(np.maximum(np.diag(var_cov), 0))
        
        point_estimate = beta[3]
        standard_error = std_errors[3]
        sample_size = n
    
    print(f"\n=== RESULTS ===", flush=True)
    print(f"Coefficient (interaction): {point_estimate:.6f}", flush=True)
    print(f"Standard Error: {standard_error:.6f}", flush=True)
    print(f"Sample Size: {sample_size}", flush=True)
    
    # Output results
    results = {
        "point_estimate": float(point_estimate),
        "standard_error": float(standard_error),
        "sample_size": int(sample_size)
    }
    
    # Print JSON to stdout
    print(json.dumps(results))
    
    return results

if __name__ == "__main__":
    main()
