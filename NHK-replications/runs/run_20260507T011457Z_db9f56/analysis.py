import pandas as pd
import numpy as np
from scipy import stats
import json
import sys

# Read fixed-width ACS data
# Parse only the variables we need to manage memory efficiently
positions = {
    'year': (0, 4),
    'age': (740, 743),
    'birthyr': (747, 751),
    'hispan': (763, 764),
    'bpl': (767, 770),
    'citizen': (789, 790),
    'yrimmig': (794, 798),
    'empstat': (874, 875),
    'uhrswork': (904, 906),
    'perwt': (691, 701),
}

# Read data in chunks to manage memory
def read_acs_chunks():
    """Read ACS fixed-width data in chunks, filtering for relevant variables."""
    chunk_size = 50000
    chunks = []
    
    with open('ACS_extract_expanded.dat', 'r') as f:
        chunk = []
        for line_num, line in enumerate(f, 1):
            # Parse fixed-width fields
            row = {}
            for var_name, (start, end) in positions.items():
                row[var_name] = line[start:end].strip()
            
            chunk.append(row)
            
            if len(chunk) >= chunk_size:
                chunks.append(pd.DataFrame(chunk))
                chunk = []
        
        if chunk:
            chunks.append(pd.DataFrame(chunk))
    
    return pd.concat(chunks, ignore_index=True)

# Read the data
print("Reading ACS data...", file=sys.stderr)
df = read_acs_chunks()

# Convert types
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df['birthyr'] = pd.to_numeric(df['birthyr'], errors='coerce')
df['hispan'] = pd.to_numeric(df['hispan'], errors='coerce')
df['bpl'] = pd.to_numeric(df['bpl'], errors='coerce')
df['citizen'] = pd.to_numeric(df['citizen'], errors='coerce')
df['yrimmig'] = pd.to_numeric(df['yrimmig'], errors='coerce')
df['empstat'] = pd.to_numeric(df['empstat'], errors='coerce')
df['uhrswork'] = pd.to_numeric(df['uhrswork'], errors='coerce')
df['perwt'] = pd.to_numeric(df['perwt'], errors='coerce')

# Normalize weights (PERWT has two implied decimals, so divide by 100)
df['perwt'] = df['perwt'] / 100.0

print(f"Total records read: {len(df)}", file=sys.stderr)

# Apply sample selection criteria
print("\nApplying sample selection...", file=sys.stderr)

# 1. Ethnically Hispanic-Mexican (hispan == 1)
df = df[df['hispan'] == 1]
print(f"After Hispanic Mexican filter: {len(df)}", file=sys.stderr)

# 2. Mexican-born (bpl == 200)
df = df[df['bpl'] == 200]
print(f"After Mexico-born filter: {len(df)}", file=sys.stderr)

# 3. Valid year of immigration (must have arrived)
df = df[df['yrimmig'].notna() & (df['yrimmig'] > 0) & (df['yrimmig'] < 9999)]
print(f"After valid year of immigration: {len(df)}", file=sys.stderr)

# 4. Valid citizenship status (non-citizen: 3, 4, 5)
df = df[df['citizen'].isin([3, 4, 5])]
print(f"After non-citizen filter: {len(df)}", file=sys.stderr)

# 5. Valid age and birth year
df = df[df['age'].notna() & df['birthyr'].notna() & (df['age'] > 0) & (df['birthyr'] > 0)]
print(f"After valid age/birthyr: {len(df)}", file=sys.stderr)

# DACA eligibility criteria:
# - Had not yet had their 31st birthday as of June 15, 2012 (birthyr >= 1981)
# - Lived continuously in the US since June 15, 2007 (yrimmig <= 2007)
# - Arrived unlawfully before their 16th birthday (we'll approximate with age - (current_year - yrimmig) >= 16 at arrival)
# For people observed in ACS: if age >= 16 and they immigrated before turning 16, then age at immigration was < 16

df['age_at_immigration'] = df['age'] - (df['year'] - df['yrimmig'])

# DACA eligibility
df['eligible_for_daca'] = (
    (df['birthyr'] >= 1981) &  # Not yet 31 as of June 15, 2012
    (df['yrimmig'] <= 2007) &  # Lived continuously in US since June 15, 2007
    (df['age_at_immigration'] < 16)  # Arrived before 16th birthday
).astype(int)

print(f"Eligible for DACA: {df['eligible_for_daca'].sum()}", file=sys.stderr)
print(f"Not eligible for DACA: {(1 - df['eligible_for_daca']).sum()}", file=sys.stderr)

# Create outcome: Full-time employment (35+ hours per week)
# Only consider those with valid employment status
df['full_time_employed'] = (
    (df['empstat'] == 1) &  # Employed
    (df['uhrswork'] >= 35)  # Working 35+ hours per week
).astype(int)

# Create post-DACA period indicator (2012 implementation, 2013-2016 post)
df['post_daca'] = (df['year'] >= 2013).astype(int)

# For the analysis, we use all years to estimate treatment effect
# We'll focus on years 2013-2016 as specified
df_analysis = df[df['year'].isin([2013, 2014, 2015, 2016])].copy()
print(f"\nSample size for analysis (2013-2016): {len(df_analysis)}", file=sys.stderr)

# Check for treatment variation
print(f"Variation in eligibility: {df_analysis['eligible_for_daca'].std()}", file=sys.stderr)
print(f"Treatment variation (2013-2016): {df_analysis['eligible_for_daca'].sum()} eligible", file=sys.stderr)

if df_analysis['eligible_for_daca'].sum() == 0 or (len(df_analysis) - df_analysis['eligible_for_daca'].sum()) == 0:
    # No variation - revise specification
    print("WARNING: No variation in treatment in 2013-2016", file=sys.stderr)
    # Fall back to broader sample
    df_analysis = df[(df['year'] >= 2012) & (df['year'] <= 2016)].copy()
    print(f"Expanded sample (2012-2016): {len(df_analysis)}", file=sys.stderr)

# Simple regression specification:
# Model: full_time_employed ~ eligible_for_daca + controls
# We'll use a weighted regression with person weights

# Remove records with missing outcome or treatment
df_analysis = df_analysis[
    df_analysis['eligible_for_daca'].notna() &
    df_analysis['full_time_employed'].notna() &
    df_analysis['perwt'].notna() &
    (df_analysis['perwt'] > 0)
].copy()

print(f"Sample size after removing missing values: {len(df_analysis)}", file=sys.stderr)

# Calculate weighted means by treatment status
eligible = df_analysis[df_analysis['eligible_for_daca'] == 1]
ineligible = df_analysis[df_analysis['eligible_for_daca'] == 0]

if len(eligible) > 0:
    weighted_mean_eligible = (eligible['full_time_employed'] * eligible['perwt']).sum() / eligible['perwt'].sum()
    se_eligible = np.sqrt((eligible['full_time_employed'] * (1 - weighted_mean_eligible))).std() / np.sqrt(len(eligible))
else:
    weighted_mean_eligible = 0
    se_eligible = 0

if len(ineligible) > 0:
    weighted_mean_ineligible = (ineligible['full_time_employed'] * ineligible['perwt']).sum() / ineligible['perwt'].sum()
    se_ineligible = np.sqrt((ineligible['full_time_employed'] * (1 - weighted_mean_ineligible))).std() / np.sqrt(len(ineligible))
else:
    weighted_mean_ineligible = 0
    se_ineligible = 0

# Simple difference-in-means as the treatment effect
point_estimate = weighted_mean_eligible - weighted_mean_ineligible
standard_error = np.sqrt(se_eligible**2 + se_ineligible**2)

# Sample size
sample_size = len(df_analysis)

print(f"\n=== RESULTS ===", file=sys.stderr)
print(f"Point estimate: {point_estimate}", file=sys.stderr)
print(f"Standard error: {standard_error}", file=sys.stderr)
print(f"Sample size: {sample_size}", file=sys.stderr)

# Output the results JSON to stdout (only)
results = {
    "point_estimate": float(point_estimate),
    "standard_error": float(standard_error),
    "sample_size": int(sample_size)
}

print(json.dumps(results))
