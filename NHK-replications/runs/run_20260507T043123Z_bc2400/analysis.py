#!/usr/bin/env python3
"""
DACA Impact Analysis: Hispanic-Mexican Population Employment Effects

This analysis estimates the causal impact of DACA eligibility on full-time employment
among ethnically Hispanic-Mexican Mexican-born individuals in the US during 2013-2016.

Research Question:
Among ethnically Hispanic-Mexican Mexican-born people living in the United States,
what was the causal impact of eligibility for the Deferred Action for Childhood Arrivals
(DACA) program on the probability of full-time employment (35+ hours per week)?

DACA was implemented June 15, 2012. Analysis period: 2013-2016 (post-implementation).
"""

import pandas as pd
import numpy as np
from statsmodels.regression.linear_model import WLS
from statsmodels.tools.tools import add_constant
import json
import sys

# Parse the fixed-width ACS data file
def parse_acs_data():
    """
    Parse the fixed-width ACS data file using column positions from layout.
    Column positions are 1-based in Stata/documentation, converted to 0-based for Python.
    
    Returns DataFrame with relevant variables for DACA analysis.
    """
    
    # Column specifications (0-based Python indexing):
    # year: cols 1-4 (0-based: 0-4)
    # age: cols 741-743 (0-based: 740-743)
    # birthyr: cols 748-751 (0-based: 747-751)
    # hispan: col 764 (0-based: 763-764)
    # bpl: cols 768-770 (0-based: 767-770)
    # citizen: col 790 (0-based: 789-790)
    # empstat: col 875 (0-based: 874-875)
    # uhrswork: cols 905-906 (0-based: 904-906)
    # perwt: cols 692-701 (0-based: 691-701)
    
    df = pd.read_fwf(
        'ACS_extract_expanded.dat',
        colspecs=[
            (0, 4),       # year
            (740, 743),   # age
            (747, 751),   # birthyr
            (763, 764),   # hispan
            (767, 770),   # bpl
            (789, 790),   # citizen
            (874, 875),   # empstat
            (904, 906),   # uhrswork
            (691, 701),   # perwt
        ],
        names=['year', 'age', 'birthyr', 'hispan', 'bpl', 'citizen', 'empstat', 'uhrswork', 'perwt'],
        dtype={'year': int, 'age': int, 'birthyr': int, 'hispan': int, 'bpl': int, 
                'citizen': int, 'empstat': int, 'uhrswork': int, 'perwt': float}
    )
    
    return df

# Load ACS data
df = parse_acs_data()

# Scale person weight from integer (scaled by 100) to actual weight
df['perwt'] = df['perwt'] / 100.0

# Apply sample selection filters
# Selection criteria based on DACA research question and eligibility:
df_sample = df[
    # Ethnicity and origin
    (df['hispan'] == 1) &           # Mexican ethnicity (HISPAN==1: Mexican)
    (df['bpl'] == 200) &            # Born in Mexico (BPL==200: Mexico)
    
    # Immigration status (DACA requires non-citizen status)
    (df['citizen'].isin([3, 4, 5])) &  # Not a citizen (3), first papers (4), or status unknown (5)
    
    # Time period (post-DACA implementation)
    (df['year'] >= 2013) &          # 2013-2016: post-DACA
    (df['year'] <= 2016) &
    
    # Age group analysis
    (df['age'] >= 16) &             # Old enough to potentially work
    (df['age'] <= 50)               # Working age population
].copy()

# DACA Eligibility Criteria (all must be true):
# 1. Arrived unlawfully before 16th birthday
# 2. Had not yet turned 31 as of June 15, 2012
# 3. Lived continuously in US since June 15, 2007
# 4. Were present in US on June 15, 2012 without lawful status
#
# For observational estimation, we use BIRTH YEAR to proxy eligibility:
# - Birth year 1982: age 30 on 6/15/2012 ✓
# - Birth year 1998: age 14 on 6/15/2012 ✓
# - Birth year 1997-1982: qualifies for age cutoff
#
# We assume:
# - All Mexican-born non-citizens in our sample arrived before age 16
#   (reasonable given undocumented immigration patterns from Mexico)
# - Continuous residence can be approximated by year in sample

# Birth year range for DACA eligibility (born 1982-1998)
daca_birth_year_min = 1982  # Would be age 30 in June 2012
daca_birth_year_max = 1998  # Would be age 14 in June 2012

# Create treatment variable: DACA eligibility
df_sample['daca_eligible'] = (
    (df_sample['birthyr'] >= daca_birth_year_min) & 
    (df_sample['birthyr'] <= daca_birth_year_max)
).astype(int)

# Create outcome variable: Full-time employment
# Full-time employment: 
#   - Employed (EMPSTAT==1)
#   - Usually working 35+ hours per week (UHRSWORK >= 35)
df_sample['fulltime_employed'] = (
    (df_sample['empstat'] == 1) & 
    (df_sample['uhrswork'] >= 35)
).astype(int)

# Verify treatment variable has meaningful variation
treatment_counts = df_sample['daca_eligible'].value_counts()
if treatment_counts.shape[0] < 2 or treatment_counts.min() < 10:
    # Treatment lacks sufficient variation; analysis not possible
    output = {
        "point_estimate": None,
        "standard_error": None,
        "sample_size": 0,
        "error": "Treatment variable lacks sufficient variation"
    }
    print(json.dumps(output))
    sys.exit(1)

# Remove missing values for analysis
df_analysis = df_sample[
    ['daca_eligible', 'fulltime_employed', 'perwt']
].dropna()

# Verify sample size
if len(df_analysis) < 100:
    output = {
        "point_estimate": None,
        "standard_error": None,
        "sample_size": 0,
        "error": "Sample size too small"
    }
    print(json.dumps(output))
    sys.exit(1)

# Specification: Weighted Least Squares (WLS) with person weights
# Model: fulltime_employed = constant + beta * daca_eligible
# Weights: perwt (ACS person weights)
#
# This estimates the difference in full-time employment probability
# between DACA-eligible and ineligible Mexican-born non-citizens

# Create design matrix (add constant for intercept)
X = add_constant(df_analysis[['daca_eligible']])
y = df_analysis['fulltime_employed']
weights = df_analysis['perwt']

# Fit WLS model
model = WLS(y, X, weights=weights)
results = model.fit()

# Extract coefficient, standard error, and sample size
point_estimate = results.params['daca_eligible']
standard_error = results.bse['daca_eligible']
sample_size = len(df_analysis)

# Output ONLY the JSON result object (no other text or warnings)
output_json = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

print(json.dumps(output_json))
