---
title: Regime Change & Non-Stationarity
topic_id: 15-pitfalls-and-antipatterns/regime-change-non-stationarity
tags: [non-stationarity, regime-change, concept-drift, structural-break, backtest-validity, walk-forward, fractional-differentiation]
last_updated: 2026-07-19
confidence: robust
sources: [S384, S385, S386, S387, S251, S215, S241, S380, S316, S319, S136]
---

## TL;DR
- Financial return series are **non-stationary**: their moments (mean, variance, correlations) and the coefficients of any predictive model drift, and occasionally jump. A backtest that fits one stable data-generating process (DGP) over the full sample will systematically **overstate live performance**.
- The remedy is not "use more history" — it is **regime-aware estimation** (walk-forward / rolling windows / shrinkage), **stationarity-preserving transforms** (fractional differentiation), and **explicit break tests** (Chow, CUSUM, Bai–Perron). These reduce the damage; they do not make non-stationarity disappear.
- This is not a theoretical footnote. Value-premium decay (Fama–French 2020), the Aug-2007 quant meltdown (Khandani & Lo 2010), and the broad out-of-sample failure of return predictors (Goyal–Welch / Campbell–Thompson 2008) are all manifestations of the same problem.

## Core explanation
**Plain language.** Markets change. The "rules" that printed money in 2003–2007 (momentum, statistical arbitrage) partly stopped working in 2008 and again in 2018. *Non-stationarity* means the probability distribution that produces tomorrow's returns is not the same as the one that produced last year's. *Regime change* is the discrete version — a sudden shift (a crash, an interest-rate regime change, a regulation). *Concept drift* is the continuous, gradual version. A backtest assumes tomorrow looks like the whole history; reality is that the history is a mix of different "tomorrows."

**Precise.** A process is (weakly) stationary when its first two moments are time-invariant. Prices are integrated I(1); raw returns are closer to I(0) but exhibit time-varying variance (GARCH effects) and time-varying higher moments. In practice "non-stationarity" means the parameters θ_t of your model p(y | x; θ_t) are themselves functions of time. Full-sample backtests estimate a single θ over the whole window and implicitly assume θ_{T+1} = θ; the live world delivers θ_{T+1} ≈ θ_{post-break} ≠ θ.

**Three-bucket labeling:**
- **ROBUST:** the phenomenon itself (markets are non-stationary; backtests that ignore it overstate live edge) — corroborated across primary theory and empirical record (S384, S387, S215, S241, S380).
- **EMERGING / CONTESTED:** which mitigations actually work net of cost (walk-forward, fractional differentiation, shrinkage, regime-switching models) — helpful but regime-dependent and never sufficient.
- **FOLKLORE:** "markets are stationary at long horizons, so a long-horizon backtest is safe"; "walk-forward fully fixes non-stationarity"; "a passing ADF test proves the series is safe to trade."

## Math / formulas
**Weak stationarity.** E[r_t] = μ, Var(r_t) = σ², Cov(r_t, r_{t−h}) = γ(h) — all independent of t.

**Structural break (Pesaran & Timmermann 2007, S384).** A single-break DGP:
  y_{t+1} = 𝟙{t ≤ T₁}·β₁′x_t + (1 − 𝟙{t ≤ T₁})·β₂′x_t + u_{t+1}
where β changes at break point T₁. The central result: when forecasting out-of-sample, it can be *optimal* to keep using **pre-break** data (trading off bias against lower variance) rather than discarding it — the naive "use only the post-break window" rule is not always best.

**Chow test for a known break date (MetricGate, S386).** Fit a pooled OLS over the full sample (RSSR) and two separate OLS fits pre/post break (RSSU = RSS_pre + RSS_post). The test statistic:
  F = [(RSSR − RSSU) / k] / [RSSU / (n − 2k)]  ~  F(k, n − 2k)
Reject H₀ (stable coefficients) for a large F. Requires a *specified* break date; switch to sup-F / Quandt–Andrews / Bai–Perron when the date is unknown.

**CUSUM test (Brown, Durbin & Evans 1975; cited in S384).** Cumulative sum of *recursive residuals* plotted against a boundary band — detects parameter instability when the break date is unknown. (Formal 5% boundary follows Brown–Durbin–Evans; the snippet below uses an illustrative ±2σ band and is a diagnostic, not a published critical value.)

**Bai–Perron (multiple unknown breaks).** Estimates the number and location of multiple breaks via sup-F statistics and dynamic programming (S319). Use when you expect several shifts, not one.

**Fractional differentiation (López de Prado, AFML Ch.5 via S385).** A fractional difference of order d:
  X̃_t = Σ_{k=0}^∞ ω_k X_{t−k},  ω_k = (−1)^k ∏_{i=0}^{k−1} (d − i)/k!
The minimum d* that makes X̃ stationary (passes ADF) quantifies how much memory must be removed. If d* < 1 the series had a unit root; if d* > 1 it was explosive (bubble-like). Crucially, 0 < d* ≪ 1 ("mildly non-stationary") means full integer differentiation (d = 1) *over-removes* memory and destroys the predictive signal.

## Worked example / code
Two self-contained, pure-stdlib (Python 3.14) snippets. **Data source: synthetic (clearly labeled)** — they demonstrate the *mechanism*, not a market claim.

**Snippet A — a fitted model breaks when its coefficient is non-stationary (sign flip).**
```python
import random

random.seed(42)
n_pre, n_post = 600, 400

def gen(beta, n, sd=1.0):
    xs, ys = [], []
    for _ in range(n):
        x = random.gauss(0, 1.0)
        y = beta * x + random.gauss(0, sd)
        xs.append(x); ys.append(y)
    return xs, ys

def ols(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    sxx = sum((xi-mx)**2 for xi in x)
    sxy = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
    b = sxy/sxx; a = my - b*mx
    sst = sum((yi-my)**2 for yi in y)
    ssr = sum((yi-(a+b*xi))**2 for xi, yi in zip(x, y))
    return a, b, 1 - ssr/sst

# Regime 1: y responds POSITIVELY to x. Regime 2: the loading FLIPS sign.
x1, y1 = gen(+0.5, n_pre)
x2, y2 = gen(-0.5, n_post)

a_pre, b_pre, r2_pre = ols(x1, y1)
def pnl(x, y, b):
    return sum((b*xi)*yi for xi, yi in zip(x, y))   # position = b*x

pnl_pre  = pnl(x1, y1, b_pre)
pnl_post = pnl(x2, y2, b_pre)
my2 = sum(y2)/len(y2)
ssr_post = sum((yi-(a_pre+b_pre*xi))**2 for xi, yi in zip(x2, y2))
sst_post = sum((yi-my2)**2 for yi in y2)
r2_oos = 1 - ssr_post/sst_post

print(f"pre-fit coeff b={b_pre:.3f}  (true pre-loading +0.5)")
print(f"in-sample R2={r2_pre:.3f}   OOS(post-break) R2={r2_oos:.3f}")
print(f"strategy P&L in-sample={pnl_pre:.1f}   OOS={pnl_post:.1f}")
```
Verified output (CPython 3.14.4, seed 42):
```
pre-fit coeff b=0.514  (true pre-loading +0.5)
in-sample R2=0.212   OOS(post-break) R2=-0.681
strategy P&L in-sample=160.0   OOS=-117.7
```
The model that "worked" in-sample (R²=0.21, +160 P&L) is **wrong-signed out-of-sample** (R²=−0.68, −117.7 P&L) the moment the loading flips. This is exactly what happened to many stat-arb factors in Aug-2007 (S241).

**Snippet B — full-sample OLS hides a time-varying coefficient.**
```python
import random

random.seed(7)
N = 1000
xs, ys = [], []
for t in range(N):
    x = random.gauss(0, 1.0)
    beta_t = 0.5 if t < 600 else -0.5     # one discrete break at t=600
    ys.append(beta_t * x + random.gauss(0, 1.0))
    xs.append(x)

def ols(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    sxx = sum((xi-mx)**2 for xi in x)
    sxy = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
    return my - (sxy/sxx)*mx, sxy/sxx

def roll_beta(x, y, win):
    out = []
    for i in range(win, len(x)+1):
        xi, yi = x[i-win:i], y[i-win:i]
        n = len(xi); mx = sum(xi)/n; my = sum(yi)/n
        sxx = sum((v-mx)**2 for v in xi)
        sxy = sum((v-mx)*(w-my) for v, w in zip(xi, yi))
        out.append(sxy/sxx)
    return out

_, fb = ols(xs, ys)
rb = roll_beta(xs, ys, 120)
print(f"full-sample beta={fb:.3f}   (spurious average of +0.5 and -0.5)")
print(f"rolling beta first={rb[0]:.3f}  mid={rb[300]:.3f}  last={rb[-1]:.3f}")
```
Verified output (seed 7):
```
full-sample beta=0.104   (spurious average of +0.5 and -0.5)
rolling beta first=0.398  mid=0.310  last=-0.534
```
The full-sample estimate (0.10) says "almost no relationship," while **every** local window shows |β|≈0.5 with opposite signs. A strategy calibrated on the full-sample coefficient would be calibrated on a relationship that exists in neither regime.

## Assumptions & limitations
- **Detection tests have low power near the break.** Chow needs a *known* date (S386); CUSUM/Bai–Perron need enough post-break observations — MetricGate recommends ≥ 10(k+1) per regime. A fresh break with little post-data is effectively invisible.
- **Stationarity is in-sample only.** Passing ADF on history does **not** certify future stationarity; it certifies the past.
- **Fractional differentiation reduces but does not eliminate non-stationarity**; d* is itself estimated with error and drifts.
- **Non-stationarity is managed, not fixed.** Even regime-aware models *lag* the new regime (estimation needs post-break data), so live drawdowns at transitions are unavoidable.
- **Costs and capacity are also regime-dependent** (slippage explodes in stress — see 08-backtesting-methodology, 09-market-microstructure), so a "stationarity-correct" backtest can still fail on the cost side.

## Empirical evidence
- **Regimes exist and matter for performance.** Ang & Bekaert (2011, S316) estimate a two-volatility-regime model on equity returns; the low-volatility regime carries a Sharpe of ~0.87 vs ~0.27 for the high-volatility regime, and the mean-variance frontier using regime timing dominates the unconditional one. Markov-switching variance recovers two distinct volatility states (S136).
- **Factor means shift.** Fama & French (2020, S215) show the U.S. value premium roughly *halved* after 2007 and cannot be statistically distinguished from zero out-of-sample given its volatility — a textbook non-stationary mean.
- **Crises are discrete breaks.** Khandani & Lo (2010, S241) document the Aug-2007 quant meltdown: many long/short statistical-arbitrage factors stopped working *simultaneously*, consistent with a regime/classical break compounded by crowding.
- **Return predictors fail out-of-sample.** Campbell & Thompson (2008) / Goyal & Welch (2008, S380) find most macroeconomic return predictors have *negative* out-of-sample R² — i.e., the historical "predictive" relationship does not survive the next regime.
- **Estimation-window theory.** Pesaran & Timmermann (2007, S384) prove that under breaks the optimal forecasting window is a bias–variance trade-off: discarding all pre-break data is often suboptimal, and pre-testing/forecast-combination across windows helps. Naive full-sample estimation is not optimal.

## Conflicting views
- **"Non-stationarity is the whole problem" (ML/stat-arb camp, López de Prado S251/S385)** vs **"valuations mean-revert, so long-horizon backtests are safe enough" (value-investing camp)**. The value-decay finding (S215) is real but cyclical, not proof that all long-horizon relations are unstable.
- **Walk-forward fixes it vs walk-forward still snoops.** Walk-forward (08-backtesting-methodology) reduces in-sample overfit but, if you re-optimize the window length or parameters on the same data, it re-introduces selection bias (05-stats-and-ml/overfitting-lookahead, 15-pitfalls/data-snooping).
- **Shrinkage vs ignore history.** Pesaran–Timmermann (S384) argue *keeping* some pre-break data (shrunk) can beat pure recency; practitioners often prefer pure recency for fast-moving factors. Both have regime-dependent merit.

## Common mistakes
1. **Assuming the full-sample mean/variance/correlation persists** into the live regime (the core trap; Snippet B shows it directly).
2. **One big in-sample fit = "the" model**, then deploying it unchanged.
3. **Treating a backtest spanning a mixed regime as representative of the live regime** — the historical average blends regimes you will not live through.
4. **Over-differencing (d = 1)** and destroying the memory that carries the signal (López de Prado, S385).
5. **Look-ahead via smoothed regime probabilities** — using *smoothed* (two-sided) Markov probabilities for live signals leaks future information (see 11-macro-and-regimes/regime-detection-methods).
6. **Believing a stationarity test "proves" tradeability** — ADF/KPSS describe the past.
7. **Ignoring that costs/capacity also shift by regime** — a stationarity-correct alpha can still die on execution.

## Further reading
- **[S384]** Pesaran, M.H. & Timmermann, A. (2006/2007), "Selection of Estimation Window in the Presence of Breaks." PDF: https://rady.ucsd.edu/_files/faculty-research/timmermann/estimation-window.pdf — Tier 1 (primary). Optimal forecasting window under structural breaks; bias–variance trade-off; cites Chow 1960, Brown–Durbin–Evans 1975, Bai–Perron.
- **[S385]** mlfinpy docs, "Fractionally Differentiated" (López de Prado, AFML Ch.5): https://mlfinpy.readthedocs.io/en/latest/FractionalDifferentiated.html — Tier 2. Fracdiff weights, d* = min stationary order, "most papers over-differentiate."
- **[S386]** MetricGate, "Chow Test for Structural Break": https://metricgate.com/docs/chow-test-structural-break — Tier 2. Chow F formula, known-date test, sup-F/Bai–Perron for unknown.
- **[S387]** Bailey, D.H., Borwein, J., Salehipour, A., López de Prado, M. & Zhu, Q. (2016), "Backtest overfitting in financial markets." PDF: https://www.davidhbailey.com/dhbpapers/overfit-tools-at.pdf — Tier 1 (primary). MinBTL: ≤45 variations on 5y daily data before SR≥1.0 by chance; multiple-testing fragility.
- **[S251]** López de Prado, M. (2018), "The 10 Reasons Most Machine Learning Funds Fail" (GARP). — Tier 1. Lists non-stationarity / feature decay as a top failure mode.
- **[S215]** Fama, E. & French, K. (2020), "The Value Premium." — Tier 1. Value-premium decay = non-stationary factor mean.
- **[S241]** Khandani, A. & Lo, A. (2010), "What Happened to the Quants in August 2007?" — Tier 1. Factor breakdown as regime break.
- **[S380]** Campbell, J. & Thompson, S. (2008) / Goyal, A. & Welch, I. (2008). — Tier 1. Out-of-sample predictor failure.
- **[S316]** Ang, A. & Bekaert, G. (2011), regime-switching volatility & allocation. — Tier 1.
- **[S319]** MetricGate, Bai–Perron multiple breakpoint test. — Tier 2.
- **[S136]** Hamilton, J. (1989), "A New Approach to the Economic Analysis of Nonstationary Time Series." — Tier 1.
- Books: López de Prado, *Advances in Financial Machine Learning* (Ch.5 fracdiff, Ch.7 cross-validation); Tsay, *Analysis of Financial Time Series* (structural breaks); Bai & Perron (2003) for multiple-break econometrics.
