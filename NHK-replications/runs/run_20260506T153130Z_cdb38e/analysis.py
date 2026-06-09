#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment (Phase 12)
Analysis of causal impact of DACA eligibility on full-time employment
among ethnically Hispanic-Mexican, Mexican-born individuals (2013-2016).
"""

import pandas as pd
import numpy as np
import json
import statsmodels.api as sm
import warnings

warnings.filterwarnings('ignore')

def load_acs_data():
    """
    Load ACS_extract_expanded.dat as fixed-width file using pandas.read_fwf.
    This is much faster than manual line-by-line parsing.
    """
    
    # Define column specifications for pandas.read_fwf
    # (column name, start position, end position) - note: pandas uses 0-based positions
    colspecs = [
        (0, 4),      # year
        (65, 67),    # statefip
        (739, 740),  # sex
        (740, 743),  # age
        (763, 764),  # hispan
        (767, 770),  # bpl
        (789, 790),  # citizen
        (691, 701),  # perwt
        (794, 798),  # yrimmig
        (904, 906),  # uhrswork
    ]
    
    names = ['year', 'statefip', 'sex', 'age', 'hispan', 'bpl', 'citizen', 
             'perwt', 'yrimmig', 'uhrswork']
    
    print("Loading ACS data...")
    df = pd.read_fwf('ACS_extract_expanded.dat', colspecs=colspecs, names=names, 
                      dtype={'year': int, 'statefip': int, 'sex': int, 'age': int,
                             'hispan': int, 'bpl': int, 'citizen': int, 'perwt': float,
                             'yrimmig': int, 'uhrswork': int})
    
    print(f"  Loaded {len(df)} total observations")
    return df

def filter_sample(df):
    """Apply sample selection criteria for DACA-eligible population."""
    
    # Select ethnically Hispanic-Mexican, Mexican-born noncitizens in 2013-2016
    sample = df[
        (df['hispan'] == 1) &  # Mexican ethnicity
        (df['bpl'] == 200) &   # Born in Mexico
        (df['citizen'].isin([3, 4, 5])) &  # Noncitizen or status not reported
        (df['year'].isin([2013, 2014, 2015, 2016]))  # Post-DACA years
    ].copy()
    
    # Age filter: 15-35 years (to target DACA-eligible age range)
    sample = sample[(sample['age'] >= 15) & (sample['age'] <= 35)].copy()
    
    # Remove rows with missing values in key variables
    sample = sample.dropna(subset=['age', 'uhrswork', 'perwt', 'year', 'statefip'])
    
    print(f"  After sample selection: {len(sample)} observations")
    return sample

def create_treatment_variable(df):
    """Create DACA eligibility indicator."""
    
    df['daca_eligible'] = 0
    
    # DACA eligible as of June 15, 2012 if:
    # 1. Arrived unlawfully before age 16 (by June 1996)
    # 2. Not yet age 31 (born after June 1981)
    for idx, row in df.iterrows():
        year = row['year']
        age = row['age']
        yrimmig = row['yrimmig']
        
        if pd.notna(yrimmig) and yrimmig > 0:
            birth_year = year - age
            
            # Check eligibility criteria
            arrived_before_16 = (yrimmig - birth_year) < 16 and yrimmig <= 1996
            age_criteria = birth_year > 1981
            
            if arrived_before_16 and age_criteria:
                df.at[idx, 'daca_eligible'] = 1
    
    return df

def load_policy_data():
    """Load state-year policy and labor market controls."""
    policy_df = pd.read_csv('policy_labor_market_data.csv')
    policy_df.columns = [c.upper() for c in policy_df.columns]
    return policy_df

def prepare_analysis_data():
    """Prepare data for analysis."""
    
    # Load and filter ACS data
    df = load_acs_data()
    df = filter_sample(df)
    
    # Create treatment variable
    print("Creating DACA eligibility variable...")
    df = create_treatment_variable(df)
    
    eligible_count = df['daca_eligible'].sum()
    print(f"  {eligible_count} DACA-eligible observations")
    
    if eligible_count == 0:
        raise ValueError("No DACA-eligible individuals. Revise specification.")
    
    # Create outcome variable
    df['fulltime'] = (df['uhrswork'] >= 35).astype(int)
    
    # Merge with policy data
    print("Loading policy and labor market controls...")
    policy_df = load_policy_data()
    policy_df['statefip'] = policy_df['STATE_FIPS']
    policy_df['year'] = policy_df['YEAR']
    
    df = pd.merge(df, policy_df[['statefip', 'year', 'UNEMP', 'LFPR']], 
                  on=['statefip', 'year'], how='left')
    
    print(f"  Merged data: {len(df)} observations")
    
    return df

def estimate_daca_effect(df):
    """
    Estimate DACA treatment effect using difference-in-differences.
    
    Model: fulltime_it = β0 + β1*daca_eligible_i + β2*post_2012_t 
                         + β3*(daca_eligible * post_2012)
                         + β4*UNEMP_t + β5*LFPR_t + β6*male + β7*age
                         + state_FE + ε
    
    Treatment effect estimate is β3 (interaction coefficient).
    """
    
    print("Estimating DACA treatment effect...")
    
    # Create time indicators
    df['post_2012'] = (df['year'] >= 2013).astype(int)
    df['daca_x_post'] = df['daca_eligible'] * df['post_2012']
    
    # State fixed effects
    state_dummies = pd.get_dummies(df['statefip'], prefix='state', drop_first=True)
    
    # Build regression specification
    X = pd.DataFrame({
        'const': 1.0,
        'daca_eligible': df['daca_eligible'].astype(float).values,
        'post_2012': df['post_2012'].astype(float).values,
        'daca_x_post': df['daca_x_post'].astype(float).values,
        'unemp': df['UNEMP'].fillna(df['UNEMP'].mean()).astype(float).values,
        'lfpr': df['LFPR'].fillna(df['LFPR'].mean()).astype(float).values,
        'male': (df['sex'] - 1).astype(float).values,
        'age': df['age'].astype(float).values
    })
    
    # Add state dummies (ensure float type)
    for col in state_dummies.columns:
        X[col] = state_dummies[col].astype(float).values
    
    # Convert to numpy arrays with explicit float dtype
    X_arr = X.astype(float).values
    y = df['fulltime'].astype(float).values
    weights = df['perwt'].astype(float).values / 100.0  # Adjust for 2 implied decimals
    
    # Weighted least squares estimation
    wls = sm.WLS(y, X_arr, weights=weights)
    results = wls.fit()
    
    # Extract treatment effect (coefficient on daca_x_post)
    # Note: daca_x_post is at position 3 in our design matrix (0=const, 1=daca_eligible, 2=post_2012, 3=daca_x_post)
    point_est = float(results.params[3])
    se = float(results.bse[3])
    n = len(df)
    
    return {
        'point_estimate': point_est,
        'standard_error': se,
        'sample_size': n
    }

def main():
    """Main execution."""
    try:
        # Prepare data
        df = prepare_analysis_data()
        
        # Estimate effect
        results = estimate_daca_effect(df)
        
        # Report results
        print("\n" + "="*70)
        print("DACA IMPACT ON FULL-TIME EMPLOYMENT")
        print("="*70)
        print(f"Point Estimate: {results['point_estimate']:.6f}")
        print(f"Standard Error: {results['standard_error']:.6f}")
        print(f"Sample Size: {results['sample_size']}")
        if results['standard_error'] > 0:
            t_stat = results['point_estimate'] / results['standard_error']
            print(f"t-statistic: {t_stat:.4f}")
        print("="*70)
        
        # Output JSON only
        print(json.dumps({
            'point_estimate': results['point_estimate'],
            'standard_error': results['standard_error'],
            'sample_size': results['sample_size']
        }))
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    main()
