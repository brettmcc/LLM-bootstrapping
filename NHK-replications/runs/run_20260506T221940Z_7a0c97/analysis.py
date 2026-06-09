#!/usr/bin/env python3
"""
DACA Impact on Full-Time Employment Analysis
Analyzes the effect of DACA eligibility on probability of full-time employment
for Mexican-born, non-citizen Hispanic individuals using ACS 2006-2016 data.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
import json
import re
warnings.filterwarnings('ignore')

# Variable positions (0-based indexing from start of line):
# year: cols 1-4 (indices 0-3)
# hispan: col 764 (index 763)
# bpl: cols 768-770 (indices 767-769)
# citizen: col 790 (index 789)
# empstat: col 875 (index 874)
# uhrswork: cols 905-906 (indices 904-905)

# Read the ACS data file in chunks to manage memory
chunk_size = 100000
all_data = []

try:
    with open('ACS_extract_expanded.dat', 'r') as f:
        lines = f.readlines()
    
    # Process in chunks
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i+chunk_size]
        
        for line in chunk_lines:
            # Ensure line is long enough for all variables
            if len(line) < 910:
                continue
            
            try:
                year = int(line[0:4].strip())
                hispan = int(line[763:764].strip())
                bpl = int(line[767:770].strip())
                citizen = int(line[789:790].strip())
                empstat = int(line[874:875].strip())
                uhrswork_str = line[904:906].strip()
                
                # Skip if any required value is missing
                if not uhrswork_str:
                    continue
                    
                uhrswork = int(uhrswork_str)
                
                all_data.append({
                    'year': year,
                    'hispan': hispan,
                    'bpl': bpl,
                    'citizen': citizen,
                    'empstat': empstat,
                    'uhrswork': uhrswork
                })
            except (ValueError, IndexError):
                continue
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Apply sample selection filters
    # 1. Years 2006-2016 (pre- and post-DACA)
    df = df[df['year'].isin(range(2006, 2017))]
    
    # 2. Hispanic origin = Mexican (hispan == 1)
    df = df[df['hispan'] == 1]
    
    # 3. Birthplace = Mexico (bpl == 200)
    df = df[df['bpl'] == 200]
    
    # 4. Not a citizen (citizen in [3, 5])
    # 3 = Not a citizen
    # 5 = Foreign born, citizenship status not reported
    df = df[df['citizen'].isin([3, 5])]
    
    # 5. Valid employment status (exclude missing/unknown)
    df = df[df['empstat'].isin([1, 2, 3])]
    
    # 6. Non-missing hours worked
    df = df[df['uhrswork'] > 0]
    
    # Create outcome variable: Full-time employment (35+ hours per week)
    df['fulltime'] = (df['uhrswork'] >= 35).astype(int)
    
    # Create treatment variable: Post-DACA period (year >= 2013)
    # DACA implemented June 15, 2012; applications started August 15, 2012
    # 2013 is first full year post-DACA
    df['post_daca'] = (df['year'] >= 2013).astype(int)
    
    # Check for variation in treatment
    treatment_variation = df['post_daca'].sum()
    
    # Prepare data for analysis
    X = df[['post_daca']].values
    y = df['fulltime'].values
    
    # Fit linear regression: fulltime = b0 + b1*post_daca
    model = LinearRegression()
    model.fit(X, y)
    
    point_estimate = float(model.coef_[0])
    
    # Calculate standard error
    residuals = y - model.predict(X)
    n = len(y)
    mse = np.sum(residuals ** 2) / (n - 2)
    
    # SE for simple bivariate regression
    X_centered = X[:, 0] - X[:, 0].mean()
    denominator = np.sum(X_centered ** 2)
    if denominator > 0:
        standard_error = float(np.sqrt(mse / denominator))
    else:
        standard_error = np.nan
    
    sample_size = int(len(df))
    
    # Output JSON to stdout
    results = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size
    }
    
    print(json.dumps(results))

except Exception as e:
    # If there's an error, output error in JSON format
    error_result = {
        "point_estimate": None,
        "standard_error": None,
        "sample_size": 0
    }
    print(json.dumps(error_result))
    raise
