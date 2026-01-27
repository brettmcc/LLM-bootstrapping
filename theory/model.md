# Formal Model: LLM-Bootstrap for Researcher Uncertainty

## 1. Setup and Notation

### 1.1 The Research Question

Consider a researcher attempting to estimate a causal parameter $\theta_0 \in \mathbb{R}$ representing the effect of treatment $D$ on outcome $Y$. For concreteness, think of:
- $\theta_0$: Returns to a year of education on log wages (Mincer regression)
- $D$: Years of schooling
- $Y$: Log hourly wages

### 1.2 The Population and True Parameter

Let $\mathcal{P}$ denote the true data-generating process over $(Y, D, X)$ where:
- $Y$: Outcome of interest
- $D$: Treatment/key explanatory variable  
- $X$: Observable covariates

The true structural relationship is:
$$Y = g(D, X, U; \theta_0)$$

where $U$ represents unobservables and $\theta_0$ is the parameter of interest.

**Definition 1 (True Parameter).** The true parameter $\theta_0$ is defined as:
$$\theta_0 \equiv \mathbb{E}_\mathcal{P}\left[\frac{\partial Y}{\partial D} \Big| \text{do}(D)\right]$$

This is the average causal effect under interventions on $D$.

### 1.3 The Researcher Choice Space

A **researcher** makes choices from a **choice space** $\mathcal{R}$:

**Definition 2 (Researcher Choice Set).** A researcher choice $r \in \mathcal{R}$ is a tuple:
$$r = (S, V, M, E)$$

where:
- $S \in \mathcal{S}$: **Sample restrictions** (age ranges, geographic scope, year ranges, outlier trimming rules)
- $V \in \mathcal{V}$: **Variable construction** (how $Y$, $D$, and $X$ are operationalized from raw data)
- $M \in \mathcal{M}$: **Model specification** (functional form, control variables included, fixed effects)
- $E \in \mathcal{E}$: **Estimation method** (OLS, IV, matching, etc.)

**Example (Mincer Regression):**
- $S$: Full-time workers ages 25-65, or ages 18-64, or include part-time, etc.
- $V$: Hourly vs. annual wages; years of schooling vs. degree dummies; potential experience vs. actual experience
- $M$: Log-linear, polynomial in experience, with/without industry controls
- $E$: OLS, IV using quarter-of-birth, or compulsory schooling laws

### 1.4 The Estimand Under a Given Choice

Given choice $r \in \mathcal{R}$ and a sample $\omega$ from population $\mathcal{P}$:

**Definition 3 (Choice-Specific Estimand and Estimator).** 
- The **estimand** under choice $r$ is $\theta(r) \in \mathbb{R}$
- The **estimator** from sample $\omega$ under choice $r$ is $\hat{\theta}(r, \omega)$

Note: Different choices may target different causal parameters. A key assumption below is that all choices identify "the same" parameter.

---

## 2. Uncertainty Decomposition

### 2.1 Three Sources of Variance

The total variance in estimates across researchers and samples can be decomposed:

**Proposition 1 (Variance Decomposition).** 
$$\text{Var}[\hat{\theta}(R, \Omega)] = \underbrace{\mathbb{E}_R[\text{Var}_\Omega(\hat{\theta}|R)]}_{\text{Sampling Variance}} + \underbrace{\text{Var}_R(\mathbb{E}_\Omega[\hat{\theta}|R])}_{\text{Researcher Variance}} + \underbrace{\text{Var}_R(\theta(R) - \theta_0)}_{\text{Specification Bias Variance}}$$

where:
- $R$ is a random draw from researcher choice distribution $\pi$ over $\mathcal{R}$
- $\Omega$ is a random sample from population $\mathcal{P}$

**Interpretation:**
1. **Sampling Variance**: Classical uncertainty from finite samples (what standard errors capture)
2. **Researcher Variance**: Heterogeneity in point estimates due to different choices, holding estimand fixed
3. **Specification Bias Variance**: Heterogeneity arising because different specifications identify different quantities

### 2.2 Assumption: Common Estimand

**Assumption 1 (Common Estimand).** All researcher choices in $\mathcal{R}$ target the same parameter:
$$\theta(r) = \theta_0 \quad \forall r \in \mathcal{R}$$

Under Assumption 1, the decomposition simplifies to:
$$\text{Var}[\hat{\theta}(R, \Omega)] = \mathbb{E}_R[\text{Var}_\Omega(\hat{\theta}|R)] + \text{Var}_R(\mathbb{E}_\Omega[\hat{\theta}|R])$$

**Remark.** Assumption 1 is strong but can be relaxed. It is analogous to requiring that different bootstrap resamples all target the same population parameter.

---

## 3. The LLM as a Stochastic Researcher

### 3.1 LLM Sampling from the Choice Space

Let $\pi_{\text{LLM}}: \mathcal{R} \to [0,1]$ denote the probability distribution over researcher choices induced by an LLM when prompted with a research question.

**Definition 4 (LLM-Induced Choice Distribution).** Given:
- A fixed prompt $P$ (the research question)
- Temperature parameter $\tau > 0$
- An LLM $\Lambda$

The LLM induces a distribution $\pi_{\text{LLM}}(r | P, \tau, \Lambda)$ over $\mathcal{R}$.

Due to the autoregressive sampling with temperature $\tau$, different runs produce different choices $r_1, r_2, \ldots \stackrel{iid}{\sim} \pi_{\text{LLM}}$.

### 3.2 Key Assumption: Relevance of LLM Distribution

**Assumption 2 (Relevance).** The LLM distribution $\pi_{\text{LLM}}$ satisfies:
$$\text{supp}(\pi_{\text{LLM}}) \supseteq \mathcal{R}_{\text{reasonable}}$$

where $\mathcal{R}_{\text{reasonable}} \subseteq \mathcal{R}$ is the set of "defensible" researcher choices.

**Remark.** This assumes the LLM's training on research papers allows it to produce the range of choices a reasonable researcher might make.

### 3.3 The LLM-Bootstrap Procedure

**Algorithm 1: LLM-Bootstrap**

**Input:** 
- Research question prompt $P$
- Number of LLM runs $K$
- LLM $\Lambda$ with temperature $\tau > 0$

**Procedure:**
1. For $k = 1, \ldots, K$:
   - Run LLM with prompt $P$ → LLM outputs code implementing choice $r_k$
   - Execute code to obtain estimate $\hat{\theta}_k \equiv \hat{\theta}(r_k, \omega)$
2. Collect estimates $\{\hat{\theta}_k\}_{k=1}^K$

**Output:**
- LLM-Bootstrap mean: $\bar{\theta}^{LB} = \frac{1}{K} \sum_{k=1}^K \hat{\theta}_k$
- LLM-Bootstrap variance: $\hat{V}^{LB} = \frac{1}{K-1} \sum_{k=1}^K (\hat{\theta}_k - \bar{\theta}^{LB})^2$

---

## 4. Asymptotic Properties

### 4.1 Law of Large Numbers for LLM-Bootstrap

**Proposition 2 (Consistency).** Under Assumptions 1-2, as $K \to \infty$:
$$\bar{\theta}^{LB} \stackrel{p}{\to} \mathbb{E}_{\pi_{\text{LLM}}}[\hat{\theta}(R, \omega)]$$

If additionally $\hat{\theta}(r, \omega)$ is an unbiased estimator for each $r$:
$$\bar{\theta}^{LB} \stackrel{p}{\to} \theta_0$$

### 4.2 Central Limit Theorem

**Proposition 3 (Asymptotic Normality).** Under regularity conditions, as $K \to \infty$:
$$\sqrt{K}(\bar{\theta}^{LB} - \mu_\theta) \stackrel{d}{\to} N(0, \sigma^2_\theta)$$

where:
- $\mu_\theta = \mathbb{E}_{\pi_{\text{LLM}}}[\hat{\theta}(R, \omega)]$
- $\sigma^2_\theta = \text{Var}_{\pi_{\text{LLM}}}(\hat{\theta}(R, \omega))$

This variance includes both researcher heterogeneity AND sampling variance (but these are confounded since we use the same sample $\omega$ across runs).

### 4.3 Variance Decomposition with Fixed Sample

**Important Observation.** In practice, LLM runs often use the **same underlying data** (e.g., downloaded from a common source). In this case:

$$\hat{V}^{LB} \stackrel{p}{\to} \text{Var}_R(\hat{\theta}(R, \omega)) \neq \text{Var}_R(\mathbb{E}_\Omega[\hat{\theta}|R])$$

The LLM-Bootstrap variance captures:
- **Researcher heterogeneity** in point estimates
- **Interaction** between researcher choices and the specific sample

But **not** sampling variability (since $\omega$ is fixed).

**Proposition 4 (Fixed-Sample Variance Interpretation).** For fixed sample $\omega$:
$$\hat{V}^{LB} \stackrel{p}{\to} \text{Var}_R(\hat{\theta}(R, \omega))$$

This is the **researcher variance given the sample**, which may be of independent interest.

---

## 5. Inference with LLM-Bootstrap

### 5.1 Confidence Intervals

Two types of confidence intervals can be constructed:

**Type 1: Researcher-Heterogeneity CI**
$$CI_{1-\alpha}^{RH} = \left[\bar{\theta}^{LB} - z_{1-\alpha/2} \sqrt{\frac{\hat{V}^{LB}}{K}}, \bar{\theta}^{LB} + z_{1-\alpha/2} \sqrt{\frac{\hat{V}^{LB}}{K}}\right]$$

This is a CI for the **mean estimate across researcher choices**, $\mu_\theta$.

**Type 2: Prediction Interval for a Single Replication**
$$PI_{1-\alpha} = \left[\bar{\theta}^{LB} - z_{1-\alpha/2} \sqrt{\hat{V}^{LB}}, \bar{\theta}^{LB} + z_{1-\alpha/2} \sqrt{\hat{V}^{LB}}\right]$$

This gives the range within which a new researcher's estimate would likely fall.

### 5.2 Comparison with Classical Standard Errors

Let $\hat{SE}_k$ denote the reported standard error from LLM run $k$.

**Definition 5 (Researcher Variability Ratio).** 
$$\lambda = \frac{\sqrt{\hat{V}^{LB}}}{\text{median}_k(\hat{SE}_k)}$$

**Interpretation:**
- $\lambda \approx 1$: Researcher heterogeneity ≈ Sampling uncertainty
- $\lambda \gg 1$: Researcher choices dominate; classical CIs are too narrow
- $\lambda \ll 1$: Sampling dominates; classical inference appropriate

---

## 6. Optimal Number of LLM Runs

### 6.1 Cost-Benefit Framework

Let:
- $c$: Cost per LLM run (API cost + compute)
- $V(K)$: Value of information from $K$ runs
- Total cost: $C(K) = Kc$

**Definition 6 (Value of Information).** One natural metric:
$$V(K) = -\text{Var}(\bar{\theta}^{LB}) = -\frac{\sigma^2_\theta}{K}$$

(Higher variance = lower value)

### 6.2 Optimal K Under Quadratic Loss

**Proposition 5 (Optimal Stopping Rule).** Under quadratic loss for uncertainty about $\mu_\theta$:
$$K^* = \arg\min_K \left\{ \frac{\sigma^2_\theta}{K} + Kc \cdot \delta \right\}$$

where $\delta$ converts costs to variance units.

**Solution:**
$$K^* = \sqrt{\frac{\sigma_\theta^2}{c \cdot \delta}}$$

### 6.3 Adaptive Rule

Since $\sigma^2_\theta$ is unknown, use an adaptive rule:

**Algorithm 2: Adaptive LLM-Bootstrap**

1. Start with $K_0$ initial runs (e.g., $K_0 = 10$)
2. Compute $\hat{V}^{LB}_{K_0}$
3. Estimate pilot variance: $\hat{\sigma}^2 = \hat{V}^{LB}_{K_0}$
4. Compute adaptive $K^*$:
$$\hat{K}^* = \left\lceil \sqrt{\frac{\hat{\sigma}^2}{c \cdot \delta}} \right\rceil$$
5. Run additional $\max(0, \hat{K}^* - K_0)$ LLM instances
6. Recompute $\hat{V}^{LB}$ with all runs

### 6.4 Connection to Bootstrap Literature

This is analogous to Andrews & Buchinsky (2000, 2001) on optimal bootstrap replications:

| Bootstrap | LLM-Bootstrap |
|-----------|---------------|
| Resample data | Resample researcher choices |
| $B$ replications | $K$ LLM runs |
| Convergence: $O(1/B)$ | Convergence: $O(1/K)$ |
| Cost per rep: computational | Cost per rep: API + compute |

Andrews & Buchinsky suggest $B = 400$ is often sufficient for SE estimation. Similar analysis applies here.

---

## 7. Extensions and Robustness

### 7.1 Weighted LLM-Bootstrap

If some specifications are more "defensible," use importance weighting:
$$\bar{\theta}^{WLB} = \frac{\sum_k w_k \hat{\theta}_k}{\sum_k w_k}$$

where $w_k$ could reflect:
- Prior beliefs about specification validity
- Inverse propensity weights if LLM oversamples certain choices
- Quality scores based on code correctness, data validity checks

### 7.2 Bayesian Aggregation

Model the estimates as:
$$\hat{\theta}_k | \theta_0, r_k \sim N(\theta_0 + \gamma_{r_k}, \sigma^2_k)$$

where $\gamma_{r_k}$ is specification bias for choice $r_k$.

Posterior on $\theta_0$ can be computed via hierarchical modeling.

### 7.3 Multiple Parameters

Extend to vector-valued parameters $\boldsymbol{\theta} \in \mathbb{R}^p$:
$$\hat{\boldsymbol{\Sigma}}^{LB} = \frac{1}{K-1} \sum_k (\hat{\boldsymbol{\theta}}_k - \bar{\boldsymbol{\theta}}^{LB})(\hat{\boldsymbol{\theta}}_k - \bar{\boldsymbol{\theta}}^{LB})'$$

---

## 8. Identification and Limitations

### 8.1 What Does LLM-Bootstrap Identify?

**Proposition 6 (Identification).** The LLM-Bootstrap variance identifies:
$$\hat{V}^{LB} \stackrel{p}{\to} \text{Var}_{R \sim \pi_{\text{LLM}}}(\hat{\theta}(R, \omega))$$

This is the **variance induced by the LLM's choice distribution**, not necessarily the variance across **all conceivable** researcher choices.

### 8.2 Limitations

1. **LLM training bias**: The LLM reflects patterns in its training data. If training papers cluster on similar specifications, LLM diversity is limited.

2. **Same sample**: Using the same underlying data underestimates total variance if choice of dataset contributes significantly.

3. **Code correctness**: LLMs make coding errors; estimates may include bugs.

4. **Finite temperature**: Low temperature reduces choice diversity.

5. **Prompt sensitivity**: Results depend on how the research question is framed.

### 8.3 Validation via Human Comparison

The ultimate test is comparing $\pi_{\text{LLM}}$ to distributions from human researchers:
- Multi-analyst studies (Silberzahn et al. 2018)
- Institute for Replication efforts

If LLM-Bootstrap variance correlates with human-researcher variance across studies, the method is validated.

---

## 9. Summary

The LLM-Bootstrap provides:
1. A **computationally tractable** approximation to researcher heterogeneity
2. **Variance estimates** for the spread of estimates across choices
3. **Guidance on optimal K** following bootstrap literature
4. A **complement** to classical standard errors

The key insight: LLM stochasticity is a feature, not a bug, when characterizing research uncertainty.

