# LLM-Bootstrap: Agents and Architecture Overview

## Project Vision

This project develops a novel econometric framework for characterizing **researcher-induced parameter uncertainty** using Large Language Models (LLMs) as stochastic replication agents. The core insight is that LLM stochasticity, typically seen as a limitation, can be leveraged as a feature—providing a computationally tractable way to explore the vast space of researcher choices.

---

## Conceptual Framework

### The Problem of Researcher Degrees of Freedom

Traditional econometrics assumes:
- **Fixed specification**: The researcher has chosen one model
- **Given data**: The dataset is taken as exogenous
- **Standard errors** capture only **sampling uncertainty**: $\text{Var}(\hat{\beta}) = (X'X)^{-1}\sigma^2$

But in reality, researchers face myriad choices:
1. **Dataset selection** (which survey, which years, merging strategies)
2. **Sample restrictions** (age ranges, geographic scope, outlier handling)
3. **Variable construction** (how to measure education, wages, experience)
4. **Specification choices** (functional form, control variables, fixed effects)
5. **Estimation methods** (OLS, IV, matching, etc.)

These choices generate a **distribution of estimates** even for the same research question.

### The LLM as Stochastic Researcher

An LLM prompted to "replicate the Mincer regression finding" will:
- Make different variable construction choices across runs (due to temperature sampling)
- Select different control variables
- Handle missing data differently
- Choose different sample restrictions

**Key Insight**: Multiple LLM runs = Multiple synthetic researchers = Approximation to the distribution of estimates across researcher choices.

---

## Formal Structure

### Three Sources of Uncertainty

Let $\beta$ be the true parameter. An estimate $\hat{\beta}_{i,j}$ from researcher $i$ using sample $j$ has uncertainty from:

1. **Sampling uncertainty** (classical): $\text{Var}_S(\hat{\beta} | X, \mathcal{R})$
2. **Researcher heterogeneity**: $\text{Var}_R(\hat{\beta} | \text{Population}, X)$  
3. **Model uncertainty** (Bayesian): $\text{Var}_M(\beta | \mathcal{M})$

Traditional standard errors capture only (1). This project focuses on (2).

### The LLM-Bootstrap Procedure

1. **Define the research question precisely**: e.g., "Effect of years of education on log wages"
2. **Prompt K independent LLM instances** to estimate this parameter
3. **Each LLM makes its own choices** regarding data, sample, specification
4. **Collect estimates**: $\{\hat{\beta}_k\}_{k=1}^K$
5. **Characterize the distribution**: 
   - Point estimate: $\bar{\beta} = \frac{1}{K}\sum_k \hat{\beta}_k$
   - Variance: $\hat{V}_R = \frac{1}{K-1}\sum_k (\hat{\beta}_k - \bar{\beta})^2$

---

## File Structure

```
LLM-bootstrapping/
├── agents.md                  # This file: project overview
├── paper/
│   ├── main.tex              # Main paper (Econometrica format)
│   ├── appendix.tex          # Technical appendix
│   └── bibliography.bib      # References
├── theory/
│   ├── model.md              # Formal model development
│   ├── simple_example.md     # Mincer regression example
│   └── optimal_K.md          # Optimal number of LLM runs
├── simulations/
│   ├── monte_carlo.py        # Simulation code
│   └── results/              # Simulation outputs
└── notes/
    └── literature.md         # Related work and connections
```

---

## Key Theoretical Contributions

1. **Variance Decomposition**: Separating sampling variance from researcher-choice variance
2. **Identification**: Conditions under which LLM heterogeneity approximates human researcher heterogeneity
3. **Optimal K**: Cost-benefit analysis for choosing number of LLM runs (analogous to bootstrap literature)
4. **Inference**: Valid confidence intervals that incorporate researcher heterogeneity
5. **Aggregation**: How to combine estimates from multiple LLM runs

---

## Connections to Existing Literature

| Literature | Connection |
|------------|------------|
| Bootstrap (Efron 1979) | Resampling analogy; optimal B theory |
| Specification curve (Simonsohn et al.) | Systematic specification exploration |
| Multiverse analysis | All possible analyses |
| Bayesian Model Averaging | Uncertainty across models |
| Institute for Replication | Multi-team replications |
| Many Analysts, One Dataset | Crowdsourced researcher heterogeneity |

---

## Implementation Notes

### LLM Requirements
- **Temperature > 0**: Stochasticity is essential
- **Identical prompts**: Only the LLM's choices should vary
- **Constrained objective**: Parameter of interest must be unambiguous
- **Independence**: Each run must be independent (no memory)

### Cost Considerations
- API costs per run: $c$
- Value of information from additional run: $V(K) - V(K-1)$
- Optimal $K^*$: where marginal benefit = marginal cost

---

## Next Steps

1. Formalize the theoretical model
2. Develop the simple Mincer example
3. Derive optimal K formula
4. Write simulation code to verify
5. Draft Econometrica paper
