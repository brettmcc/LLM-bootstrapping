#!/usr/bin/env python3
"""
DACA Effect on Full-Time Employment Analysis
Implements a difference-in-differences specification to estimate the causal
effect of DACA eligibility on full-time employment probability.
"""

import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

# Fixed-width format specifications from ACS_extract_expanded_layout_excerpt.do
# Format: (name, start_col, end_col, dtype)
# Note: columns are 1-based in the .do file, convert to 0-based for Python slicing
ACS_FIELDS = {
    'year': (0, 4, int),
    'statefip': (65, 67, int),
    'sex': (739, 740, int),
    'age': (740, 743, int),
    'birthyr': (747, 751, int),
    'hispan': (763, 764, int),
    'bpl': (767, 770, int),
    'citizen': (789, 790, int),
    'yrimmig': (794, 798, int),
    'empstat': (874, 875, int),
    'uhrswork': (904, 906, int),
    'perwt': (691, 701, int),
}

def read_acs_fixed_width(filename, fields, max_rows=None):
    """
    Read ACS fixed-width data file, extracting only specified fields.
    Implements chunked reading to manage memory with large files.
    """
    data = {name: [] for name in fields.keys()}
    
    with open(filename, 'rb') as f:
        chunk_size = 50000
        row_count = 0
        
        while True:
            # Read chunk of data
            chunk = []
            for _ in range(chunk_size):
                line = f.readline()
                if not line:
                    break
                chunk.append(line)
            
            if not chunk:
                break
            
            # Parse records in chunk
            for line in chunk:
                if isinstance(line, bytes):
                    line = line.decode('utf-8', errors='ignore')
                
                # Extract fields using fixed-width positions
                record = {}
                for name, (start, end, dtype) in fields.items():
                    try:
                        value_str = line[start:end].strip()
                        if value_str == '':
                            record[name] = np.nan
                        else:
                            record[name] = dtype(value_str)
                    except (ValueError, IndexError):
                        record[name] = np.nan
                
                # Append to data lists
                for name in fields.keys():
                    data[name].append(record[name])
                
                row_count += 1
                if max_rows and row_count >= max_rows:
                    break
            
            if max_rows and row_count >= max_rows:
                break
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

def create_daca_variables(df):
    """
    Create treatment and outcome variables for DACA analysis.
    
    Treatment: DACA eligibility
    - Mexican-born (bpl == 200)
    - Ethnically Hispanic-Mexican (hispan == 1)
    - Age at DACA implementation (June 15, 2012): 15-30 years old
      (born 1982-1997, i.e., birthyr in [1982, 1997])
    - Presumed noncitizen status (citizen in [3, 4, 5])
    
    Outcome: Full-time employment
    - Working 35+ hours per week (uhrswork >= 35)
    - Must be employed (empstat == 1)
    """
    
    # Calculate age at DACA implementation (June 15, 2012)
    age_at_daca = 2012 - df['birthyr']
    
    # Treatment: DACA eligible
    # Must be Mexican-born, Hispanic-Mexican, eligible age, and noncitizen status
    df['daca_eligible'] = (
        (df['bpl'] == 200) &  # Born in Mexico
        (df['hispan'] == 1) &  # Ethnically Mexican
        (age_at_daca >= 15) & (age_at_daca <= 30) &  # Eligible age at DACA
        (df['citizen'].isin([3, 4, 5]))  # Noncitizen or status not reported
    ).astype(int)
    
    # Outcome: Full-time employment (35+ hours per week AND employed)
    df['fulltime'] = (
        (df['empstat'] == 1) &  # Employed
        (df['uhrswork'] >= 35)  # 35+ hours per week
    ).astype(int)
    
    # Post-DACA period indicator (2013-2016)
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    
    # Interaction term for DD
    df['eligible_x_post'] = df['daca_eligible'] * df['post_daca']
    
    return df

def estimate_dd_model(df):
    """
    Estimate difference-in-differences model using OLS (linear probability model).
    Model: fulltime = β0 + β1*daca_eligible + β2*post_daca + β3*eligible_x_post
    
    Uses memory-efficient weighted regression that avoids creating large diagonal matrices.
    """
    from scipy import stats
    
    # Filter to population of interest (Mexican-born, Hispanic, working age)
    # Keep both eligible and ineligible for comparison
    analysis_sample = df[
        (df['bpl'] == 200) &  # Mexican-born
        (df['hispan'] == 1) &  # Hispanic-Mexican
        (df['age'] >= 16) & (df['age'] <= 40) &  # Working age window
        (df['year'].isin([2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016])) &  # Pre and post-DACA
        (df['empstat'].isin([1, 2])) &  # Employed or unemployed
        (~df['uhrswork'].isna()) &  # Have hours worked info
        (~df['perwt'].isna())  # Have weights
    ].copy()
    
    print(f"Analysis sample size: {len(analysis_sample)}")
    print(f"DACA eligible: {analysis_sample['daca_eligible'].sum()}")
    print(f"Outcome variation in eligible: {analysis_sample[analysis_sample['daca_eligible']==1]['fulltime'].mean():.4f}")
    print(f"Outcome variation in ineligible: {analysis_sample[analysis_sample['daca_eligible']==0]['fulltime'].mean():.4f}")
    
    # Check for treatment variation
    if analysis_sample['daca_eligible'].sum() == 0:
        raise ValueError("No DACA-eligible individuals in analysis sample")
    
    # Normalize weights
    weights = analysis_sample['perwt'].values / 100.0
    sqrt_w = np.sqrt(weights)
    
    # Prepare model data
    X = analysis_sample[['daca_eligible', 'post_daca', 'eligible_x_post']].values
    y = analysis_sample['fulltime'].values
    
    # Add constant
    X = np.column_stack([np.ones(len(X)), X])
    
    # Transform data by sqrt(weights) for WLS
    # This avoids creating a large diagonal weight matrix
    X_weighted = X * sqrt_w[:, np.newaxis]
    y_weighted = y * sqrt_w
    
    # Standard OLS on weighted data: (X'X)^-1 X'y
    XtX = X_weighted.T @ X_weighted
    Xty = X_weighted.T @ y_weighted
    
    try:
        beta = np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        print("Warning: Singular matrix in WLS. Using pseudo-inverse.")
        beta = np.linalg.pinv(XtX) @ Xty
    
    # Calculate residuals and standard errors
    y_pred = X @ beta
    residuals = y - y_pred
    weighted_residuals = residuals * sqrt_w
    
    # Residual sum of squares (weighted)
    rss = np.sum(weighted_residuals**2)
    
    # Degrees of freedom
    n = len(y)
    k = X.shape[1]
    dof = n - k
    
    # Variance of residuals
    sigma_sq = rss / dof
    
    # Variance-covariance matrix
    try:
        var_cov = sigma_sq * np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        var_cov = sigma_sq * np.linalg.pinv(XtX)
    
    # Standard errors
    se = np.sqrt(np.diag(var_cov))
    
    # DD coefficient (eligible_x_post interaction)
    dd_coef = beta[3]
    dd_se = se[3]
    
    results = {
        'point_estimate': float(dd_coef),
        'standard_error': float(dd_se),
        'sample_size': int(len(analysis_sample)),
        'coefficients': {
            'intercept': float(beta[0]),
            'daca_eligible': float(beta[1]),
            'post_daca': float(beta[2]),
            'eligible_x_post': float(beta[3])
        },
        'standard_errors': {
            'intercept': float(se[0]),
            'daca_eligible': float(se[1]),
            'post_daca': float(se[2]),
            'eligible_x_post': float(se[3])
        }
    }
    
    return results

def main():
    """Main analysis workflow."""
    
    # Read ACS data
    df = read_acs_fixed_width('ACS_extract_expanded.dat', ACS_FIELDS)
    
    # Create analysis variables
    df = create_daca_variables(df)
    
    # Verify treatment variation
    n_eligible = df['daca_eligible'].sum()
    
    if n_eligible == 0:
        raise ValueError("No DACA-eligible individuals found in dataset. Check variable definitions.")
    
    # Estimate DD model
    results = estimate_dd_model(df)
    
    # Output results as JSON
    print(json.dumps(results))
    
    return results

if __name__ == '__main__':
    results = main()
