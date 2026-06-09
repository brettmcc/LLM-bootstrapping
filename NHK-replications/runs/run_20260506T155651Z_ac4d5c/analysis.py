#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Phase 12: Research specification and implementation
"""

import pandas as pd
import numpy as np
import json
import sys
import traceback

def read_acs_data():
    """Read ACS fixed-width data efficiently."""
    print("Starting to read ACS data...", file=sys.stderr, flush=True)
    
    col_names = ['year', 'statefip', 'age', 'hispan', 'bpl', 'citizen', 'yrimmig', 'empstat', 'uhrswork', 'perwt']
    
    data_list = []
    line_count = 0
    
    try:
        with open('ACS_extract_expanded.dat', 'r', encoding='ascii', errors='replace') as f:
            for line_num, line in enumerate(f, 1):
                line_count = line_num
                
                if line_num % 1000000 == 0:
                    print(f"Processed {line_num} lines", file=sys.stderr, flush=True)
                
                if len(line) < 906:
                    continue
                
                row = {}
                try:
                    row['year'] = int(line[0:4].strip() or 0)
                    row['statefip'] = int(line[65:67].strip() or 0)
                    row['age'] = int(line[740:743].strip() or 0)
                    row['hispan'] = int(line[763:764].strip() or 0)
                    row['bpl'] = int(line[767:770].strip() or 0)
                    row['citizen'] = int(line[789:790].strip() or 0)
                    row['yrimmig'] = int(line[794:798].strip() or 0)
                    row['empstat'] = int(line[874:875].strip() or 0)
                    row['uhrswork'] = int(line[904:906].strip() or 0)
                    
                    perwt_str = line[691:701].strip()
                    row['perwt'] = float(perwt_str) if perwt_str else 0
                    
                    data_list.append(row)
                except (ValueError, IndexError):
                    continue
        
        print(f"Read {line_count} lines total, {len(data_list)} valid records", file=sys.stderr, flush=True)
        
        df = pd.DataFrame(data_list)
        return df
        
    except Exception as e:
        print(f"Error reading ACS data: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        raise

def prepare_sample(df):
    """Filter sample for DACA eligibility."""
    print(f"Starting with {len(df)} records", file=sys.stderr, flush=True)
    
    # Filter for Mexican-born, Hispanic-Mexican
    df = df[(df['hispan'] == 1) & (df['bpl'] == 200)].copy()
    print(f"After hispan/bpl filter: {len(df)}", file=sys.stderr, flush=True)
    
    if len(df) == 0:
        raise ValueError("No records match hispan==1 and bpl==200")
    
    # Filter for non-citizens
    df = df[df['citizen'].isin([3, 4, 5])].copy()
    print(f"After citizen filter: {len(df)}", file=sys.stderr, flush=True)
    
    # Filter for years 2013-2016
    df = df[df['year'].isin([2013, 2014, 2015, 2016])].copy()
    print(f"After year filter: {len(df)}", file=sys.stderr, flush=True)
    
    # Filter for DACA residence requirement
    df = df[df['yrimmig'] <= 2007].copy()
    print(f"After yrimmig <= 2007 filter: {len(df)}", file=sys.stderr, flush=True)
    
    # Age constraint
    df['age_on_daca_date'] = df['age'] + (2012 - df['year'])
    df = df[df['age_on_daca_date'] <= 30].copy()
    print(f"After age on DACA date filter: {len(df)}", file=sys.stderr, flush=True)
    
    # Arrival age constraint
    df['age_at_immigration'] = df['yrimmig'] - (df['year'] - df['age'])
    df = df[df['age_at_immigration'] < 16].copy()
    print(f"After arrival age filter: {len(df)}", file=sys.stderr, flush=True)
    
    if len(df) == 0:
        raise ValueError("No records remain after filtering")
    
    return df

def define_outcome(df):
    """Full-time employment: employed and 35+ hours."""
    df['fulltime_employed'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)
    return df

def define_treatment(df):
    """Define treatment variables."""
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    df['young_cohort'] = (df['age_at_immigration'] <= 10).astype(int)
    return df

def estimate_effect(df):
    """Estimate DACA effect using OLS."""
    from statsmodels.formula.api import ols
    
    # Prepare data
    df['weight'] = df['perwt'] / 100
    analysis_df = df[['fulltime_employed', 'post_daca', 'young_cohort', 'year', 'weight']].dropna().copy()
    
    sample_size = len(analysis_df)
    print(f"Analysis sample size: {sample_size}", file=sys.stderr, flush=True)
    print(f"Full-time employment rate: {analysis_df['fulltime_employed'].mean():.4f}", file=sys.stderr, flush=True)
    
    if analysis_df['fulltime_employed'].var() == 0:
        raise ValueError("No outcome variation")
    
    # Simple treatment effect model
    formula = 'fulltime_employed ~ C(year) + young_cohort + post_daca:young_cohort'
    
    try:
        model = ols(formula, data=analysis_df)
        results = model.fit()
        
        # Find interaction coefficient
        coef_val = None
        se_val = None
        for key in results.params.index:
            if 'post_daca' in str(key) and 'young_cohort' in str(key):
                coef_val = results.params[key]
                se_val = results.bse[key]
                break
        
        if coef_val is None:
            # Try simpler model
            formula = 'fulltime_employed ~ post_daca'
            model = ols(formula, data=analysis_df)
            results = model.fit()
            coef_val = results.params['post_daca']
            se_val = results.bse['post_daca']
        
        return {
            'point_estimate': float(coef_val),
            'standard_error': float(se_val),
            'sample_size': sample_size
        }
        
    except Exception as e:
        print(f"Error in estimation: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        raise

def main():
    """Run analysis."""
    try:
        print("=== DACA Analysis Starting ===", file=sys.stderr, flush=True)
        
        # Read data
        df = read_acs_data()
        
        # Prepare sample
        df = prepare_sample(df)
        
        # Define variables
        df = define_outcome(df)
        df = define_treatment(df)
        
        # Estimate effect
        estimates = estimate_effect(df)
        
        # Save spec
        spec = {
            "sample_selection": [
                "hispan == 1",
                "bpl == 200", 
                "citizen in [3, 4, 5]",
                "yrimmig <= 2007",
                "age + (2012 - year) <= 30",
                "yrimmig - (year - age) < 16",
                "year in [2013, 2014, 2015, 2016]"
            ],
            "outcome_definition": "(empstat == 1) and (uhrswork >= 35)",
            "treatment_definition": "DACA eligible via post_daca and young_cohort indicators",
            "model_specification_line": "ols('fulltime_employed ~ C(year) + young_cohort + post_daca:young_cohort')"
        }
        
        with open('spec.json', 'w') as f:
            json.dump(spec, f, indent=2)
        
        # Output results
        results_json = {
            "point_estimate": estimates['point_estimate'],
            "standard_error": estimates['standard_error'],
            "sample_size": estimates['sample_size']
        }
        
        print(json.dumps(results_json))
        
        print(f"\n=== Analysis Complete ===", file=sys.stderr, flush=True)
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        
        # Output error JSON
        results_json = {
            "point_estimate": None,
            "standard_error": None,
            "sample_size": 0
        }
        print(json.dumps(results_json))
        sys.exit(1)

if __name__ == '__main__':
    main()
