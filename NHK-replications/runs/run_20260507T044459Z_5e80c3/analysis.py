#!/usr/bin/env python3
"""
DACA Employment Analysis
Estimates the effect of DACA eligibility on full-time employment among
Mexican-born, ethnically Hispanic noncitizens in the US (2013-2016).
"""

import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
import json
import sys

# Fixed-width column specifications (Stata 1-based -> Python 0-based)
# Format: name, (start_0based, end_0based)
col_specs = [
    (0, 4, 'year'),
    (65, 67, 'statefip'),
    (691, 701, 'perwt'),
    (740, 743, 'age'),
    (763, 764, 'hispan'),
    (767, 770, 'bpl'),
    (789, 790, 'citizen'),
    (794, 798, 'yrimmig'),
    (874, 875, 'empstat'),
    (904, 906, 'uhrswork'),
]

def read_acs_data_fast(filename):
    """
    Read fixed-width ACS data using efficient line parsing.
    """
    print("Reading ACS data...", file=sys.stderr)
    
    data_dict = {name: [] for _, _, name in col_specs}
    line_count = 0
    
    with open(filename, 'r') as f:
        for line in f:
            line_count += 1
            
            # Extract fields from fixed positions
            for start, end, name in col_specs:
                value_str = line[start:end].strip()
                
                if value_str == '' or value_str == '.':
                    value = np.nan
                else:
                    try:
                        if name == 'perwt':
                            value = float(value_str)
                        else:
                            value = int(value_str)
                    except (ValueError, IndexError):
                        value = np.nan
                
                data_dict[name].append(value)
            
            # Progress reporting
            if line_count % 100000 == 0:
                print(f"Processed {line_count} records...", file=sys.stderr)
    
    print(f"Total records: {line_count}", file=sys.stderr)
    
    # Create DataFrame
    df = pd.DataFrame(data_dict)
    return df


def process_data():
    """
    Load ACS data, filter sample, and compute outcome/treatment variables.
    """
    # Read data
    df = read_acs_data_fast('ACS_extract_expanded.dat')
    print(f"Sample before filtering: {len(df)}", file=sys.stderr)
    
    # Apply sample selection criteria:
    # 1. Mexican ethnicity (hispan == 1)
    # 2. Mexico-born (bpl == 200)
    # 3. Noncitizen (citizen in (3, 4, 5))
    # 4. Age >= 16
    # 5. Years 2013-2016
    # 6. Non-missing values for key variables
    
    df = df[
        (df['hispan'] == 1) &
        (df['bpl'] == 200) &
        (df['citizen'].isin([3, 4, 5])) &
        (df['age'] >= 16) &
        (df['year'].isin([2013, 2014, 2015, 2016])) &
        (df['perwt'].notna()) &
        (df['empstat'].notna()) &
        (df['uhrswork'].notna())
    ].copy()
    
    print(f"Sample after filtering: {len(df)}", file=sys.stderr)
    
    if len(df) == 0:
        print("ERROR: Empty sample after filtering", file=sys.stderr)
        return None
    
    # Create outcome: full-time employed
    # 1 if employed (empstat == 1) AND working 35+ hours per week
    df['full_time'] = (
        (df['empstat'] == 1) & (df['uhrswork'] >= 35)
    ).astype(int)
    
    # Create treatment: DACA eligible
    # 1 if arrived by 2007 (YRIMMIG <= 2007)
    df['daca_eligible'] = (df['yrimmig'] <= 2007).astype(int)
    
    # Check variation in treatment
    n_eligible = (df['daca_eligible'] == 1).sum()
    n_ineligible = (df['daca_eligible'] == 0).sum()
    print(f"DACA eligible: {n_eligible}, DACA ineligible: {n_ineligible}", file=sys.stderr)
    
    if n_eligible == 0 or n_ineligible == 0:
        print("WARNING: No variation in treatment variable", file=sys.stderr)
        return None
    
    # Prepare for regression
    df['state'] = df['statefip'].astype(int).astype(str)
    df['year_fe'] = df['year'].astype(int).astype(str)
    
    return df


def run_analysis(df):
    """
    Estimate the effect of DACA eligibility on full-time employment.
    """
    print("Running OLS regression...", file=sys.stderr)
    
    formula = 'full_time ~ daca_eligible + C(year_fe) + C(state)'
    weights = df['perwt'] / 100
    
    model = ols(formula, data=df).fit(weights=weights)
    
    # Extract results
    point_estimate = model.params['daca_eligible']
    standard_error = model.bse['daca_eligible']
    sample_size = len(df)
    
    print(f"Point estimate: {point_estimate:.6f}", file=sys.stderr)
    print(f"Standard error: {standard_error:.6f}", file=sys.stderr)
    print(f"Sample size: {sample_size}", file=sys.stderr)
    print(f"R-squared: {model.rsquared:.6f}", file=sys.stderr)
    
    return {
        'point_estimate': float(point_estimate),
        'standard_error': float(standard_error),
        'sample_size': int(sample_size),
    }


def main():
    """Main execution function."""
    df = process_data()
    if df is None:
        results = {
            'point_estimate': None,
            'standard_error': None,
            'sample_size': 0
        }
        print(json.dumps(results))
        sys.exit(1)
    
    results = run_analysis(df)
    print(json.dumps(results))


if __name__ == '__main__':
    main()

