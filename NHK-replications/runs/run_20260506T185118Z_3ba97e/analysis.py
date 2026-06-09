#!/usr/bin/env python3
"""
Phase 12 Analysis: DACA Impact on Full-Time Employment

Research Question: Among ethnically Hispanic-Mexican Mexican-born people,
what was the causal impact of eligibility for DACA (treatment) on the probability
of full-time employment (35+ hours per week)?

Estimation Strategy:
- Sample: Hispanic-Mexican Mexican-born individuals aged 15-30 in 2013-2016
- Outcome: Binary indicator of full-time employment (35+ hours/week)
- Treatment: DACA eligibility (based on birth cohort)
- DACA eligibility criteria (as of June 15, 2012):
  * Arrived before age 16
  * Not yet age 31 as of June 15, 2012
  * Continuously present in US since June 15, 2007
  * Not authorized as of June 15, 2012
- Model: OLS with individual-level weights and fixed effects for state and year
"""

import numpy as np
import pandas as pd
import json
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Import statsmodels
try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "statsmodels", "-q"])
    import statsmodels.api as sm
    import statsmodels.formula.api as smf


def parse_acs_fixed_width():
    """
    Parse the ACS fixed-width data file.
    Key fields based on ACS_extract_expanded_layout_excerpt.do:
    - year: 1-4 (1-based)
    - statefip: 66-67
    - hispan: 764-764
    - bpl: 768-770
    - citizen: 790-790
    - age: 741-743
    - birthyr: 748-751
    - empstat: 875-875
    - uhrswork: 905-906
    - perwt: 692-701 (person weight, scaled by 100)
    """
    
    # Column specifications: (name, start, end) where positions are 1-based
    specs = [
        ('year', 0, 4),           # 1-4
        ('statefip', 65, 67),     # 66-67
        ('hispan', 763, 764),     # 764-764
        ('bpl', 767, 770),        # 768-770
        ('citizen', 789, 790),    # 790-790
        ('age', 740, 743),        # 741-743
        ('birthyr', 747, 751),    # 748-751
        ('empstat', 874, 875),    # 875-875
        ('uhrswork', 904, 906),   # 905-906
        ('perwt', 691, 701),      # 692-701
    ]
    
    # Read the fixed-width file in chunks to manage memory
    dfs = []
    chunk_size = 50000
    
    print("Parsing ACS fixed-width data...")
    try:
        with open('ACS_extract_expanded.dat', 'r') as f:
            chunk_lines = []
            for line_num, line in enumerate(f, 1):
                chunk_lines.append(line)
                
                if len(chunk_lines) == chunk_size:
                    # Process this chunk
                    chunk_df = process_chunk(chunk_lines, specs)
                    if chunk_df is not None and len(chunk_df) > 0:
                        dfs.append(chunk_df)
                    chunk_lines = []
                    
                    if line_num % 500000 == 0:
                        print(f"  Processed {line_num:,} lines...")
            
            # Process remaining lines
            if chunk_lines:
                chunk_df = process_chunk(chunk_lines, specs)
                if chunk_df is not None and len(chunk_df) > 0:
                    dfs.append(chunk_df)
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    if not dfs:
        print("No data parsed!")
        return None
    
    df = pd.concat(dfs, ignore_index=True)
    print(f"Parsed {len(df):,} total records")
    return df


def process_chunk(lines, specs):
    """Process a chunk of fixed-width lines"""
    chunk_data = {spec[0]: [] for spec in specs}
    
    for line in lines:
        if not line.strip():
            continue
        
        try:
            for name, start, end in specs:
                # Extract substring (positions already converted to 0-based)
                value_str = line[start:end].strip()
                
                # Convert to appropriate type
                if name == 'perwt':
                    # perwt is 10 digits with 2 implied decimals
                    val = int(value_str) / 100 if value_str else 0
                elif name in ['age', 'year', 'statefip', 'bpl']:
                    val = int(value_str) if value_str else 0
                else:
                    # Single digit codes
                    val = int(value_str[0]) if value_str and value_str[0].isdigit() else 0
                
                chunk_data[name].append(val)
        except (ValueError, IndexError):
            continue
    
    if not chunk_data['year']:
        return None
    
    return pd.DataFrame(chunk_data)


def define_sample_and_variables(df):
    """
    Define sample restrictions and create key variables.
    
    Sample selection:
    1. Years 2013-2016 (post-DACA implementation in June 2012)
    2. Hispanic-Mexican ethnicity (hispan == 1)
    3. Mexican-born (bpl == 200)
    4. Age 15-30 in survey year (to identify those eligible for DACA)
    5. Non-citizen as of survey (citizen in {3, 4, 5})
    6. Valid employment status responses
    7. Valid hours worked data
    
    Variables:
    - outcome: full_time = 1 if usual hours worked >= 35, 0 otherwise
    - treatment: daca_eligible = 1 if birth cohort meets DACA eligibility
      DACA eligibility requires (as of June 15, 2012):
      * Age 16-30 as of June 15, 2012 → born 1982-1996
    """
    
    # Sample restrictions
    df = df[df['year'].isin([2013, 2014, 2015, 2016])].copy()
    df = df[df['hispan'] == 1].copy()  # Mexican
    df = df[df['bpl'] == 200].copy()   # Mexico
    df = df[(df['age'] >= 15) & (df['age'] <= 30)].copy()
    df = df[df['citizen'].isin([3, 4, 5])].copy()  # Non-citizen
    df = df[df['empstat'].isin([1, 2])].copy()  # Employed or unemployed
    
    # Create outcome: full-time employment (35+ hours per week)
    # uhrswork is coded 0-98 (0=N/A, 1-98=hours)
    df['full_time'] = (df['uhrswork'] >= 35).astype(int)
    
    # Create treatment: DACA eligibility
    # Born between 1982 and 1996 (age 16-30 in June 2012)
    df['birth_year'] = df['year'] - df['age']
    df['daca_eligible'] = ((df['birth_year'] >= 1982) & (df['birth_year'] <= 1996)).astype(int)
    
    # Only include those with valid hours worked
    df = df[df['uhrswork'] > 0].copy()
    
    return df


def fit_model(df):
    """
    Fit OLS model with state and year fixed effects.
    
    Model:
    full_time = β0 + β1*daca_eligible + state FE + year FE + ε
    
    The coefficient β1 estimates the difference in full-time employment
    probability between those eligible for DACA and those ineligible,
    controlling for state and year differences.
    """
    
    # Create the formula with fixed effects
    formula = 'full_time ~ C(daca_eligible) + C(year) + C(statefip)'
    
    try:
        # Fit weighted least squares with person weights
        model = smf.wls(
            formula,
            data=df,
            weights=df['perwt']
        )
        results = model.fit()
        
        # Extract the treatment effect coefficient
        coef = results.params.get('C(daca_eligible)[T.1.0]', None)
        if coef is None:
            coef = results.params.get('C(daca_eligible)[T.1]', None)
        
        se = results.bse.get('C(daca_eligible)[T.1.0]', None)
        if se is None:
            se = results.bse.get('C(daca_eligible)[T.1]', None)
        
        # If still not found, return first parameter after intercept
        if coef is None:
            param_names = list(results.params.index)
            if len(param_names) > 1:
                coef = results.params.iloc[1]
                se = results.bse.iloc[1]
        
        return results, coef, se, df
    
    except Exception as e:
        print(f"Regression error: {e}")
        return None, None, None, df


def main():
    """Main analysis pipeline"""
    
    # Parse ACS data
    df = parse_acs_fixed_width()
    
    if df is None or len(df) == 0:
        print("ERROR: No data parsed")
        output = {
            "spec": {
                "sample_selection": ["Error: No data"],
                "outcome_definition": "Error",
                "treatment_definition": "Error",
                "model_specification_line": "Error"
            },
            "results": {
                "point_estimate": None,
                "standard_error": None,
                "sample_size": 0
            }
        }
        print(json.dumps(output))
        return
    
    print(f"Initial records: {len(df):,}")
    
    # Define sample and variables
    df = define_sample_and_variables(df)
    print(f"After sample restrictions: {len(df):,}")
    
    # Check variation in treatment
    n_eligible = (df['daca_eligible'] == 1).sum()
    n_ineligible = (df['daca_eligible'] == 0).sum()
    print(f"Eligible: {n_eligible:,}, Ineligible: {n_ineligible:,}")
    
    if n_eligible == 0 or n_ineligible == 0:
        print("ERROR: No variation in treatment")
        output = {
            "spec": {
                "sample_selection": ["year in [2013, 2014, 2015, 2016]",
                                      "hispan == 1",
                                      "bpl == 200",
                                      "age in [15, 30]",
                                      "citizen in [3, 4, 5]",
                                      "empstat in [1, 2]",
                                      "uhrswork > 0"],
                "outcome_definition": "1 if uhrswork >= 35 else 0",
                "treatment_definition": "1 if birth_year in [1982, 1996] else 0",
                "model_specification_line": "smf.wls('full_time ~ C(daca_eligible) + C(year) + C(statefip)', data=df, weights=df['perwt']).fit()"
            },
            "results": {
                "point_estimate": None,
                "standard_error": None,
                "sample_size": len(df)
            }
        }
        print(json.dumps(output))
        return
    
    # Fit model
    results, coef, se, df_final = fit_model(df)
    
    if results is None:
        print("ERROR: Model fit failed")
        output = {
            "spec": {
                "sample_selection": ["year in [2013, 2014, 2015, 2016]",
                                      "hispan == 1",
                                      "bpl == 200",
                                      "age in [15, 30]",
                                      "citizen in [3, 4, 5]",
                                      "empstat in [1, 2]",
                                      "uhrswork > 0"],
                "outcome_definition": "1 if uhrswork >= 35 else 0",
                "treatment_definition": "1 if birth_year in [1982, 1996] else 0",
                "model_specification_line": "smf.wls('full_time ~ C(daca_eligible) + C(year) + C(statefip)', data=df, weights=df['perwt']).fit()"
            },
            "results": {
                "point_estimate": None,
                "standard_error": None,
                "sample_size": len(df_final)
            }
        }
        print(json.dumps(output))
        return
    
    # Prepare and output the JSON result
    output = {
        "spec": {
            "sample_selection": [
                "year in [2013, 2014, 2015, 2016]",
                "hispan == 1",
                "bpl == 200",
                "age in [15, 30]",
                "citizen in [3, 4, 5]",
                "empstat in [1, 2]",
                "uhrswork > 0"
            ],
            "outcome_definition": "(df['uhrswork'] >= 35)",
            "treatment_definition": "(df['birth_year'] >= 1982) & (df['birth_year'] <= 1996)",
            "model_specification_line": "smf.wls('full_time ~ C(daca_eligible) + C(year) + C(statefip)', data=df, weights=df['perwt']).fit()"
        },
        "results": {
            "point_estimate": float(coef) if coef is not None else None,
            "standard_error": float(se) if se is not None else None,
            "sample_size": len(df_final)
        }
    }
    
    print(json.dumps(output))


if __name__ == '__main__':
    main()
