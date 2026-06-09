#!/usr/bin/env python
"""
DACA Impact Analysis on Full-Time Employment for Hispanic-Mexican Individuals.

This analysis estimates the causal impact of DACA eligibility on full-time employment
among ethnically Hispanic-Mexican, Mexican-born people in the United States.

Research Question: What was the impact of DACA eligibility on full-time employment
(defined as working 35+ hours per week) for Hispanic-Mexican Mexican-born individuals
in 2013-2016?

Methodology: Logistic regression with DACA eligibility treatment indicator,
state-level controls (unemployment rate, LFPR), and weighted least squares.
"""

import json
import pandas as pd
import numpy as np
import warnings
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings('ignore')

# ============================================================================
# SECTION 1: DATA LOADING AND PARSING
# ============================================================================

def parse_acs_fixed_width():
    """
    Parse the ACS fixed-width data file based on the Stata layout.
    Returns a DataFrame with only the variables we need.
    """
    # Define the columns we need with their position ranges (1-indexed in Stata, 0-indexed in Python)
    # From ACS_extract_expanded_layout_excerpt.do:
    # year: 1-4, statefip: 66-67, pernum: 688-691, perwt: 692-701
    # age: 741-743, hispan: 764-764, bpl: 768-770, citizen: 790-790
    # empstat: 875-875, uhrswork: 905-906
    
    # Convert 1-indexed Stata positions to 0-indexed Python slices
    colspecs = [
        (0, 4),        # year
        (65, 67),      # statefip
        (687, 691),    # pernum
        (691, 701),    # perwt
        (740, 743),    # age
        (763, 764),    # hispan
        (767, 770),    # bpl
        (789, 790),    # citizen
        (874, 875),    # empstat
        (904, 906),    # uhrswork
    ]
    
    names = ['year', 'statefip', 'pernum', 'perwt', 'age', 'hispan', 'bpl', 'citizen', 'empstat', 'uhrswork']
    
    # Read fixed-width file with column specifications
    df = pd.read_fwf(
        'ACS_extract_expanded.dat',
        colspecs=colspecs,
        names=names,
        dtype={
            'year': 'int32',
            'statefip': 'int32',
            'pernum': 'int32',
            'perwt': 'float64',
            'age': 'int32',
            'hispan': 'int32',
            'bpl': 'int32',
            'citizen': 'int32',
            'empstat': 'int32',
            'uhrswork': 'int32',
        }
    )
    
    return df

def load_policy_data():
    """Load state-level policy and labor market data."""
    policy_df = pd.read_csv('policy_labor_market_data.csv')
    # Normalize column names to lowercase
    policy_df.columns = policy_df.columns.str.lower()
    return policy_df

# ============================================================================
# SECTION 2: SAMPLE SELECTION AND FILTERING
# ============================================================================

def create_analysis_sample(acs_df, policy_df):
    """
    Create the analysis sample by applying selection criteria for DACA-eligible population.
    
    Criteria:
    1. Hispanic-Mexican: hispan == 1
    2. Mexican-born: bpl == 200
    3. Not a citizen (CITIZEN in [3, 4, 5] indicates noncitizen status)
    4. Age 16-65 (those who could potentially work)
    5. In years 2013-2016 (post-DACA implementation, 2012)
    6. Employment status is recorded (empstat in [1, 2, 3])
    """
    
    df = acs_df.copy()
    
    # Sample selection filters
    df = df[df['hispan'] == 1]  # Mexican
    df = df[df['bpl'] == 200]   # Mexico-born
    df = df[df['citizen'].isin([3, 4, 5])]  # Non-citizens (3=Not a citizen, 4=First papers, 5=Not reported)
    df = df[(df['age'] >= 16) & (df['age'] <= 65)]  # Working age
    df = df[df['year'].isin([2013, 2014, 2015, 2016])]  # Post-DACA years
    df = df[df['empstat'].isin([1, 2, 3])]  # Valid employment status
    
    # Merge with policy data
    df = df.merge(
        policy_df[['state_fips', 'year', 'lfpr', 'unemp']],
        left_on=['statefip', 'year'],
        right_on=['state_fips', 'year'],
        how='left'
    )
    
    return df

# ============================================================================
# SECTION 3: OUTCOME AND TREATMENT VARIABLE CREATION
# ============================================================================

def create_outcome_variable(df):
    """
    Create outcome variable: Full-time employment (empstat==1 AND uhrswork>=35).
    Returns binary indicator (1 if employed full-time, 0 otherwise).
    """
    # empstat==1 means Employed
    # uhrswork>=35 means usually working 35+ hours per week
    df['fulltime_employed'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)
    return df

def create_treatment_variable(df):
    """
    Create treatment variable for DACA eligibility.
    
    DACA eligible individuals were:
    - Age <= 30 on June 15, 2012
    - Age >= 16 on arrival (assumed before this analysis period)
    - Born between June 1982 and June 1996 (ages 16-30 on June 15, 2012)
    
    Treatment = 1 if person was of DACA-eligible age in 2012 (born 1982-1996).
    """
    # Approximate birth year from age in survey year
    df['birth_year'] = df['year'] - df['age']
    
    # Treatment: Born between 1982 and 1996 (would be ages 16-30 on June 15, 2012)
    df['daca_eligible'] = ((df['birth_year'] >= 1982) & (df['birth_year'] <= 1996)).astype(int)
    
    return df

# ============================================================================
# SECTION 4: ANALYSIS
# ============================================================================

def run_analysis(df):
    """
    Run logistic regression to estimate DACA eligibility impact on full-time employment.
    
    Model: Logistic regression with
    - Outcome: Full-time employment (binary)
    - Treatment: DACA eligibility (binary)
    - Controls: State unemployment rate, state LFPR
    """
    
    # Remove rows with missing outcome, treatment, or control variables
    required_cols = ['fulltime_employed', 'daca_eligible', 'unemp', 'lfpr', 'perwt']
    df_clean = df.dropna(subset=required_cols)
    
    # Check for treatment variation
    treatment_variation = df_clean['daca_eligible'].nunique()
    if treatment_variation < 2:
        raise ValueError(f"No variation in treatment variable. Found {treatment_variation} unique values.")
    
    # Prepare features for regression
    X = df_clean[['daca_eligible', 'unemp', 'lfpr']].copy()
    y = df_clean['fulltime_employed'].copy()
    weights = df_clean['perwt'].copy() / 100  # PERWT has 2 implied decimals
    
    # Normalize control variables for numerical stability
    scaler = StandardScaler()
    controls = scaler.fit_transform(X[['unemp', 'lfpr']])
    X['unemp_scaled'] = controls[:, 0]
    X['lfpr_scaled'] = controls[:, 1]
    X = X[['daca_eligible', 'unemp_scaled', 'lfpr_scaled']]
    
    # Run weighted logistic regression
    model = LogisticRegression(
        fit_intercept=True,
        max_iter=1000,
        random_state=42
    )
    
    # Fit with sample weights
    model.fit(X, y, sample_weight=weights)
    
    # Get predictions and residuals for standard error calculation
    y_pred_proba = model.predict_proba(X)[:, 1]
    
    # Calculate residuals
    residuals = y - y_pred_proba
    
    # Calculate weighted standard error using sandwich estimator approach
    n = len(y)
    weighted_residuals_sq = (residuals ** 2) * weights
    var_estimate = np.sum(weighted_residuals_sq) / (n ** 2)
    
    # Standard error for the treatment coefficient
    se_treatment = np.sqrt(var_estimate)
    
    # Extract coefficient for DACA eligibility (point estimate)
    point_estimate = model.coef_[0][0]
    
    # Sample size (actual observations used)
    sample_size = len(y)
    
    return {
        'point_estimate': float(point_estimate),
        'standard_error': float(se_treatment),
        'sample_size': int(sample_size)
    }

# ============================================================================
# SECTION 5: SPECIFICATION DOCUMENTATION
# ============================================================================

def create_specification_dict():
    """Create the specification dictionary for output."""
    spec = {
        "sample_selection": [
            "hispan == 1 (Mexican ethnicity)",
            "bpl == 200 (Mexican-born)",
            "citizen in [3, 4, 5] (non-citizen status)",
            "age between 16 and 65",
            "year in [2013, 2014, 2015, 2016] (post-DACA implementation)"
        ],
        "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
        "treatment_definition": "birth_year in [1982, 1996] (would be age 16-30 on June 15, 2012)",
        "model_specification_line": "LogisticRegression(model.fit(X, y, sample_weight=perwt/100)) with X=[daca_eligible, scaled_unemp, scaled_lfpr]"
    }
    return spec

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    # Load data
    acs_df = parse_acs_fixed_width()
    policy_df = load_policy_data()
    
    # Create analysis sample
    sample_df = create_analysis_sample(acs_df, policy_df)
    
    # Create outcome variable
    sample_df = create_outcome_variable(sample_df)
    
    # Create treatment variable
    sample_df = create_treatment_variable(sample_df)
    
    # Run analysis
    results = run_analysis(sample_df)
    
    # Create specification
    spec = create_specification_dict()
    
    # Prepare output JSON
    output = {
        "spec": spec,
        "results": {
            "point_estimate": results['point_estimate'],
            "standard_error": results['standard_error'],
            "sample_size": results['sample_size']
        }
    }
    
    # Print JSON output to stdout (only this output)
    print(json.dumps(output))

if __name__ == '__main__':
    main()
