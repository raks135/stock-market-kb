---
title: Cointegration and Pairs Trading
topic_id: 05-stats-and-ml/cointegration-pairs-trading
tags: [cointegration, engle-granger, johansen, pairs-trading, mean-reversion, statistical-arbitrage, stationarity, half-life, Ornstein-Uhlenbeck]
last_updated: 2026-07-18
confidence: contested
sources: [S243, S244, S245, S246, S247, S248, S249]
---

## TL;DR
- Two price series are **cointegrated** when each wanders randomly on its own (I(1)) but a fixed linear combination stays stationary (I(0)) — i.e. they share a long-run equilibrium and deviations mean-revert.
- The workhorse test is the **Engle–Granger two-step** (OLS cointegrating regression, then ADF on residuals with MacKinnon critical values); **Johansen** extends it to >2 assets via maximum likelihood.
- **Pairs trading** exploits this: long the cheap leg, short the rich leg when the spread z-score is extreme, exit on reversion. The original GGR (2006) rule earned ~11%/yr excess (1962–2002) and held up out-of-sample at ~10.4%/yr; recent replications (Zhu 2024, 2003–2023) show it has **decayed to ~6.2%/yr** and may be crowded out.
- Treat the live edge as **contested/folklore**: cointegration is estimated, not constant; transaction costs, shorting constraints, regime breaks, and look-ahead in pair selection are the usual killers.

## Core explanation
**Plain language.** Pick two stocks (or an ETF and its future) that historically move together. Their *prices* drift apart and together like drunks linked by a rubber band: each wanders, but the gap between them keeps snapping back to a stable average. Cointegration is the statistician's way of confirming the rubber band is real and not coincidence. Pairs trading is the trading recipe that bets on the snap-back.

**Precise.** Let \(y_{1,t}\) and \(y_{2,t}\) each be integrated of order 1, \(I(1)\) (their own levels are non-stationary random walks, but their first differences are stationary). They are **cointegrated of order (1,1)** if there exists a scalar \(\beta\neq 0\) such that the **spread** (cointegrating residual)

\[
z_t = y_{2,t} - \beta\, y_{1,t} \quad \text{is } I(0)\;\text{(stationary, mean-reverting)}.
\]

\(\beta\) is the **hedge ratio** (how many units of asset 1 to hold per unit of asset 2 so the combined position is market-neutral). The vector \((\beta,-1)\) is the **cointegrating vector**. The relationship can be written as an **error-correction model (ECM)**:

\[
\Delta y_{2,t} = \alpha + \gamma\, z_{t-1} + \sum \phi_i \Delta y_{2,t-i} + \varepsilon_t,
\]

where \(\gamma<0\) pulls \(y_{2,t}\) back toward the equilibrium defined by \(z_{t-1}\) — the mechanism pairs trading monetizes.

## Math / formulas

**1. Engle–Granger two-step test (S243, S246).**
- Step 1 — OLS cointegrating regression: \(\hat y_{2,t} = \hat c + \hat\beta\, y_{1,t} + \hat e_t\).
- Step 2 — Augmented Dickey–Fuller test on residuals \(\hat e_t\). **Null: no cointegration.** Critical values are *not* the usual ADF values — they are shifted (MacKinnon 1991/1994 surfaces), so use the test's own critical values. `statsmodels.tsa.stattools.coint` returns exactly this (null = no cointegration; p-value and 1/5/10% crit from MacKinnon).

**2. Half-life of mean reversion (S247).** Model the spread as a stationary AR(1):

\[
z_t = \phi\, z_{t-1} + \eta_t,\qquad \text{or in OU form } dz = \mu(\theta-z)\,dt + \sigma\,dW.
\]

Regress \(\Delta z_t\) on \(z_{t-1}\) (or on \(z_{t-1}-\theta\)): the slope is \(\lambda = -(1-e^{-\mu\Delta t})\approx -\mu\Delta t\). The **half-life** (time to close half the gap) is

\[
\text{HL} = \frac{\ln 2}{\mu} = \frac{-\ln 2}{\lambda}\quad (\Delta t = 1).
\]

Use HL to size holding periods: a common rule is to trade with a look-back ≈ HL.

**3. Johansen (multivariate).** For \(k>2\) series, test the cointegration *rank* of \(\Pi\) in a VAR via trace/max-eigenvalue statistics (MLE). Use when you need a portfolio of several assets or a unique cointegrating vector is not identified in the bivariate case (S246).

**4. Pairs-trading signal.** Form the normalized spread \(z\text{-score} = (z_t-\bar z)/\sigma_z\). Rule (distance / GGR style): open long-spread when \(z<-2\), short-spread when \(z>+2\), flatten near \(z\approx 0\) (S244, S249).

## Worked example / code

Synthetic, **illustrative only** — demonstrates the mechanics, *not* a market claim. Pinned: Python 3.14.4, numpy 2.5.1, statsmodels 0.14.6. Run with `PYTHONPATH=/path/to/.venv/lib/python3.14/site-packages` so the venv packages resolve.

```python
import numpy as np
from statsmodels.tsa.stattools import coint, adfuller

rng = np.random.default_rng(42)
n = 2000
y1 = np.cumsum(rng.standard_normal(n))          # I(1) common trend
u = np.zeros(n)
for t in range(1, n):                            # stationary AR(1) spread
    u[t] = 0.90 * u[t - 1] + rng.standard_normal()
y2 = 5.0 + 2.0 * y1 + u                          # y2 cointegrated with y1

# 1) Engle-Granger two-step cointegration test
coint_t, pval, crit = coint(y1, y2)              # crit is array [1%,5%,10%]
print("coint t=%.4f p=%.2g crit(1/5/10%%)=%.3f/%.3f/%.3f"
      % (coint_t, pval, crit[0], crit[1], crit[2]))

# 2) Hedge ratio via OLS slope
b_hat, c_hat = np.polyfit(y1, y2, 1)
spread = y2 - (b_hat * y1 + c_hat)
print("hedge ratio b_hat=%.4f (true 2.00)" % b_hat)

# 3) Is the spread stationary? ADF on residuals
adf_stat, adf_p, *_ = adfuller(spread, autolag='AIC')
print("ADF spread: stat=%.4f p=%.4f stationary=%s" % (adf_stat, adf_p, adf_p < 0.05))

# 4) Half-life of mean reversion
dS, Slag = np.diff(spread), spread[:-1]
lam = np.cov(dS, Slag, bias=True)[0, 1] / np.var(Slag)
print("lambda=%.4f half-life=%.2f periods" % (lam, -np.log(2) / lam))

# 5) Toy backtest on the SAME synthetic spread (mechanism demo only)
z = (spread - spread.mean()) / spread.std()
holding, pnl, trades = 0, 0.0, 0
for t in range(1, n):
    if holding == 0:
        if z[t-1] < -2 and z[t] >= -2: holding, trades = 1, trades+1
        elif z[t-1] > 2 and z[t] <= 2: holding, trades = -1, trades+1
    if holding != 0:
        pnl += holding * (z[t] - z[t-1])        # long spread profits as z rises
        if abs(z[t]) < 0.5: holding = 0
print("#trades=%d cumulative P&L (z-units)=%.2f" % (trades, pnl))
```

Verified output (seed 42):
```
coint t=-10.0462 p=1.9e-16 crit(1/5/10%)=-3.902/-3.339/-3.047
hedge ratio b_hat=2.0134 (true 2.00)
ADF spread: stat=-10.0512 p=0.0000 stationary=True
lambda=-0.0963 half-life=7.20 periods
#trades=25 cumulative P&L (z-units)=49.89
```
The strongly negative cointegration t-stat (well beyond the 1% critical value) and stationary ADF on the spread confirm cointegration; the half-life (~7 periods) matches the 0.90 AR(1) used to generate the spread; the toy backtest is positive *because the data was built to be mean-reverting* — that is the point to internalize, not a tradable return.

## Assumptions & limitations
- **Cointegration is estimated, not eternal.** The relationship is a sample statistic; it can break (a merger, a business-model change, a regime shift) — "cointegration is not a constant" (S248). Re-test out-of-sample; don't assume a 1995 cointegrating vector still binds in 2025.
- **Inputs must be I(1).** Testing cointegration on already-stationary series is meaningless; testing on levels that are actually I(2) gives spurious results. Pair with stationarity tests (see `05-stats-and-ml/stationarity-adf-autocorrelation`).
- **Low power in small samples / short windows**; the ADF-on-residuals test is known to over-reject no-cointegration with few observations (S246).
- **Hedge-ratio instability.** A single static \(\beta\) is a simplification; rolling/kalman estimates drift and add parameter risk.
- **Market frictions dominate.** Pairs trading needs *shorting* (often costly or unavailable) and tight execution; two-SD entry may not cover costs once the spread converges (S244, S249).
- **Capacity / crowding.** The edge shrinks as more capital crowds the same pairs (see decay evidence).

## Empirical evidence
- **Gatev, Goetzmann & Rouwenhorst (2006, RFS)** — the canonical study, daily US data 1962–2002, pairs formed by *minimum distance between normalized historical prices*, positions opened at a **2-standard-deviation** spread. Result: **average annualized excess returns up to ~11%** for top-pairs portfolios; **profits typically exceed conservative transaction-cost estimates**; a true out-of-sample holdout (1999–2002, parameters frozen) earned **10.4%/yr** (annual σ 3.8%, Newey–West t = 4.82). Bootstrap evidence suggested the effect is distinct from simple short-term reversal; returns linked to a common factor, not conventional risk measures (S244).
- **Zhu (2024, Yale)** — replicates GGR on 2003–2023 data: **~6.2% annual excess return, Sharpe 1.35**, i.e. roughly *half* the original magnitude, consistent with decay/crowding. Also finds the strategy's profit is increasingly exposed to the momentum factor (a +1σ momentum shock can nearly wipe out returns) and rises with the aggregate risk premium — supporting an "arbitrageurs are compensated for enforcing the Law of One Price" view. Notes **Rubesam (2021) argues the edge has disappeared** and **Chen et al. (2019) explains pairs profits via short-term reversal + industry momentum** rather than a separate risk factor (S245).
- **Krauss (2017, Journal of Economic Surveys)** — review establishing distance-based pairs trading as profitable across markets, asset classes and time frames, but with **declining profitability over time**; within-industry pairs perform best (Do & Faff 2010); cointegration is *one* selection method, not uniformly superior (S248).
- **Huck & Afawubo (2015)** / **Rad, Low & Faff (2015)** — method-comparison studies finding cointegration not reliably better than the simple distance method; copula-based variants often underperformed. (Referenced in S245/S248; flagged as corroborating leads — open the primaries before asserting magnitudes.)

## Conflicting views
- **Why does it work?** (a) *Risk-based* (GGR): pairs trading earns a premium for restoring the bivariate Law of One Price after shocks — an omitted, time-varying risk factor. (b) *Behavioral* (Engelberg, Gao & Jagannathan 2009; Jacobs & Weber 2015): profits come from investor inattention / under-reaction to common information, especially when divergence is caused by a common shock priced at different speeds. (c) *Factor explanation* (Chen et al. 2019): pairs profits are largely short-term reversal + industry momentum, not a distinct phenomenon. **Credible sources disagree on the cause; all agree the raw premium has shrunk.**
- **Best pair-selection method?** Distance (GGR) vs cointegration (Vidyamurthy 2004) vs copula vs ML — the literature gives **no unambiguous winner**; cointegration is theoretically cleaner but empirically not reliably better (S248, S249). Assert "cointegration is the superior method" only as folklore.
- **Is it still alive?** GGR's own OOS held; Zhu (2024) still finds a positive (smaller) edge; Rubesam (2021) contests that it works post-publication. Net: **contested, decaying, capacity-constrained**.

## Common mistakes
- Using **standard ADF critical values** on the cointegrating residual instead of the MacKinnon cointegration-specific surfaces (S243, S246).
- Declaring cointegration from an in-sample fit and **never re-testing** — the band snaps, the stat doesn't.
- **Look-ahead in pair selection**: choosing pairs because they "obviously" co-moved using the *whole* history, then backtesting on that same history (data snooping — see `15-pitfalls-and-antipatterns/data-snooping-phacking`).
- Ignoring **transaction costs and short-sale constraints** — the single most common reason a beautifully mean-reverting backtest dies in live trading (S249).
- Treating **z-score thresholds as universal**; calibrate entry/exit to the estimated half-life and cost structure, not to a fixed ±2.
- **Survivorship / point-in-time bias**: building pairs from currently-listed names excludes delisted firms and bakes in hindsight (see `13-data-and-tooling` and `15-pitfalls-and-antipatterns`).
- Over-reading the synthetic demo above as a return estimate — it is a mechanism illustration only.

## Further reading
- **Tier 1:** Engle, R.F. & Granger, C.W.J. (1987), "Co-integration and Error Correction: Representation, Estimation and Testing," *Econometrica* 55(2):251–276 (DOI 10.2307/1913236) — foundational primary; operational mechanics corroborated here via S243 + S246. Gatev, E., Goetzmann, W.N. & Rouwenhorst, K.G. (2006), "Pairs Trading: Performance of a Relative-Value Arbitrage Rule," *RFS* 19(3):797–827 (open-access PDF at stat.wharton.upenn.edu).
- **Tier 2:** statsmodels `coint` docs (S243); martinsewell.com cointegration primer (S246); arbitragelab Ornstein–Uhlenbeck documentation (S247); Krauss, C. (2017), "Statistical Arbitrage Pairs Trading Strategies: Review and Outlook," *Journal of Economic Surveys* 31:513–545 (S248); Zhu, X. (2024), "Examining Pairs Trading Profitability," Yale (S245); Vidyamurthy, G. (2004), *Pairs Trading: Quantitative Methods and Analysis*; Johansen, S. (1991), "Estimation and Hypothesis Testing of Cointegration Vectors…," *Econometrica* 59:1551.
- **Tier 3 (leads only):** arxiv:2412.12458 (OU applied to pairs trading; coursework/educational, no transaction costs — S249); Huck & Afawubo (2015), Rad/Low/Faff (2015) for method comparisons (verify primaries before asserting).
