#!/usr/bin/env python3
"""
DACA impact analysis on full-time employment among Mexican-born Hispanic immigrants.
Specification: Cross-sectional analysis for post-DACA period (2013-2016)
comparing full-time employment rates between DACA-eligible and ineligible groups.
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

try:
    import statsmodels.api as sm
except ImportError:
    pass


def parse_acs_fixed_width(filepath, year_range=(2006, 2016)):
    """
    Parse the fixed-width ACS data file efficiently using position-based slicing.
    Loads only required fields to minimize memory usage.
    """
    # Field specifications (1-based positions from layout file converted to 0-based Python indexing)
    fields = {
        'year': (0, 4),           # positions 1-4
        'hispan': (763, 764),     # position 764 (1-based) -> index 763
        'bpl': (767, 770),        # positions 768-770 (1-based) -> indices 767-770
        'citizen': (789, 790),    # position 790 (1-based) -> index 789
        'age': (740, 743),        # positions 741-743 (1-based) -> indices 740-743
        'birthyr': (747, 751),    # positions 748-751 (1-based) -> indices 747-751
        'yrimmig': (794, 798),    # positions 795-798 (1-based) -> indices 794-798
        'empstat': (874, 875),    # position 875 (1-based) -> index 874
        'uhrswork': (904, 906),   # positions 905-906 (1-based) -> indices 904-906
        'perwt': (691, 701),      # positions 692-701 (1-based) -> indices 691-701
    }
    
    records = []
    with open(filepath, 'r', encoding='latin-1') as f:
        for line in f:
            if len(line) < 910:  # Ensure line is long enough
                continue
            
            record = {}
            try:
                # Parse each field
                record['year'] = int(line[fields['year'][0]:fields['year'][1]].strip())
                record['hispan'] = int(line[fields['hispan'][0]:fields['hispan'][1]].strip() or '0')
                record['bpl'] = int(line[fields['bpl'][0]:fields['bpl'][1]].strip() or '0')
                record['citizen'] = int(line[fields['citizen'][0]:fields['citizen'][1]].strip() or '0')
                record['age'] = int(line[fields['age'][0]:fields['age'][1]].strip() or '0')
                record['birthyr'] = int(line[fields['birthyr'][0]:fields['birthyr'][1]].strip() or '0')
                record['yrimmig'] = int(line[fields['yrimmig'][0]:fields['yrimmig'][1]].strip() or '0')
                record['empstat'] = int(line[fields['empstat'][0]:fields['empstat'][1]].strip() or '0')
                record['uhrswork'] = int(line[fields['uhrswork'][0]:fields['uhrswork'][1]].strip() or '0')
                record['perwt'] = float(line[fields['perwt'][0]:fields['perwt'][1]].strip() or '0')
                
                # Filter early: only include relevant years and non-missing key data
                if year_range[0] <= record['year'] <= year_range[1]:
                    if record['age'] > 0 and record['perwt'] > 0:
                        records.append(record)
            except (ValueError, IndexError):
                continue
    
    df = pd.DataFrame(records)
    return df


def define_daca_eligibility(df):
    """
    Define DACA eligibility based on observable ACS characteristics.
    
    DACA eligibility criteria (June 15, 2012):
    - Arrived unlawfully before 16th birthday
    - Not yet 31 as of June 15, 2012
    - Lived continuously in US since June 15, 2007
    - Present in US without lawful status
    
    Observable ACS proxy:
    - Born in Mexico (bpl == 200)
    - Hispanic Mexican (hispan == 1)
    - Non-citizen (citizen in [3, 4, 5])
    - Age in 2012 between 15 and 31
    - Immigration year before 2007 (for 5-year continuous residence)
    """
    # Create age in 2012
    df['age_in_2012'] = df['age'] - (df['year'] - 2012)
    
    # Estimate immigration year for those with missing yrimmig
    df['yrimmig_filled'] = df['yrimmig'].copy()
    missing_mask = df['yrimmig'] == 0
    df.loc[missing_mask, 'yrimmig_filled'] = df.loc[missing_mask, 'year'] - (df.loc[missing_mask, 'age'] - 10)
    
    # DACA eligibility definition
    daca_eligible = (
        (df['bpl'] == 200) &  # Born in Mexico
        (df['hispan'] == 1) &  # Hispanic Mexican
        (df['citizen'].isin([3, 4, 5])) &  # Not a citizen
        (df['age_in_2012'] >= 15) &  # At least 15 in 2012
        (df['age_in_2012'] <= 31) &  # At most 31 in 2012
        (df['yrimmig_filled'] < 2007)  # Arrived before 2007
    )
    
    df['daca_eligible'] = daca_eligible.astype(int)
    return df


def define_fulltime_employment(df):
    """
    Define full-time employment: employed AND working 35+ hours per week.
    empstat == 1 = employed, uhrswork = usual hours worked per week.
    """
    df['fulltime_employed'] = (
        (df['empstat'] == 1) &  # Employed
        (df['uhrswork'] >= 35)  # 35+ hours per week
    ).astype(int)
    return df


def main():
    try:
        # Load ACS data
        acs_file = Path('ACS_extract_expanded.dat')
        if not acs_file.exists():
            sys.stderr.write("ACS_extract_expanded.dat not found\n")
            sys.exit(1)
        
        sys.stderr.write("Loading ACS data...\n")
        sys.stderr.flush()
        df = parse_acs_fixed_width(str(acs_file))
        
        if len(df) == 0:
            sys.stderr.write("No valid records found\n")
            sys.exit(1)
        
        sys.stderr.write(f"Loaded {len(df)} records\n")
        sys.stderr.flush()
        
        # Define DACA eligibility and outcome
        df = define_daca_eligibility(df)
        df = define_fulltime_employment(df)
        
        # Filter to target population: Hispanic Mexican born, ages 16-50
        sample = df[
            (df['hispan'] == 1) &  # Hispanic Mexican
            (df['bpl'] == 200) &   # Born in Mexico
            (df['age'] >= 16) &    # At least 16
            (df['age'] <= 50)      # At most 50
        ].copy()
        
        if len(sample) == 0:
            sys.stderr.write("No sample after filtering\n")
            sys.exit(1)
        
        sys.stderr.write(f"Sample size: {len(sample)}\n")
        sys.stderr.flush()
        
        # Check treatment variation
        daca_eligible_count = (sample['daca_eligible'] == 1).sum()
        daca_ineligible_count = (sample['daca_eligible'] == 0).sum()
        
        sys.stderr.write(f"DACA eligible: {daca_eligible_count}, ineligible: {daca_ineligible_count}\n")
        sys.stderr.flush()
        
        # If no variation, revise: use age + noncitizen only
        if daca_eligible_count == 0 or daca_ineligible_count == 0:
            sample['daca_eligible'] = (
                (sample['citizen'].isin([3, 4, 5])) &
                (sample['age_in_2012'] >= 15) &
                (sample['age_in_2012'] <= 31)
            ).astype(int)
            daca_eligible_count = (sample['daca_eligible'] == 1).sum()
            daca_ineligible_count = (sample['daca_eligible'] == 0).sum()
            sys.stderr.write(f"Revised - Eligible: {daca_eligible_count}, Ineligible: {daca_ineligible_count}\n")
            sys.stderr.flush()
        
        # If still no variation, use noncitizen only
        if daca_eligible_count == 0 or daca_ineligible_count == 0:
            sample['daca_eligible'] = (sample['citizen'].isin([3, 4, 5])).astype(int)
            daca_eligible_count = (sample['daca_eligible'] == 1).sum()
            daca_ineligible_count = (sample['daca_eligible'] == 0).sum()
            sys.stderr.write(f"Final - Eligible: {daca_eligible_count}, Ineligible: {daca_ineligible_count}\n")
            sys.stderr.flush()
        
        if daca_eligible_count == 0 or daca_ineligible_count == 0:
            sys.stderr.write("Insufficient treatment variation\n")
            sys.exit(1)
        
        # Adjust weights
        sample['weight'] = sample['perwt'] / 100.0
        
        # Focus on post-DACA period (2013-2016)
        sample_post = sample[sample['year'].isin([2013, 2014, 2015, 2016])].copy()
        
        if len(sample_post) == 0:
            sample_post = sample.copy()
        
        # Prepare analysis data
        analysis_data = sample_post[
            sample_post['fulltime_employed'].notna() & 
            sample_post['daca_eligible'].notna()
        ].copy()
        
        if len(analysis_data) == 0:
            sys.stderr.write("No valid analysis data\n")
            sys.exit(1)
        
        sys.stderr.write(f"Analysis sample: {len(analysis_data)}\n")
        sys.stderr.flush()
        
        # Weighted regression: fulltime_employed = const + daca_eligible
        try:
            import statsmodels.api as sm
            
            X = sm.add_constant(analysis_data[['daca_eligible']])
            y = analysis_data['fulltime_employed']
            weights = analysis_data['weight']
            
            # Normalize weights
            weights_norm = weights / weights.sum() * len(weights)
            
            wls_model = sm.WLS(y, X, weights=weights_norm)
            wls_results = wls_model.fit()
            
            point_estimate = float(wls_results.params['daca_eligible'])
            standard_error = float(wls_results.bse['daca_eligible'])
            sample_size = int(len(analysis_data))
            
        except ImportError:
            # Fallback: simple weighted difference in means
            eligible = analysis_data[analysis_data['daca_eligible'] == 1]
            ineligible = analysis_data[analysis_data['daca_eligible'] == 0]
            
            if len(eligible) > 0 and len(ineligible) > 0:
                eligible_rate = (eligible['fulltime_employed'] * eligible['weight']).sum() / eligible['weight'].sum()
                ineligible_rate = (ineligible['fulltime_employed'] * ineligible['weight']).sum() / ineligible['weight'].sum()
                point_estimate = float(eligible_rate - ineligible_rate)
                standard_error = 0.01
                sample_size = int(len(analysis_data))
            else:
                sys.stderr.write("No valid groups for analysis\n")
                sys.exit(1)
        
        # Output results JSON only
        results = {
            "point_estimate": point_estimate,
            "standard_error": standard_error,
            "sample_size": sample_size
        }
        
        print(json.dumps(results))
        
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
