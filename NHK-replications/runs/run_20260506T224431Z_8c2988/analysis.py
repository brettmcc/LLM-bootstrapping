#!/usr/bin/env python3
"""
DACA Impact on Full-Time Employment Analysis
Analyzes the causal impact of DACA eligibility on full-time employment (35+ hours/week)
for ethnically Hispanic-Mexican, Mexican-born individuals in the ACS 2013-2016.
"""

import pandas as pd
import numpy as np
from scipy import stats
import json

# Fixed-width file positions for key variables
FIELD_SPECS = {
    'year': (0, 4),
    'perwt': (691, 701),  # 692-701 in 1-based indexing
    'age': (740, 743),    # 741-743 in 1-based indexing
    'hispan': (763, 764),  # 764-764 in 1-based indexing
    'bpl': (767, 770),     # 768-770 in 1-based indexing
    'citizen': (789, 790), # 790-790 in 1-based indexing
    'empstat': (874, 875), # 875-875 in 1-based indexing
    'uhrswork': (904, 906) # 905-906 in 1-based indexing
}

def read_acs_data(filename):
    """Read fixed-width ACS data file, extracting only needed variables."""
    data = {}
    
    with open(filename, 'r', encoding='latin-1') as f:
        for line_idx, line in enumerate(f):
            try:
                # Parse each field
                year = int(line[FIELD_SPECS['year'][0]:FIELD_SPECS['year'][1]].strip())
                perwt = int(line[FIELD_SPECS['perwt'][0]:FIELD_SPECS['perwt'][1]].strip() or 0)
                age = int(line[FIELD_SPECS['age'][0]:FIELD_SPECS['age'][1]].strip() or 0)
                hispan = int(line[FIELD_SPECS['hispan'][0]:FIELD_SPECS['hispan'][1]].strip() or 0)
                bpl = int(line[FIELD_SPECS['bpl'][0]:FIELD_SPECS['bpl'][1]].strip() or 0)
                citizen = int(line[FIELD_SPECS['citizen'][0]:FIELD_SPECS['citizen'][1]].strip() or 0)
                empstat = int(line[FIELD_SPECS['empstat'][0]:FIELD_SPECS['empstat'][1]].strip() or 0)
                uhrswork_str = line[FIELD_SPECS['uhrswork'][0]:FIELD_SPECS['uhrswork'][1]].strip()
                uhrswork = int(uhrswork_str) if uhrswork_str else 0
                
                # Store record
                record_key = line_idx
                data[record_key] = {
                    'year': year,
                    'perwt': perwt,
                    'age': age,
                    'hispan': hispan,
                    'bpl': bpl,
                    'citizen': citizen,
                    'empstat': empstat,
                    'uhrswork': uhrswork
                }
            except (ValueError, IndexError):
                # Skip malformed lines
                continue
    
    return pd.DataFrame.from_dict(data, orient='index')

def main():
    # Read ACS data
    df = read_acs_data('ACS_extract_expanded.dat')
    
    # Initial sample size
    initial_n = len(df)
    
    # ===== SAMPLE SELECTION FILTERS =====
    # Filter 1: Years 2013-2016 (post-DACA implementation for observing treatment effects)
    df = df[df['year'].isin([2013, 2014, 2015, 2016])]
    
    # Filter 2: Hispanic origin = 1 (Mexican)
    df = df[df['hispan'] == 1]
    
    # Filter 3: Birthplace = 200 (Mexico)
    df = df[df['bpl'] == 200]
    
    # Filter 4: Citizenship status in (3, 4, 5) - noncitizen
    # 3: Not a citizen, 4: Not a citizen but received first papers, 5: Foreign born, status not reported
    df = df[df['citizen'].isin([3, 4, 5])]
    
    # Filter 5: Age must be in range where DACA eligibility can be determined
    # DACA eligibility on June 15, 2012: age 15-30
    # In year Y, this person was age 15-30 in 2012, so their birth year is Y-age+30 to Y-age+15
    # Calculate what age they would have been in 2012:
    # age_in_2012 = age - (year - 2012) = age - year + 2012
    # For DACA eligible: age_in_2012 should be 15-30
    # So: 15 <= age - year + 2012 <= 30
    # Rearranging: age - 15 - 2012 <= -year <= age - 30 - 2012
    # Which gives: year + age - 2012 >= 15 and year + age - 2012 <= 30
    # Actually simpler: just calculate age_in_2012 = age - (year - 2012)
    df['age_in_2012'] = df['age'] - (df['year'] - 2012)
    
    # Keep people who were working-age in 2012 (16-65)
    # This ensures we can identify DACA eligibility vs ineligibility
    df = df[(df['age_in_2012'] >= 16) & (df['age_in_2012'] <= 65)]
    
    # Filter 6: Non-missing employment variables
    df = df[(df['empstat'] != 0) & (df['uhrswork'] >= 0)]
    
    # ===== TREATMENT DEFINITION =====
    # DACA eligible if age was 15-30 on June 15, 2012
    # Since we observe current age, calculate age in 2012 and create eligibility indicator
    df['daca_eligible'] = ((df['age_in_2012'] >= 15) & (df['age_in_2012'] <= 30)).astype(int)
    
    # ===== OUTCOME DEFINITION =====
    # Full-time employment: employed (empstat==1) AND working 35+ hours per week
    df['fulltime_employed'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)
    
    # ===== CHECK TREATMENT VARIATION =====
    treatment_counts = df['daca_eligible'].value_counts()
    if len(treatment_counts) < 2:
        raise ValueError(f"Insufficient treatment variation. Counts: {treatment_counts.to_dict()}")
    
    # ===== PREPARE FOR REGRESSION =====
    # Scale person weights (divide by 100 as per documentation)
    df['weight'] = df['perwt'] / 100.0
    
    # Remove rows with zero or negative weights
    df = df[df['weight'] > 0]
    
    # ===== WEIGHTED LEAST SQUARES REGRESSION =====
    # Model: fulltime_employed = intercept + beta * daca_eligible
    # Weighted by person weight
    # Memory-efficient approach: apply weights directly without creating diagonal matrix
    
    # Create design matrix
    X = df[['daca_eligible']].copy()
    X.insert(0, 'constant', 1.0)
    y = df['fulltime_employed'].values
    w = df['weight'].values
    
    # Convert to numpy arrays
    X_array = X.values
    
    # Apply square root of weights to transform the problem
    # WLS: y* = X* beta + error*, where X* = sqrt(W) @ X, y* = sqrt(W) @ y
    sqrt_w = np.sqrt(w)
    X_weighted = X_array * sqrt_w[:, np.newaxis]  # Element-wise weight multiplication
    y_weighted = y * sqrt_w
    
    # Solve weighted least squares using normal equations
    # (X'WX)^-1 X'Wy = (X*'X*)^-1 X*'y*
    XWX = X_weighted.T @ X_weighted
    XWy = X_weighted.T @ y_weighted
    
    # Solve for coefficients
    beta = np.linalg.solve(XWX, XWy)
    
    # Calculate fitted values and residuals
    y_pred = X_array @ beta
    residuals = y - y_pred
    
    # Calculate standard errors
    # For weighted regression: Var(beta) = sigma^2 * (X'WX)^-1
    df_resid = len(y) - X_array.shape[1]
    
    # Calculate weighted sum of squared residuals
    sse = np.sum(w * residuals**2)
    sigma2 = sse / df_resid
    
    # Variance-covariance matrix
    XWX_inv = np.linalg.inv(XWX)
    var_cov = sigma2 * XWX_inv
    se = np.sqrt(np.diag(var_cov))
    
    # Extract point estimate and standard error for daca_eligible coefficient
    point_estimate = beta[1]  # Index 1 is for daca_eligible (index 0 is constant)
    standard_error = se[1]
    sample_size = len(df)
    
    # ===== PREPARE OUTPUT =====
    spec = {
        "sample_selection": [
            "year in (2013, 2014, 2015, 2016)",
            "hispan == 1 (Mexican)",
            "bpl == 200 (Mexico)",
            "citizen in (3, 4, 5) (noncitizen)",
            "age in 2012 between 16 and 65 (working age)"
        ],
        "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
        "treatment_definition": "(age - (year - 2012) >= 15) & (age - (year - 2012) <= 30)",
        "model_specification_line": "WLS regression: y = const + beta * daca_eligible, weights=perwt/100"
    }
    
    results = {
        "point_estimate": float(point_estimate),
        "standard_error": float(standard_error),
        "sample_size": int(sample_size)
    }
    
    output = {
        "spec": spec,
        "results": results
    }
    
    # Print only the JSON output (no extra text)
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
