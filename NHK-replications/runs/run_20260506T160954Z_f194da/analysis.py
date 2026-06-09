#!/usr/bin/env python3
"""
DACA Full-Time Employment Analysis
Estimates the effect of DACA eligibility on full-time employment probability
for Hispanic-Mexican individuals born in Mexico.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

# Fixed-width data specification based on ACS_extract_expanded_layout_excerpt.do
FIELD_SPECS = {
    'year': (0, 4),
    'statefip': (65, 67),
    'perwt': (691, 701),
    'age': (740, 743),
    'hispan': (763, 764),
    'bpl': (767, 770),
    'citizen': (789, 790),
    'yrimmig': (794, 798),
    'empstat': (874, 875),
    'uhrswork': (904, 906),
}

# DACA eligibility cutoff date: June 15, 2012
DACA_DATE = '2012-06-15'
DACA_START_YEAR = 2012

# ============================================================================
# Data Loading
# ============================================================================

def read_acs_data(filepath, chunk_size=100000):
    """Read fixed-width ACS data and extract required fields."""
    records = []
    try:
        with open(filepath, 'r', encoding='ascii', errors='ignore') as f:
            for line in f:
                # Parse fields using fixed-width positions
                rec = {}
                for field, (start, end) in FIELD_SPECS.items():
                    try:
                        value = line[start:end].strip()
                        rec[field] = int(value) if value else None
                    except (ValueError, IndexError):
                        rec[field] = None
                records.append(rec)
                if len(records) % chunk_size == 0:
                    pass
        
        df = pd.DataFrame(records)
        return df
    except Exception as e:
        raise RuntimeError(f"Error reading ACS data: {e}")

# ============================================================================
# DACA Eligibility Determination
# ============================================================================

def calculate_daca_eligibility(df):
    """
    Calculate DACA eligibility based on the four criteria:
    1. Arrived unlawfully before age 16
    2. Had not yet had 31st birthday as of June 15, 2012
    3. Lived continuously in the US since June 15, 2007 (yrimmig <= 2007)
    4. Were not citizens or LPRs (citizen in [3, 4, 5])
    5. Hispanic-Mexican (hispan == 1) and Mexican-born (bpl == 200)
    """
    
    # Filter for Hispanic-Mexican, Mexican-born individuals
    df['is_mexican_hisp'] = (df['hispan'] == 1) & (df['bpl'] == 200)
    
    # Filter for noncitizen/unknown status (citizen in [3, 4, 5])
    # 3 = Not a citizen, 4 = Not a citizen but has received first papers, 5 = Foreign born, citizenship status not reported
    df['is_noncitizen'] = df['citizen'].isin([3, 4, 5])
    
    # Filter for continuous residence since June 15, 2007 (arrived by 2007)
    df['arrived_by_2007'] = df['yrimmig'] <= 2007
    
    # Calculate age at arrival (approximation using year of immigration)
    # Age at survey = age, Survey year = year, so age_at_arrival ~ age - (year - yrimmig)
    df['age_at_arrival'] = df['age'] - (df['year'] - df['yrimmig'])
    
    # Filter for arrived before age 16
    df['arrived_before_16'] = df['age_at_arrival'] < 16
    
    # Calculate age as of June 15, 2012
    # For simplicity, if survey year is 2012, use age - 0.5 (mid-year assumption)
    # For other years, adjust back to 2012
    df['age_in_2012'] = df['age'] - (df['year'] - 2012)
    
    # Filter for 15-30 years old as of June 15, 2012
    # (must be at least 15 to have been < 31 on 6/15/2012, and was < 31 on that date)
    df['age_criteria'] = (df['age_in_2012'] >= 15) & (df['age_in_2012'] < 31)
    
    # Combine all criteria
    df['daca_eligible'] = (
        df['is_mexican_hisp'] & 
        df['is_noncitizen'] & 
        df['arrived_by_2007'] & 
        df['arrived_before_16'] & 
        df['age_criteria']
    )
    
    return df

# ============================================================================
# Outcome Definition
# ============================================================================

def calculate_fulltime_employment(df):
    """
    Full-time employment: empstat == 1 (employed) AND uhrswork >= 35
    """
    df['fulltime'] = (df['empstat'] == 1) & (df['uhrswork'] >= 35)
    df['fulltime'] = df['fulltime'].astype(int)
    return df

# ============================================================================
# Treatment Definition
# ============================================================================

def calculate_treatment(df):
    """
    Treatment: Post-DACA implementation (year >= 2013)
    DACA was implemented on June 15, 2012, so 2013 is the first full year
    """
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    return df

# ============================================================================
# Analysis
# ============================================================================

def run_analysis():
    """Main analysis function."""
    
    print("Loading ACS data...", flush=True)
    df = read_acs_data('ACS_extract_expanded.dat')
    print(f"Loaded {len(df)} records", flush=True)
    
    # Restrict to years 2013-2016 plus 2012 for comparison
    df = df[df['year'].isin([2012, 2013, 2014, 2015, 2016])]
    print(f"After year filter: {len(df)} records", flush=True)
    
    # Calculate eligibility and outcomes
    df = calculate_daca_eligibility(df)
    df = calculate_fulltime_employment(df)
    df = calculate_treatment(df)
    
    # Filter to DACA-eligible sample
    sample_df = df[df['daca_eligible'] == True].copy()
    print(f"DACA-eligible sample size: {len(sample_df)}", flush=True)
    
    # Check for variation in treatment
    treatment_counts = sample_df['post_daca'].value_counts()
    print(f"Treatment variation: {treatment_counts.to_dict()}", flush=True)
    
    if len(treatment_counts) < 2:
        raise ValueError("No variation in treatment. Cannot estimate effect.")
    
    # Apply weights and prepare for analysis
    sample_df = sample_df[sample_df['perwt'].notna() & (sample_df['perwt'] > 0)].copy()
    
    # Prepare data for analysis
    # Handle missing values
    sample_df['fulltime'] = pd.to_numeric(sample_df['fulltime'], errors='coerce')
    sample_df['post_daca'] = pd.to_numeric(sample_df['post_daca'], errors='coerce')
    sample_df = sample_df[sample_df['fulltime'].notna() & sample_df['post_daca'].notna()].copy()
    
    print(f"Final analysis sample: {len(sample_df)} observations", flush=True)
    
    # Weighted least squares regression
    # Outcome: fulltime employment
    # Treatment: post_daca indicator
    # Simple difference-in-differences: Compare pre and post DACA employment rates
    
    # Aggregate to state-year level to reduce computational burden and stabilize estimates
    agg_data = sample_df.groupby(['statefip', 'year']).agg({
        'fulltime': 'mean',  # Employment rate
        'perwt': 'sum'       # Total weight
    }).reset_index()
    
    agg_data['post_daca'] = (agg_data['year'] >= 2013).astype(int)
    
    # Add state and year fixed effects indicators
    agg_data['state_id'] = agg_data['statefip']
    agg_data['year_id'] = agg_data['year']
    
    # Create dummies
    state_dummies = pd.get_dummies(agg_data['state_id'], prefix='state', drop_first=True)
    year_dummies = pd.get_dummies(agg_data['year_id'], prefix='year', drop_first=True)
    
    # Build X matrix
    X = pd.concat([
        agg_data[['post_daca']],
        state_dummies,
        year_dummies
    ], axis=1).astype(float)
    
    # Add constant
    X = sm.add_constant(X)
    
    # y vector
    y = agg_data['fulltime'].values
    
    # Weights
    weights = agg_data['perwt'].values
    weights = weights / weights.mean()  # Normalize for numerical stability
    
    # Fit weighted least squares
    wls_model = sm.WLS(y, X, weights=weights)
    wls_result = wls_model.fit()
    
    # Extract treatment coefficient and standard error
    # Coefficient on 'post_daca' is at index 1 (after constant at index 0)
    point_estimate = wls_result.params[1]
    treatment_se = wls_result.bse[1]
    
    # Get additional statistics
    t_stat = wls_result.tvalues[1]
    p_value = wls_result.pvalues[1]
    
    # Sample size (use weighted count from original data)
    sample_size = len(sample_df)
    
    print(f"Point estimate: {point_estimate:.6f}", flush=True)
    print(f"Standard error: {treatment_se:.6f}", flush=True)
    print(f"T-statistic: {t_stat:.4f}", flush=True)
    print(f"P-value: {p_value:.6f}", flush=True)
    print(f"Sample size: {sample_size}", flush=True)
    
    return {
        'point_estimate': float(point_estimate),
        'standard_error': float(treatment_se),
        'sample_size': sample_size,
        't_stat': float(t_stat),
        'p_value': float(p_value)
    }

# ============================================================================
# Main Execution
# ============================================================================

if __name__ == '__main__':
    try:
        results = run_analysis()
        
        # Output JSON as required
        output = {
            "point_estimate": results['point_estimate'],
            "standard_error": results['standard_error'],
            "sample_size": results['sample_size']
        }
        
        import json
        print(json.dumps(output))
        
    except Exception as e:
        print(f"Error: {e}", flush=True)
        import traceback
        traceback.print_exc()
        exit(1)
