from __future__ import annotations

import json
from pathlib import Path

import numpy as np


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ACS_extract_expanded.dat"
SPEC_PATH = BASE_DIR / "spec.json"


SPEC = {
    "sample_selection": [
        "2006 <= year <= 2011 or 2013 <= year <= 2016",
        "hispan == 1",
        "bpl == 200",
        "citizen in (3, 4, 5)",
        "birthyr is not None and yrimmig is not None and age is not None",
    ],
    "outcome_definition": "empstat == 1 and uhrswork >= 35",
    "treatment_definition": "birthyr >= 1982 and yrimmig <= 2007 and 0 <= yrimmig - birthyr < 16",
    "model_specification_line": (
        'point_estimate, standard_error, sample_size = fit_did_lpm('
        'df, outcome_col="full_time", treatment_col="eligible", '
        'post_col="post_daca", weight_col="perwt")'
    ),
}


def parse_int(field: str) -> int | None:
    """Parse a fixed-width integer field and treat blanks as missing."""
    text = field.strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def load_spec() -> None:
    """Persist the final specification alongside the analysis script."""
    SPEC_PATH.write_text(json.dumps(SPEC, indent=2), encoding="utf-8")


def load_sample() -> dict[str, np.ndarray]:
    """Read only the fixed-width fields needed for the DACA specification."""
    years: list[int] = []
    states: list[int] = []
    weights: list[float] = []
    ages: list[float] = []
    treatment: list[int] = []
    post: list[int] = []
    outcome: list[int] = []

    # The ACS extract is a raw fixed-width file with 1,540-character rows.
    # We slice only the variables needed for this task to keep memory use low.
    with DATA_PATH.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if len(line) < 906:
                continue

            year = parse_int(line[0:4])
            statefip = parse_int(line[65:67])
            perwt = parse_int(line[691:701])
            age = parse_int(line[740:743])
            birthyr = parse_int(line[747:751])
            hispan = parse_int(line[763:764])
            bpl = parse_int(line[767:770])
            citizen = parse_int(line[789:790])
            yrimmig = parse_int(line[794:798])
            empstat = parse_int(line[874:875])
            uhrswork = parse_int(line[904:906])

            if any(
                value is None
                for value in (
                    year,
                    statefip,
                    perwt,
                    age,
                    birthyr,
                    hispan,
                    bpl,
                    citizen,
                    yrimmig,
                    empstat,
                    uhrswork,
                )
            ):
                continue

            if year not in {2006, 2007, 2008, 2009, 2010, 2011, 2013, 2014, 2015, 2016}:
                continue
            if hispan != 1 or bpl != 200 or citizen not in (3, 4, 5):
                continue
            if perwt <= 0 or age < 0 or age > 120 or birthyr < 1900 or yrimmig < 1900:
                continue

            age_at_arrival = yrimmig - birthyr
            eligible = int(birthyr >= 1982 and 0 <= age_at_arrival < 16 and yrimmig <= 2007)
            post_daca = int(year >= 2013)
            full_time = int(empstat == 1 and uhrswork >= 35)

            years.append(year)
            states.append(statefip)
            weights.append(perwt / 100.0)
            ages.append(float(age))
            treatment.append(eligible)
            post.append(post_daca)
            outcome.append(full_time)

    if not years:
        raise ValueError("No observations matched the requested sample.")

    return {
        "year": np.asarray(years, dtype=np.int16),
        "statefip": np.asarray(states, dtype=np.int16),
        "perwt": np.asarray(weights, dtype=np.float64),
        "age": np.asarray(ages, dtype=np.float64),
        "eligible": np.asarray(treatment, dtype=np.float64),
        "post_daca": np.asarray(post, dtype=np.float64),
        "full_time": np.asarray(outcome, dtype=np.float64),
    }


def build_design_matrix(year: np.ndarray, statefip: np.ndarray, age: np.ndarray, eligible: np.ndarray, post: np.ndarray) -> np.ndarray:
    """Construct a dense weighted-regression design matrix with fixed effects."""
    n = year.shape[0]
    age_centered = age - 30.0

    year_levels = sorted(set(int(v) for v in year))
    state_levels = sorted(set(int(v) for v in statefip))

    # Intercept + treatment + DACA interaction + age controls + year FE + state FE.
    n_cols = 1 + 1 + 1 + 2 + (len(year_levels) - 1) + (len(state_levels) - 1)
    X = np.empty((n, n_cols), dtype=np.float64)

    col = 0
    X[:, col] = 1.0
    col += 1
    X[:, col] = eligible
    col += 1
    X[:, col] = eligible * post
    col += 1
    X[:, col] = age_centered
    col += 1
    X[:, col] = age_centered * age_centered
    col += 1

    base_year = year_levels[0]
    for value in year_levels:
        if value == base_year:
            continue
        X[:, col] = (year == value).astype(np.float64)
        col += 1

    base_state = state_levels[0]
    for value in state_levels:
        if value == base_state:
            continue
        X[:, col] = (statefip == value).astype(np.float64)
        col += 1

    return X


def fit_did_lpm(df: dict[str, np.ndarray], outcome_col: str, treatment_col: str, post_col: str, weight_col: str) -> tuple[float, float, int]:
    """Estimate the weighted DiD linear probability model and return the interaction effect."""
    y = df[outcome_col].astype(np.float64)
    eligible = df[treatment_col].astype(np.float64)
    post = df[post_col].astype(np.float64)
    weights = df[weight_col].astype(np.float64)

    X = build_design_matrix(df["year"], df["statefip"], df["age"], eligible, post)
    n_obs, n_params = X.shape
    if n_obs <= n_params:
        raise ValueError("Not enough observations to estimate the model.")

    # Weighted least squares via the square-root weight transformation.
    w_sqrt = np.sqrt(weights)
    x_w = X * w_sqrt[:, None]
    y_w = y * w_sqrt
    beta = np.linalg.lstsq(x_w, y_w, rcond=None)[0]

    residuals = y - X @ beta
    xtwx = X.T @ (weights[:, None] * X)
    xtwx_inv = np.linalg.pinv(xtwx)

    # HC1 robust covariance for the weighted regression.
    meat = X.T @ ((weights * residuals**2)[:, None] * X)
    cov = xtwx_inv @ meat @ xtwx_inv
    cov *= n_obs / (n_obs - n_params)

    point_estimate = float(beta[2])
    standard_error = float(np.sqrt(cov[2, 2]))

    if not np.isfinite(point_estimate) or not np.isfinite(standard_error):
        raise ValueError("Estimation failed to produce finite results.")

    return point_estimate, standard_error, n_obs


def main() -> None:
    load_spec()

    df = load_sample()

    if not (np.any(df["eligible"] == 1.0) and np.any(df["eligible"] == 0.0)):
        raise ValueError("Treatment has no variation in the selected sample.")

    point_estimate, standard_error, sample_size = fit_did_lpm(
        df,
        outcome_col="full_time",
        treatment_col="eligible",
        post_col="post_daca",
        weight_col="perwt",
    )

    output = {
        "point_estimate": point_estimate,
        "standard_error": standard_error,
        "sample_size": sample_size,
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
