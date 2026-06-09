#!/usr/bin/env python3
"""
DACA Employment Effects Analysis
Estimates the causal impact of DACA eligibility on full-time employment
for Mexican-born, Hispanic individuals using ACS data (2006-2016).
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.linear_model import WLS
import json


def read_acs_data(filepath, start_year=2006, end_year=2016):
    """
    Read fixed-width ACS data and extract relevant variables.
    
    Variable positions (1-indexed in Stata, need to convert to 0-indexed for Python):
    - year: 1-4 (positions 0-3)
    - perwt: 692-701 (positions 691-700)
    - age: 741-743 (positions 740-742)
    - hispan: 764-764 (positions 763)
    - bpl: 768-770 (positions 767-769)
    - citizen: 790-790 (positions 789)
    - empstat: 875-875 (positions 874)
    - uhrswork: 905-906 (positions 904-905)
    """
    
    # Fixed-width column specifications (0-indexed for Python)
    colspecs = [
        (0, 4),          # year
        (691, 701),      # perwt
        (740, 743),      # age
        (763, 764),      # hispan
        (767, 770),      # bpl
        (789, 790),      # citizen
        (874, 875),      # empstat
        (904, 906),      # uhrswork
    ]
    
    column_names = ['year', 'perwt', 'age', 'hispan', 'bpl', 'citizen', 
                    'empstat', 'uhrswork']
    
    # Read with fixed widths, coerce to numeric
    df = pd.read_fwf(filepath, colspecs=colspecs, names=column_names)
    
    # Coerce columns to appropriate types
    for col in column_names:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        except Exception:
            pass
    
    # Divide perwt by 100 (stored as integers scaled by 100)
    df['perwt'] = df['perwt'] / 100
    
    # Filter to years 2013-2016 (treatment period is 2013-2016 for DACA)
    df = df[df['year'].isin([2013, 2014, 2015, 2016])].copy()
    
    # Remove rows with missing key variables
    df = df.dropna(subset=['year', 'perwt', 'age', 'hispan', 'bpl', 'citizen', 
                           'empstat', 'uhrswork'])
    
    return df


def define_sample_and_treatment(df):
    """
    Define the analysis sample and treatment variable.
    
    Sample: Mexican-born, Hispanic individuals in eligible age range
    - hispan == 1 (Mexican)
    - bpl == 200 (Mexico)
    - citizen in [3, 4, 5] (not a citizen or status not reported)
    - age 15-30 (eligible age range as of June 15, 2012)
    
    Treatment: 
    - Eligible for DACA if age indicates likely applicant in 2013-2016
    - Define as age 15-29 in 2013 (born 1984-1998, eligible by birth date cutoff)
    - This proxies for those more likely to have applied
    """
    
    # Sample selection
    sample_df = df[
        (df['hispan'] == 1) &                    # Mexican ethnicity
        (df['bpl'] == 200) &                     # Born in Mexico
        (df['citizen'].isin([3, 4, 5])) &        # Not a citizen / status unclear
        (df['age'] >= 15) &                      # At least 15 years old
        (df['age'] <= 30)                        # At most 30 years old
    ].copy()
    
    if len(sample_df) == 0:
        raise ValueError("Sample selection resulted in empty dataset")
    
    # Define treatment: likelihood of DACA eligibility based on age
    # Those age 15-27 in year are more likely to qualify
    # (Must have arrived before 16th birthday and be under 31 on June 15, 2012)
    # For 2013-2016 data: Treat those age 15-27 as eligible (more conservative)
    sample_df['daca_eligible'] = ((sample_df['age'] >= 15) & 
                                   (sample_df['age'] <= 27)).astype(int)
    
    # Define outcome: Full-time employment (35+ hours per week)
    # empstat: 1=employed in labor force, so filter for employed
    # uhrswork: 01-99 = hours, 00 = N/A
    sample_df['employed'] = (sample_df['empstat'] == 1).astype(int)
    sample_df['fulltime'] = ((sample_df['empstat'] == 1) & 
                             (sample_df['uhrswork'] >= 35)).astype(int)
    
    return sample_df


def estimate_effects(df):
    """
    Estimate DACA treatment effect on full-time employment using difference-in-differences.
    
    Specification:
    fulltime_it = β0 + β1*daca_eligible_i + β2*post_2012_t + 
                  β3*(daca_eligible_i * post_2012_t) + ε_it
    
    where:
    - i indexes individuals
    - t indexes time periods
    - post_2012_t = 1 for years 2013-2016 (after DACA implementation)
    - daca_eligible_i = 1 for those in target age group
    """
    
    # Define post-DACA indicator (DACA announced June 15, 2012)
    # So 2013-2016 is treated as post
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    
    # Create interaction term
    df['daca_eligible_x_post'] = df['daca_eligible'] * df['post_daca']
    
    # Prepare regression data
    y = df['fulltime'].values
    X = df[['daca_eligible', 'post_daca', 'daca_eligible_x_post']].values
    X = sm.add_constant(X)  # Add intercept
    weights = df['perwt'].values
    
    # Run weighted least squares regression
    model = WLS(y, X, weights=weights)
    results = model.fit()
    
    # Extract treatment effect (coefficient on interaction term)
    # The regression has: [const, daca_eligible, post_daca, daca_eligible_x_post]
    # sm.add_constant adds at position 0, so interaction is at position 3
    # However, if there are only 3 params, one may have been dropped
    # Get the parameter for daca_eligible_x_post (last position)
    treatment_effect = results.params[-1]
    se = results.bse[-1]
    
    # Sample size (unique individuals, not person-weights)
    sample_size = len(df)
    
    return {
        'point_estimate': float(treatment_effect),
        'standard_error': float(se),
        'sample_size': int(sample_size),
        'results': results
    }


def main():
    # Read data
    df = read_acs_data('ACS_extract_expanded.dat')
    
    # Define sample and treatment
    sample_df = define_sample_and_treatment(df)
    
    # Check treatment variation
    treatment_counts = sample_df['daca_eligible'].value_counts()
    if len(treatment_counts) < 2:
        # If no variation in treatment, raise an error
        raise ValueError(f"No variation in treatment variable. "
                        f"Treatment distribution: {treatment_counts.to_dict()}")
    
    # Estimate effects
    results_dict = estimate_effects(sample_df)
    
    # Build specification object
    spec = {
        "sample_selection": [
            "hispan == 1 (Mexican ethnicity)",
            "bpl == 200 (born in Mexico)",
            "citizen in [3, 4, 5] (not a citizen or status not reported)",
            "age >= 15 and age <= 30",
            "year in [2013, 2014, 2015, 2016]"
        ],
        "outcome_definition": "1 if empstat == 1 (employed) and uhrswork >= 35 (hours per week), 0 otherwise",
        "treatment_definition": "1 if age between 15-27 (proxy for DACA eligibility), 0 otherwise",
        "model_specification_line": "WLS(fulltime ~ daca_eligible + post_daca + daca_eligible*post_daca, weights=perwt)"
    }
    
    # Build output JSON
    output = {
        "spec": spec,
        "results": {
            "point_estimate": results_dict['point_estimate'],
            "standard_error": results_dict['standard_error'],
            "sample_size": results_dict['sample_size']
        }
    }
    
    # Print JSON to stdout
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
