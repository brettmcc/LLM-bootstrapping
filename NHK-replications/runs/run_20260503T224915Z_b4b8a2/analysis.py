"""
Analysis: Effect of DACA eligibility on full-time employment.

Target population: Hispanic-Mexican, Mexico-born non-citizens in the ACS.

Identification strategy: Difference-in-Differences (DiD)
  - Treated: born 1982-1996 (age-eligible for DACA as of June 15, 2012:
             not yet 31 years old, and at least 15 years old)
  - Control: born 1974-1981 (just above the age cutoff; similar population
             but too old to qualify for DACA)
  - Pre-period:  2009, 2010, 2011
  - Post-period: 2013, 2014, 2015, 2016  (2012 excluded as DACA transition year)
  - Both groups must have arrived in the US before age 16 (key DACA criterion)

Outcome: probability of being employed full-time
  full_time = 1 if empstat==1 (employed) AND uhrswork>=35 (usually >=35 hrs/week)

Model: OLS linear probability model with year FE, state FE, age, and sex controls.
  Clustered standard errors at the state (statefip) level.
  Weighted by survey person weights (perwt / 100).
"""

import os
import json
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# ---------------------------------------------------------------
# Fixed-width column specifications
# Stata layout positions are 1-indexed: variable at bytes a-b.
# Python colspec: (a-1, b)  [0-indexed, end-exclusive].
# Source: ACS_extract_expanded_layout_excerpt.do
# ---------------------------------------------------------------
COLSPECS = [
    (0,   4),    # year:     bytes 1-4
    (65,  67),   # statefip: bytes 66-67
    (138, 139),  # gq:       byte  139
    (691, 701),  # perwt:    bytes 692-701 (10-char field; 2 implied decimals)
    (739, 740),  # sex:      byte  740
    (740, 743),  # age:      bytes 741-743
    (747, 751),  # birthyr:  bytes 748-751
    (763, 764),  # hispan:   byte  764
    (767, 770),  # bpl:      bytes 768-770
    (789, 790),  # citizen:  byte  790
    (794, 798),  # yrimmig:  bytes 795-798
    (874, 875),  # empstat:  byte  875
    (904, 906),  # uhrswork: bytes 905-906
]

COLNAMES = [
    'year', 'statefip', 'gq', 'perwt', 'sex', 'age',
    'birthyr', 'hispan', 'bpl', 'citizen', 'yrimmig', 'empstat', 'uhrswork',
]

# Analysis years: pre-DACA (2009-2011) and post-DACA (2013-2016); skip 2012
VALID_YEARS = {2009, 2010, 2011, 2013, 2014, 2015, 2016}

# Birth year bounds for the full analysis sample (treated + control)
BIRTHYR_MIN = 1974   # control group floor: age ~38 as of June 2012
BIRTHYR_MAX = 1996   # treated group ceiling: age ~15-16 as of June 2012

# DACA age cutoff: born on or after 1982 means not yet 31 as of June 2012
DACA_BIRTHYR_CUTOFF = 1982


def load_data(filepath):
    """
    Read the large fixed-width ACS file in chunks.
    Apply early row-level filters inside the loop to keep memory usage low.
    Returns a single concatenated DataFrame of the analysis sample.
    """
    chunks = []

    for chunk in pd.read_fwf(
        filepath,
        colspecs=COLSPECS,
        names=COLNAMES,
        # Use memory-efficient nullable integer types
        dtype={
            'year':     'Int16',
            'statefip': 'Int16',
            'gq':       'Int16',
            'perwt':    'Int32',
            'sex':      'Int16',
            'age':      'Int16',
            'birthyr':  'Int16',
            'hispan':   'Int16',
            'bpl':      'Int16',
            'citizen':  'Int16',
            'yrimmig':  'Int16',
            'empstat':  'Int16',
            'uhrswork': 'Int16',
        },
        chunksize=250_000,
        header=None,
    ):
        # --- Early filters to minimise memory footprint ---
        mask = (
            chunk['year'].isin(VALID_YEARS)        # only analysis years
            & (chunk['hispan'] == 1)               # Mexican Hispanic ethnicity
            & (chunk['bpl'] == 200)                # born in Mexico
            & (chunk['citizen'] == 3)              # not a citizen (proxy undocumented)
            & (chunk['yrimmig'] > 0)               # has a recorded immigration year
            & chunk['gq'].isin([1, 2, 5])          # household resident (not institutionalized)
            & (chunk['age'] >= 16)                 # working-age
            & (chunk['birthyr'] >= BIRTHYR_MIN)    # within analysis age window
            & (chunk['birthyr'] <= BIRTHYR_MAX)
        )
        filtered = chunk.loc[mask].copy()
        if len(filtered) > 0:
            chunks.append(filtered)

    if not chunks:
        sys.exit('ERROR: No observations survived the sample filters.')

    return pd.concat(chunks, ignore_index=True)


def main():
    # Locate data file in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'ACS_extract_expanded.dat')

    # ---------------------------------------------------------------
    # 1. Load and filter data
    # ---------------------------------------------------------------
    df = load_data(data_path)

    # Convert nullable integer columns to plain Python ints for arithmetic
    for col in df.columns:
        if hasattr(df[col], 'dtype') and str(df[col].dtype).startswith('Int'):
            df[col] = df[col].astype(int)

    # Restrict to individuals who arrived in the US before age 16
    # (key DACA eligibility criterion; approximate using yrimmig - birthyr)
    df['age_at_immig'] = df['yrimmig'] - df['birthyr']
    df = df[df['age_at_immig'] < 16].copy()

    # Drop rows with missing values in variables used in the regression
    df = df.dropna(subset=['year', 'statefip', 'birthyr', 'empstat', 'uhrswork', 'perwt'])

    # ---------------------------------------------------------------
    # 2. Construct analysis variables
    # ---------------------------------------------------------------

    # Outcome: employed AND usually works >=35 hours per week
    df['full_time'] = ((df['empstat'] == 1) & (df['uhrswork'] >= 35)).astype(int)

    # DACA age eligibility indicator:
    #   born >=1982 (not yet 31 as of June 2012) AND <=1996 (>=15 as of June 2012)
    df['daca_eligible'] = (
        (df['birthyr'] >= DACA_BIRTHYR_CUTOFF) & (df['birthyr'] <= BIRTHYR_MAX)
    ).astype(int)

    # Post-DACA time indicator (2013 onward)
    df['post'] = (df['year'] >= 2013).astype(int)

    # DiD interaction: the coefficient of interest
    df['dida'] = df['daca_eligible'] * df['post']

    # Survey person weight; PERWT has 2 implied decimal places
    df['weight'] = df['perwt'] / 100.0

    # ---------------------------------------------------------------
    # 3. Verify treatment variation exists in the data
    # ---------------------------------------------------------------
    cell_counts = df.groupby(['daca_eligible', 'post']).size()
    if len(cell_counts) < 4:
        sys.exit(f'ERROR: Only {len(cell_counts)} DiD cells found — insufficient variation.')

    # ---------------------------------------------------------------
    # 4. Estimate the DiD model
    # ---------------------------------------------------------------
    # OLS linear probability model:
    #   full_time ~ daca_eligible (main effect) + dida (DiD term)
    #             + year FE + state FE + age + sex
    # Weighted by survey person weights; SEs clustered at the state level.
    # Use WLS (weighted least squares) so survey weights are actually applied
    model = smf.wls(
        'full_time ~ daca_eligible + dida + age + C(sex) + C(year) + C(statefip)',
        data=df,
        weights=df['weight'],
    ).fit(
        cov_type='cluster',
        cov_kwds={'groups': df['statefip']},
    )

    # ---------------------------------------------------------------
    # 5. Output results as JSON (ONLY this JSON goes to STDOUT)
    # ---------------------------------------------------------------
    print(json.dumps({
        'point_estimate': round(float(model.params['dida']), 6),
        'standard_error': round(float(model.bse['dida']),    6),
        'sample_size':    int(model.nobs),
    }))


if __name__ == '__main__':
    main()
