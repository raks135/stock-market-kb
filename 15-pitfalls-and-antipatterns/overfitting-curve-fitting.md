---
title: Overfitting and Curve Fitting in Trading Models
topic_id: 15-pitfalls-and-antipatterns/overfitting-curve-fitting
tags: [overfitting, curve-fitting, bias-variance, backtest-overfitting, selection-bias, deflated-sharpe, model-complexity]
last_updated: 2026-07-18
confidence: robust
sources: [S68, S69, S381, S380, S382, S383, S87, S83, S72, S86]
---

## TL;DR
- Overfitting means a model has been tuned to the *noise* in the sample, not the *signal* that generalizes; "curve fitting" is the special case of bending a flexible function (e.g. a high-degree polynomial) through the data points.
- The danger is mechanical and unavoidable at scale: the more parameter combinations, feature choices, or strategies you test on the same data, the nearer to certain a "significant" result becomes **even if the data contains no signal at all** (family-wise error rate 1−(1−α)^m → 1).
- Counter-measures exist (deflated Sharpe ratio, probability-of-backtest-overfitting / CSCV, model confidence set, regularization, walk-forward, honest trial accounting) but they are the exception, not the rule, in published backtests.
- Backtests are not forecasts: a good in-sample fit says nothing about out-of-sample performance, especially under regime non-stationarity. See also KB articles 05-stats-and-ml/overfitting-lookahead, 15-pitfalls-and-antipatterns/data-snooping-phacking, and 08-backtesting-methodology/deflated-sharpe-multiple-testing.

## Core explanation
**Plain language.** Suppose you try to predict a stock's next move using a smooth curve drawn through its past prices. If you use a very flexible curve (say, a 15th-degree polynomial) you can make it pass almost exactly through every historical point — the in-sample error goes to nearly zero. But that curve is mostly tracking random wiggles ("noise") that will not repeat. On new data it performs terribly. That is curve fitting / overfitting. The same logic applies whenever you pick a model's settings (indicator lengths, threshold levels, which features to include, which of 500 candidate strategies to deploy) by how well they did in the past: you are likely selecting the setting that happened to ride the luckiest random pattern, not a genuine edge.

**Precise.** Overfitting is a property of the *fit procedure*, not the model alone. A model is overfit when its in-sample performance materially exceeds its out-of-sample (OOS) performance because the procedure minimized in-sample error that included irreducible noise. The canonical decomposition is the **bias–variance tradeoff** (S382): the expected prediction error of an estimator decomposes into three additive parts —

E[(y−ŷ)²] = Bias² + Variance + σ²_noise,

where Bias = E[ŷ] − f(x) (systematic error from under-flexibility), Variance = E[(ŷ−E[ŷ])²] (sensitivity of the fit to the particular training sample), and σ²_noise is the irreducible error in the target. As model flexibility (number of tunable parameters, polynomial degree, tree depth, network size) increases, bias falls but variance rises. The OOS error is minimized at an intermediate complexity, not at the maximum complexity that minimizes training error. Curve fitting is overfitting whenever chosen complexity sits past that optimum.

In finance the train/test split is not a clean i.i.d. draw: returns are autocorrelated at short horizons, fat-tailed, and **non-stationary** (regimes shift), so the "test" period is itself a small, dependent sample from a moving distribution. This is why textbook cross-validation is necessary but not sufficient.

## Math / formulas

**Bias–variance (regression / squared error):**
- Bias²(ŷ) = (E[ŷ] − f(x))²
- Var(ŷ) = E[(ŷ − E[ŷ])²]
- EPE = Bias² + Var + σ²_ε

**Multiple-testing / selection inflation (the core overfitting engine).** If you run m independent tests at per-test size α, the probability of *at least one* false positive is

FWER = 1 − (1−α)^m.

With α = 0.05 and m = 500, FWER ≈ 1 − 0.95^500 ≈ 1 − 3.6e−12 ≈ 1.0. Even *correlated* trials inflate the rate (effective m is lower but still large); the Deflated Sharpe Ratio (below) bounds this properly. This is why "I only kept the 95%-significant strategy" is meaningless when that strategy was selected from hundreds tried.

**Deflated Sharpe Ratio (DSR, S68; see KB 08 deflated-sharpe article for formulas).** The DSR is the Probabilistic Sharpe Ratio evaluated at the *expected maximum* Sharpe ratio attainable under the null of no skill across N trials:

DSR = PSR(SR*) where SR* = E[max_i Sharpe_i] under the null.

It corrects a reported Sharpe for (a) selection bias from N trials and (b) non-normal (skewed/kurtotic) returns. A backtest reporting Sharpe 2.0 with naive p ≈ 0 can have DSR ≈ 0.03 once the number of trials is admitted.

**Probability of Backtest Overfitting (PBO, S69).** Frame each strategy configuration as a pair (IS performance, OOS performance). The PBO is the conditional probability that the configuration which is *optimal in-sample* nevertheless *underperforms the median OOS configuration*:

PBO = Pr( config is IS-optimal AND OOS < median OOS | IS-optimal ).

Bailey, Borwein, López de Prado & Zhu (2015) estimate PBO non-parametrically via **Combinatorially Symmetric Cross-Validation (CSCV)**, which splits the backtest history into many train/test blocks and checks whether the IS-best block consistently dominates OOS.

**Model Confidence Set (MCS, S383).** Rather than declare a single "best" model, the MCS is the set of models that, at confidence level 1−α, contains the truly best model. Uninformative data → a large MCS (many models tied); informative data → a small MCS. This is the honest way to report model selection under uncertainty.

## Worked example / code
Both snippets use synthetic data only (no market claim) and are pinned to `numpy==2.5.1` (run via the repo `.venv`). Reproduce with seeds 42 and 7.

**Snippet A — polynomial curve fitting (bias–variance in action).** Fit polynomials of increasing degree to 30 noisy points sampled from y = sin(2πx) + N(0, 0.3²), then measure error on a noiseless 400-point test grid.

```python
import numpy as np
rng = np.random.default_rng(42)
n = 30
x = np.linspace(0, 1, n)
f = np.sin(2 * np.pi * x)
y = f + rng.normal(0, 0.3, n)
xt = np.linspace(0, 1, 400); ft = np.sin(2 * np.pi * xt)
for d in [1, 3, 5, 9, 15]:
    p = np.poly1d(np.polyfit(x, y, d))
    print(d, round(np.mean((p(x)-y)**2), 4), round(np.mean((p(xt)-ft)**2), 4))
```

Verified output (train_MSE, test_MSE): deg1 (0.2844, 0.2064) → deg3 (0.0617, **0.0055 best**) → deg5 (0.0466, 0.0060) → deg9 (0.0411, 0.0119) → deg15 (0.0269, 0.0382). Training error falls monotonically as degree rises (the curve memorizes noise), while test error bottoms near degree 3 and then climbs — the textbook U-shape. The degree-15 fit "fits the past" 10× better than degree 3 yet generalizes ~7× worse.

**Snippet B — selection bias from a parameter/strategy search.** Simulate 500 independent "strategies" whose monthly returns are pure noise N(0, 0.04). Pick the one with the highest in-sample Sharpe and check its out-of-sample Sharpe.

```python
import numpy as np
from math import erf, sqrt
rng = np.random.default_rng(7)
T, N = 120, 500
def sharpe(r): return r.mean()/r.std()*sqrt(12)
def pval(t): return 2*(1 - 0.5*(1+erf(abs(t)/sqrt(2))))
best_is, best_oos = -1e9, None
for _ in range(N):
    is_r = rng.normal(0, 0.04, T); oos_r = rng.normal(0, 0.04, T)
    s = sharpe(is_r)
    if s > best_is: best_is, best_oos = s, sharpe(oos_r)
print(best_is, best_oos)   # 1.011  0.006
```

Verified output: best in-sample Sharpe = **1.011** (t ≈ 11.1, naive two-sided p ≈ 0 — "highly significant!") but that same strategy's OOS Sharpe = **0.006** (t ≈ 0.06, p ≈ 0.95 — pure noise). Selecting the best of 500 noise trials manufactures a false positive. This is exactly the mechanism behind published "strategies" that die on contact with live data.

## Assumptions & limitations
- **Needs a genuine OOS partition that was never used for any decision** (including "which model family to try"). Reusing the test set, even implicitly, leaks information.
- **Stationarity is assumed** when you treat OOS history as representative of the future. Regime change (see KB 11-macro-and-regimes/regime-detection-methods) can invalidate even a clean OOS result.
- **Independence of trials is assumed** by the simple FWER formula; real strategy variants are correlated, so the effective m is lower but still large. DSR and CSCV handle dependence better than 1−(1−α)^m.
- **Sample size matters:** with T = 120 months a single noise strategy already gives Sharpe up to ~1 by luck; small samples make overfitting trivial.
- **Costs/capacity are not captured** by raw backtest fit; a strategy that "fits" pre-cost can be negative net-of-cost (see KB 08 transaction-costs-slippage-walkforward, 15 transaction-cost neglect).

## Empirical evidence
- **Backtests are prone to false positives by construction.** Bailey, Borwein, López de Prado & Zhu (2015, S69) note that even the simplest crossover system has ≥5 free parameters (two moving-average lengths, entry, exit, stop), yielding billions of combinations across thousands of securities; a 5% false-positive rate holds only if the test is applied *once*, not billions of times. They show standard hold-out is unreliable for investment backtests and propose CSCV/PBO.
- **Backtest optimizers find random patterns.** Bailey & López de Prado (2014, S68) show optimizers search for parameter combinations maximizing simulated history, identifying rules that profit from the most extreme random patterns in sample; failing to control for trial count inflates expected performance. Their Deflated Sharpe corrects for selection bias + non-normality.
- **Finance is structurally prone to false discovery.** Bailey (Significance/RSS, 2022, S381, summarizing SSRN 3895330) gives three reasons: (a) the chance of a statistically significant profitable strategy is low because of competition; (b) true discoveries are short-lived due to rapidly changing financial systems (non-stationarity); (c) false claims are rarely debunked by controlled OOS experiments. They add that academic journals seldom require authors to disclose the extent of their computer search, so "optimal" designs are often statistical mirages.
- **Past fit does not predict.** Campbell & Thompson (2008, S380) show that in out-of-sample equity-premium forecasting, most predictor variables yield *negative* OOS R² (the model does worse than just using the historical average); only a handful (e.g. cay, the T-bill rate, the term spread, dividend payout, equity share of new issues, the consumption–wealth ratio) beat the historical average, and only under sign restrictions. This is direct evidence that in-sample explanatory power is routinely illusory.
- **Model selection under uncertainty.** Hansen, Lunde & Nason (2011, S383) introduce the Model Confidence Set: instead of crowning one model, report the set that contains the best with confidence 1−α; uninformative data yield a large set. This is the disciplined alternative to "pick the highest Sharpe."
- **Factor-zoo context / scale of the problem.** Harvey, Liu & Zhu (2016, S72) estimate that with hundreds of published factors, a t-statistic near 3.0 is needed to clear multiple-testing — corroborating that naive significance is insufficient (conflict on the exact count is detailed in KB 08 deflated-sharpe-multiple-testing).

## Conflicting views
- **"Hold-out / cross-validation works" vs "hold-out is unreliable in finance" (both partly right).** Naive single train/test splits are unreliable for backtests because of dependence, non-stationarity, and trial reuse (S69). Proper procedures (CSCV, combinatorial purged CV, strict walk-forward with embargo/purge per López de Prado) *do* work — the disagreement is about method, not whether the problem exists.
- **Is there a replication crisis in finance?** Bailey et al. (S381) argue yes, citing the poor aggregate OOS record of active funds and forecasters. Some practitioners dispute the magnitude or relevance. The preponderance of poor OOS performance supports caution; the debate is over degree, not direction.
- **"More parameters capture more signal."** The bias–variance result (S382) says the opposite past the optimum: extra flexibility mostly captures noise. Complex ML models can win (see KB 05 feature-engineering-ml-pitfalls, Gu–Kelly–Xiu), but only with leakage control and regularization — not by maximizing in-sample fit.
- **"A 95%-significant backtest is validated."** False once selection across many trials is admitted; DSR/MCS are the remedies (S68, S383).

## Common mistakes
1. **Treating in-sample fit as predictive.** A degree-15 polynomial "explains" the past perfectly and predicts the future worse than a straight line (Snippet A).
2. **Reporting the IS-optimal setting's own performance as if it were OOS.** You must evaluate the *chosen* configuration on data it never touched (Snippet B shows the gap: Sharpe 1.01 → 0.01).
3. **Not counting all the trials.** Parameter grids, feature selections, strategy families, and even "which idea to test" all count toward m. Failing to disclose m is the single most common sin (S381).
4. **Single split with reuse.** Tuning hyperparameters on the test set, or re-running until the test set "looks good," leaks.
5. **Ignoring non-stationarity.** A clean OOS result on 2000–2010 may not survive a 2022 regime (see KB 11 regime articles).
6. **Neglecting costs and capacity.** Overfitting to a net-of-cost appearance that evaporates with realistic slippage (see KB 08, 15 transaction-cost neglect).
7. **Polynomial/parameter explosion.** Adding degrees of freedom to "improve the curve" is the literal definition of curve fitting; it guarantees the U-shape.
8. **Survivorship / look-ahead leakage in the data** (see KB 13 data-hygiene, 15 survivorship bias) — overfitting sits on top of these and compounds them.

## Further reading
- **Tier 1 (primary):** Bailey & López de Prado (2014), "The Deflated Sharpe Ratio" — https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf (S68). Bailey, Borwein, López de Prado & Zhu (2015), "The Probability of Backtest Overfitting" — https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf (S69). Campbell & Thompson (2008), "Predicting Excess Stock Returns Out of Sample" — https://www.nber.org/system/files/working_papers/w11468/w11468.pdf (S380). Hansen, Lunde & Nason (2011), "The Model Confidence Set," *Econometrica* — https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA5771 (S383). White (2000), "A Reality Check for Data Snooping," *Econometrica* (S87). Lo (2002), "The Statistics of Sharpe Ratios" (S86). Harvey, Liu & Zhu (2016), "...and the Cross-Section of Expected Returns" (S72). Benjamini & Hochberg (1995), FDR control (S83).
- **Tier 2 (practitioner):** Bailey (2022), "How backtest overfitting in finance leads to false discoveries," *Significance* (RSS) — https://mathinvestor.org/2022/01/how-backtest-overfitting-in-finance-leads-to-false-discoveries (S381). Wikipedia, "Bias–variance tradeoff" — https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff (S382). López de Prado, *Advances in Financial Machine Learning* (CSCV/CPCV, purged CV).
- **Related KB articles:** 05-stats-and-ml/overfitting-lookahead, 05-stats-and-ml/feature-engineering-ml-pitfalls, 08-backtesting-methodology/deflated-sharpe-multiple-testing, 08-backtesting-methodology/transaction-costs-slippage-walkforward, 13-data-and-tooling/backtesting-libraries-cookbook, 15-pitfalls-and-antipatterns/data-snooping-phacking, 15-pitfalls-and-antipatterns/transaction-cost-neglect, 15-pitfalls-and-antipatterns/survivorship-bias.
