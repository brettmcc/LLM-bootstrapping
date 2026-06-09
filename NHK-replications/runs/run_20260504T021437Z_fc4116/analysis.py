"""
DACA effect on full-time employment among Hispanic-Mexican Mexican-born non-citizens.

Strategy: Difference-in-Differences using the DACA age cutoff (must be < 31 as of
June 15, 2012, i.e., born after June 15, 1981).

Treatment group: born 1982-1996, arrived before age 16, in US since ≤ 2007, non-citizen.
Control group:   born 1977-1981 (just above the DACA age cutoff), same other conditions.

Outcome: employed full-time (empstat==1 AND uhrswork>=35).
Model: weighted OLS DiD with state + year fixed effects, SEs clustered by state.
"""

import os
import sys
import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Change to the script's directory so all file paths are relative
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

DATA_FILE = "ACS_extract_expanded.dat"
CHUNK_SIZE = 100_000  # rows per chunk; keeps memory well under 30 GB

# Column positions from the Stata .do layout file.
# The .do file uses 1-based inclusive column numbers; Python needs 0-based, exclusive-end tuples.
# Conversion: Stata col a-b  →  Python (a-1, b)
colspecs = [
    (0,   4),    # year     (Stata 1-4)
    (65,  67),   # statefip (Stata 66-67)
    (691, 701),  # perwt    (Stata 692-701) — 2 implied decimal places → divide by 100
    (747, 751),  # birthyr  (Stata 748-751)
    (763, 764),  # hispan   (Stata 764-764) — 1=Mexican
    (767, 770),  # bpl      (Stata 768-770) — 200=Mexico
    (789, 790),  # citizen  (Stata 790-790) — 3=not citizen, 4=not citizen w/ 1st papers
    (794, 798),  # yrimmig  (Stata 795-798) — 0=N/A
    (874, 875),  # empstat  (Stata 875-875) — 1=employed, 2=unemployed, 3=NILF
    (904, 906),  # uhrswork (Stata 905-906) — 0=N/A, 1-99=hours/week
]
names = ["year", "statefip", "perwt", "birthyr",
         "hispan", "bpl", "citizen", "yrimmig", "empstat", "uhrswork"]

# ── Read the fixed-width file in memory-efficient chunks ──────────────────────
chunks = []
for chunk in pd.read_fwf(DATA_FILE, colspecs=colspecs, names=names,
                          header=None, chunksize=CHUNK_SIZE):
    # Apply aggressive early filters to minimize memory consumption:
    #   • Hispanic-Mexican ethnicity (hispan == 1)
    #   • Born in Mexico (bpl == 200)
    #   • Non-citizen (citizen 3 or 4) — proxy for undocumented status
    #   • Has a recorded immigration year ≤ 2007 (proxy for continuous US presence since 2007)
    #   • Birth year 1977-1996: 1977-1981 = control group, 1982-1996 = treatment group
    #     (upper bound 1996 ensures everyone is ≥ 17 in 2013, old enough to be in labour market)
    #   • Exclude 2012 (DACA rollout year; ambiguous treatment timing)
    mask = (
        (chunk["hispan"] == 1) &
        (chunk["bpl"] == 200) &
        (chunk["citizen"].isin([3, 4])) &
        (chunk["yrimmig"] > 0) &          # must have immigration year recorded
        (chunk["yrimmig"] <= 2007) &      # in US since at least 2007
        (chunk["birthyr"] >= 1977) &      # control group lower bound
        (chunk["birthyr"] <= 1996) &      # treatment group upper bound
        (chunk["year"] != 2012)           # drop DACA rollout year
    )
    keep = chunk.loc[mask]
    if len(keep) > 0:
        chunks.append(keep.copy())

df = pd.concat(chunks, ignore_index=True)
print(f"After initial filters: {len(df):,} rows", file=sys.stderr)

# DACA requires arrival before the 16th birthday.
# With only year-level yrimmig, approximate as: yrimmig - birthyr < 16
df = df[df["yrimmig"] - df["birthyr"] < 16].copy()
print(f"After arrival-before-16 filter: {len(df):,} rows", file=sys.stderr)

# ── Construct analysis variables ──────────────────────────────────────────────

# Person weight: the .do file divides perwt by 100 (2 implied decimal places in .dat)
df["perwt"] = df["perwt"] / 100.0

# Post-DACA indicator: pre = 2006-2011, post = 2013-2016 (2012 already excluded)
df["post"] = (df["year"] >= 2013).astype(int)

# Treatment: DACA-eligible if born after June 15, 1981 → birthyr >= 1982
# Control:   born 1977-1981 (just above the age cutoff, so DACA-ineligible)
df["treatment"] = (df["birthyr"] >= 1982).astype(int)

# Outcome: full-time employment — employed (empstat==1) AND usual hours ≥ 35/week
# Defined over all individuals (not conditional on employment), so NILF/unemployed → 0
df["full_time"] = ((df["empstat"] == 1) & (df["uhrswork"] >= 35)).astype(int)

# ── Verify treatment variation ────────────────────────────────────────────────
trt_counts = df["treatment"].value_counts()
print(f"Treatment value counts: {trt_counts.to_dict()}", file=sys.stderr)
if 1 not in trt_counts.index or 0 not in trt_counts.index:
    print("ERROR: No variation in treatment — revising specification.", file=sys.stderr)
    sys.exit(1)

print(
    f"Mean full_time by (treatment, post):\n"
    f"{df.groupby(['treatment', 'post'])['full_time'].mean()}",
    file=sys.stderr,
)

# ── DiD regression ────────────────────────────────────────────────────────────
# Linear probability model with two-way fixed effects (state + year).
# Weighted by person weight; standard errors clustered at the state level.
result = smf.wls(
    "full_time ~ treatment * post + C(year) + C(statefip)",
    data=df,
    weights=df["perwt"],
).fit(cov_type="cluster", cov_kwds={"groups": df["statefip"]})

point_estimate = float(result.params["treatment:post"])
standard_error = float(result.bse["treatment:post"])
sample_size    = int(len(df))

# ── Output: print ONLY the JSON object to stdout ──────────────────────────────
print(json.dumps({
    "point_estimate": round(point_estimate, 6),
    "standard_error": round(standard_error, 6),
    "sample_size":    sample_size,
}))
