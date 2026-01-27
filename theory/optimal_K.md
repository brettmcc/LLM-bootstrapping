# Optimal Number of LLM Instances

## 1. Introduction

A fundamental question in the LLM-Bootstrap is: **How many LLM runs K are optimal?** This parallels the classical bootstrap literature on choosing the number of replications B.

This analysis develops the theory for optimal K, drawing on Andrews & Buchinsky (2000, 2001) and adapting their framework to the LLM setting.

---

## 2. The Cost-Benefit Tradeoff

### 2.1 Costs

Let the cost of running K LLM instances be:
$$C(K) = c_0 + K \cdot c$$

where:
- $c_0$: Fixed setup cost (preparing the prompt, data access)
- $c$: Marginal cost per LLM run (API cost + compute + verification time)

**Current (2024) cost estimates:**
| LLM | Cost per run (approximate) |
|-----|---------------------------|
| GPT-4 | $0.05 - $0.50 |
| Claude 3 Opus | $0.10 - $1.00 |
| Claude 3 Sonnet | $0.02 - $0.20 |
| Open source (self-hosted) | $0.01 - $0.10 |

### 2.2 Benefits

The benefit of more runs is **precision** in estimating researcher variance.

Let:
- $\mu = \mathbb{E}_R[\hat{\theta}(R)]$: Mean estimate across researcher choices
- $\sigma^2 = \text{Var}_R(\hat{\theta}(R))$: Researcher variance

With K runs, the estimator $\bar{\theta}^{LB}$ has:
$$\text{Var}(\bar{\theta}^{LB}) = \frac{\sigma^2}{K}$$

And the variance estimator $\hat{V}^{LB}$:
$$\mathbb{E}[\hat{V}^{LB}] = \sigma^2$$
$$\text{Var}(\hat{V}^{LB}) = \frac{2\sigma^4}{K-1} \quad \text{(under normality)}$$

**More K means:**
- More precise estimate of mean $\mu$
- More precise estimate of variance $\sigma^2$
- Better coverage for confidence intervals

---

## 3. Optimal K for Mean Estimation

### 3.1 Mean Squared Error Framework

Consider the MSE of $\bar{\theta}^{LB}$ as an estimator of the true parameter $\theta_0$:
$$\text{MSE}(\bar{\theta}^{LB}) = \text{Bias}^2 + \text{Var}(\bar{\theta}^{LB}) = (\mu - \theta_0)^2 + \frac{\sigma^2}{K}$$

The bias $(\mu - \theta_0)$ cannot be reduced by increasing K—it reflects systematic specification bias averaged across LLM choices.

### 3.2 Pure Variance Minimization

If only variance matters, minimize:
$$L(K) = \frac{\sigma^2}{K} + \lambda \cdot K \cdot c$$

where $\lambda$ converts monetary cost to variance units.

**First-order condition:**
$$\frac{\partial L}{\partial K} = -\frac{\sigma^2}{K^2} + \lambda c = 0$$

**Solution:**
$$K^* = \sqrt{\frac{\sigma^2}{\lambda c}}$$

**Interpretation:** Optimal K increases with researcher variance $\sigma^2$ and decreases with per-run cost $c$.

### 3.3 Numerical Example

Suppose:
- $\sigma = 0.02$ (SD of researcher estimates)
- $c = \$0.10$ (cost per run)
- $\lambda = 10000$ (1 unit of variance "costs" $10,000)

Then:
$$K^* = \sqrt{\frac{0.02^2}{10000 \times 0.10}} = \sqrt{\frac{0.0004}{1000}} = \sqrt{0.0000004} \approx 0.63$$

This seems too low! The issue is our $\lambda$ is poorly calibrated. Let's reframe.

---

## 4. Precision-Based Optimal K

### 4.1 Target Precision

A more practical approach: choose K to achieve a target precision for estimating researcher variance.

**Precision of variance estimator:**

Under normality, the coefficient of variation of $\hat{V}^{LB}$ is:
$$CV(\hat{V}^{LB}) = \sqrt{\frac{2}{K-1}}$$

| K | CV of variance estimate |
|---|------------------------|
| 10 | 47% |
| 50 | 20% |
| 100 | 14% |
| 200 | 10% |
| 400 | 7% |
| 1000 | 4.5% |

**Rule of thumb:** For 20% precision in variance, use $K \approx 50$.

### 4.2 Target Coverage

For confidence interval coverage, Andrews & Buchinsky (2000) show that the **error in nominal coverage** due to simulation is approximately:
$$\epsilon_K \approx \frac{c_\alpha}{\sqrt{K}}$$

where $c_\alpha$ is a constant depending on the confidence level.

For 95% CIs, to achieve coverage error $\leq 0.01$ (i.e., 94%-96% instead of 95%):
$$K \geq \left(\frac{c_{0.05}}{0.01}\right)^2$$

Empirically, $c_{0.05} \approx 0.1$, so $K \geq 100$.

---

## 5. Andrews-Buchinsky Approach

### 5.1 Three-Step Adaptive Rule

Andrews & Buchinsky (2000, 2001) propose an adaptive procedure:

**Step 1: Pilot runs**
- Run $K_0$ initial replications (e.g., $K_0 = 100$)
- Compute pilot variance estimate $\hat{V}_{K_0}$

**Step 2: Compute optimal K**
- Based on target relative error $\delta$:
$$K^* = \left\lceil \frac{2\hat{V}_{K_0}}{\delta^2 \cdot \hat{V}_{K_0}} \right\rceil = \left\lceil \frac{2}{\delta^2} \right\rceil$$

Wait, this doesn't depend on $\hat{V}$! The formula simplifies because we target **relative** precision.

**Corrected formula for variance estimation:**
- For the sample variance to have relative error $\delta$:
$$K^* = \left\lceil \frac{2}{\delta^2} \right\rceil$$

| Target relative error $\delta$ | Required K |
|-------------------------------|------------|
| 50% | 8 |
| 30% | 22 |
| 20% | 50 |
| 10% | 200 |
| 5% | 800 |

**Step 3: Additional runs**
- If $K^* > K_0$, run $K^* - K_0$ additional replications
- Recompute with all K replications

### 5.2 Accounting for Kurtosis

If estimates are non-normal (fat tails), the variance of $\hat{V}$ increases:
$$\text{Var}(\hat{V}) = \frac{\mu_4 - \sigma^4}{K} + O(K^{-2})$$

where $\mu_4$ is the fourth central moment.

**Adjusted formula:**
$$K^* = \left\lceil \frac{\kappa - 1}{\delta^2} \right\rceil$$

where $\kappa = \mu_4/\sigma^4$ is the kurtosis. For normal, $\kappa = 3$.

For heavy-tailed researcher estimates (e.g., some LLM runs produce outliers), $\kappa$ could be 5-10, requiring more runs.

---

## 6. Application to LLM-Bootstrap

### 6.1 Key Differences from Standard Bootstrap

| Aspect | Standard Bootstrap | LLM-Bootstrap |
|--------|-------------------|---------------|
| Cost per run | ~0 (computational) | ~$0.10-$1.00 |
| Resampling from | Data | Researcher choices |
| Parallel execution | Easy | Possible but adds complexity |
| Variance of interest | Sampling variance | Researcher variance |

The non-negligible cost per run means K is often limited by budget.

### 6.2 Budget-Constrained Optimal K

Given budget $B$, the constraint is:
$$K \cdot c \leq B \quad \Rightarrow \quad K \leq B/c$$

**Practical recommendation:**
- **Minimum K** for any meaningful analysis: 20-30
- **Standard K** for publication-quality estimates: 100
- **High-precision K** for definitive conclusions: 400+

### 6.3 Sequential Stopping Rule

A more sophisticated approach: run until the estimate stabilizes.

**Stopping Criterion:** Stop at K if:
$$\frac{|\hat{V}_K - \hat{V}_{K-m}|}{\hat{V}_K} < \delta$$

for some window size $m$ (e.g., $m = 10$) and tolerance $\delta$ (e.g., 5%).

**Algorithm:**
```
K = 20  # minimum
while True:
    Run LLM instance K
    Compute cumulative variance estimate V_K
    if K > 30 and relative_change(V_K, V_{K-10}) < 0.05:
        break
    if K > 500:  # safety limit
        break
    K += 1
```

---

## 7. Variance Reduction Techniques

### 7.1 Stratified LLM-Bootstrap

Instead of letting the LLM choose freely, stratify across key choice dimensions:

**Example stratification for Mincer:**
- Stratum 1: Sample ages 25-55
- Stratum 2: Sample ages 25-45  
- Stratum 3: Include industry FE
- Stratum 4: Exclude industry FE

Run K/4 replications in each stratum (with remaining choices free), then compute weighted variance.

**Benefit:** Reduces variance of $\hat{V}$ for fixed K by ensuring coverage of key dimensions.

### 7.2 Control Variates

If some specification gives a known benchmark, use as control variate:
$$\hat{\theta}^{CV} = \bar{\theta}^{LB} - \alpha(\hat{\theta}^{base} - \theta^{base})$$

where $\hat{\theta}^{base}$ is a baseline estimate (e.g., the "standard" Mincer).

### 7.3 Antithetic Variates

Design prompts that encourage "opposite" choices:
- Prompt A: "Use parsimonious specification"
- Prompt B: "Use rich specification with many controls"

Pair estimates to reduce variance:
$$\hat{\theta}^{AV}_j = \frac{\hat{\theta}_A + \hat{\theta}_B}{2}$$

---

## 8. Practical Recommendations

### 8.1 Rule of Thumb

$$K \approx \max\left(50, \frac{2}{\delta^2}\right)$$

where $\delta$ is desired relative precision for variance.

### 8.2 Decision Tree

```
Is this exploratory or definitive research?
├── Exploratory: K = 30-50
└── Definitive: Is precision critical?
    ├── No: K = 100
    └── Yes: K = 400+

What is budget per run?
├── < $0.05: K = 200+
├── $0.05-$0.50: K = 50-100
└── > $0.50: K = 20-50
```

### 8.3 Cost-Effectiveness

For a typical project with:
- 10 parameters of interest
- Budget of $100-500
- Precision requirement: 20% relative error on variance

**Calculation:**
- Per-parameter budget: $10-50
- Required K per parameter: 50
- Cost per run: $0.20-$1.00
- Total runs: 50 × 10 = 500
- Total cost: $100-500

This is feasible for academic research.

---

## 9. Connection to Sample Size Calculations

### 9.1 Analogy to Power Analysis

Just as power analysis determines sample size for detecting effects, we determine K for detecting researcher variance.

**"Power" of LLM-Bootstrap:**
- Null: $\sigma^2 = 0$ (no researcher variance)
- Alternative: $\sigma^2 = \sigma_A^2$
- Test: $\hat{V}^{LB} / \sigma_0^2$ follows scaled chi-squared

To detect researcher variance of size $\sigma_A$ with 80% power:
$$K \geq \frac{(\chi^2_{1-\beta, K-1})^2}{\sigma_A^2 / \sigma_0^2}$$

### 9.2 Minimum Detectable Effect

Inverting: with K runs, the minimum detectable researcher SD is approximately:
$$\sigma_{\min} \approx \frac{c \cdot \text{median SE}}{\sqrt{K}}$$

where $c \approx 2.8$ for 80% power.

**Example:** With K = 100 and median SE = 0.01:
$$\sigma_{\min} \approx \frac{2.8 \times 0.01}{\sqrt{100}} = 0.0028$$

We can detect researcher SD as small as 0.28 × the sampling SE.

---

## 10. Summary Table

| Objective | Recommended K | Precision |
|-----------|--------------|-----------|
| Quick exploration | 20-30 | ~40% relative error |
| Standard analysis | 50-100 | ~20% relative error |
| Publication quality | 100-200 | ~10-15% relative error |
| Definitive research | 400+ | ~7% relative error |

**Key Insight:** The optimal K balances precision gains (which diminish as $1/\sqrt{K}$) against cost (which grows linearly in K). For typical academic budgets, K = 50-200 is the sweet spot.
