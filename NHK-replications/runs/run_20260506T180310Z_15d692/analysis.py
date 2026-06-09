#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment
Analyzes the causal effect of DACA eligibility on full-time employment for 
Hispanic-Mexican Mexican-born individuals in the US, using ACS data from 2006-2016.
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
import struct

# Read the fixed-width ACS data file using positions from the layout
def read_acs_data(filename, chunk_size=50000):
    """
    Read the ACS_extract_expanded.dat fixed-width file and extract relevant variables.
    Uses exact column positions from ACS_extract_expanded_layout_excerpt.do
    Reads in chunks for memory efficiency.
    """
    
    # Column positions (1-indexed in .do file, convert to 0-indexed Python)
    columns = {
        'year': (0, 4),           # 1-4 in .do file
        'hispan': (763, 764),     # 764-764 in .do file
        'bpl': (767, 770),        # 768-770 in .do file
        'citizen': (789, 790),    # 790-790 in .do file
        'age': (740, 743),        # 741-743 in .do file
        'empstat': (874, 875),    # 875-875 in .do file
        'uhrswork': (904, 906),   # 905-906 in .do file
        'perwt': (691, 701),      # 692-701 in .do file
    }
    
    all_data = []
    
    # Read the fixed-width file in chunks
    try:
        with open(filename, 'r', encoding='latin-1', buffering=256*1024) as f:
            chunk = []
            chunk_count = 0
            
            for line_num, line in enumerate(f, 1):
                try:
                    row_data = {}
                    for var, (start, end) in columns.items():
                        # Extract the substring (accounting for Python 0-indexing)
                        if len(line) > start:
                            value_str = line[start:min(end, len(line))].strip()
                        else:
                            value_str = ''
                        
                        if not value_str:
                            # Missing value
                            row_data[var] = np.nan
                        else:
                            # Try to convert to numeric
                            try:
                                value = float(value_str)
                                row_data[var] = value
                            except ValueError:
                                row_data[var] = np.nan
                    
                    chunk.append(row_data)
                    
                    # Process chunk when it reaches the size limit
                    if len(chunk) >= chunk_size:
                        chunk_df = pd.DataFrame(chunk)
                        all_data.append(chunk_df)
                        chunk = []
                        chunk_count += 1
                        if chunk_count % 10 == 0:
                            print(f"  Processed {line_num} lines...", flush=True)
                except Exception as e:
                    # Skip problematic lines
                    pass
            
            # Process remaining chunk
            if chunk:
                chunk_df = pd.DataFrame(chunk)
                all_data.append(chunk_df)
    
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        return pd.DataFrame()
    
    # Concatenate all chunks
    if all_data:
        df = pd.concat(all_data, ignore_index=True)
    else:
        df = pd.DataFrame()
    
    if len(df) > 0:
        # Convert to appropriate types
        df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
        df['hispan'] = pd.to_numeric(df['hispan'], errors='coerce').astype('Int64')
        df['bpl'] = pd.to_numeric(df['bpl'], errors='coerce').astype('Int64')
        df['citizen'] = pd.to_numeric(df['citizen'], errors='coerce').astype('Int64')
        df['age'] = pd.to_numeric(df['age'], errors='coerce').astype('Int64')
        df['empstat'] = pd.to_numeric(df['empstat'], errors='coerce').astype('Int64')
        df['uhrswork'] = pd.to_numeric(df['uhrswork'], errors='coerce').astype('Int64')
        df['perwt'] = pd.to_numeric(df['perwt'], errors='coerce') / 100.0  # ACS weights have implied 2 decimals
    
    return df

# Load ACS data
print("Loading ACS data...", flush=True)
df = read_acs_data('ACS_extract_expanded.dat')

print(f"Total records: {len(df)}", flush=True)

# Apply sample selection filters
# 1. Hispanic-Mexican: hispan==1 (Mexican) AND bpl==200 (Mexico)
# 2. Non-citizen (to match DACA eligibility): citizen in [3, 4, 5]
# 3. Age eligibility: born between 1982-1995 (to be 16-31 in 2012)
#    In year Y, birth year is approximately Y - age
#    For DACA eligibility: need to be 31 or younger on June 15, 2012
#    So need birth year >= 1981
#    And need to be at least 16 by 2012, so birth year <= 1996
#    Using 1982-1995 to be conservative
# 4. Years 2013-2016 (post-DACA implementation, adequate treatment period)

# Filter for Hispanic-Mexican Mexican-born
df = df[(df['hispan'] == 1) & (df['bpl'] == 200)].copy()
print(f"After hispan-Mexican-born filter: {len(df)}", flush=True)

# Filter for non-citizens
df = df[df['citizen'].isin([3, 4, 5])].copy()
print(f"After non-citizen filter: {len(df)}", flush=True)

# Filter for age eligibility (birth year 1982-1995)
# Birth year ≈ year - age
df['birth_year'] = df['year'] - df['age']
df = df[(df['birth_year'] >= 1982) & (df['birth_year'] <= 1995)].copy()
print(f"After age eligibility filter: {len(df)}", flush=True)

# Filter for years 2013-2016 (post-DACA, excluding partial 2012)
df = df[(df['year'] >= 2013) & (df['year'] <= 2016)].copy()
print(f"After year filter (2013-2016): {len(df)}", flush=True)

# Define outcome: full-time employment (working 35+ hours per week)
# empstat == 1 (employed) AND uhrswork >= 35
df['full_time_employed'] = (
    (df['empstat'] == 1) & (df['uhrswork'] >= 35)
).astype(int)

# Check outcome variation
outcome_mean = df['full_time_employed'].mean()
print(f"Full-time employment rate: {outcome_mean:.4f}", flush=True)

# Verify sample has variation in treatment
# Since all observations are post-DACA (2013-2016) and meet DACA eligibility criteria,
# treatment=1 for all in this sample
# We need variation - let's use a difference-in-differences style approach
# by comparing against pre-treatment years (2007-2011)

# Re-read data and create full sample with pre and post-DACA periods
print("\nReloading data for comparison group...", flush=True)
df_full = read_acs_data('ACS_extract_expanded.dat')

# Apply same selection filters but keep pre-treatment period
df_full = df_full[(df_full['hispan'] == 1) & (df_full['bpl'] == 200)].copy()
df_full = df_full[df_full['citizen'].isin([3, 4, 5])].copy()
df_full['birth_year'] = df_full['year'] - df_full['age']
df_full = df_full[(df_full['birth_year'] >= 1982) & (df_full['birth_year'] <= 1995)].copy()

# Filter for years 2007-2016 (to include pre-treatment period)
df_full = df_full[(df_full['year'] >= 2007) & (df_full['year'] <= 2016)].copy()
print(f"Full sample (2007-2016): {len(df_full)}", flush=True)

# Define treatment and outcome
df_full['post_daca'] = (df_full['year'] >= 2013).astype(int)
df_full['full_time_employed'] = (
    (df_full['empstat'] == 1) & (df_full['uhrswork'] >= 35)
).astype(int)

# Check variation in treatment and outcome
print(f"\nTreatment variation (post_daca):")
print(f"  Pre-DACA (2007-2012): {(df_full['post_daca'] == 0).sum()}")
print(f"  Post-DACA (2013-2016): {(df_full['post_daca'] == 1).sum()}")

# Check outcome variation within treatment group
post_daca_sample = df_full[df_full['post_daca'] == 1]
pre_daca_sample = df_full[df_full['post_daca'] == 0]

print(f"\nFull-time employment rates:")
print(f"  Pre-DACA: {pre_daca_sample['full_time_employed'].mean():.4f}")
print(f"  Post-DACA: {post_daca_sample['full_time_employed'].mean():.4f}")

if post_daca_sample['full_time_employed'].var() == 0 or pre_daca_sample['full_time_employed'].var() == 0:
    print("\nWarning: No variation in outcome - revising specification")

# Estimate DACA effect using difference-in-differences
# Model: full_time_employed = β₀ + β₁*post_daca + controls
# We'll use statsmodels for robust weighted OLS

try:
    import statsmodels.api as sm
    
    # Prepare data for regression
    df_reg = df_full.dropna(subset=['full_time_employed', 'post_daca', 'age', 'year', 'perwt'])
    
    # Ensure all variables are numeric
    df_reg = df_reg.copy()
    df_reg['post_daca'] = pd.to_numeric(df_reg['post_daca'], errors='coerce')
    df_reg['age'] = pd.to_numeric(df_reg['age'], errors='coerce')
    df_reg['full_time_employed'] = pd.to_numeric(df_reg['full_time_employed'], errors='coerce')
    df_reg['perwt'] = pd.to_numeric(df_reg['perwt'], errors='coerce')
    
    # Drop any rows with NaN after conversion
    df_reg = df_reg.dropna()
    
    # Create year dummies
    year_dummies = pd.get_dummies(df_reg['year'].astype(str), prefix='year_', drop_first=True, dtype=float)
    
    # Construct design matrix
    X = df_reg[['post_daca', 'age']].copy().astype(float)
    X = pd.concat([X, year_dummies], axis=1)
    X = sm.add_constant(X)
    
    y = df_reg['full_time_employed'].values.astype(float)
    weights = df_reg['perwt'].values.astype(float)
    
    # Fit weighted OLS regression
    wls_model = sm.WLS(y, X, weights=weights)
    results = wls_model.fit()
    
    # Extract treatment effect (post_daca coefficient)
    point_estimate = results.params['post_daca']
    standard_error = results.bse['post_daca']
    sample_size = len(df_reg)
    
    print(f"\nRegression Results:")
    print(f"  Point Estimate (DACA Effect): {point_estimate:.6f}")
    print(f"  Standard Error: {standard_error:.6f}")
    print(f"  Sample Size: {sample_size}")

except ImportError:
    print("statsmodels not available, using alternative method...")
    
    # Fallback: Use manual weighted regression
    # Prepare data for regression
    df_reg = df_full.dropna(subset=['full_time_employed', 'post_daca', 'age', 'year', 'perwt'])
    
    # Ensure all variables are numeric
    df_reg = df_reg.copy()
    df_reg['post_daca'] = pd.to_numeric(df_reg['post_daca'], errors='coerce')
    df_reg['age'] = pd.to_numeric(df_reg['age'], errors='coerce')
    df_reg['full_time_employed'] = pd.to_numeric(df_reg['full_time_employed'], errors='coerce')
    df_reg['perwt'] = pd.to_numeric(df_reg['perwt'], errors='coerce')
    
    # Drop any rows with NaN
    df_reg = df_reg.dropna()
    
    # Create year dummies
    year_dummies = pd.get_dummies(df_reg['year'].astype(str), prefix='year_', drop_first=True, dtype=float)
    
    # Construct design matrix with constant
    X = df_reg[['post_daca', 'age']].copy().astype(float)
    X = pd.concat([X, year_dummies], axis=1)
    X.insert(0, 'const', 1.0)
    
    y = df_reg['full_time_employed'].values.astype(float)
    weights = df_reg['perwt'].values.astype(float)
    
    # Use lstsq for weighted regression (more stable than inv)
    X_array = X.values.astype(float)
    y_array = y.astype(float)
    
    # Create weighted versions
    sqrt_weights = np.sqrt(np.abs(weights))  # Add abs to handle any negative weights
    X_weighted = X_array * sqrt_weights[:, np.newaxis]
    y_weighted = y_array * sqrt_weights
    
    try:
        # Use least squares solver (more stable than matrix inverse)
        beta, residuals_sum, rank, s = np.linalg.lstsq(X_weighted, y_weighted, rcond=None)
        
        # Calculate residuals and standard errors
        y_pred = X_array @ beta
        residuals = y_array - y_pred
        weighted_residuals = residuals * sqrt_weights
        rss = np.sum(weighted_residuals**2)
        
        # Degrees of freedom
        n = len(y_array)
        k = X_array.shape[1]
        df_resid = n - k
        
        # Variance estimate
        sigma2 = rss / df_resid
        
        # For standard errors, we need the covariance matrix
        # (X'WX)^(-1) where X is weighted X
        XtX = X_weighted.T @ X_weighted
        try:
            XtX_inv = np.linalg.pinv(XtX)  # Use pseudo-inverse for stability
            var_beta = sigma2 * XtX_inv
            se_beta = np.sqrt(np.maximum(np.diag(var_beta), 0))  # Ensure non-negative values
        except:
            # If even pinv fails, use rough SE estimate
            se_beta = np.ones(len(beta)) * np.sqrt(sigma2)
        
        # Extract treatment effect (post_daca coefficient at index 1)
        point_estimate = beta[1]
        standard_error = se_beta[1]
        sample_size = n
        
        print(f"\nRegression Results (using lstsq):")
        print(f"  Point Estimate (DACA Effect): {point_estimate:.6f}")
        print(f"  Standard Error: {standard_error:.6f}")
        print(f"  Sample Size: {sample_size}")
        
    except Exception as e:
        print(f"Error in regression: {e}")
        point_estimate = np.nan
        standard_error = np.nan
        sample_size = len(df_reg)

print(f"\nRegression Results:")
print(f"  Point Estimate (DACA Effect): {point_estimate:.6f}")
print(f"  Standard Error: {standard_error:.6f}")
print(f"  Sample Size: {sample_size}")

# Prepare final specification JSON
spec = {
    "sample_selection": [
        "hispan == 1 (Mexican)",
        "bpl == 200 (Mexico)",
        "citizen in [3, 4, 5] (non-citizen)",
        "birth_year between 1982-1995 (age eligibility for DACA)",
        "year between 2007-2016"
    ],
    "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
    "treatment_definition": "post_daca = (year >= 2013)",
    "model_specification_line": "OLS with weights, covariates: post_daca, age, year fixed effects"
}

results = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

# Output results as JSON to stdout (only the results part for analysis.py)
output = {
    "point_estimate": results["point_estimate"],
    "standard_error": results["standard_error"],
    "sample_size": results["sample_size"]
}

print(json.dumps(output))

# Also save the full specification to spec.json
with open('spec.json', 'w') as f:
    json.dump(spec, f, indent=2)

print(f"\nSpecification saved to spec.json", flush=True)
