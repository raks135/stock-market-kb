---
title: CAPM and Beta — Expected Return from Systematic Risk
topic_id: 04-quant-and-factors/capm-beta
tags: [capm, beta, cost-of-equity, systematic-risk, security-market-line, factor-models]
last_updated: 2026-07-18
confidence: contested
sources: [S96, S97, S98, S99, S100, S101, S102, S54]
---

## TL;DR
- CAPM prices an asset by one number — **beta (β)**, its sensitivity to the market portfolio: `E(Rᵢ) = R_f + βᵢ·(E(R_m) − R_f)`.
- Beta is a **robust, measurable** quantity (regress excess asset returns on excess market returns), but the claim that *beta alone* explains the cross-section of expected returns is **contested and largely rejected** by post-1992 evidence.
- In practice CAPM is still the default way to estimate the **cost of equity** (it feeds WACC in DCF — see 02-valuation/dcf.md and source S54), even though academics prefer multi-factor models (Fama–French) for explaining returns.
- Three-bucket label: **mechanics & beta estimate = robust**; **"beta explains cross-sectional returns" = contested/folklore**; **"CAPM dead in practice" = emerging (it survives as a cost-of-capital convention)**.

## Core explanation
Plain language: every stock moves partly with the whole market and partly on its own. CAPM says you should only be paid for the *market* part (systematic risk), because you can diversify the *own* part (idiosyncratic risk) away for free. The price of market risk is the **equity risk premium** (market return minus the risk-free rate). Beta scales that premium to the stock.

Precise: under mean-variance optimization with homogeneous expectations and frictionless markets, the market portfolio is mean-variance efficient, and any asset's expected excess return is linear in its covariance with the market. The intercept is zero (no alpha) and the slope coefficient is beta. This is the **Security Market Line (SML)**. Assets above the SML are "undervalued" (expected return > required), those below are "overvalued."

Beta itself (`βᵢ = Cov(Rᵢ, R_m) / Var(R_m)`) is the asset's **systematic-risk loading**. β = 1 means it moves one-for-one with the market; β > 1 is more volatile/risky; β < 1 is defensive. Beta is estimable from historical data and is the single most-used risk statistic in practitioner finance (Damodaran publishes sector betas annually — S98).

## Math / formulas
**CAPM (SML):**
```
E(Rᵢ) = R_f + βᵢ · [E(R_m) − R_f]
```
where `E(R_m) − R_f` is the **equity risk premium (ERP)**.

**Beta (OLS regression of excess returns):**
```
βᵢ = Cov(Rᵢ − R_f, R_m − R_f) / Var(R_m − R_f)
αᵢ = mean(Rᵢ − R_f) − βᵢ · mean(R_m − R_f)   # Jensen's alpha
```
A statistically significant positive α means the asset earned more than CAPM predicts (an "anomaly" vs the model).

**Levered (equity) vs unlevered (asset) beta** — to compare firms of different leverage or build a "bottom-up" beta (Damodaran, S98):
```
β_unlevered = β_levered / [ 1 + (1 − t) · (D / E) ]      # Hamada-style
β_levered   = β_unlevered · [ 1 + (1 − t) · (D / E) ]
```
Bottom-up beta = value-weighted average of the unlevered betas of the firm's businesses, then re-levered at the firm's target D/E. This is more stable than a single stock's historical beta.

**Blume (1971) adjusted beta** — raw OLS betas are unstable and **revert toward 1** over time (Blume 1971; Levy 1971; see S101/S102). Practitioners shrink the estimate:
```
β_Blume ≈ (2/3) · β_raw + (1/3) · 1.0
```
(Exact coefficients are empirical estimates that vary; the shrinkage *direction* — toward the market mean of 1 — is the robust part. Bloomberg and many vendors report Blume-adjusted betas.)

## Worked example / code
Pure standard-library Python (no third-party deps, fully reproducible). The returns are **synthetic/illustrative** (seeded LCG + Box–Muller), *not* market data — the point is to show the mechanics.

```python
import math

def rng(seed=42):
    state = seed
    while True:
        state = (state * 1103515245 + 12345) % 2147483647
        yield state / 2147483647.0

def normal(gen):
    u1 = next(gen); u2 = next(gen)
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

n = 120
gen = rng(42)
mkt_ex = [0.008 + 0.04 * normal(gen) for _ in range(n)]      # market excess return
asset_ex = [1.2 * m + 0.02 * normal(gen) for m in mkt_ex]    # true beta = 1.2

def mean(xs): return sum(xs) / len(xs)
def var(xs):
    mx = mean(xs); return sum((x - mx) ** 2 for x in xs) / (len(xs) - 1)
def cov(xs, ys):
    mx = mean(xs); my = mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)

beta = cov(asset_ex, mkt_ex) / var(mkt_ex)
alpha = mean(asset_ex) - beta * mean(mkt_ex)
Rf, ERP = 0.04 / 12, 0.06
E_R = Rf * 12 + beta * ERP
beta_blume = (2.0 / 3.0) * beta + (1.0 / 3.0)
print("beta(OLS)=%.4f alpha=%.6f CAPM_annual=%.4f Blume=%.4f" % (beta, alpha, E_R, beta_blume))
```

Output (deterministic):
```
beta(OLS)=1.2425 alpha=-0.003296 CAPM_annual=0.1145 Blume=1.1616
```
The OLS recovers ~1.24 (close to the planted 1.2; sampling error from n=120), alpha is near zero, CAPM cost of equity ≈ 11.45% at R_f=4% and ERP=6%, and the Blume shrink pulls the extreme beta toward 1.0 (1.24 → 1.16).

To run on **real** data, replace the synthetic blocks with excess returns from a source such as `yfinance` (e.g. `R_m` = SPY minus T-bill, `Rᵢ` = a stock minus T-bill) — but always use **point-in-time** total returns and a `R_f` matched in maturity/period (see 15-pitfalls survivorship & look-ahead articles for data hygiene).

## Assumptions & limitations
CAPM's derivation rests on (standard textbook / CFA reading, S97):
1. Investors are rational, risk-averse, mean-variance optimizers.
2. Homogeneous expectations (everyone agrees on the same distribution).
3. A single risk-free rate, known and constant; unlimited borrowing/lending at it.
4. No taxes, no transaction costs, all assets infinitely divisible and tradable.
5. All relevant information is instantly reflected in prices (efficient markets).

When these break (they always do in reality, S96), the SML can be misspecified. Key failure modes:
- **Proxy problem**: the "market" is unobservable. Tests use the S&P 500 or similar, which is not the true market portfolio (see Roll's critique below).
- **Beta instability**: raw betas drift with the estimation window, regime, and leverage changes; Blume/shrinkage only partially fixes this.
- **Non-stationarity**: a beta estimated in one regime (e.g. low-vol bull market) need not hold in the next.
- **Costs & capacity**: CAPM gives an expected return, not net-of-cost tradable alpha; transaction costs (08-backtesting-methodology) erode any apparent edge.
- **Single-factor only**: by construction it cannot explain size, value, profitability, or investment patterns — which is exactly where the cross-sectional action is.

## Empirical evidence
- **Time-series (market factor is real):** the excess market return carries a positive, persistent premium; the market factor survives in every later multi-factor model (Fama–French 3/5 factor). This part of CAPM is **robust**.
- **Cross-section (beta alone fails):** Fama & French (1992, S100, abstract) find that *"size and book-to-market equity combine to capture the cross-sectional variation in average stock returns associated with market beta, size, leverage, BE/ME, and E/P,"* and that *"when tests allow for variation in beta unrelated to size, the relation between market beta and average return is flat, even when beta is the only explanatory variable."* Investopedia (S96) independently reports the same: F&F found differing betas did **not** explain cross-sectional performance, and the linear beta–return link breaks down over shorter periods.
- **Beta decay / reversion:** raw betas over-predict for extreme names and revert toward 1 (Blume 1971; Levy 1971; S101/S102). Shrinkage improves forecast quality.
- **Still used in practice:** despite the academic critique, CAPM remains the dominant cost-of-equity input in WACC/DCF (S54, S97) and in regulator/utility rate cases — a convention, not a proven description of expected returns.

Strength of evidence: the *flat cross-sectional beta* result is **strong and replicated** (thousands of citations); the *practical usefulness as a cost-of-capital number* is **conventional/empirically weak but pervasive**.

## Conflicting views
- **"CAPM is dead" vs "CAPM is alive":** Academics (post F&F 1992) largely reject the cross-sectional CAPM; practitioners (and CFA curriculum, S97) still teach and use it — mainly as a cost-of-equity building block, not as a return-forecasting truth. Both are correct in their domains.
- **Roll's critique (S99, Roll 1977 JFE 4(2):129–176):** two statements — (1) *mean-variance tautology*: any mean-variance-efficient portfolio satisfies the CAPM equation exactly, so testing CAPM against a proxy is really just testing whether that proxy is mean-variance efficient; (2) *the true market portfolio is unobservable* (it would include every asset — real estate, stamps, private business). Therefore the CAPM can never be definitively tested. Many interpret Roll as merely "the market portfolio is unobservable," but the tautology point is deeper. Implication: a failed CAPM test may reflect a bad *proxy*, not a wrong *theory*.
- **Time-series vs cross-section confusion:** CAPM "works" in the time series (market premium is real) but "fails" in the cross-section (beta doesn't price assets alone). Conflicting claims usually talk past each other on this distinction.
- **ERP input is a free parameter:** CAPM is only as good as your `R_f` and ERP. Reasonable ERP assumptions range ~4–6% (Damodaran) and dominate the output — a hidden degree of freedom that makes CAPM "calibratable" to almost any answer.

## Common mistakes
- **Treating beta as a stable constant.** It is a noisy, regime-dependent estimate; always report the estimation window, frequency, and whether it's Blume-adjusted.
- **Using price volatility as "risk."** CAPM beta measures *covariance with the market*, not total variance; a low-beta stock can be highly volatile on its own (idiosyncratic) without raising required return under the model.
- **Mismatched `R_f` / ERP.** Mixing a 3-month T-bill `R_f` with an annual ERP, or a nominal ERP with real cash flows, silently breaks the equation.
- **Levered/unlevered confusion.** Comparing a high-debt firm's equity beta to an all-equity peer without unlevering/re-levering conflates financial and business risk.
- **Assuming alpha = skill.** A positive historical α can be luck, survivorship, or look-ahead (15-pitfalls); it is not a durable edge.
- **Believing CAPM predicts individual stock returns.** It is a *cross-sectional* pricing relation under strict assumptions; out-of-sample single-name return prediction is weak (see 05-stats-and-ml, 14-strategy-catalog).

## Further reading
- **Tier 1 (primary / authoritative):**
  - Sharpe, W.F. (1964), "Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk," *Journal of Finance*.
  - Lintner, J. (1965), "The Valuation of Risk Assets…," *Review of Economics and Statistics*.
  - Fama, E. & French, K. (1992), "The Cross-Section of Expected Stock Returns," *JF* 47(2):427–65 — https://econpapers.repec.org/article/blajfinan/v_3a47_3ay_3a1992_3ai_3a2_3ap_3a427-65.htm (S100).
  - Roll, R. (1977), "A Critique of the Asset Pricing Theory's Tests," *JFE* 4(2):129–176 — summarized at https://en.wikipedia.org/wiki/Roll%27s_critique (S99).
  - CFA Institute (2026), "Portfolio Risk and Return: Part II" (CAPM/SML reading) — https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-risk-return-part-2 (S97).
  - Damodaran, A., "Betas by Sector (US)," NYU Stern (updated Jan 2026) — https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html (S98).
- **Tier 2 (practitioner):**
  - Investopedia, "Capital Asset Pricing Model (CAPM)" — https://www.investopedia.com/terms/c/capm.asp (S96).
  - Damodaran, NYU Stern session slides on bottom-up / levered betas — https://pages.stern.nyu.edu/~adamodar/pdfiles/valonlineslides/session5.pdf.
  - Prajapati (MPRA 2012), "Empirical Analysis of the Forecast Error Impact of Classical and Bayesian Beta Adjustment Techniques" — https://mpra.ub.uni-muenchen.de/37662/ (S102).
- **Tier 3 (formula only, corroborate elsewhere):**
  - Folio Lab, "Blume Adjusted Beta" — https://www.foliolab.ai/docs/metrics/blume-adjusted-beta (S101).
- **Cross-links in this KB:** 02-valuation/dcf.md (CAPM → WACC cost of equity), 05-stats-and-ml (stationarity, overfitting), 08-backtesting-methodology (costs, deflated Sharpe), 15-pitfalls-and-antipatterns (survivorship, look-ahead, data snooping), and the 04 follow-on articles on Fama–French factors and factor timing.
