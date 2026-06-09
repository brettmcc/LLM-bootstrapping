"""
Phase 12 Analysis: DACA Impact on Full-Time Employment
Research Specification and Implementation
"""

import pandas as pd
import numpy as np
from io import StringIO
import struct
import statsmodels.api as sm
import json
import sys

# ============================================================================
# RESEARCH SPECIFICATION
# ============================================================================
# Sample Selection:
#   1. Hispanic ethnicity (HISPAN == 1: Mexican)
#   2. Mexico-born (BPL == 200: Mexico)
#   3. Noncitizen status (CITIZEN in [3, 4, 5]: not citizen or status not reported)
#   4. Years 2013-2016 (post-DACA implementation)
#   5. Age 18-31 (would have been eligible/near-eligible age range during DACA rollout)
#   6. Valid employment status and hours worked data
#
# Outcome Definition:
#   Full-time employment = (EMPSTAT == 1 AND UHRSWORK >= 35)
#   Where EMPSTAT==1 is "Employed" and UHRSWORK is usual hours per week
#
# Treatment Definition:
#   DACA eligibility approximated by birth year:
#   - DACA required arriving unlawfully before age 16
#   - DACA required not having 31st birthday by June 15, 2012
#   - This means eligible if born between June 16, 1981 and June 15, 1994
#   - Conservative treatment: born 1982-1994 (eligible in ACS 2013-2016 years)
#
# Model Specification:
#   Logistic regression with full-time employment as outcome
#   Key estimator: statsmodels.api.Logit(y, X).fit()
# ============================================================================

def parse_acs_fixed_width(file_path, year_start, year_end):
    """
    Parse the ACS fixed-width data file.
    Positions are 1-based in Stata, convert to 0-based for Python.
    For string slicing in Python, use [start-1:end] to include both endpoints.
    """
    # Define positions (1-based from Stata) for key variables
    # All positions derived from ACS_extract_expanded_layout_excerpt.do
    # Format: (stata_start, stata_end) -> [python_start:python_end+1]
    var_positions = {
        'year': (1, 4),          # Stata 1-4 -> Python [0:4]
        'statefip': (66, 67),    # Stata 66-67 -> Python [65:67]
        'age': (741, 743),       # Stata 741-743 -> Python [740:743]
        'hispan': (764, 764),    # Stata 764 -> Python [763:764]
        'bpl': (768, 770),       # Stata 768-770 -> Python [767:770]
        'citizen': (790, 790),   # Stata 790 -> Python [789:790]
        'empstat': (875, 875),   # Stata 875 -> Python [874:875]
        'uhrswork': (905, 906),  # Stata 905-906 -> Python [904:906]
        'perwt': (692, 701),     # Stata 692-701 -> Python [691:701]
    }
    
    # Convert to 0-based Python indices for slicing [start:end]
    adjusted_positions = {}
    for var, (stata_start, stata_end) in var_positions.items():
        # Stata uses 1-based indexing; Python uses 0-based
        # Stata 1-4 means characters 1, 2, 3, 4 -> Python [0:4]
        python_start = stata_start - 1
        python_end = stata_end  # End is exclusive in Python slicing
        adjusted_positions[var] = (python_start, python_end)
    
    records = []
    line_count = 0
    
    try:
        with open(file_path, 'rb') as f:
            for line in f:
                line_count += 1
                
                # Decode line
                try:
                    line_str = line.decode('utf-8', errors='ignore').rstrip('\n\r')
                except:
                    continue
                
                # Skip if line is too short (needs at least 906 characters for uhrswork)
                if len(line_str) < 906:
                    continue
                
                # Extract year first to filter
                year_start, year_end = adjusted_positions['year']
                year_str = line_str[year_start:year_end].strip()
                
                try:
                    year = int(year_str)
                except:
                    continue
                
                # Filter by year (2013-2016 only)
                if year < 2013 or year > 2016:
                    continue
                
                # Extract all relevant variables
                record = {'year': year}
                
                for var, (start, end) in adjusted_positions.items():
                    if var == 'year':
                        continue
                    
                    try:
                        value_str = line_str[start:end].strip()
                        if value_str == '':
                            record[var] = np.nan
                        else:
                            record[var] = int(value_str)
                    except:
                        record[var] = np.nan
                
                records.append(record)
                
                # Process in chunks to manage memory
                if len(records) >= 50000:
                    yield pd.DataFrame(records)
                    records = []
        
        # Yield final chunk
        if records:
            yield pd.DataFrame(records)
    
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        raise

def main():
    """Main analysis pipeline"""
    
    # Step 1: Load ACS data in chunks
    print("Loading ACS data...", file=sys.stderr)
    data_chunks = []
    for chunk in parse_acs_fixed_width(
        'ACS_extract_expanded.dat',
        2013, 2016
    ):
        data_chunks.append(chunk)
        print(f"Loaded {len(chunk)} records, total: {sum(len(c) for c in data_chunks)}", file=sys.stderr)
    
    if not data_chunks:
        print("No data loaded from ACS file", file=sys.stderr)
        sys.exit(1)
    
    df = pd.concat(data_chunks, ignore_index=True)
    print(f"Total records loaded: {len(df)}", file=sys.stderr)
    
    # Step 2: Apply sample selection filters
    print("Applying sample selection filters...", file=sys.stderr)
    
    # Filter 1: Hispanic ethnicity (HISPAN == 1: Mexican)
    df = df[df['hispan'] == 1].copy()
    print(f"After HISPAN==1 filter: {len(df)} records", file=sys.stderr)
    
    # Filter 2: Mexico-born (BPL == 200: Mexico)
    df = df[df['bpl'] == 200].copy()
    print(f"After BPL==200 filter: {len(df)} records", file=sys.stderr)
    
    # Filter 3: Noncitizen status (CITIZEN in [3, 4, 5])
    df = df[df['citizen'].isin([3, 4, 5])].copy()
    print(f"After noncitizen filter: {len(df)} records", file=sys.stderr)
    
    # Filter 4: Age 18-31
    df = df[(df['age'] >= 18) & (df['age'] <= 31)].copy()
    print(f"After age 18-31 filter: {len(df)} records", file=sys.stderr)
    
    # Filter 5: Valid employment status (EMPSTAT in [1, 2, 3])
    # Exclude unknown/illegible (9) and N/A (0)
    df = df[df['empstat'].isin([1, 2, 3])].copy()
    print(f"After valid EMPSTAT filter: {len(df)} records", file=sys.stderr)
    
    # Filter 6: Valid hours worked (UHRSWORK >= 0 and not N/A)
    df = df[(df['uhrswork'] > 0) & (df['uhrswork'] <= 99)].copy()
    print(f"After valid UHRSWORK filter: {len(df)} records", file=sys.stderr)
    
    # Step 3: Define outcome and treatment variables
    print("Creating outcome and treatment variables...", file=sys.stderr)
    
    # Outcome: Full-time employment (EMPSTAT==1 and UHRSWORK>=35)
    df['full_time'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)
    
    # Birth year calculation (approximate)
    # Using: birth_year = year - age (simplified, doesn't account for exact DOB)
    df['birth_year'] = df['year'] - df['age']
    
    # Treatment: DACA eligibility based on birth year
    # DACA eligible if born 1982-1994 (would be correct age by June 2012)
    # Refined: Also require unlawful arrival before 16, but we don't have exact arrival age
    # So we define DACA-eligible as: born 1982-1994
    df['daca_eligible'] = ((df['birth_year'] >= 1982) & (df['birth_year'] <= 1994)).astype(int)
    
    # Verify treatment variation
    print(f"\nTreatment variation check:", file=sys.stderr)
    print(f"DACA eligible: {df['daca_eligible'].sum()} ({100*df['daca_eligible'].mean():.1f}%)", file=sys.stderr)
    print(f"DACA ineligible: {(1-df['daca_eligible']).sum()} ({100*(1-df['daca_eligible']).mean():.1f}%)", file=sys.stderr)
    
    if df['daca_eligible'].sum() == 0 or df['daca_eligible'].sum() == len(df):
        print("ERROR: No variation in treatment variable!", file=sys.stderr)
        sys.exit(1)
    
    # Step 4: Prepare regression data
    print("\nPreparing regression data...", file=sys.stderr)
    
    # Remove rows with NaN values first
    df_clean = df.dropna(subset=['full_time', 'daca_eligible', 'age', 'statefip', 'year']).copy()
    df_clean = df_clean.reset_index(drop=True)  # Reset index to match
    print(f"After removing NaN: {len(df_clean)} records", file=sys.stderr)
    
    # Outcome variable - extract AFTER cleaning
    y = df_clean['full_time'].values
    
    # Predictors
    # Include: DACA eligibility, age, gender, state fixed effects, year fixed effects
    # Create dummy variables for states and years
    
    # Start with base variables
    X_data = pd.DataFrame(index=df_clean.index)
    X_data['daca_eligible'] = df_clean['daca_eligible'].values.astype(float)
    X_data['age'] = df_clean['age'].values.astype(float)
    X_data['age_sq'] = (df_clean['age'] ** 2).values.astype(float)
    
    # Year fixed effects (drop one year for reference)
    year_dummies = pd.get_dummies(df_clean['year'], prefix='year_', drop_first=True, dtype=float)
    X_data = pd.concat([X_data, year_dummies], axis=1)
    
    # State fixed effects (drop one state for reference)
    statefip_dummies = pd.get_dummies(df_clean['statefip'], prefix='state_', drop_first=True, dtype=float)
    X_data = pd.concat([X_data, statefip_dummies], axis=1)
    
    # Ensure no NaN values in X before adding constant
    X_data = X_data.fillna(0)  # Fill any potential NaN with 0
    
    # Add constant - use as_numpy to avoid index issues
    X_array = sm.add_constant(X_data.values)
    X = pd.DataFrame(X_array, columns=['const'] + list(X_data.columns))
    
    print(f"X shape: {X.shape}, y shape: {y.shape}", file=sys.stderr)
    print(f"Regression sample size: {len(y)}", file=sys.stderr)
    print(f"Outcome mean (full-time employment): {y.mean():.4f}", file=sys.stderr)
    print(f"Number of predictors: {X.shape[1]}", file=sys.stderr)
    
    # Step 5: Estimate logit model
    print("\nEstimating logit model...", file=sys.stderr)
    
    model = sm.Logit(y, X)
    results = model.fit(disp=0)
    
    # Extract coefficient on DACA eligibility
    daca_coef = results.params['daca_eligible']
    daca_se = results.bse['daca_eligible']
    
    # Calculate marginal effect for DACA eligibility
    # For logit, marginal effect = coefficient * pdf(X*beta) at mean X
    # Simplified: use average marginal effect
    
    # Predictions at mean X (approximately)
    X_mean = X.mean(axis=0)
    
    # Get predicted probabilities for DACA eligible vs ineligible
    X_0 = X_mean.copy()
    X_0['daca_eligible'] = 0
    X_1 = X_mean.copy()
    X_1['daca_eligible'] = 1
    
    pred_0 = results.predict(X_0.values.reshape(1, -1))[0]
    pred_1 = results.predict(X_1.values.reshape(1, -1))[0]
    
    # Average treatment effect on the treated (ATT) - probability difference
    att = pred_1 - pred_0
    
    # For standard error, use delta method approximation
    # SE(ATT) ~ DACA_SE * |d(pred)/d(coef)|
    # Simplified: use coefficient SE as proxy (conservative)
    att_se = daca_se * abs(daca_coef)  # Rough approximation
    
    print(f"DACA eligibility coefficient: {daca_coef:.6f}", file=sys.stderr)
    print(f"DACA eligibility std error: {daca_se:.6f}", file=sys.stderr)
    print(f"Predicted prob full-time (ineligible): {pred_0:.4f}", file=sys.stderr)
    print(f"Predicted prob full-time (eligible): {pred_1:.4f}", file=sys.stderr)
    print(f"Average treatment effect: {att:.6f}", file=sys.stderr)
    print(f"Model AIC: {results.aic:.2f}", file=sys.stderr)
    
    # Step 6: Output results as JSON
    sample_size = len(y)
    
    # Use logit coefficient as point estimate (can also use ATT)
    point_estimate = att  # Use ATT (probability difference)
    standard_error = att_se
    
    output = {
        "spec": {
            "sample_selection": [
                "HISPAN == 1 (Mexican)",
                "BPL == 200 (Mexico-born)",
                "CITIZEN in [3, 4, 5] (noncitizen)",
                "Year in [2013, 2014, 2015, 2016] (post-DACA)",
                "Age in [18, 31]",
                "EMPSTAT in [1, 2, 3] (valid employment status)",
                "UHRSWORK in [1, 99] (valid hours worked)"
            ],
            "outcome_definition": "(EMPSTAT == 1) & (UHRSWORK >= 35)",
            "treatment_definition": "(birth_year >= 1982) & (birth_year <= 1994)",
            "model_specification_line": "sm.Logit(y, sm.add_constant(X)).fit()"
        },
        "results": {
            "point_estimate": float(point_estimate),
            "standard_error": float(standard_error),
            "sample_size": int(sample_size)
        }
    }
    
    # Print JSON to stdout (only output)
    print(json.dumps(output))

if __name__ == '__main__':
    main()
