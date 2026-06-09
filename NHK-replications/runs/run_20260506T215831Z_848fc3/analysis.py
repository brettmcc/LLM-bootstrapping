#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Estimates the causal effect of DACA eligibility on full-time employment
among Mexican-born Hispanic individuals in 2013-2016.
"""

import json
import struct
import numpy as np
import pandas as pd
from scipy import stats

# Define field positions (1-based in Stata, convert to 0-based for Python)
# From ACS_extract_expanded_layout_excerpt.do
FIELD_SPECS = {
    'year': (0, 4),           # columns 1-4
    'perwt': (691, 701),      # columns 692-701
    'age': (740, 743),        # columns 741-743
    'birthyr': (747, 751),    # columns 748-751
    'hispan': (763, 764),     # columns 764-764
    'bpl': (767, 770),        # columns 768-770
    'citizen': (789, 790),    # columns 790-790
    'empstat': (874, 875),    # columns 875-875
    'uhrswork': (904, 906),   # columns 905-906
}

def parse_fixed_width_line(line, field_specs):
    """Parse a fixed-width line from ACS data using field specifications."""
    data = {}
    for field_name, (start, end) in field_specs.items():
        try:
            value_str = line[start:end].strip()
            if value_str == '':
                data[field_name] = np.nan
            else:
                data[field_name] = int(value_str)
        except (ValueError, IndexError):
            data[field_name] = np.nan
    return data

def read_acs_data_chunked(filename, chunk_size=10000):
    """
    Read ACS fixed-width data file in chunks to manage memory.
    Only loads necessary fields for the analysis.
    """
    records = []
    with open(filename, 'r', encoding='latin1') as f:
        for line_num, line in enumerate(f):
            if len(line.rstrip('\n')) > 900:  # Ensure line is long enough
                data = parse_fixed_width_line(line.rstrip('\n'), FIELD_SPECS)
                records.append(data)
                
                if len(records) >= chunk_size:
                    df = pd.DataFrame(records)
                    yield df
                    records = []
    
    if records:
        df = pd.DataFrame(records)
        yield df

def define_daca_eligibility(df):
    """
    Define DACA eligibility based on ACS data.
    
    DACA eligibility criteria (from prompt):
    1. Arrived unlawfully before age 16
    2. Not yet 31 on June 15, 2012 (born Dec 15, 1981 or later)
    3. Lived continuously since June 15, 2007
    4. Present in US on June 15, 2012 without lawful status
    
    Proxies from ACS:
    - Mexican-born (BPL == 200) or Mexican ethnicity (HISPAN == 1)
    - Not a citizen (CITIZEN in [3, 4, 5])
    - Age eligibility: born 1982-2000 (to be 0-30 in 2012)
    - Present in ACS data = present in US
    """
    
    # Create eligibility indicator
    # Age-based: Not yet 31 on June 15, 2012 means birth year >= 1982 (born Dec 15, 1981 or later)
    # For ACS data, we use birth year from age: birthyr = year - age
    # In our case, we have birthyr directly
    
    df['daca_eligible'] = (
        # Mexican birth or ethnicity
        ((df['bpl'] == 200) | (df['hispan'] == 1)) &
        # Not a citizen (3=not citizen, 4=first papers, 5=citizenship status not reported)
        (df['citizen'].isin([3, 4, 5])) &
        # Age eligibility: born 1982 or later (age < 31 on June 15, 2012)
        (df['birthyr'] >= 1982) &
        # Not too young: born before 2000 (need some time to arrive before age 16)
        (df['birthyr'] < 2000)
    )
    
    return df

def define_outcome(df):
    """
    Define full-time employment outcome.
    Full-time: usually working >= 35 hours per week
    """
    # EMPSTAT == 1 means employed
    # UHRSWORK is usual hours worked per week
    df['full_time'] = (
        (df['empstat'] == 1) &
        (df['uhrswork'] >= 35)
    ).astype(int)
    
    return df

def create_sample(df):
    """
    Create analysis sample.
    - Years: 2013-2016 (post-DACA period for effect estimation)
    - Age: 18-65 (working age)
    - Mexican-born or Mexican Hispanic ethnicity
    - Data must be non-missing for key variables
    """
    
    # Filter to post-DACA years for effect estimation
    df = df[df['year'].isin([2013, 2014, 2015, 2016])].copy()
    
    # Working age population
    df = df[(df['age'] >= 18) & (df['age'] <= 65)].copy()
    
    # Mexican-born or Mexican ethnicity
    df = df[((df['bpl'] == 200) | (df['hispan'] == 1))].copy()
    
    # Non-citizens only (likely undocumented or recent immigrants)
    df = df[df['citizen'].isin([3, 4, 5])].copy()
    
    # Non-missing key variables
    df = df[
        df['empstat'].notna() &
        df['uhrswork'].notna() &
        df['birthyr'].notna()
    ].copy()
    
    # Define treatment based on birth year cutoff
    # DACA eligibility requires age < 31 on June 15, 2012
    # Born on or after Dec 15, 1981 = age < 31 on June 15, 2012
    # Using conservative cutoff: born 1982 or later for treated
    df['daca_treated'] = (df['birthyr'] >= 1982).astype(int)
    
    return df

def calculate_weights(df):
    """
    Convert ACS person weights from scaled integers to proper weights.
    According to layout file: perwt needs to be divided by 100
    """
    df['weight'] = df['perwt'] / 100.0
    return df

def estimate_effect_dd(df):
    """
    Estimate DACA effect using a differences approach.
    
    Treated: DACA eligible (born 1982-1999)
    Control: Too old for DACA (born 1981 or earlier)
    
    This uses variation in treatment eligibility based on birth year cutoff.
    """
    
    # Remove missing weights
    df = df[(df['weight'].notna()) & (df['weight'] > 0)].copy()
    
    # Prepare data for WLS regression
    # Outcome: full_time employment
    # Predictor: daca_treated eligibility
    
    y = df['full_time'].values
    X = np.column_stack([np.ones(len(df)), df['daca_treated'].values])
    weights = df['weight'].values
    
    # Weighted least squares using direct computation
    # Normalize weights
    sqrt_w = np.sqrt(weights)
    
    # Transform variables by sqrt(weights)
    X_weighted = X * sqrt_w[:, np.newaxis]
    y_weighted = y * sqrt_w
    
    try:
        # Solve normal equations: (X'WX)^-1 X'Wy
        XtX = X_weighted.T @ X_weighted
        Xty = X_weighted.T @ y_weighted
        
        # Solve for beta
        beta = np.linalg.solve(XtX, Xty)
        
        # Calculate residuals (unweighted for SE calculation)
        y_pred = X @ beta
        residuals = y - y_pred
        
        # Calculate standard errors using HC1 (heteroskedasticity-consistent)
        # Var(beta) = (X'WX)^-1 X'W Var(residuals) W X (X'WX)^-1
        
        residuals_sq = residuals ** 2
        
        # Compute X'W Diag(residuals_sq) W X without forming full matrix
        # This is equivalent to: X' @ diag(weights * residuals_sq) @ X
        weighted_residuals = (weights * residuals_sq)[:, np.newaxis] * X
        XtWRWX = X.T @ weighted_residuals
        
        # Var(beta) = (X'WX)^-1 @ XtWRWX @ (X'WX)^-1
        XtX_inv = np.linalg.inv(XtX)
        var_beta = XtX_inv @ XtWRWX @ XtX_inv
        
        se_beta = np.sqrt(np.diag(var_beta))
        
        # Extract treatment effect (second coefficient, index 1)
        point_estimate = beta[1]
        standard_error = se_beta[1]
        
        sample_size = len(df)
        
        return point_estimate, standard_error, sample_size
        
    except np.linalg.LinAlgError:
        # If matrix is singular, return NaN
        return np.nan, np.nan, len(df)

def main():
    """Main analysis function."""
    
    # Read ACS data in chunks and process
    all_records = []
    
    print("Reading ACS data...", flush=True)
    for chunk_df in read_acs_data_chunked('ACS_extract_expanded.dat', chunk_size=50000):
        # Process each chunk
        chunk_df = define_daca_eligibility(chunk_df)
        chunk_df = define_outcome(chunk_df)
        chunk_df = calculate_weights(chunk_df)
        all_records.append(chunk_df)
    
    # Combine all chunks
    if all_records:
        df = pd.concat(all_records, ignore_index=True)
    else:
        raise ValueError("No data read from ACS file")
    
    print(f"Total records read: {len(df)}", flush=True)
    
    # Create analysis sample
    df = create_sample(df)
    print(f"Sample size after filtering: {len(df)}", flush=True)
    
    # Check treatment variation
    treated_count = df['daca_treated'].sum()
    control_count = (~df['daca_treated'].astype(bool)).sum()
    print(f"Treated (born 1982+): {treated_count}", flush=True)
    print(f"Control (born <1982): {control_count}", flush=True)
    
    if treated_count == 0 or control_count == 0:
        raise ValueError("No variation in treatment variable")
    
    # Calculate descriptive statistics
    treated_employment = df[df['daca_treated'] == 1]['full_time'].mean()
    control_employment = df[df['daca_treated'] == 0]['full_time'].mean()
    print(f"Full-time employment rate - Treated: {treated_employment:.4f}", flush=True)
    print(f"Full-time employment rate - Control: {control_employment:.4f}", flush=True)
    
    # Estimate treatment effect
    point_estimate, standard_error, sample_size = estimate_effect_dd(df)
    
    print(f"Point estimate: {point_estimate}", flush=True)
    print(f"Standard error: {standard_error}", flush=True)
    print(f"Sample size: {sample_size}", flush=True)
    
    # Output results as JSON
    results = {
        "point_estimate": float(point_estimate) if not np.isnan(point_estimate) else None,
        "standard_error": float(standard_error) if not np.isnan(standard_error) else None,
        "sample_size": int(sample_size)
    }
    
    # Save spec to spec.json
    spec = {
        "sample_selection": [
            "year in [2013, 2014, 2015, 2016]",
            "age >= 18 and age <= 65",
            "(bpl == 200) or (hispan == 1)",
            "citizen in [3, 4, 5]",
            "empstat and uhrswork not missing"
        ],
        "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
        "treatment_definition": "birthyr >= 1982",
        "model_specification_line": "WLS regression with treatment indicator on full-time employment"
    }
    
    with open('spec.json', 'w') as f:
        json.dump(spec, f, indent=2)
    
    # Output results only
    print(json.dumps(results))

if __name__ == '__main__':
    main()
