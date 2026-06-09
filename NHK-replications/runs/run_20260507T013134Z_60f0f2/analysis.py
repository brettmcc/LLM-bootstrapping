#!/usr/bin/env python3
"""
DACA Impact Analysis: Effect on Full-Time Employment for Mexican-Born Non-Citizens
Uses chunked reading and memory-efficient weighted OLS.
"""

import pandas as pd
import numpy as np

def read_acs_fixed_width_chunked(filepath, chunksize=100000):
    """
    Read ACS fixed-width data file in chunks.
    Only loads necessary columns and filters early to conserve memory.
    """
    colspecs = [
        (0, 4),        # year
        (691, 701),    # perwt
        (740, 743),    # age
        (763, 764),    # hispan
        (767, 770),    # bpl
        (789, 790),    # citizen
        (874, 875),    # empstat
        (904, 906),    # uhrswork
    ]
    
    names = ['year', 'perwt', 'age', 'hispan', 'bpl', 'citizen', 'empstat', 'uhrswork']
    
    # Read all chunks and filter early
    chunks = []
    for chunk in pd.read_fwf(filepath, colspecs=colspecs, names=names, header=None, chunksize=chunksize):
        # Divide perwt by 100
        chunk['perwt'] = chunk['perwt'] / 100.0
        
        # Filter for sample criteria
        filtered = chunk[
            (chunk['hispan'] == 1) &  # Mexican ethnicity
            (chunk['bpl'] == 200) &   # Mexican-born
            (chunk['citizen'].isin([3, 4, 5])) &  # Non-citizen
            (chunk['year'] >= 2013) & (chunk['year'] <= 2016)  # Post-DACA
        ].copy()
        
        if len(filtered) > 0:
            chunks.append(filtered)
    
    if not chunks:
        raise ValueError("No data matched sample criteria")
    
    return pd.concat(chunks, ignore_index=True)

def create_indicators(df):
    """Create outcome and treatment indicators"""
    
    # Outcome: Full-time employment (35+ hours/week)
    df['fulltime'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)
    
    # Treatment: DACA eligible (age 16-31 in survey year)
    df['DACA_eligible'] = ((df['age'] >= 16) & (df['age'] <= 31)).astype(int)
    
    # Year effects
    df['year_2013'] = (df['year'] == 2013).astype(int)
    df['year_2014'] = (df['year'] == 2014).astype(int)
    df['year_2015'] = (df['year'] == 2015).astype(int)
    df['year_2016'] = (df['year'] == 2016).astype(int)
    
    # Center age
    df['age_centered'] = df['age'] - df['age'].mean()
    
    return df

def fit_model(df):
    """Fit weighted OLS model without creating large diagonal matrix"""
    
    # Prepare data
    model_data = df[['fulltime', 'DACA_eligible', 'age_centered', 'year_2013', 
                      'year_2014', 'year_2015', 'perwt']].dropna()
    
    if len(model_data) == 0:
        raise ValueError("No valid data for model")
    
    # Extract variables
    y = model_data['fulltime'].values
    X = model_data[['DACA_eligible', 'age_centered', 'year_2013', 'year_2014', 'year_2015']].values
    weights = model_data['perwt'].values
    
    # Add constant
    X = np.column_stack([np.ones(len(X)), X])
    n = len(y)
    k = X.shape[1]
    
    # Compute weighted OLS using normal equations
    # (X'WX)^-1 X'Wy where W is diagonal weight matrix
    # To avoid creating W explicitly, compute weighted sums directly
    
    # Weighted X'X
    sqrt_w = np.sqrt(weights)
    X_weighted = X * sqrt_w[:, np.newaxis]  # Multiply each row by sqrt(weight)
    XtWX = X_weighted.T @ X_weighted
    
    # Weighted X'y
    y_weighted = y * sqrt_w
    XtWy = X_weighted.T @ y_weighted
    
    # Solve normal equations
    beta = np.linalg.solve(XtWX, XtWy)
    
    # Calculate residuals and standard errors
    y_pred = X @ beta
    residuals = y - y_pred
    
    # Residual sum of squares (weighted)
    rss = np.sum((residuals ** 2) * weights)
    df_resid = n - k
    sigma_sq = rss / df_resid
    
    # Variance-covariance matrix
    var_cov = sigma_sq * np.linalg.inv(XtWX)
    se = np.sqrt(np.diag(var_cov))
    
    return {
        'point_estimate': float(beta[1]),
        'standard_error': float(se[1]),
        'sample_size': int(n)
    }

def main():
    """Main analysis"""
    
    # Read data
    df = read_acs_fixed_width_chunked('ACS_extract_expanded.dat')
    
    # Create indicators
    df = create_indicators(df)
    
    # Check treatment variation
    if df['DACA_eligible'].sum() == 0 or df['DACA_eligible'].sum() == len(df):
        raise ValueError("No treatment variation")
    
    # Fit model
    results = fit_model(df)
    
    # Output JSON
    import json
    print(json.dumps(results))

if __name__ == '__main__':
    main()
