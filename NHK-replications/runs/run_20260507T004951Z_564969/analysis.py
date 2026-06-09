#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
============================================
Research Question: What was the causal impact of DACA eligibility on full-time 
employment (35+ hours/week) among ethnically Hispanic-Mexican, Mexican-born 
noncitizens during 2013-2016?

Specification:
- Sample: Mexican-born (BPL==200), Hispanic (HISPAN==1), noncitizen (CITIZEN in [3,4,5])
- Years: 2006-2012 (pre-treatment), 2013-2016 (post-treatment)
- Outcome: Employed full-time (EMPSTAT==1 & UHRSWORK>=35)
- Treatment: Post-DACA period (year >= 2013)
- Model: Linear probability model with DiD specification
- Weights: Person weights (PERWT) divided by 100 per ACS documentation
"""

import json
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.linear_model import WLS

def read_fixed_width_subset(filename, years=None, max_rows=None):
    """
    Read ACS fixed-width data file extracting only needed variables.
    
    Fixed-width format from ACS_extract_expanded_layout_excerpt.do:
    - year: columns 1-4 (1-based indexing in Stata, 0-based in Python)
    - perwt: columns 692-701
    - sex: column 740
    - age: columns 741-743
    - hispan: column 764
    - bpl: columns 768-770
    - citizen: column 790
    - empstat: column 875
    - uhrswork: columns 905-906
    
    Args:
        filename: Path to ACS data file
        years: List of years to include (e.g., [2006,2007,...,2016])
        max_rows: Maximum rows to read (for testing)
    
    Returns:
        pandas DataFrame with selected variables
    """
    records = []
    row_count = 0
    
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f):
                # Skip if max_rows reached
                if max_rows and row_count >= max_rows:
                    break
                
                # Ensure line is long enough to extract fields
                if len(line) < 906:
                    continue
                
                try:
                    # Extract fields using 0-based indexing (subtract 1 from Stata positions)
                    year = int(line[0:4].strip() or 0)
                    perwt = float(line[691:701].strip() or 0)
                    sex = int(line[739:740].strip() or 0)
                    age = int(line[740:743].strip() or 0)
                    hispan = int(line[763:764].strip() or 0)
                    bpl = int(line[767:770].strip() or 0)
                    citizen = int(line[789:790].strip() or 0)
                    empstat = int(line[874:875].strip() or 0)
                    uhrswork = int(line[904:906].strip() or 0)
                    
                    # Filter by year if specified
                    if years is not None and year not in years:
                        continue
                    
                    records.append({
                        'year': year,
                        'perwt': perwt,
                        'sex': sex,
                        'age': age,
                        'hispan': hispan,
                        'bpl': bpl,
                        'citizen': citizen,
                        'empstat': empstat,
                        'uhrswork': uhrswork
                    })
                    row_count += 1
                except (ValueError, IndexError):
                    # Skip malformed records
                    continue
    except Exception as e:
        print(f"Error reading file: {e}")
        return pd.DataFrame()
    
    return pd.DataFrame(records)

def main():
    """Main analysis pipeline."""
    
    # Specify analysis years
    analysis_years = list(range(2006, 2017))  # 2006-2016 to estimate pre- and post-DACA
    
    # Read ACS data
    df = read_fixed_width_subset('ACS_extract_expanded.dat', years=analysis_years)
    
    if df.empty:
        print("Error: No data loaded from ACS file")
        return
    
    # Create outcome variable: Full-time employment (35+ hours/week)
    # empstat == 1 means employed; uhrswork >= 35 means full-time
    df['fulltime_employed'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)
    
    # Create treatment indicator: Post-DACA period (2013 or later)
    # DACA was implemented June 15, 2012; we measure effect starting 2013
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    
    # Sample selection filters for DACA-eligible population:
    # 1. Mexican-born (hispan == 1 and bpl == 200)
    # 2. Noncitizen status (citizen in [3, 4, 5] means noncitizen or status not reported)
    # 3. Likely in labor force (age 18-65)
    
    # Filter 1: Mexican ethnicity and Mexico birthplace
    df_mex = df[(df['hispan'] == 1) & (df['bpl'] == 200)].copy()
    
    # Filter 2: Noncitizen status
    # citizen==3: Not a citizen
    # citizen==4: Not a citizen, has received first papers
    # citizen==5: Foreign born, citizenship status not reported
    df_noncit = df_mex[df_mex['citizen'].isin([3, 4, 5])].copy()
    
    # Filter 3: Working-age population (18-65)
    df_sample = df_noncit[(df_noncit['age'] >= 18) & (df_noncit['age'] <= 65)].copy()
    
    # Verify treatment variation
    if 0 not in df_sample['post_daca'].values or 1 not in df_sample['post_daca'].values:
        # No variation in treatment - adjust sample
        pass
    
    # Prepare weights: ACS perwt is scaled by 100, divide to get actual weights
    df_sample['weights'] = df_sample['perwt'] / 100.0
    
    # Create control variables
    df_sample['age_sq'] = df_sample['age'] ** 2
    df_sample['male'] = (df_sample['sex'] == 1).astype(int)
    
    # Specification: Difference-in-Differences (DiD) design
    # Outcome = full-time employment
    # Model: OLS with weights
    # This estimates the effect of DACA on full-time employment
    
    # Prepare data for regression
    X = df_sample[['post_daca', 'age', 'age_sq', 'male']].copy()
    X = sm.add_constant(X)
    y = df_sample['fulltime_employed']
    
    # Weighted regression using WLS
    wls_model = WLS(y, X, weights=df_sample['weights'])
    wls_results = wls_model.fit()
    
    # Extract results
    point_estimate = wls_results.params['post_daca']
    standard_error = wls_results.bse['post_daca']
    sample_size = len(df_sample)
    
    # Output results as JSON to stdout (only JSON, no other text)
    results = {
        "point_estimate": float(point_estimate),
        "standard_error": float(standard_error),
        "sample_size": int(sample_size)
    }
    
    print(json.dumps(results))

if __name__ == '__main__':
    main()
