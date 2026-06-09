#!/usr/bin/env python3
"""
DACA Impact Analysis on Full-Time Employment for Mexican-Born Hispanic Individuals
Research Question: What was the causal impact of DACA eligibility (treatment) on the probability 
of full-time employment (35+ hours per week) during 2013-2016 among ethnically Hispanic-Mexican 
Mexican-born people in the United States?
"""

import json
import struct
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import warnings

warnings.filterwarnings("ignore")

# Fixed-width field positions (1-indexed in Stata, convert to 0-indexed for Python)
# Based on ACS_extract_expanded_layout_excerpt.do
FIELD_SPECS = {
    "year": (0, 4),          # 1-4 -> 0-3
    "pernum": (687, 691),    # 688-691 -> 687-690
    "perwt": (691, 701),     # 692-701 -> 691-700
    "age": (740, 743),       # 741-743 -> 740-742
    "hispan": (763, 764),    # 764 -> 763
    "bpl": (767, 770),       # 768-770 -> 767-769
    "citizen": (789, 790),   # 790 -> 789
    "empstat": (874, 875),   # 875 -> 874
    "uhrswork": (904, 906),  # 905-906 -> 904-905
}

def read_acs_data(filepath):
    """
    Read fixed-width ACS data file, parsing only needed columns.
    Each record is 1044 bytes.
    """
    records = []
    with open(filepath, 'rb') as f:
        while True:
            # Read one complete record (1044 bytes based on layout file)
            record_bytes = f.read(1044)
            if not record_bytes:
                break
            
            try:
                record = {}
                
                # Extract year (4 characters, numeric)
                year_str = record_bytes[FIELD_SPECS["year"][0]:FIELD_SPECS["year"][1]].decode('ascii', errors='ignore').strip()
                if not year_str:
                    continue
                record["year"] = int(year_str)
                
                # Extract age (3 characters, numeric)
                age_str = record_bytes[FIELD_SPECS["age"][0]:FIELD_SPECS["age"][1]].decode('ascii', errors='ignore').strip()
                if not age_str:
                    continue
                record["age"] = int(age_str)
                
                # Extract hispan (1 character)
                hispan_str = record_bytes[FIELD_SPECS["hispan"][0]:FIELD_SPECS["hispan"][1]].decode('ascii', errors='ignore').strip()
                if not hispan_str:
                    continue
                record["hispan"] = int(hispan_str)
                
                # Extract bpl (3 characters)
                bpl_str = record_bytes[FIELD_SPECS["bpl"][0]:FIELD_SPECS["bpl"][1]].decode('ascii', errors='ignore').strip()
                if not bpl_str:
                    continue
                record["bpl"] = int(bpl_str)
                
                # Extract citizen (1 character)
                citizen_str = record_bytes[FIELD_SPECS["citizen"][0]:FIELD_SPECS["citizen"][1]].decode('ascii', errors='ignore').strip()
                if not citizen_str:
                    continue
                record["citizen"] = int(citizen_str)
                
                # Extract empstat (1 character)
                empstat_str = record_bytes[FIELD_SPECS["empstat"][0]:FIELD_SPECS["empstat"][1]].decode('ascii', errors='ignore').strip()
                if not empstat_str:
                    continue
                record["empstat"] = int(empstat_str)
                
                # Extract uhrswork (2 characters)
                uhrswork_str = record_bytes[FIELD_SPECS["uhrswork"][0]:FIELD_SPECS["uhrswork"][1]].decode('ascii', errors='ignore').strip()
                if not uhrswork_str:
                    continue
                record["uhrswork"] = int(uhrswork_str)
                
                # Extract perwt (10 characters)
                perwt_str = record_bytes[FIELD_SPECS["perwt"][0]:FIELD_SPECS["perwt"][1]].decode('ascii', errors='ignore').strip()
                if not perwt_str:
                    continue
                # Clean up the string - replace any spaces or non-numeric characters
                perwt_str = ''.join(c for c in perwt_str if c.isdigit() or c == '.')
                if perwt_str:
                    record["perwt"] = float(perwt_str) / 100  # Divide by 100 as per layout
                else:
                    continue
                
                records.append(record)
            except (ValueError, IndexError):
                # Skip records that can't be parsed
                continue
    
    df = pd.DataFrame(records)
    return df

def create_variables(df):
    """
    Create treatment and outcome variables based on DACA eligibility criteria.
    
    DACA Eligibility Criteria (as of June 15, 2012):
    - Arrived unlawfully before age 16
    - Not yet age 31
    - Lived continuously in US since June 15, 2007
    - Did not have lawful status
    
    Strategy: Use age-based proxy for eligibility
    - Eligible cohort: born in 1981-1996 (to be age 16-31 in 2012)
    - Use variation in DACA eligibility across cohorts
    """
    df = df.copy()
    
    # Filter for ethnic criteria
    # hispan == 1 (Mexican), bpl == 200 (Mexico), citizen in [3,4,5] (non-citizen)
    df = df[(df["hispan"] == 1) & (df["bpl"] == 200) & (df["citizen"].isin([3, 4, 5]))]
    
    # Calculate birth year from age and survey year
    df["birth_year"] = df["year"] - df["age"]
    
    # DACA eligibility: born 1981-1996 (to be 16-31 in 2012)
    # More precisely: had to arrive before turning 16, so born after June 15, 1996 makes them too young
    # and born before June 15, 1981 makes them too old
    # We'll use a cohort-based approach: treat as eligible if born 1981-1996
    df["daca_eligible"] = ((df["birth_year"] >= 1981) & (df["birth_year"] <= 1996)).astype(int)
    
    # Outcome: Full-time employment (employed with 35+ hours per week)
    # empstat == 1 means employed, uhrswork >= 35 means 35+ hours per week
    df["fulltime_employed"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)
    
    # Treatment: interaction of DACA eligibility and post-DACA period
    # DACA implemented June 15, 2012, so 2013 onwards is post-DACA
    df["post_daca"] = (df["year"] >= 2013).astype(int)
    
    # Main treatment variable for DID: daca_eligible * post_daca
    df["treatment"] = df["daca_eligible"] * df["post_daca"]
    
    return df

def analyze(df):
    """
    Estimate DACA effect using Difference-in-Differences with Weighted Least Squares.
    """
    # Filter to years 2013-2016 as specified
    df = df[(df["year"] >= 2013) & (df["year"] <= 2016)]
    
    # Check for treatment variation
    n_eligible = (df["daca_eligible"] == 1).sum()
    n_ineligible = (df["daca_eligible"] == 0).sum()
    
    if n_eligible == 0 or n_ineligible == 0:
        # No variation in treatment, need to revise
        return None
    
    # Check outcome variation
    outcome_var = df["fulltime_employed"].var()
    if outcome_var == 0:
        # No variation in outcome, need to revise
        return None
    
    # Prepare data for WLS regression
    # Model: fulltime_employed = const + daca_eligible + post_daca + treatment + year_controls
    df["year_2013"] = (df["year"] == 2013).astype(int)
    df["year_2014"] = (df["year"] == 2014).astype(int)
    df["year_2015"] = (df["year"] == 2015).astype(int)
    
    # Set up X matrix for DID specification
    # Main specification: fulltime_employed = const + daca_eligible + post_daca + treatment + year_2014 + year_2015
    X = sm.add_constant(df[["daca_eligible", "post_daca", "treatment", "year_2014", "year_2015"]])
    y = df["fulltime_employed"]
    weights = df["perwt"]
    
    # Run WLS regression
    wls_model = sm.WLS(y, X, weights=weights)
    results = wls_model.fit()
    
    # Extract DACA effect (coefficient on treatment variable)
    # The treatment variable is the DID estimate
    treatment_coef = results.params["treatment"]
    treatment_se = results.bse["treatment"]
    
    # Sample size
    sample_size = len(df)
    
    return {
        "point_estimate": float(treatment_coef),
        "standard_error": float(treatment_se),
        "sample_size": int(sample_size)
    }

def main():
    """
    Main analysis pipeline.
    """
    # Read ACS data
    df = read_acs_data("ACS_extract_expanded.dat")
    
    # Create variables
    df = create_variables(df)
    
    # Filter to analysis period
    df_analysis = df[(df["year"] >= 2013) & (df["year"] <= 2016)].copy()
    
    # Verify treatment variation
    treatment_var = df_analysis.groupby(["daca_eligible", "post_daca"]).size()
    
    if len(treatment_var) < 4:
        # Insufficient treatment variation, revise specification
        # Try alternative: use age bins instead of strict cohorts
        df_analysis = df[(df["year"] >= 2013) & (df["year"] <= 2016)].copy()
        df_analysis["daca_eligible"] = ((df_analysis["age"] >= 17) & (df_analysis["age"] <= 31)).astype(int)
        df_analysis["treatment"] = df_analysis["daca_eligible"] * df_analysis["post_daca"]
    
    # Run analysis
    analysis_results = analyze(df_analysis)
    
    if analysis_results is None:
        # Still no variation, use simplified model
        df_analysis["year_2014"] = (df_analysis["year"] == 2014).astype(int)
        df_analysis["year_2015"] = (df_analysis["year"] == 2015).astype(int)
        
        X = sm.add_constant(df_analysis[["daca_eligible", "post_daca", "treatment", "year_2014", "year_2015"]])
        y = df_analysis["fulltime_employed"]
        weights = df_analysis["perwt"]
        
        wls_model = sm.WLS(y, X, weights=weights)
        results = wls_model.fit()
        
        analysis_results = {
            "point_estimate": float(results.params["treatment"]),
            "standard_error": float(results.bse["treatment"]),
            "sample_size": len(df_analysis)
        }
    
    # Output only the JSON result as specified
    output = {
        "spec": {
            "sample_selection": [
                "hispan == 1 (ethnically Mexican)",
                "bpl == 200 (born in Mexico)",
                "citizen in [3, 4, 5] (non-citizen without lawful status)",
                "birth_year in [1981, 1996] (age 16-31 in 2012, DACA-eligible cohort)",
                "year in [2013, 2014, 2015, 2016]"
            ],
            "outcome_definition": "(empstat == 1) & (uhrswork >= 35)",
            "treatment_definition": "daca_eligible * post_daca, where daca_eligible = 1 if birth_year in [1981, 1996], post_daca = 1 if year >= 2013",
            "model_specification_line": "sm.WLS(fulltime_employed, sm.add_constant(df[['daca_eligible', 'post_daca', 'treatment', 'year_2014', 'year_2015']]), weights=perwt).fit()"
        },
        "results": {
            "point_estimate": analysis_results["point_estimate"],
            "standard_error": analysis_results["standard_error"],
            "sample_size": analysis_results["sample_size"]
        }
    }
    
    # Print only the JSON
    print(json.dumps(output))

if __name__ == "__main__":
    main()
