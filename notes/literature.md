# Related Literature and Connections

## 1. Core Literatures

### 1.1 Bootstrap and Resampling Methods

**Foundational:**
- Efron, B. (1979). "Bootstrap Methods: Another Look at the Jackknife." *Annals of Statistics* 7(1): 1-26.
- Efron, B., & Tibshirani, R. (1993). *An Introduction to the Bootstrap*. Chapman & Hall.

**Optimal Bootstrap Replications:**
- Andrews, D.W.K., & Buchinsky, M. (2000). "A Three-Step Method for Choosing the Number of Bootstrap Repetitions." *Econometrica* 68(1): 23-51.
- Andrews, D.W.K., & Buchinsky, M. (2001). "Evaluation of a Three-Step Method for Choosing the Number of Bootstrap Repetitions." *Journal of Econometrics* 103(1-2): 345-386.

**Connection to LLM-Bootstrap:**
The bootstrap resamples from the data to approximate sampling variance. The LLM-Bootstrap "resamples" from researcher choices to approximate researcher variance. Both are Monte Carlo procedures requiring choice of replication number.

### 1.2 Researcher Degrees of Freedom

**Specification Curves:**
- Simonsohn, U., Simmons, J.P., & Nelson, L.D. (2020). "Specification Curve Analysis." *Nature Human Behaviour* 4: 1208-1214.

**Multiverse Analysis:**
- Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). "Increasing Transparency Through a Multiverse Analysis." *Perspectives on Psychological Science* 11(5): 702-712.

**Vibration of Effects:**
- Patel, C.J., Burford, B., & Ioannidis, J.P.A. (2015). "Assessment of Vibration of Effects due to Model Specification Can Demonstrate the Instability of Observational Associations." *Journal of Clinical Epidemiology* 68(9): 1046-1058.

**Connection to LLM-Bootstrap:**
These literatures document that researcher choices affect results substantially. Our contribution: use LLMs to efficiently sample from the choice space rather than enumerate it manually.

### 1.3 Multi-Analyst Studies

**Many Analysts, One Data Set:**
- Silberzahn, R., et al. (2018). "Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results." *Advances in Methods and Practices in Psychological Science* 1(3): 337-356.

**Institute for Replication:**
- Dreber, A., & Johannesson, M. (2019). "Statistical Significance and the Replication Crisis in the Social Sciences." *Oxford Research Encyclopedia of Economics and Finance*.

**Connection to LLM-Bootstrap:**
Multi-analyst studies provide ground truth for researcher variance. They are expensive (require many human teams). LLM-Bootstrap offers a scalable alternative.

### 1.4 Model Uncertainty and Averaging

**Bayesian Model Averaging:**
- Raftery, A.E., Madigan, D., & Hoeting, J.A. (1997). "Bayesian Model Averaging for Linear Regression Models." *Journal of the American Statistical Association* 92(437): 179-191.
- Hoeting, J.A., Madigan, D., Raftery, A.E., & Volinsky, C.T. (1999). "Bayesian Model Averaging: A Tutorial." *Statistical Science* 14(4): 382-417.

**Frequentist Model Averaging:**
- Hansen, B.E. (2007). "Least Squares Model Averaging." *Econometrica* 75(4): 1175-1189.

**Connection to LLM-Bootstrap:**
BMA averages over model uncertainty with explicit prior weights. LLM-Bootstrap provides an implicit weighting via the LLM's choice distribution—essentially the prior induced by training on research papers.

---

## 2. LLM and AI in Economics Literature

### 2.1 LLMs for Economic Research

**Early Applications:**
- Korinek, A. (2023). "Generative AI for Economic Research: Use Cases and Implications for Economists." *Journal of Economic Literature* (forthcoming).
- Athey, S., & Imbens, G. (2019). "Machine Learning Methods That Economists Should Know About." *Annual Review of Economics* 11: 685-725.

**LLMs as Respondents/Subjects:**
- Horton, J.J. (2023). "Large Language Models as Simulated Economic Agents: What Can We Learn from Homo Silicus?" *NBER Working Paper*.
- Brand, J., Israeli, A., & Ngwe, D. (2023). "Using GPT for Market Research." *NBER Working Paper*.

**Connection to LLM-Bootstrap:**
We use LLMs not as data or subjects, but as **synthetic researchers**—a novel application.

### 2.2 Algorithmic and Computational Economics

- Mullainathan, S., & Spiess, J. (2017). "Machine Learning: An Applied Econometric Approach." *Journal of Economic Perspectives* 31(2): 87-106.
- Kleinberg, J., Ludwig, J., Mullainathan, S., & Obermeyer, Z. (2015). "Prediction Policy Problems." *American Economic Review* 105(5): 491-495.

---

## 3. Returns to Education Literature (Mincer Example)

### 3.1 Classic References

- Mincer, J. (1974). *Schooling, Experience, and Earnings*. NBER.
- Card, D. (1999). "The Causal Effect of Education on Earnings." *Handbook of Labor Economics* 3: 1801-1863.
- Angrist, J.D., & Krueger, A.B. (1991). "Does Compulsory School Attendance Affect Schooling and Earnings?" *Quarterly Journal of Economics* 106(4): 979-1014.

### 3.2 Meta-Analyses Showing Estimate Heterogeneity

- Psacharopoulos, G., & Patrinos, H.A. (2018). "Returns to Investment in Education: A Decennial Review of the Global Literature." *Education Economics* 26(5): 445-458.

**Key Finding:** Meta-analytic variance across studies is much larger than within-study standard errors—precisely what the LLM-Bootstrap aims to quantify.

---

## 4. Statistical Theory Connections

### 4.1 Random Effects Meta-Analysis

- DerSimonian, R., & Laird, N. (1986). "Meta-analysis in Clinical Trials." *Controlled Clinical Trials* 7(3): 177-188.

**Model:**
$$\hat{\theta}_k | \theta_k \sim N(\theta_k, \sigma_k^2)$$
$$\theta_k \sim N(\mu, \tau^2)$$

where $\tau^2$ is between-study heterogeneity.

**Connection:** The LLM-Bootstrap variance $\hat{V}^{LB}$ estimates an analogous $\tau^2$—heterogeneity across researcher choices.

### 4.2 Cluster-Robust Inference

- Cameron, A.C., Gelbach, J.B., & Miller, D.L. (2008). "Bootstrap-Based Improvements for Inference with Clustered Errors." *Review of Economics and Statistics* 90(3): 414-427.

**Connection:** Just as clustering acknowledges within-cluster correlation, the LLM-Bootstrap acknowledges that estimates are clustered by researcher choice profile.

### 4.3 Sensitivity Analysis

- Rosenbaum, P.R. (2002). *Observational Studies*. Springer. (Sensitivity to hidden bias)
- Imbens, G.W. (2003). "Sensitivity to Exogeneity Assumptions in Program Evaluation." *American Economic Review* 93(2): 126-132.

**Connection:** Sensitivity analysis asks "how robust to assumption violations?" LLM-Bootstrap operationalizes this by varying assumptions empirically.

---

## 5. Philosophical and Methodological Foundations

### 5.1 Philosophy of Econometrics

- Heckman, J.J. (2000). "Causal Parameters and Policy Analysis in Economics: A Twentieth Century Retrospective." *Quarterly Journal of Economics* 115(1): 45-97.
- Leamer, E.E. (1983). "Let's Take the Con Out of Econometrics." *American Economic Review* 73(1): 31-43.

**Leamer's Insight:** Until we recognize that all specifications embed researcher choices, our standard errors are misleading.

### 5.2 Pre-Analysis Plans and Selective Reporting

- Olken, B.A. (2015). "Promises and Perils of Pre-Analysis Plans." *Journal of Economic Perspectives* 29(3): 61-80.
- Christensen, G., & Miguel, E. (2018). "Transparency, Reproducibility, and the Credibility of Economics Research." *Journal of Economic Literature* 56(3): 920-980.

**Connection:** Pre-registration locks in one specification. LLM-Bootstrap acknowledges that even honest researchers could have chosen differently.

---

## 6. Key Contributions Relative to Literature

| Existing Work | Our Contribution |
|---------------|------------------|
| Specification curves enumerate choices | LLM samples efficiently from high-dimensional choice space |
| Multi-analyst studies are expensive | LLM-Bootstrap is scalable and cheap |
| Bootstrap resamples data | LLM-Bootstrap resamples researcher choices |
| BMA requires explicit model space | LLM implicitly defines model space via training |
| Meta-analysis pools across studies | LLM-Bootstrap simulates studies |

**Novel Elements:**
1. Formal framework unifying researcher variance with sampling variance
2. Use of LLM stochasticity as a feature for inference
3. Adaptation of bootstrap optimal B theory to researcher-choice setting
4. Practical guidance for implementation

---

## 7. Empirical Validation Strategy

To validate LLM-Bootstrap against ground truth:

1. **Calibrate against multi-analyst studies**: Run LLM-Bootstrap on same questions as Silberzahn et al. (2018). Compare LLM variance to human variance.

2. **Cross-LLM comparison**: Do different LLMs (GPT-4, Claude, Gemini) produce similar variance estimates?

3. **Temperature sensitivity**: How does variance change with LLM temperature?

4. **Domain calibration**: Is LLM variance larger in contested areas (e.g., minimum wage effects) vs. consensus areas (e.g., demand curve slopes)?

---

## 8. Citation Format for Paper

### Main Text Citations

The LLM-Bootstrap relates to several established literatures. In characterizing researcher degrees of freedom, we build on specification curve analysis (Simonsohn, Simmons, and Nelson 2020) and multiverse analysis (Steegen et al. 2016). Our variance decomposition extends the classic sampling-variance framework (Efron 1979) to incorporate researcher heterogeneity. The optimal replication number follows Andrews and Buchinsky (2000, 2001). Multi-analyst studies (Silberzahn et al. 2018) provide ground truth for validation.

### BibTeX Entries (Key References)

```bibtex
@article{efron1979bootstrap,
  title={Bootstrap Methods: Another Look at the Jackknife},
  author={Efron, Bradley},
  journal={Annals of Statistics},
  volume={7},
  number={1},
  pages={1--26},
  year={1979}
}

@article{andrews2000bootstrap,
  title={A Three-Step Method for Choosing the Number of Bootstrap Repetitions},
  author={Andrews, Donald WK and Buchinsky, Moshe},
  journal={Econometrica},
  volume={68},
  number={1},
  pages={23--51},
  year={2000}
}

@article{simonsohn2020specification,
  title={Specification Curve Analysis},
  author={Simonsohn, Uri and Simmons, Joseph P and Nelson, Leif D},
  journal={Nature Human Behaviour},
  volume={4},
  pages={1208--1214},
  year={2020}
}

@article{silberzahn2018many,
  title={Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results},
  author={Silberzahn, Raphael and others},
  journal={Advances in Methods and Practices in Psychological Science},
  volume={1},
  number={3},
  pages={337--356},
  year={2018}
}

@article{card1999causal,
  title={The Causal Effect of Education on Earnings},
  author={Card, David},
  journal={Handbook of Labor Economics},
  volume={3},
  pages={1801--1863},
  year={1999}
}
```
