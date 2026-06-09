import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Read the fixed-width ACS data
# Field positions from ACS_extract_expanded_layout_excerpt.do (1-based indices)
# Convert to 0-based slicing
year_cols = (0, 4)
hispan_cols = (763, 764)
bpl_cols = (767, 770)
citizen_cols = (789, 790)
age_cols = (740, 743)
empstat_cols = (874, 875)
uhrswork_cols = (904, 906)
perwt_cols = (691, 701)
statefip_cols = (65, 67)

# Read data - process line by line to manage memory
records = []
with open('ACS_extract_expanded.dat', 'r') as f:
    for line in f:
        try:
            # Extract fields from fixed-width format
            year = int(line[year_cols[0]:year_cols[1]].strip() or 0)
            hispan = int(line[hispan_cols[0]:hispan_cols[1]].strip() or 0)
            bpl = int(line[bpl_cols[0]:bpl_cols[1]].strip() or 0)
            citizen = int(line[citizen_cols[0]:citizen_cols[1]].strip() or 0)
            age = int(line[age_cols[0]:age_cols[1]].strip() or 0)
            empstat = int(line[empstat_cols[0]:empstat_cols[1]].strip() or 0)
            uhrswork = int(line[uhrswork_cols[0]:uhrswork_cols[1]].strip() or 0)
            perwt_str = line[perwt_cols[0]:perwt_cols[1]].strip()
            perwt = float(perwt_str) / 100.0 if perwt_str else 0
            statefip = int(line[statefip_cols[0]:statefip_cols[1]].strip() or 0)
            
            # Apply sample selection filters
            if hispan != 1:
                continue
            if bpl != 200:
                continue
            if citizen not in (3, 5):
                continue
            if age < 16 or age > 30:
                continue
            if year < 2013 or year > 2016:
                continue
            if empstat == 0 or empstat == 9 or uhrswork == 0:
                continue
            
            records.append({
                'year': year,
                'age': age,
                'empstat': empstat,
                'uhrswork': uhrswork,
                'perwt': perwt,
                'statefip': statefip
            })
        except (ValueError, IndexError):
            continue

# Create DataFrame
df = pd.DataFrame(records)

if len(df) == 0:
    print('{"point_estimate": null, "standard_error": null, "sample_size": 0}')
    exit()

# Define outcome: full-time employment
df['fulltime'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

# Create treatment indicator: DACA-eligible age groups
# DACA eligible if age 16-30 in June 2012
# For 2013: age 17-31
# For 2014: age 18-32
# For 2015: age 19-33
# For 2016: age 20-34
df['treatment'] = 0
for year_val in [2013, 2014, 2015, 2016]:
    min_age = year_val - 2012 + 16
    max_age = year_val - 2012 + 30
    mask = (df['year'] == year_val) & (df['age'] >= min_age) & (df['age'] <= max_age)
    df.loc[mask, 'treatment'] = 1

# Check treatment variation
if df['treatment'].var() == 0:
    print('{"point_estimate": null, "standard_error": null, "sample_size": 0}')
    exit()

# Drop rows with missing data
df = df.dropna(subset=['fulltime', 'treatment', 'perwt', 'statefip'])

if len(df) < 100:
    print('{"point_estimate": null, "standard_error": null, "sample_size": 0}')
    exit()

# Build simple weighted regression: fulltime ~ treatment + age + state_FE + year_FE
# Use statsmodels for better WLS handling
try:
    import statsmodels.api as sm
    from statsmodels.formula.api import wls
    
    # Create state and year indicators
    df['state_str'] = 'state_' + df['statefip'].astype(str)
    df['year_str'] = 'year_' + df['year'].astype(str)
    
    # Build formula
    formula = 'fulltime ~ C(treatment) + C(state_str) + C(year_str) + age'
    
    # Fit WLS
    model = wls(formula, data=df, weights=df['perwt'])
    result = model.fit()
    
    point_estimate = result.params['C(treatment)[T.1]']
    standard_error = result.bse['C(treatment)[T.1]']
    sample_size = len(df)
    
    import json
    output = {
        'point_estimate': float(point_estimate),
        'standard_error': float(standard_error),
        'sample_size': int(sample_size)
    }
    print(json.dumps(output))
    
except ImportError:
    # Fallback to manual WLS if statsmodels not available
    # Simple regression without fixed effects to avoid memory issues
    
    # Create design matrix
    X = np.column_stack([
        np.ones(len(df)),  # intercept
        df['treatment'].values,
        df['age'].values
    ])
    
    y = df['fulltime'].values
    weights = df['perwt'].values
    
    # Weighted OLS
    W = np.diag(weights)
    XtWX = X.T @ W @ X
    XtWy = X.T @ W @ y
    
    try:
        beta = np.linalg.solve(XtWX, XtWy)
    except np.linalg.LinAlgError:
        beta = np.linalg.lstsq(XtWX, XtWy, rcond=None)[0]
    
    point_estimate = beta[1]
    
    residuals = y - X @ beta
    rss = np.sum(weights * residuals**2)
    df_residual = len(y) - X.shape[1]
    mse = rss / df_residual
    
    try:
        vcov = mse * np.linalg.inv(XtWX)
        se = np.sqrt(np.diag(vcov))
        standard_error = se[1]
    except np.linalg.LinAlgError:
        standard_error = np.nan
    
    sample_size = len(y)
    
    import json
    output = {
        'point_estimate': float(point_estimate),
        'standard_error': float(standard_error),
        'sample_size': int(sample_size)
    }
    print(json.dumps(output))
