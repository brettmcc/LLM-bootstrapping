"""
DACA Impact Analysis: Full-Time Employment Effect
Using age-based identification strategy with DiD approach
"""
import json
import pandas as pd
import numpy as np
from statsmodels.formula.api import wls

def read_acs_data_chunked(filepath):
    """
    Read fixed-width ACS data file by reading chunks and extracting columns explicitly.
    This avoids issues with read_fwf on large files.
    """
    # Define column positions (0-based for string slicing)
    # Stata 1-based positions: convert to 0-based via (pos-1)
    cols = {
        'year': (0, 4),
        'statefip': (65, 67),
        'perwt': (691, 701),
        'age': (740, 743),
        'hispan': (763, 764),
        'bpl': (767, 770),
        'citizen': (789, 790),
        'empstat': (874, 875),
        'uhrswork': (904, 906),
    }
    
    data_list = []
    with open(filepath, 'r') as f:
        for line in f:
            if len(line) < 906:  # Skip short lines
                continue
            
            row = {}
            for col_name, (start, end) in cols.items():
                val = line[start:end].strip()
                try:
                    row[col_name] = int(val) if val else None
                except ValueError:
                    row[col_name] = None
            
            data_list.append(row)
            
            # Process in chunks for memory efficiency
            if len(data_list) >= 100000:
                yield pd.DataFrame(data_list)
                data_list = []
    
    if data_list:
        yield pd.DataFrame(data_list)

def process_acs_data():
    """
    Read, process, and analyze ACS data for DACA impact on full-time employment.
    """
    print("Reading ACS data...", flush=True)
    
    # Read data in chunks and process
    dfs = []
    for i, chunk in enumerate(read_acs_data_chunked('ACS_extract_expanded.dat')):
        print(f"Chunk {i}: {len(chunk)} rows", flush=True)
        dfs.append(chunk)
    
    df = pd.concat(dfs, ignore_index=True)
    print(f"Total data: {len(df)} rows", flush=True)
    
    # Clean and type conversions
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print("Applying sample filters...", flush=True)
    
    # Sample selection filters
    # 1. Mexican-origin: hispan==1 or bpl==200
    mexican = (df['hispan'] == 1) | (df['bpl'] == 200)
    
    # 2. Noncitizen: citizen in [3, 4, 5]
    noncitizen = df['citizen'].isin([3, 4, 5])
    
    # 3. Age 16-65 (working age)
    working_age = (df['age'] >= 16) & (df['age'] <= 65)
    
    # 4. Valid employment and hours data
    has_empstat = df['empstat'].notna() & (df['empstat'] == 1)  # Only employed
    has_uhrswork = df['uhrswork'].notna() & (df['uhrswork'] > 0)
    
    # 5. Year in analysis period
    valid_year = df['year'].between(2006, 2016)
    
    # 6. Positive weight
    has_weight = df['perwt'] > 0
    
    # Apply all filters
    sample_mask = mexican & noncitizen & working_age & has_empstat & has_uhrswork & valid_year & has_weight
    df_sample = df[sample_mask].copy()
    
    print(f"Sample size after filters: {len(df_sample)}", flush=True)
    
    if len(df_sample) == 0:
        raise ValueError("Empty sample after filters. Specification needs revision.")
    
    # Create outcome: full-time employment (usually working 35+ hours per week)
    df_sample['full_time'] = (df_sample['uhrswork'] >= 35).astype(int)
    
    # Create treatment: DACA eligibility based on age
    # DACA eligible if would have been age 0-30 on June 15, 2012
    df_sample['birth_year'] = df_sample['year'] - df_sample['age']
    df_sample['daca_eligible'] = (df_sample['birth_year'] >= 1982).astype(int)
    
    print(f"DACA-eligible count: {df_sample['daca_eligible'].sum()}", flush=True)
    print(f"Full-time employed count: {df_sample['full_time'].sum()}", flush=True)
    
    # Check treatment variation
    if df_sample['daca_eligible'].sum() == 0:
        raise ValueError("No DACA-eligible individuals in sample. Specification needs revision.")
    if df_sample['daca_eligible'].sum() == len(df_sample):
        raise ValueError("All individuals are DACA-eligible. Specification needs revision.")
    
    # Create period indicator (post-DACA: 2013-2016, pre-DACA: 2006-2012)
    df_sample['post_daca'] = (df_sample['year'] >= 2013).astype(int)
    
    # Interaction term for DiD
    df_sample['eligible_x_post'] = df_sample['daca_eligible'] * df_sample['post_daca']
    
    print(f"Variation in treatment: {df_sample['daca_eligible'].var()}", flush=True)
    
    # Normalize weights for WLS
    weights = df_sample['perwt'] / df_sample['perwt'].mean()
    
    # Estimate DiD model
    model_spec = 'full_time ~ daca_eligible + post_daca + eligible_x_post'
    model = wls(model_spec, data=df_sample, weights=weights)
    results = model.fit()
    
    # Extract treatment effect (DiD coefficient)
    point_estimate = results.params['eligible_x_post']
    standard_error = results.bse['eligible_x_post']
    sample_size = len(df_sample)
    
    # Specification JSON
    spec = {
        "sample_selection": [
            "hispan==1 or bpl==200 (Mexican-origin)",
            "citizen in [3,4,5] (Noncitizen or unknown citizenship)",
            "age between 16 and 65 (Working age)",
            "empstat==1 (Employed)",
            "uhrswork > 0 (Positive hours worked)",
            "year between 2006 and 2016",
            "perwt > 0 (positive person weight)"
        ],
        "outcome_definition": "uhrswork >= 35 (usually working 35+ hours per week)",
        "treatment_definition": "DACA eligible indicator: birth year >= 1982 (would be <=30 on June 15, 2012)",
        "model_specification_line": "wls('full_time ~ daca_eligible + post_daca + eligible_x_post', data=df, weights=perwt/mean(perwt)).fit()"
    }
    
    # Results JSON
    results_dict = {
        "point_estimate": float(point_estimate),
        "standard_error": float(standard_error),
        "sample_size": int(sample_size)
    }
    
    # Output required JSON
    output = {
        "spec": spec,
        "results": results_dict
    }
    
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    process_acs_data()
