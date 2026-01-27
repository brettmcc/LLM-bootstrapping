# Simple Example: LLM-Bootstrap for the Mincer Regression

## 1. The Mincer Regression

The classic Mincer (1974) wage equation:
$$\log(w_i) = \alpha + \beta \cdot S_i + \gamma_1 \cdot X_i + \gamma_2 \cdot X_i^2 + \varepsilon_i$$

where:
- $w_i$: Wage of individual $i$
- $S_i$: Years of schooling
- $X_i$: Years of work experience
- $\beta$: **Returns to education** (parameter of interest)

**The Research Question:** "What is the causal effect of one additional year of education on log wages?"

---

## 2. Researcher Choices in a Mincer Regression

Consider the space of choices a researcher faces:

### 2.1 Sample Selection ($\mathcal{S}$)

| Choice Dimension | Options |
|-----------------|---------|
| Age range | [18, 65], [25, 54], [25, 65], [16, 75] |
| Full-time only | Yes / No (if No: include part-time) |
| Sector | Private only, All sectors, Exclude government |
| Geography | National, Major metros, State-specific |
| Years | Single cross-section, Pooled 2015-2020, Specific year |
| Outliers | Top/bottom 1% trimmed, winsorized, none |

Number of sample configurations: $\approx 4 \times 2 \times 3 \times 3 \times 4 \times 3 = 864$

### 2.2 Variable Construction ($\mathcal{V}$)

| Variable | Options |
|----------|---------|
| Wage measure | Hourly wage, Annual earnings / hours, Weekly earnings |
| Log transform | $\log(w)$, $\log(w + 1)$, asinh$(w)$ |
| Education | Years of schooling, Degree dummies, Imputed from degrees |
| Experience | Age − Education − 6, Actual experience (if available), Tenure |

Number of variable configurations: $\approx 3 \times 3 \times 3 \times 3 = 81$

### 2.3 Specification ($\mathcal{M}$)

| Choice | Options |
|--------|---------|
| Experience terms | Linear, Quadratic, Cubic, Quartic |
| Controls | None, Race/gender, Race/gender/industry, Full demographics |
| Fixed effects | None, Year, State, Year × State |
| Interaction terms | None, Education × Experience, Education × Female |

Number of specification configurations: $\approx 4 \times 4 \times 4 \times 3 = 192$

### 2.4 Total Choice Space

Combining all dimensions:
$$|\mathcal{R}| \approx 864 \times 81 \times 192 \times 3 \approx 40{,}000{,}000$$

Even this is an undercount—many choices are continuous or have more options.

---

## 3. The LLM-Bootstrap in Action

### 3.1 The Prompt

```
Research Question: Estimate the effect of years of education on log wages 
using the Current Population Survey. Report the coefficient on years of 
education along with its standard error.

You have access to CPS microdata. Write complete code to:
1. Load and clean the data  
2. Construct necessary variables
3. Estimate an appropriate regression
4. Report the coefficient and standard error

Make your own reasonable choices about sample restrictions, variable 
construction, controls, and specification. Do not ask for clarification—
just proceed with defensible choices.
```

### 3.2 Hypothetical LLM Responses

**LLM Run 1:**
- Sample: Ages 25-55, full-time workers, 2019 only
- Wage: Annual earnings / usual hours worked  
- Education: Years of schooling (constructed from degree)
- Specification: OLS with quadratic experience, race, gender controls
- **Result:** $\hat{\beta}_1 = 0.098$ (SE = 0.002)

**LLM Run 2:**
- Sample: Ages 18-65, all workers, 2018-2022 pooled
- Wage: Reported hourly wage
- Education: Actual years of schooling variable
- Specification: OLS with quartic experience, year FE, state FE
- **Result:** $\hat{\beta}_2 = 0.105$ (SE = 0.001)

**LLM Run 3:**
- Sample: Ages 25-64, private sector only, 2020
- Wage: Weekly earnings / usual hours
- Education: Imputed from highest degree
- Specification: OLS with quadratic experience, full demographics
- **Result:** $\hat{\beta}_3 = 0.091$ (SE = 0.003)

... and so on for $K$ runs.

### 3.3 Aggregating Results

After $K = 50$ runs:

| Statistic | Value |
|-----------|-------|
| Mean $\bar{\beta}^{LB}$ | 0.096 |
| Std. Dev. $\sqrt{\hat{V}^{LB}}$ | 0.012 |
| Min | 0.071 |
| Max | 0.118 |
| Median SE (classical) | 0.002 |

**Researcher Variability Ratio:**
$$\lambda = \frac{0.012}{0.002} = 6$$

**Interpretation:** The spread across researcher choices is **6 times larger** than the typical classical standard error. A 95% CI that accounts for researcher heterogeneity is:
$$[0.096 - 1.96 \times 0.012, 0.096 + 1.96 \times 0.012] = [0.073, 0.119]$$

compared to a typical classical CI of $[0.094, 0.100]$.

---

## 4. Formal Analysis of the Mincer Example

### 4.1 Model Setup

True data generating process:
$$\log(w_i) = \alpha_0 + \beta_0 S_i + g_0(X_i) + \varepsilon_i$$

where $\beta_0$ is the true returns to education.

Researcher $r$ estimates:
$$\log(w_{i,r}) = \alpha_r + \beta_r S_{i,r} + g_r(X_{i,r}, Z_{i,r}) + u_{i,r}$$

where subscript $r$ indicates that variables and samples depend on choices.

### 4.2 Sources of Estimate Variation

**Proposition (Mincer Example Decomposition).** For the Mincer regression:
$$\hat{\beta}_r - \beta_0 = \underbrace{(\hat{\beta}_r - \beta_r)}_{\text{Sampling error}} + \underbrace{(\beta_r - \beta_0)}_{\text{Specification bias}}$$

The variance across researcher choices:
$$\text{Var}_R(\hat{\beta}_R) = \text{Var}_R(\hat{\beta}_R - \beta_R) + \text{Var}_R(\beta_R) + 2\text{Cov}_R(\hat{\beta}_R - \beta_R, \beta_R)$$

Under standard regularity conditions and if specification biases are small:
$$\text{Var}_R(\hat{\beta}_R) \approx \mathbb{E}_R[\text{Var}(\hat{\beta}_R | R)] + \text{Var}_R(\beta_R)$$

### 4.3 Why Does Researcher Variance Arise?

The coefficient $\hat{\beta}_r$ varies across researchers due to:

1. **Sample composition effects**: Different age/sector restrictions → different populations → different average returns

2. **Omitted variable bias differences**: Including industry FE vs. not → different degrees of ability/selection bias

3. **Measurement differences**: Hourly vs. annual wages → different $\beta$ if hours correlate with education

4. **Functional form**: Linear vs. quadratic experience → different partial effects

### 4.4 When Is Researcher Variance Large?

**Proposition.** Researcher variance is larger when:
1. The relationship is heterogeneous across subpopulations
2. Key confounders (ability, selection) are imperfectly observed
3. Variable definitions are noisy or contested
4. Multiple data sources are available with different coverage

The Mincer regression is a **high-variance** setting because:
- Returns to education vary enormously by demographics, geography, time
- Ability bias is a perennial concern with no consensus solution
- Many ways to measure wages (hourly, annual, total compensation)

---

## 5. Monte Carlo Illustration

To validate the theory, we simulate:

### 5.1 Simulation Design

**Data Generating Process:**
$$y_i = 1 + 0.10 \cdot S_i + 0.05 \cdot X_i - 0.001 \cdot X_i^2 + 0.02 \cdot A_i + \varepsilon_i$$

where:
- $S_i \sim N(12, 3^2)$ truncated to $[6, 20]$
- $X_i = \text{Age}_i - S_i - 6$, with $\text{Age}_i \sim U(25, 55)$
- $A_i$ = unobserved ability, $A_i \sim N(0, 1)$, correlated with $S$
- $\varepsilon_i \sim N(0, 0.5^2)$

True parameter: $\beta_0 = 0.10$

**Ability-Education Correlation:**
$$S_i = 12 + 0.5 \cdot A_i + \eta_i, \quad \eta_i \sim N(0, 2.5^2)$$

### 5.2 Simulated Researcher Choices

We model researcher heterogeneity by drawing:

1. **Sample restriction**: Include ages [25, 55] or [25, 45] or [30, 55] with prob. (0.5, 0.25, 0.25)
2. **Controls**: Include $X$ and $X^2$, or just $X$, with prob. (0.7, 0.3)
3. **Sample size**: Use 1000, 2000, or 5000 observations

For each "researcher," estimate OLS regression with their choices.

### 5.3 Expected Results

| Source of Variation | Contribution to $\text{Var}(\hat{\beta})$ |
|--------------------|-------------------------------------------|
| Sampling variance (within researcher) | ~0.0001 |
| Choice of age range | ~0.0004 |
| Choice of controls | ~0.0006 |
| Total researcher variance | ~0.001 |

**Predicted:** $\sqrt{\text{Var}_R(\hat{\beta})} \approx 0.03$ vs. typical SE $\approx 0.01$

This implies $\lambda \approx 3$: researcher variance ~3× sampling variance.

### 5.4 Simulation Code Sketch

```python
import numpy as np
from scipy import stats

def simulate_dgp(n=5000, ability_education_corr=0.5, seed=None):
    """Generate synthetic Mincer data."""
    if seed is not None:
        np.random.seed(seed)
    
    # Ability (unobserved)
    A = np.random.normal(0, 1, n)
    
    # Education (correlated with ability)
    S = 12 + ability_education_corr * A + np.random.normal(0, 2.5, n)
    S = np.clip(S, 6, 20)
    
    # Age and experience
    Age = np.random.uniform(25, 55, n)
    X = Age - S - 6
    X = np.clip(X, 0, 45)
    
    # Log wages
    y = 1 + 0.10 * S + 0.05 * X - 0.001 * X**2 + 0.02 * A + np.random.normal(0, 0.5, n)
    
    return {'y': y, 'S': S, 'X': X, 'Age': Age, 'A': A}

def researcher_estimate(data, age_range, include_X2):
    """Simulate one researcher's choices and estimate."""
    import statsmodels.api as sm
    
    # Apply sample restriction
    mask = (data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1])
    y = data['y'][mask]
    S = data['S'][mask]
    X = data['X'][mask]
    
    # Build design matrix based on controls
    if include_X2:
        Xmat = np.column_stack([np.ones(len(y)), S, X, X**2])
    else:
        Xmat = np.column_stack([np.ones(len(y)), S, X])
    
    # OLS
    model = sm.OLS(y, Xmat)
    results = model.fit()
    
    return {
        'beta': results.params[1],  # Coefficient on S
        'se': results.bse[1],
        'n': len(y)
    }

def llm_bootstrap(K=100, seed=42):
    """Simulate K researcher replications."""
    np.random.seed(seed)
    
    # Generate one dataset (fixed sample)
    data = simulate_dgp(n=10000, seed=seed)
    
    results = []
    for k in range(K):
        # Random researcher choices
        age_options = [(25, 55), (25, 45), (30, 55)]
        age_range = age_options[np.random.choice(3, p=[0.5, 0.25, 0.25])]
        include_X2 = np.random.random() < 0.7
        
        res = researcher_estimate(data, age_range, include_X2)
        results.append(res)
    
    betas = np.array([r['beta'] for r in results])
    ses = np.array([r['se'] for r in results])
    
    return {
        'mean_beta': np.mean(betas),
        'var_beta': np.var(betas, ddof=1),
        'sd_beta': np.std(betas, ddof=1),
        'median_se': np.median(ses),
        'lambda_ratio': np.std(betas, ddof=1) / np.median(ses),
        'betas': betas,
        'ses': ses
    }
```

### 5.5 Interpreting Results

Running `llm_bootstrap(K=100)` would produce output like:

```
LLM-Bootstrap Results:
  Mean beta:       0.097
  SD beta:         0.028
  Median SE:       0.009
  Lambda ratio:    3.1
  95% CI (RH):     [0.091, 0.103]
  95% PI:          [0.042, 0.152]
```

The classical 95% CI (from median SE) would be $[0.079, 0.115]$—**much narrower** than the researcher-heterogeneity-adjusted interval.

---

## 6. Lessons from the Mincer Example

1. **Researcher choices matter enormously** for estimated returns to education

2. **Classical standard errors understate uncertainty** by a factor of 3-6× in this setting

3. **The LLM-Bootstrap provides a tractable way** to quantify this additional uncertainty

4. **Even "simple" regressions have vast choice spaces**—40 million+ configurations

5. **A well-identified parameter (Mincer $\beta$) still exhibits researcher variance**—this is not about identification per se, but about heterogeneity in what is being estimated

---

## 7. Connection to IV Literature

The Mincer regression has spawned a large IV literature (Angrist & Krueger 1991, Card 1999). IV estimates of returns to education range from 0.06 to 0.15.

**Key Point:** This **across-study variation** in IV estimates is exactly what researcher variance captures. The LLM-Bootstrap approximates this by simulating many "studies."

| Study | Estimate | SE |
|-------|----------|-----|
| Angrist & Krueger 1991 | 0.081 | 0.033 |
| Card 1993 | 0.132 | 0.052 |
| Ashenfelter & Krueger 1994 | 0.121 | 0.036 |
| ... | ... | ... |

The **across-study variance** is much larger than within-study SE—consistent with our $\lambda \approx 3$-$6$ finding.
