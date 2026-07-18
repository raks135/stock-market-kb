---
title: Value at Risk (VaR) and Conditional VaR (CVaR / Expected Shortfall)
topic_id: 07-risk-management/var-cvar
tags: [risk-management, var, cvar, expected-shortfall, market-risk, backtesting, coherent-risk-measure]
last_updated: 2026-07-18
confidence: robust
sources: [S110, S111, S112, S113, S114, S115, S116, S117, S118]
---

## TL;DR
- **VaR** answers "what is my minimum loss over horizon *T* that I should not exceed with probability *α*?" (e.g., 1-day 95% VaR = the loss breached on ~1 day in 20). It is a **quantile**, not a worst-case.
- **CVaR / Expected Shortfall** answers the follow-up VaR leaves open: "**given** I am beyond the VaR threshold, what is my average loss?" It is coherent (satisfies the four Artzner axioms) and is now the regulatory market-risk standard under Basel FRTB, which **replaced 99% VaR with ~97.5% Expected Shortfall** (KPMG 2025; SIFMA 2021).
- Three estimation methods — **parametric (delta-normal)**, **historical simulation**, **Monte Carlo** — give different answers; none is "right" and all inherit the quality (and non-stationarity) of their inputs (CFA Institute 2026).
- **Failure modes to respect:** VaR ignores tail *severity*; VaR is generally **not subadditive** (can penalize diversification); backtests (e.g., Kupiec) have low power at extreme tails and assume independent exceedances; normal-assumption VaR badly understates crisis risk.

## Core explanation
**Plain language.** VaR compresses "how much can I lose?" into one number: the loss threshold that, under normal market conditions and no trading, is *not* exceeded with a chosen probability (the confidence level *α*, e.g. 95% or 99%) over a chosen horizon (1 day, 10 days, 1 month). CFA Institute (S110) defines VaR as "the minimum loss in either currency units or as a percentage of portfolio value that would be expected to be incurred a certain percentage of the time over a certain period of time given assumed market conditions." If a portfolio has a 1-day 95% VaR of \$1M, that means a loss of \$1M or more is expected on about 1 day in 20 (Wikipedia, S112).

**CVaR (Expected Shortfall)** is the average loss *conditional on* exceeding that VaR cutoff. Wikipedia (S113) states it is "the expected return on the portfolio in the worst *q*% of cases" and that it is "often considered preferable to VaR because it accounts for the severity of the failure, not only the chance of failure." It is also called AVaR, TVaR, CTE, or ETL.

**Precise.** Let *L* be the portfolio loss over horizon *T* (a random variable). For confidence level *α* ∈ (0,1),
- **VaR**:  VaR_α = inf{ ℓ : P(L > ℓ) ≤ 1−α }  — the (1−α) quantile of the loss distribution.
- **CVaR / ES**:  CVaR_α = E[ L | L ≥ VaR_α ]  — the mean of the worst (1−α) tail of losses. By construction **CVaR_α ≥ VaR_α** (Wikipedia S113).

VaR is a **risk metric / measure** but, as used in practice, is better described as a *risk metric* than a *risk measure* in the coherence sense (Wikipedia S112).

## Math / formulas

### Three estimation methods (CFA Institute 2026, S110)
1. **Parametric (variance–covariance / delta-normal).** Assumes returns are multivariate normal. For a portfolio with mean return *μ_P* and volatility *σ_P* over the horizon,
   $$
   \text{VaR}_\alpha = (z_\alpha\,\sigma_P - \mu_P)\,V, \qquad z_\alpha = \Phi^{-1}(\alpha)
$$
   where *V* is portfolio value and *Φ* is the standard-normal CDF. For short horizons *μ_P ≈ 0*, so VaR ≈ *z_α σ_P V*. Portfolio volatility comes from weights **w**: *σ_P = √(wᵀΣw)*.
   **Time scaling:** VaR scales with the square root of time, $\text{VaR}_T = \text{VaR}_1\sqrt{T}$ (Investopedia parametric method, S96-style).
2. **Historical simulation.** Use the empirical (1−α) quantile of actual historical (or current-holding) P/L observations — no distribution assumed, no parameters estimated. Only useful to the extent the future resembles the past (CFA S110).
3. **Monte Carlo.** Specify a stochastic process for returns, draw many scenarios, take the empirical quantile. Flexible but computationally heavy and dependent on the specified dynamics (CFA S110).

### CVaR closed form under normality
For normal returns, the expected shortfall has an exact expression:
$$
\text{CVaR}_\alpha = \left(\frac{\sigma_P\,\phi(z_\alpha)}{1-\alpha} - \mu_P\right) V,
\qquad \phi(z)=\frac{1}{\sqrt{2\pi}}e^{-z^2/2}.
$$

### Coherent risk measures (Artzner, Delbaen, Eber & Heath 1999, S111)
A risk measure *ρ* is **coherent** if it satisfies:
- **Monotonicity:** if *X ≤ Y* always, then *ρ(X) ≥ ρ(Y)* (better portfolio ⇒ less risk).
- **Subadditivity:** *ρ(X+Y) ≤ ρ(X)+ρ(Y)* — diversification never increases measured risk.
- **Positive homogeneity:** *ρ(hX) = h ρ(X)* for *h ≥ 0* — risk scales with position size.
- **Translation invariance:** *ρ(X + a) = ρ(X) − a* for deterministic *a* — cash reduces risk one-for-one.

Artzner et al. (S111) show **VaR violates subadditivity in general** (they explicitly "examine the consequences of using value at risk" and propose the *tail conditional expectation* as a coherent repair). **CVaR/ES is coherent** (Wikipedia S113, S114).

### Backtesting: Kupiec Proportion-of-Failures (POF) test (Kupiec 1995, S116; MetricGate S115)
Define the hit sequence $I_t = 1\{r_t < -\text{VaR}_t\}$. With *n* observations, *x* exceedances, estimated breach rate $\hat\pi = x/n$, and model tail probability *α*:
$$
\text{LR}_{\text{POF}} = -2\ln\frac{\alpha^{x}(1-\alpha)^{n-x}}{\hat\pi^{x}(1-\hat\pi)^{n-x}}
$$
Under H₀ (correct coverage), LR_POF ∼ χ²₁ (asymptotically). Small p-value ⇒ model **under**-estimates risk (too many breaches). **Basel traffic-light:** map cumulative binomial *P(X≤x | n,α)* to green (<0.95), yellow (0.95–0.9999), red (>0.9999) zones, driving capital multipliers (MetricGate S115). Regulators expect ≥250 daily observations (one trading year).

## Worked example / code
Pure standard-library Python (Python 3.14, **no third-party deps** — math/statistics/random). Reproduces a parametric VaR/CVaR, a historical-simulation check, and a Kupiec backtest. Data is synthetic Gaussian (seed 42 / 7) — **illustrative only, not a market claim**.

```python
import math, random, statistics

def norm_ppf(p):  # Acklam inverse-normal CDF (~1e-9)
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00]
    b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00]
    d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00]
    pl,ph=0.02425,1-0.02425
    if p<pl:
        q=math.sqrt(-2*math.log(p)); return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p<=ph:
        q=p-0.5; r=q*q; return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    else:
        q=math.sqrt(-2*math.log(1-p)); return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

def norm_cdf(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
def norm_pdf(z): return math.exp(-0.5*z*z)/math.sqrt(2*math.pi)
def chi2_1_sf(x): return 2*(1-norm_cdf(math.sqrt(x)))  # P(chi2_1 > x)

mu, sigma, V, conf = 0.0005, 0.01, 1_000_000.0, 0.95
z = norm_ppf(conf)                       # 1.64485
VaR_p = (z*sigma - mu)*V
CVaR_p = (sigma*norm_pdf(z)/(1-conf) - mu)*V
print(f"parametric  VaR_95% = ${VaR_p:,.0f}  CVaR_95% = ${CVaR_p:,.0f}")

random.seed(42)
rets=[random.gauss(mu,sigma) for _ in range(10000)]
q=sorted(rets)[int((1-conf)*len(rets))]
VaR_h=-q*V; CVaR_h=-statistics.mean([r for r in rets if r<=q])*V
print(f"historical   VaR_95% = ${VaR_h:,.0f}  CVaR_95% = ${CVaR_h:,.0f}")

random.seed(7); n,alpha=250,1-conf
rets=[random.gauss(mu,sigma) for _ in range(n)]
x=sum(1 for r in rets if r < -VaR_p/V); pi=x/n
LR=-2*math.log((alpha**x)*(1-alpha)**(n-x)/(pi**x)/(1-pi)**(n-x))
print(f"Kupiec POF: n={n} breaches={x} (exp {alpha*n:.0f}) LR={LR:.3f} p={chi2_1_sf(LR):.3f}")
```

**Verified output (this run):**
```
parametric  VaR_95% = $15,949  CVaR_95% = $20,127
historical   VaR_95% = $16,124  CVaR_95% = $20,101
Kupiec POF: n=250 breaches=18 (exp 12) LR=2.256 p=0.133  -> fail to reject
```
The parametric and historical estimates agree closely (both assume the same Gaussian data); CVaR is ~26% larger than VaR, i.e., the average tail loss is materially worse than the threshold. The Kupiec test fails to reject the model even though breaches (18) exceed the expected 12–13, illustrating the test's **low power** at one trading year of data.

## Assumptions & limitations
- **VaR is a quantile, not a worst case.** Losses beyond VaR can be arbitrarily large; VaR "marks the boundary between normal days and extreme events" (Wikipedia S112). A position can lose far more than VaR.
- **Distributional assumptions.** Parametric VaR is only as good as its normality assumption; it "provides a poor estimate of VaR when returns are not normally distributed, as might occur when a portfolio contains options" (CFA S110). Fat tails ⇒ severe under-estimation.
- **Non-subadditivity.** VaR generally fails subadditivity, so combining two desks can *increase* measured VaR, creating a perverse incentive to fragment risk and undermining diversification capital relief (Artzner et al. S111).
- **Estimation sensitivity.** VaR is "highly sensitive to numerous discretionary choices" — confidence level, horizon, estimation window, return vs P/L convention (CFA S110). Two analysts can report very different VaRs for the same book.
- **Liquidity & correlation risk.** Standard VaR "fails to account for the lack of liquidity and is sensitive to correlation risk" and "is vulnerable to trending or volatility regimes" (CFA S110).
- **Backtest limitations.** Kupiec only tests the *average* breach rate and assumes independent breaches; clustered breaches (volatility regimes) pass Kupiec yet are dangerous. Power is low when *n·α* is small (MetricGate S115). Historical simulation inherits **non-stationarity** and any look-ahead in the input data (ties to KB 05-stats-and-ml/08-backtesting-methodology/15-pitfalls).
- **CVaR is harder to backtest** because it requires actual exceedances to estimate the tail mean; with 250 days at 97.5% ES you expect only ~6 breaches.

## Empirical evidence
- **Industry standard.** VaR is "widely accepted by regulators" and used for risk management, control, financial reporting, and regulatory capital (Wikipedia S112; CFA S110).
- **Regulatory migration to ES.** The Basel Committee's **FRTB** (final standards Jan 2019) makes **Expected Shortfall replace Value at Risk** as the internal-models market-risk measure, explicitly "to capture tail risk events" that VaR missed (KPMG 2025, S117). SIFMA (2021, S118) lists "replace the VaR approach to risk measurement with a more comprehensive alternative known as Expected Shortfall (ES)" as a core FRTB objective; the standard IMA calibration is commonly cited as **97.5% ES** replacing the prior **99% 10-day VaR** (AnalystPrep/SIFMA-consistent summaries).
- **VaR under stress.** SIFMA (S118) notes VaR "performed poorly during periods of market volatility, such as those that occurred during the GFC … it did a poor job of capturing so-called 'tail risks'," motivating the ES shift.
- **Coherence is settled mathematics.** Artzner et al. (1999, S111) definitively established VaR's non-subadditivity and CVaR/ES's coherence — this is not contested among quants.

## Conflicting views
- **"VaR gives a false sense of safety."** Critics (e.g., Taleb-style) argue the single number is misread as a worst case and that the choice of parameters is arbitrary. Defenders (CFA S110) counter that its simplicity, communicability, cross-asset comparability, and backtestability are genuine strengths.
- **Is subadditivity even desirable?** The modelsandrisk.org note (Tier-2/3) questions whether theoretical subadditivity should be preferred when it may not match observed reality; the mainstream (Artzner, regulators) treats coherence as a requirement, which is *why* ES displaced VaR.
- **ES vs VaR as the better regulatory anchor.** Regulators chose ES for tail sensitivity, but ES's weaker backtestability and dependence on the tail model are real counter-arguments still debated in practitioner literature (KPMG S117 notes NMRF/punitive treatments remain challenging).
- **Confidence/horizon conventions.** 95% vs 99%, 1-day vs 10-day (√10 scaling) vs liquidity-horizon scaling under FRTB — these are policy choices, not truths, and change the number substantially.

## Common mistakes
1. **Calling VaR a "worst-case loss."** It is not — it is a threshold with a (1−α) chance of being exceeded, and exceedances can be catastrophic.
2. **Using normal VaR on option-heavy or crisis portfolios.** Underestimates tail risk; use historical/Monte Carlo or fat-tailed (Student-t / EVT) models.
3. **Assuming VaR adds across desks.** Because VaR is non-subadditive, do not sum desk VaRs for firm-wide capital without a consolidation that captures diversification (or use ES, which is subadditive).
4. **Not backtesting / mis-reading backtests.** A "green" Kupiec zone does not guarantee correctness; clustering and short samples hide errors (MetricGate S115).
5. **Sign/convention errors.** VaR reported as −0.025 vs +0.025 inverts breach counts (MetricGate S115).
6. **Survivorship / look-ahead in historical simulation.** Using biased or forward-looking data produces optimistic VaR (see KB 15-pitfalls-and-antipatterns).
7. **Treating the point estimate as precise.** VaR is "subjective … sensitive to discretionary choices" (CFA S110) — report it with its assumptions, not as a single god-number.

## Further reading (tiered)
- **Tier 1 (primary):** Artzner, Delbaen, Eber & Heath (1999), "Coherent Measures of Risk," *Mathematical Finance* 9(3):203–228 — https://people.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf
- **Tier 1 (primary):** Kupiec, P.H. (1995), "Techniques for Verifying the Accuracy of Risk Measurement Models," *Journal of Derivatives* 2(4):173–184 (DOI 10.3905/jod.1995.407942; Fed working paper 95-24) — https://econpapers.repec.org/RePEc:fip:fedgfe:95-24
- **Tier 1 (curriculum):** CFA Institute (2026), "Measuring and Managing Market Risk" (Level II refresher) — https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/measuring-managing-market-risk
- **Tier 1 (regulation):** Basel Committee, "Minimum capital requirements for market risk" (FRTB, BCBS d457) — https://www.bis.org/bcbs/publ/d457.pdf
- **Tier 2:** Rockafellar & Uryasev (2000/2002), "Optimization of Conditional Value-at-Risk" — https://www.ise.ufl.edu/uryasev/files/2011/11/CVaR1_JOR.pdf
- **Tier 2:** Acerbi & Tasche (2002), "On the Coherence of Expected Shortfall" — https://arxiv.org/abs/cond-mat/0104295
- **Tier 2:** KPMG (2025), "Fundamental Review of the Trading Book: An Overview" — https://assets.kpmg.com/content/dam/kpmgsites/in/pdf/2025/07/fundamental-review-of-the-trading-book-an-overview.pdf
- **Tier 2:** SIFMA (2021), "The Fundamental Review of the Trading Book (FRTB): An Introductory Guide" — https://www.sifma.org/news/blog/the-fundamental-review-of-the-trading-book-frtb-an-introductory-guide
- **Tier 2 (reference/backtest formulas):** MetricGate, "VaR Backtesting (Kupiec POF Test)" — https://metricgate.com/docs/var-backtesting-kupiec
- **Tier 2 (encyclopedic):** Wikipedia, "Value at risk" — https://en.wikipedia.org/wiki/Value_at_risk ; "Expected shortfall" — https://en.wikipedia.org/wiki/Expected_shortfall ; "Coherent risk measure" — https://en.wikipedia.org/wiki/Coherent_risk_measure
