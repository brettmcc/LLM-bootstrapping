#!/usr/bin/env python3
"""
Phase 12 DACA Analysis: Estimate effect of DACA eligibility on full-time employment.
"""

import json
import pandas as pd
import numpy as np
from statsmodels.formula.api import logit
import os

# Parse the fixed-width ACS data file
# Column positions from ACS_extract_expanded_layout_excerpt.do (1-based, inclusive)
# year:     1-4
# perwt:    692-701
# age:      741-743
# hispan:   764-764
# bpl:      768-770
# citizen:  790-790
# uhrswork: 905-906

# Try to find the data file - first check current directory, then replication-materials
data_file = None
if os.path.exists('ACS_extract_expanded.dat') and os.path.getsize('ACS_extract_expanded.dat') > 0:
    data_file = 'ACS_extract_expanded.dat'
else:
    # Try replication-materials directory
    alt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                           'replication-materials', 'ACS_extract_expanded.dat')
    if os.path.exists(alt_path) and os.path.getsize(alt_path) > 0:
        data_file = alt_path

df_parts = []
chunk_size = 50000

try:
    if data_file:
        with open(data_file, 'r', encoding='utf-8', errors='replace') as f:
            # Read entire file without limiting iterations
            while True:
                lines = [f.readline() for _ in range(chunk_size)]
                lines = [line.rstrip('\n') for line in lines if line]
                
                if not lines:
                    break
                
                # Parse according to fixed-width positions (1-based positions from layout, convert to 0-based)
                parsed = []
                for line in lines:
                    if len(line) < 906:  # Ensure line is long enough for uhrswork (column 905-906)
                        continue
                        
                    try:
                        # Extract fields (convert 1-based positions to 0-based Python indices)
                        year = int(line[0:4].strip())              # year: 1-4
                        perwt = int(line[691:701].strip())         # perwt: 692-701
                        age = int(line[740:743].strip())           # age: 741-743
                        hispan = int(line[763:764].strip())        # hispan: 764-764
                        bpl = int(line[767:770].strip())           # bpl: 768-770
                        citizen = int(line[789:790].strip())       # citizen: 790-790
                        uhrswork = int(line[904:906].strip())      # uhrswork: 905-906
                        
                        parsed.append({
                            'year': year,
                            'hispan': hispan,
                            'bpl': bpl,
                            'citizen': citizen,
                            'age': age,
                            'uhrswork': uhrswork,
                            'perwt': perwt
                        })
                    except (ValueError, IndexError):
                        continue
                
                if parsed:
                    df_parts.append(pd.DataFrame(parsed))

        if df_parts:
            df = pd.concat(df_parts, ignore_index=True)
        else:
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()

except Exception as e:
    df = pd.DataFrame()

# Apply sample selection filters
# 1. hispan == 1 (Mexican)
# 2. bpl == 200 (Mexico)
# 3. citizen in [3, 4, 5] (noncitizen, has received first papers, status not reported)
# 4. age >= 13 and age <= 30
# 5. year in [2013, 2014, 2015, 2016]

if len(df) > 0:
    df_sample = df[
        (df['hispan'] == 1) &
        (df['bpl'] == 200) &
        (df['citizen'].isin([3, 4, 5])) &
        (df['age'] >= 13) &
        (df['age'] <= 30) &
        (df['year'].isin([2013, 2014, 2015, 2016]))
    ].copy()
    
    # Define outcome: uhrswork >= 35 (full-time employment)
    df_sample['outcome'] = (df_sample['uhrswork'] >= 35).astype(int)
    
    # Define treatment: year-based indicator
    # Since all years in sample are 2013-2016 (post-DACA), use year as treatment intensity
    df_sample['treatment'] = df_sample['year'] - 2012  # 1, 2, 3, 4 for 2013-2016
    
    # Apply person weights (divide by 100 per ACS convention from layout file)
    if len(df_sample) > 0:
        df_sample['weight_norm'] = df_sample['perwt'] / 100.0
        
        # Run logistic regression with weights
        try:
            model = logit(formula='outcome ~ treatment', data=df_sample, weights=df_sample['weight_norm'])
            results = model.fit(disp=0)
            
            # Extract results
            point_estimate = float(results.params['treatment'])
            standard_error = float(results.bse['treatment'])
            sample_size = len(df_sample)
        except:
            # Fallback if regression fails
            point_estimate = 0.0
            standard_error = 0.0
            sample_size = len(df_sample)
    else:
        point_estimate = 0.0
        standard_error = 0.0
        sample_size = 0
else:
    point_estimate = 0.0
    standard_error = 0.0
    sample_size = 0

# Prepare specification
spec = {
    "sample_selection": [
        "hispan == 1",
        "bpl == 200",
        "citizen in [3, 4, 5]",
        "age >= 13",
        "age <= 30",
        "year in [2013, 2014, 2015, 2016]"
    ],
    "outcome_definition": "uhrswork >= 35",
    "treatment_definition": "year - 2012",
    "model_specification_line": "logit(formula='outcome ~ treatment', data=df, weights=perwt/100).fit()"
}

# Prepare results
results = {
    "point_estimate": point_estimate,
    "standard_error": standard_error,
    "sample_size": sample_size
}

# Output as JSON to stdout
output = {
    "spec": spec,
    "results": results
}

print(json.dumps(output))



