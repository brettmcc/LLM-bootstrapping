# Measuring Estimation Uncertainty due to Researcher Degrees of Freedom with Agentic Artificial Intelligence

**Date**: 06/02/2026
**Domain**: social_sciences/economics
**Taxonomy**: academic/working_paper
**Filter**: Active comments

---

## Overall Feedback

Here are some overall reactions to the document.

**Outline**

The paper has a promising and timely idea, but the current version does not yet pin down what object the AI-agent distribution estimates or show that the validation exercise is comparable enough to support the main claims.

The contribution is potentially useful: replacing some many-analyst study costs with agentic replications could matter for empirical economics. The paper also does well to report that similar estimate distributions can arise from very different specification choices. At present, though, the evidence is too thin to justify treating the agent output distribution as a measure of researcher-degrees-of-freedom uncertainty rather than a mixture of prompt, model, execution, and coding variation.

**The target uncertainty object is not defined**

Section 2.1 says AI outputs can be interpreted as draws from a noisy representation of standard empirical social science practice, and the Introduction frames the method as measuring researcher-induced uncertainty. That is too loose for the paper's main claim. The reader needs to know whose researcher-choice distribution is being approximated: applied economists, all competent analysts, users of a given AI harness, or the conditional distribution induced by one prompt and two models. This matters because Table 1 treats every valid AI run as equally informative, even though some choices may be much more common or defensible among human researchers than others. A revision should define the estimand explicitly, including the population of researcher choices, the weighting rule over specifications, and whether invalid or low-quality analyses are outside the target population or part of the measured uncertainty.

**Independence across agent runs is assumed rather than shown**

The core design in Sections 2.1 and 2.2 relies on repeated AI agents receiving the same prompt and raw data, with LLM stochasticity said to ensure varied research choices. Stochastic output is not the same as independent analyst judgment. Runs using GPT-5.4 mini through the same GitHub Copilot CLI may share prompt priors, hidden templates, package choices, code idioms, and failure modes, so 156 runs may have far fewer effective degrees of freedom than 156 human teams. Table 3 already hints at strong dependence, with 80.8 percent of AI runs using state fixed effects by year fixed effects and 95.5 percent using sample weights. The paper should add sensitivity checks across materially different prompts, model families, temperatures or sampling settings, harnesses, and code templates, then report how much of the estimate dispersion remains within and across those design cells.

**The human benchmark is not aligned with the AI comparison**

Section 3 says the comparison uses 145 human analyses from the same research question with complete freedom, but the notes to Tables 2 and 3 say the human specification-choice data include more restricted Tasks 2 and 3 from Huntington-Klein et al. (2025). That creates a direct comparability problem. The estimate distribution in Table 1 appears to benchmark against Task 1, while the specification-choice tables mix in tasks where the design was more tightly specified and precleaned data were supplied. This matters because the paper's most interesting finding is that AI achieves similar estimates through different choices; if the human choice distribution is drawn from a different task environment, that finding is hard to interpret. The fix is to rebuild Tables 2 and 3 using only the same Task 1 human submissions, or else present separate panels by task and state clearly which comparison supports each claim.

**Specification quality is not audited enough to separate plausible choices from errors**

Section 2.2 describes agents writing a specification file, writing code, fixing errors, and reporting a preferred coefficient, but the paper gives little information on how completed analyses were checked. This is a major gap because the measured dispersion may include coding mistakes, miscoded treatment variables, inappropriate samples, duplicate observations, failed clustering, or accidental model changes. Table 1 reports AI standard errors as low as 0.000 and a maximum standard error of 0.088, and footnote 5 says Haiku runs were dropped after degenerate outcomes; those facts make an explicit audit protocol necessary. The paper should specify preregistered exclusion rules, run-level validation checks, and manual review criteria for economic defensibility. A useful addition would be a table classifying AI runs as valid, questionable, or invalid, with the main Table 1 results recomputed under stricter inclusion rules.

**Researcher-choice uncertainty is mixed with sampling, execution, and LLM noise**

The Introduction distinguishes standard errors from uncertainty due to researcher degrees of freedom, but the empirical design in Sections 2 and 3 does not cleanly isolate that second component. The AI distribution includes variation in specification choices, but also variation from code execution, possible package defaults, data parsing decisions, model hallucinations, and random LLM behavior unrelated to a defensible empirical choice. Conversely, the reported coefficient dispersion in Table 1 is compared alongside standard errors, but the paper does not say how these two uncertainty sources should be combined or interpreted for inference. This matters because the method could overstate researcher uncertainty if it counts implementation noise, or understate it if the prompt suppresses broader human exploration. The revision should decompose variation by rerunning identical generated specifications, bootstrapping or resampling within fixed specifications, and separately measuring the dispersion from specification choice versus implementation noise.

**The claim that AI sometimes better follows field standards needs evidence**

Section 3.2 concludes that AI agents often better hewed to the field's empirical standard, citing two-way fixed effects, linear probability models, and ACS weights. That claim goes beyond the evidence currently shown. In the DACA setting, controls such as education, state-by-year structure, sample restrictions, and treatment eligibility proxies can change the estimand, not just polish the specification. Human analysts may have omitted some controls or weights for substantive reasons, while AI agents may have converged on a familiar template without matching the research question. The paper should not infer quality from convention alone. A stronger version would define ex ante audit criteria for defensible choices in this application, have independent reviewers score a sample of human and AI specifications, and report whether estimate dispersion changes after excluding analyses that fail those criteria.

**The evidence is too narrow for the stated methodological contribution**

The paper's contribution in the Introduction is framed as a scalable approach to multi-analyst designs, but the evidence comes from one application, one public benchmark, one main model, and one main harness. The Conclusion acknowledges possible training contamination from public OSF materials, which is important because the task, codebooks, and human submissions may have been visible before the AI runs. That limitation is not just external validity; it affects the main validation exercise, since the agents may partly reproduce public artifacts rather than independently approximate analyst behavior. A top-field version of this paper needs at least one additional task where the human benchmark was not public during model training, or a design that withholds benchmark-specific materials from the agent beyond what human analysts received. Short of that, the claims should be narrowed to a diagnostic case study rather than a validated substitute for many-analyst studies.

**No decision-level validation of the AI distribution**

The paper reports that AI and human coefficient, standard-error, and sample-size distributions are broadly similar, but it does not show whether the AI exercise would lead a researcher to the same substantive uncertainty assessment as the human many-analyst study. This matters because the proposed use is to measure researcher-induced uncertainty, not only to match a few marginal summary statistics. A more publication-ready version would compute the non-standard error or interquartile spread used in Menkveld et al. (2024) for both AI and human analysts, then compare resulting decision margins: for example, whether the interval formed by the median estimate plus or minus the human versus AI non-standard error crosses zero, and whether the share of positive and statistically significant estimates is similar. The paper should also report a distributional distance measure, such as a Kolmogorov-Smirnov statistic or Wasserstein distance, for the coefficient distribution rather than relying on visual resemblance and selected percentiles. That calculation would make clear whether the method has bite for the inferential object it claims to approximate.

**Missing worked example of one complete agent specification**

Readers never see a fully worked agent analysis from raw research prompt to estimating equation and sample construction. Footnote 4 sketches one generated file, but the paper does not show the exact regression equation, the construction of treated and post indicators, the sample restrictions applied in sequence, or the resulting coefficient and standard error for a single run. This is a real gap because the unit of analysis in the paper is an “AI agent-generated empirical specification,” yet the reader cannot inspect what one such specification concretely looks like. The paper should add a short worked example using a representative AI run: define full-time work as usual hours worked at least 35, construct DACA eligibility from Mexican birthplace, Hispanic origin, non-citizenship, childhood arrival, and birth cohort, then estimate the linear probability model with state and year fixed effects, state clustering, and ACS weights. A table showing the sample count after each restriction would also help readers judge whether the agent’s implementation is substantively coherent.

**No practical guidance for choosing the number of agent runs**

The method is presented as scalable because many AI agents can be run cheaply, but the paper does not say how many runs are needed to estimate researcher-induced uncertainty with useful precision. The reported 156 runs may be enough, too few, or far more than needed; without a convergence exercise, users have no basis for designing their own AI multi-analyst study. The revision should add a subsampling analysis that draws 10, 25, 50, 100, and 150 agent runs many times and reports the sampling variability of the estimated median, interquartile range, non-standard error, and share of significant estimates. A stopping rule would be even better: for example, continue runs until the 95 percent bootstrap interval for the AI interquartile range is narrower than a prespecified tolerance. That would turn the method from a proof of concept into something other researchers can implement responsibly.

**Existing AI-agent approaches are not empirically benchmarked**

The introduction cites concurrent papers by Gao and Xiao, Grundl, and Huang et al., but the paper does not compare its pipeline or findings against those approaches beyond a short priority footnote. Since the claimed contribution is methodological, readers need to know whether the conclusions depend on this particular agent design or are consistent with nearby designs already in circulation. A useful addition would be a comparison table listing each study’s task, model, harness, prompt structure, number of runs, validation target, and main dispersion measure. If Grundl also studies the Huntington-Klein benchmark, the paper should compute at least one common statistic across both studies, such as the AI coefficient interquartile range, share using nonlinear models, or share using state-clustered standard errors. That would clarify what this paper adds beyond being another application of agentic AI to many-analyst replication.

**Recommendation**: major revision. The paper asks an important question and has a clear empirical starting point, but the current design does not yet establish that the agent distribution measures researcher-degrees-of-freedom uncertainty. The largest problems are the undefined estimand, the weak evidence on independence, the benchmark mismatch in Tables 2 and 3, and the lack of a run-quality audit.

**Key revision targets**:

1. Define the target estimand for agent-generated researcher-choice uncertainty, including the population of choices, weighting rule, and treatment of invalid or low-quality analyses.
2. Rebuild the human-AI benchmark so all estimate and specification-choice comparisons use the same Huntington-Klein et al. (2025) task, or present task-specific comparisons separately.
3. Add an audit protocol for AI runs, with validation checks for code correctness, sample construction, treatment definition, standard errors, and economic defensibility; recompute the main results under stricter inclusion rules.
4. Run sensitivity analyses across prompts, models, harnesses, and randomness settings to show how much variation is induced by researcher-like choices rather than shared AI priors or execution noise.
5. Either add a second, less contaminated application or narrow the paper's claims to a proof-of-concept diagnostic rather than a scalable substitute for human many-analyst studies.

**Status**: [Pending]

---

## Detailed Comments (11)

### 1. Similarity claim overstates Table 1

**Status**: [Pending]

**Quote**:
> Across all four outcomes, means and medians are fairly similar between human and AI
> 
> researchers. Moreover, both humans and AI agents exhibit substantial dispersion in their
> 
> estimation outcomes, underling the stochasticity of AI outputs.

**Feedback**:
The sentence is too broad for the numbers in Table 1. Effect-size medians are close, and some lower-quartile standard errors match, but the mean standard error is 0.019 for humans versus 0.008 for AI, and the mean sample size is 828,318 versus 165,965. Those are large differences, not small ones. A more accurate version would say that the coefficient distributions have similar central tendencies, while human analyses have a higher mean standard error and a much larger mean sample size.

---

### 2. Significance shares need run-level support

**Status**: [Pending]

**Quote**:
> For
> 
> standard errors, the minimum, 25th percentile, and median are identical across humans and
> 
> AI, while humans exhibit higher standard errors at the 75th percentile and maximum. As a
> 
> result, AI agents obtain coefficients statistically significantly different from 0 about 90% of
> 
> the time, compared to 78% time among humans.

**Feedback**:
The move from marginal standard-error summaries to the share of statistically significant estimates needs one more step. Significance is determined run by run from paired estimates and standard errors; the marginal distributions alone do not imply the 90 percent and 78 percent figures. Add a sentence stating exactly how these shares were computed, for example: “The significance shares are computed run by run using |estimate/standard error| > 1.96 among analyses with both quantities available.”

---

### 3. Fully saturated design is overstated

**Status**: [Pending]

**Quote**:
> Nearly 90% of AI
> 
> agents included year fixed effects, compared to just 24% of human runs. Similarly, nearly 90%
> 
> of AIs included state fixed effects compared to 36% of human runs. Using a fully-saturated
> 
> difference-in-difference diminishes the downsides of linear probability models, the choice of
> 
> every AI agent.

**Feedback**:
The phrase “fully-saturated difference-in-difference” appears to refer to the state-by-year interaction in Table 3, but that row is 80.8 percent for AI agents, not nearly 90 percent, and it is distinct from the separate state and year fixed-effect rows. The next claim also goes too far: state and year saturation does not by itself address the usual linear-probability-model issues such as fitted values outside [0,1] or heteroskedastic errors. A safer revision would say that many AI specifications used a common fixed-effects template, including state-by-year fixed effects in 80.8 percent of runs, while avoiding the claim that this fixes the limitations of linear probability models.

---

### 4. Stochastic output and bounds are misstated

**Status**: [Pending]

**Quote**:
> Large language AI models, such as GPT or Claude, by construction give non-deterministic
> 
> responses: the same prompt can generate a range of responses ex-ante. By submitting a
> 
> prompt to estimate a given empirical parameter many times to independent AI agents, I
> 
> 
> 3
> 
> 
> propose to simulate at much lower cost a many-analyst approach for generating bounds on
> 
> the degree of estimation uncertainty due to researcher degrees of freedom.

**Feedback**:
This passage should separate the model class from the sampling procedure. A probabilistic next-token model does not guarantee different observed responses if decoding is deterministic; variation comes from stochastic decoding or other randomness in the agent pipeline. The word “bounds” is also stronger than what a finite set of 156 runs delivers unless the paper states a coverage rule or support assumption. Consider revising to: “With stochastic decoding enabled, large language AI models such as GPT or Claude can generate different responses to the same prompt. Repeated agent runs can then estimate the distribution, quantiles, or dispersion of outcomes induced by the agent pipeline.”

---

### 5. Interquartile range is reported as endpoints

**Status**: [Pending]

**Quote**:
> Across 156 AI
> 
> agent-generated specifications, I obtain an interquartile range from 0.014 to 0.099, resembling
> 
> the human many-analyst coefficient distribution.

**Feedback**:
The numbers reported are the 25th and 75th percentile endpoints, not the interquartile range itself. Given Table 1, the scalar interquartile range is 0.099 - 0.014 = 0.085. This is easy to fix: write that the middle 50 percent of AI estimates spans 0.014 to 0.099, implying an interquartile range of 0.085.

---

### 6. LLM mechanism is described too literally

**Status**: [Pending]

**Quote**:
> 2Large language models (LLM) work by predicting the next token in their output using a logit function.
> This logit function can have billions or even trillions of parameters. Not all of these parameters are ’activated’
> each run. Which parameters are activated depends on the context fed into the model; in my empirical
> application, the prompt and files provided to the AI agent. Parameters associated to econometrics (e.g., a
> Stata command to estimate a difference-in-differences model) may be given a higher weight when the prompt
> includes such words as “causal” and “identification”, while data science parameters may be more heavily
> weighted when the prompt includes such words as “prediction”.

**Feedback**:
The footnote has the right broad idea: prompts can shift the model toward econometric or data-science continuations. The mechanism is described too literally, though. For ordinary dense transformer models, the learned weights are fixed at inference time; the prompt changes activations, attention patterns, and output probabilities, not which Stata- or econometrics-specific parameters are switched on. A cleaner version would say that the prompt changes the probability assigned to possible continuations, so words such as “causal” and “identification” may make econometric analysis choices more likely.

---

### 7. Zero marginal cost conflicts with usage limits

**Status**: [Pending]

**Quote**:
> Each run has 0 dollar marginal cost when using a
> 
> subscription such as GitHub Copilot, Codex, or Claude Code, making large-scale replication
> 
> affordable for individual researchers. [6]

**Feedback**:
The main text says each run has zero-dollar marginal cost, while footnote 6 says each run consumes scarce 5-hour and weekly usage limits. That is a real resource cost even if there is no immediate cash charge. The claim would be more precise as: “Within an existing subscription such as GitHub Copilot, Codex, or Claude Code, each run may have no additional out-of-pocket charge until usage limits bind, making moderate-scale replication affordable for individual researchers.”

---

### 8. Sample-size range is numerically overstated

**Status**: [Pending]

**Quote**:
> The range of sample sizes chosen by human researchers—between 681 and over 29 million
> 
> observations—is several orders of magnitudes larger than what the AI agents chose. Still, the
> 
> interquartile range is comparable: 75 to 248 thousand for the AI, and 61 to 357 thousand for
> 
> the humans.

**Feedback**:
If “range” means the width between the minimum and maximum, the statement overstates the difference. From Table 1, the human range is 29,536,580 - 681 = 29,535,899, while the AI range is 636,722 - 1,764 = 634,958. The human range is about 46.5 times wider, which is large but not “several orders of magnitude” larger. Say “about 47 times wider” if the intended comparison is the min-to-max width.

---

### 9. Human denominators vary in Table 2

**Status**: [Pending]

**Quote**:
> **Notes:** Estimation choices are inferred from each generated model specification and execution
> metadata. Data from Huntington-Klein _et_ _al._ (2025) includes more restricted human runs
> (Tasks 2 and 3) in which the research design was more tightly specified and precleaned data
> was provided.

**Feedback**:
Table 2 appears to use different human denominators across categories. The human method counts sum to 437, while the human standard-error and weighting counts each sum to 438. That may reflect missing classifications or different source files, but the note does not say. Add a denominator sentence, such as: “Human method choices are available for 437 runs, while standard-error and weighting choices are available for 438 runs; percentages use the non-missing denominator within each category.”

---

### 10. Log sample-size values are not reported exactly

**Status**: [Pending]

**Quote**:
> Figure 1 depicts box-and-whisker plots for both human and AI analyses for weighted and
> 
> unweighted effects, standard errors, and sample size. The left-most whisker depicts the
> 
> minimum value, the box depicts the 25th percentile value, median, and 75th percentile, with
> 
> the right-most whisker showing the maximum reported value. Exact values are reported in
> 
> Table 1.

**Feedback**:
The figure note says the bottom-right panel plots log sample sizes, while Table 1 reports raw sample-size summaries. Those are related, but they are not the exact plotted values. Revise the last sentence to something like: “Table 1 reports the raw sample-size summaries underlying the log sample-size panel.”

---

### 11. Parallel-invention claim exceeds the cited evidence

**Status**: [Pending]

**Quote**:
> 1There are at least 3 other concurrent, unpublished papers that attempt to do broadly what I propose in
> this article: Gao and Xiao (2026), Grundl (2026), and Huang _et_ _al._ (2026). Given the timing of the release
> of these working papers and the work on my own public GitHub repository for this article dating back to
> January 2026 (see [https://github.com/brettmcc/LLM-bootstrapping),](https://github.com/brettmcc/LLM-bootstrapping) this is a clear case of parallel invention.

**Feedback**:
The timing evidence supports a narrower statement than “a clear case of parallel invention.” A public GitHub repository can document when this project existed, and the release dates can show that several projects appeared close together. They do not, on their own, prove independent invention by all parties. The footnote would be stronger if it used a chronological claim: “these papers appear to have been developed contemporaneously.”

---
