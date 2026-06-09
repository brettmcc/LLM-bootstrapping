"""
DACA Effect on Full-Time Employment: Difference-in-Differences Analysis
=======================================================================
Research question: Among Hispanic-Mexican, Mexico-born non-citizens who arrived
in the US before age 16 and by 2007, what is the causal effect of DACA eligibility
(being under age 31 as of June 15, 2012) on the probability of full-time employment
(usually working 35+ hours/week)?

Identification strategy: Difference-in-differences (DiD)
  - Treatment group: Born 1982-1996 (under 31 on June 15, 2012; DACA-eligible by age)
  - Control group:   Born 1976-1981 (just above the age cutoff; ineligible)
  - Pre period:  2009-2011 (post-recession but pre-DACA)
  - Post period: 2013-2016 (DACA implemented June 2012, exclude 2012 transition year)
  - DiD estimator: daca_eligible * post, with year FEs, state FEs, and controls
"""

import os
import sys
import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


# ============================================================
# Fixed-width column specs (0-indexed Python slices).
# Stata layout is 1-indexed; Python slice for Stata col N is [N-1:N].
# Source: ACS_extract_expanded_layout_excerpt.do
# ============================================================
COLSPECS = [
    (0,   4),    # year:     Stata cols  1-4
    (65,  67),   # statefip: Stata cols 66-67
    (691, 701),  # perwt:    Stata cols 692-701 (raw; divide by 100)
    (739, 740),  # sex:      Stata col  740
    (747, 751),  # birthyr:  Stata cols 748-751
    (763, 764),  # hispan:   Stata col  764  (1=Mexican)
    (767, 770),  # bpl:      Stata cols 768-770 (200=Mexico)
    (789, 790),  # citizen:  Stata col  790  (3=not a citizen)
    (794, 798),  # yrimmig:  Stata cols 795-798 (0=N/A i.e. US-born)
    (859, 861),  # educ:     Stata cols 860-861
    (874, 875),  # empstat:  Stata col  875  (1=employed, 2=unemployed, 3=NILF)
    (904, 906),  # uhrswork: Stata cols 905-906 (usual hrs/week; 0=N/A)
]

COLNAMES = [
    'year', 'statefip', 'perwt', 'sex', 'birthyr',
    'hispan', 'bpl', 'citizen', 'yrimmig',
    'educ', 'empstat', 'uhrswork',
]


def main():
    # Locate data file relative to this script (portable across machines)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, 'ACS_extract_expanded.dat')

    chunks = []

    # Read in chunks to stay within 30 GB memory limit
    reader = pd.read_fwf(
        filepath,
        colspecs=COLSPECS,
        names=COLNAMES,
        header=None,
        # Use float32 for everything initially to save memory;
        # we will cast to appropriate types after filtering
        dtype='float32',
        chunksize=200_000,
    )

    for chunk in reader:
        # ---- Filter early to minimise memory footprint ----

        # 1. Keep only pre-DACA (2009-2011) and post-DACA (2013-2016) years
        chunk = chunk[chunk['year'].isin([2009, 2010, 2011, 2013, 2014, 2015, 2016])]
        if chunk.empty:
            continue

        # 2. Ethnic/origin filter: Hispanic-Mexican (hispan==1)
        chunk = chunk[chunk['hispan'] == 1]
        if chunk.empty:
            continue

        # 3. Country-of-birth filter: Born in Mexico (bpl==200)
        chunk = chunk[chunk['bpl'] == 200]
        if chunk.empty:
            continue

        # 4. Citizenship filter: non-citizen (citizen==3) approximates
        #    undocumented/unlawful status — a DACA eligibility prerequisite
        chunk = chunk[chunk['citizen'] == 3]
        if chunk.empty:
            continue

        # 5. Immigration year must be valid (yrimmig>0 means they immigrated;
        #    0 = N/A i.e. US-born) and must be by 2007 (continuous US residence
        #    since June 15, 2007 is a DACA requirement)
        chunk = chunk[(chunk['yrimmig'] > 0) & (chunk['yrimmig'] <= 2007)]
        if chunk.empty:
            continue

        # 6. Arrived before 16th birthday — another DACA requirement
        chunk = chunk[(chunk['yrimmig'] - chunk['birthyr']) < 16]
        if chunk.empty:
            continue

        # 7. Cohort window:
        #    - Control: born 1976-1981 (31-36 years old on June 15, 2012; too old)
        #    - Treatment: born 1982-1996 (under 31 on June 15, 2012; age-eligible)
        chunk = chunk[(chunk['birthyr'] >= 1976) & (chunk['birthyr'] <= 1996)]
        if chunk.empty:
            continue

        # 8. Restrict to civilian population of working age
        #    (empstat 1=employed, 2=unemployed, 3=NILF — all are valid for this outcome)
        chunk = chunk[chunk['empstat'].isin([1.0, 2.0, 3.0])]
        if chunk.empty:
            continue

        chunks.append(chunk)

    if not chunks:
        sys.stderr.write("ERROR: No observations remain after filtering.\n")
        sys.exit(1)

    # Concatenate all kept chunks into a single DataFrame
    df = pd.concat(chunks, ignore_index=True)

    # ============================================================
    # Construct analysis variables
    # ============================================================

    # Person weight: the layout file shows raw perwt must be divided by 100
    df['perwt_adj'] = df['perwt'] / 100.0

    # Outcome: 1 if employed AND usually works 35+ hours/week (full-time)
    # For those not employed, empstat != 1 so the condition fails -> outcome = 0
    df['full_time'] = (
        (df['empstat'] == 1) & (df['uhrswork'] >= 35)
    ).astype('int8')

    # Treatment indicator: DACA-eligible by the age criterion
    # (born 1982 or later -> under 31 as of June 15, 2012)
    df['daca_eligible'] = (df['birthyr'] >= 1982).astype('int8')

    # Post-DACA period indicator (applications opened August 2012;
    # we use 2013 onward to allow time for diffusion)
    df['post'] = (df['year'] >= 2013).astype('int8')

    # DiD treatment variable: eligible group x post period
    df['did'] = (df['daca_eligible'] * df['post']).astype('int8')

    # Cohort trend control: linear birth-year deviation from the 1982 cutoff.
    # Absorbs smooth cohort-level trends so the discontinuity at 1982
    # identifies the treatment effect without confounding by age/cohort.
    df['birthyr_c'] = (df['birthyr'] - 1982).astype('int16')

    # Cast categorical variables to int for statsmodels C() dummy encoding
    for col in ['statefip', 'year', 'sex', 'educ']:
        df[col] = df[col].astype(int)

    # Sanity check: must have observations in all four treatment x period cells
    tab = df.groupby(['daca_eligible', 'post']).size()
    if len(tab) < 4:
        sys.stderr.write("ERROR: Insufficient variation in treatment x period cells.\n")
        sys.exit(1)

    # ============================================================
    # DiD regression: weighted least squares with two-way fixed effects
    #
    # full_time = beta_did * (daca_eligible x post)
    #           + beta_g  * daca_eligible      [group main effect]
    #           + alpha_s  (state FEs)         [absorbs state differences]
    #           + alpha_t  (year FEs)          [absorbs post main effect & year trends]
    #           + gamma * birthyr_c            [smooth cohort trend control]
    #           + controls (sex, educ)
    #           + epsilon
    #
    # beta_did is the DiD estimate of the DACA effect on P(full-time employed).
    # Standard errors clustered at the state level to account for within-state
    # correlation across years and individuals.
    # ============================================================
    formula = (
        'full_time ~ did + daca_eligible + birthyr_c'
        ' + C(sex) + C(educ)'
        ' + C(statefip) + C(year)'
    )

    model = smf.wls(formula, data=df, weights=df['perwt_adj'])

    result = model.fit(
        cov_type='cluster',
        cov_kwds={'groups': df['statefip']},
    )

    # Extract results for the key DiD coefficient
    point_estimate = float(result.params['did'])
    standard_error = float(result.bse['did'])
    sample_size    = int(result.nobs)

    # Print ONLY the JSON object to stdout (no extra text)
    print(json.dumps({
        "point_estimate": round(point_estimate, 6),
        "standard_error": round(standard_error, 6),
        "sample_size":    sample_size,
    }))


if __name__ == '__main__':
    main()
