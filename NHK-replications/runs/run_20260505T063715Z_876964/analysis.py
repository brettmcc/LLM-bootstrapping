from pathlib import Path
import json

import pandas as pd
import statsmodels.formula.api as smf


BASE_DIR = Path(__file__).resolve().parent
ACS_PATH = BASE_DIR / "ACS_extract_expanded.dat"
POLICY_PATH = BASE_DIR / "policy_labor_market_data.csv"


# Only keep the ACS columns needed for the research design.
ACS_COLS = [
    ("year", (0, 4)),
    ("statefip", (65, 67)),
    ("gq", (138, 139)),
    ("sex", (739, 740)),
    ("age", (740, 743)),
    ("birthqtr", (745, 746)),
    ("birthyr", (747, 751)),
    ("hispan", (763, 764)),
    ("bpl", (767, 770)),
    ("citizen", (789, 790)),
    ("yrimmig", (794, 798)),
    ("empstat", (874, 875)),
    ("uhrswork", (904, 906)),
    ("perwt", (691, 701)),
]


def load_acs():
    """Read the ACS extract in chunks so the large file never needs to be loaded all at once."""
    colspecs = [span for _, span in ACS_COLS]
    names = [name for name, _ in ACS_COLS]
    pieces = []

    for chunk in pd.read_fwf(
        ACS_PATH,
        colspecs=colspecs,
        names=names,
        chunksize=200_000,
    ):
        # The file stores person weights as integers scaled by 100.
        chunk["perwt"] = chunk["perwt"] / 100.0

        # Restrict to the sample before merging the policy file.
        keep = (
            chunk["year"].isin([2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016])
            & chunk["statefip"].between(1, 56)
            & chunk["gq"].isin([1, 2, 5])
            & chunk["sex"].isin([1, 2])
            & chunk["birthyr"].between(1978, 1984)
            & (chunk["birthyr"] != 1981)
            & (chunk["hispan"] == 1)
            & (chunk["bpl"] == 200)
            & chunk["citizen"].isin([3, 4, 5])
            & chunk["yrimmig"].between(1, 2007)
            & (chunk["yrimmig"] - chunk["birthyr"]).between(0, 15)
        )

        pieces.append(chunk.loc[keep].copy())

    if not pieces:
        raise RuntimeError("No ACS records matched the sample restrictions.")

    return pd.concat(pieces, ignore_index=True)


def build_analysis_frame():
    """Attach state-year controls and create the analysis variables used in the regression."""
    acs = load_acs()
    policy = pd.read_csv(POLICY_PATH)
    policy = policy.rename(columns={"state_fips": "statefip"})

    # Merge the person-level ACS data to the state-year policy controls.
    analysis_df = acs.merge(policy, on=["statefip", "year"], how="inner", validate="many_to_one")

    # Define the binary post-DACA period.
    analysis_df["post_daca"] = (analysis_df["year"] >= 2013).astype(int)

    # Define the eligibility proxy used by this specification.
    analysis_df["daca_eligible"] = (analysis_df["birthyr"] >= 1982).astype(int)

    # Define the full-time employment outcome.
    analysis_df["full_time_employed"] = (
        (analysis_df["empstat"] == 1) & (analysis_df["uhrswork"] >= 35)
    ).astype(int)

    return analysis_df


def main():
    analysis_df = build_analysis_frame()

    # Linear probability model with state-clustered standard errors.
    results = smf.wls(
        "full_time_employed ~ daca_eligible * post_daca + C(birthyr) + C(year) + C(statefip) + C(sex) + UNEMP + LFPR + DRIVERSLICENSES + INSTATETUITION + STATEFINANCIALAID + HIGHEREDBAN + EVERIFY + LIMITEVERIFY + OMNIBUS + TASK287G + JAIL287G + SECURECOMMUNITIES",
        data=analysis_df,
        weights=analysis_df["perwt"],
    ).fit(cov_type="cluster", cov_kwds={"groups": analysis_df["statefip"]})

    estimate = float(results.params["daca_eligible:post_daca"])
    stderr = float(results.bse["daca_eligible:post_daca"])
    sample_size = int(len(analysis_df))

    print(
        json.dumps(
            {
                "point_estimate": estimate,
                "standard_error": stderr,
                "sample_size": sample_size,
            }
        )
    )


if __name__ == "__main__":
    main()
