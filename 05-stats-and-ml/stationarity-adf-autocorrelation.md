---
title: Stationarity, the Augmented Dickey–Fuller (ADF) Test, and Autocorrelation in Financial Time Series
topic_id: 05-stats-and-ml/stationarity-adf-autocorrelation
tags: [stationarity, unit-root, ADF, autocorrelation, ACF, Ljung-Box, volatility-clustering, ARCH, GARCH, stylized-facts]
last_updated: 2026-07-18
confidence: robust
sources: [S62, S63, S64, S65, S66, S67]
---

## TL;DR
- A series is **stationary** when its mean, variance, and autocovariance structure are stable over time. Most equity **price levels** are non-stationary (they contain a unit root / are integrated of order 1, I(1)); **log returns** are approximately stationary (I(0)).
- Test non-stationarity with the **Augmented Dickey–Fuller (ADF)** test: its null hypothesis is *"a unit root is present (non-stationary)"* — you reject only when the p-value is small. Pair it with **KPSS**, which has the opposite null, to avoid misclassification.
- **Autocorrelation**: daily equity returns show *little linear autocorrelation* (a core market stylized fact), but **squared/absolute returns** show *strong, slowly decaying autocorrelation* — this is **volatility clustering**, the empirical motivation for ARCH/GARCH models.
- Stationarity is a property of the *observed sample window*, not a guarantee about the future; it is a modeling convenience, not proof of tradability.

## Core explanation

### What "stationary" means
In plain terms, a stationary time series is one whose statistical behavior does not depend on *when* you observe it. If you shifted the series in time, its distribution would look the same. This matters because classical time-series models (ARIMA, GARCH), lagged-regression inference, and many ML pipelines assume relationships that are stable across time — an assumption violated by trends, changing variance, and shifting means.

There are two standard notions (S63; statsmodels notebook S67):
- **Strong (strict) stationarity:** the full finite-dimensional joint distribution is invariant to time shifts.
- **Weak (covariance / second-order) stationarity:** the mean is constant, the variance is finite and constant, and the autocovariance `Cov(X_t, X_{t-k})` depends only on the lag `k`, not on `t`. Most applied work uses weak stationarity.

### Why this is the central fact of equity data
Stock **prices** behave like a random walk with drift: `P_t = P_{t-1} + drift + shock`. Each shock永久ently changes the level, so the mean is undefined and variance grows with time → non-stationary, integrated I(1). Taking **log returns** `r_t = ln P_t − ln P_{t-1}` removes the level: the shock is now transitory, the series fluctuates around a roughly constant mean with bounded variance → approximately stationary, I(0). This is why essentially all quantitative equity work is done on returns, not prices.

### The ADF test, intuitively
A **unit root** is a root of the characteristic polynomial equal to 1; its presence makes a series non-stationary and makes naive trend/autoregressive models misbehave (spurious regressions, non-mean-reverting forecasts). The ADF test is a *unit-root test*: it fits an autoregressive model augmented with lagged differences to soak up serial correlation, then checks whether the coefficient on the lagged level is significantly negative of zero. **Null hypothesis: a unit root exists (series is non-stationary).** A small p-value lets you reject the null and call the series stationary (S62, S65).

### Autocorrelation, intuitively
The **autocorrelation function (ACF)** at lag `k` measures how much a series correlates with its own `k`-steps-ago value. **Ljung–Box** is a portmanteau test of whether *any* of the first `h` autocorrelations differ from zero (null: the data are independently distributed / i.i.d.). In equities, the empirical regularity is: raw returns ≈ uncorrelated (efficient-market stylized fact), but squared returns are strongly autocorrelated (volatility clusters — quiet periods and turbulent periods persist). This asymmetry is why we test *both* raw and squared returns (S63, S64).

## Math / formulas

**Weak stationarity conditions**
```
E[X_t]         = μ                (constant mean)
Var(X_t)       = γ(0) = σ² < ∞    (constant, finite variance)
Cov(X_t,X_{t-k}) = γ(k)           (depends only on lag k, not on t)
```

**ADF regression** (S62, S65):
```
Δy_t = α + β·t + γ·y_{t-1} + Σ_{i=1}^{p} φ_i·Δy_{t-i} + ε_t
```
- `Δy_t = y_t − y_{t-1}` (first difference).
- Null H₀: `γ = 0` (unit root → non-stationary). Alternative H₁: `γ < 0` (stationary).
- The test statistic is `γ̂ / SE(γ̂)`, but its distribution under H₀ is *non-standard* (Dickey–Fuller), so it is compared against special critical values (≈ −2.86 at 5% for the constant-only case), **not** a normal t-table. statsmodels computes an approximate MacKinnon p-value.
- `regression` controls deterministic terms: `'c'` (constant), `'ct'` (constant+trend), `'ctt'` (constant+quadratic trend), `'n'` (none). Wrong specification is a common error.

**Autocorrelation / ACF**
```
ρ(k) = γ(k) / γ(0) = Cov(X_t, X_{t-k}) / Var(X_t)
```

**Ljung–Box statistic** (S66):
```
Q = n(n+2) · Σ_{k=1}^{h} [ ρ̂(k)² / (n − k) ]   ~  χ²(h − model_df)  under H₀
```
- H₀: data are i.i.d. (no autocorrelation up to lag `h`).
- `model_df` subtracts degrees of freedom used by a fitted model (e.g., `p+q` for ARMA(p,q)); otherwise omitted (`model_df=0`).

**Volatility clustering → ARCH / GARCH** (S64; Engle 1982; Bollerslev 1986):
```
ARCH(1):   σ²_t = α_0 + α_1·ε²_{t-1}
GARCH(1,1): σ²_t = α_0 + α_1·ε²_{t-1} + β_1·σ²_{t-1}
```
A large recent squared shock `ε²_{t-1}` or large recent variance `σ²_{t-1}` inflates today's variance. **Persistence** `α_1 + β_1` near 1 (e.g., 0.99 in the Wilshire 5000 example, S64) means volatility stays elevated for a long time — the quantitative signature of clustering.

## Worked example / code

Self-contained, reproducible (seeded). Pinned: `numpy==1.26.4`, `pandas==2.2.3`, `scipy==1.13.1`, `statsmodels==0.14.4`. Data source: **synthetic** (random walk + Gaussian shocks) so it runs offline; for live data substitute `yfinance`/`pandas_datareader`/`Alpha Vantage` (see note below).

```python
# stationarity_adf_autocorr.py
# Pinned: numpy==1.26.4, pandas==2.2.3, scipy==1.13.1, statsmodels==0.14.4
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox

rng = np.random.default_rng(0)
n = 2000

# 1) Non-stationary LEVEL series: random walk with small drift  -> I(1)
noise  = rng.normal(0, 1, n)
price  = 100 + np.cumsum(noise) + 0.01 * np.arange(n)
logret = np.diff(np.log(price))                    # ~ stationary I(0)

def adf_report(name, x, regression='c'):
    res = adfuller(x, regression=regression, autolag='AIC')
    stat, pval, usedlag, nobs, crit = res[0], res[1], res[2], res[3], res[4]
    verdict = "STATIONARY (reject unit root)" if pval < 0.05 else \
              "NON-STATIONARY (fail to reject unit root)"
    print(f"[{name}] ADF={stat:.3f} p={pval:.4f} lags={usedlag} "
          f"crit(5%)={crit['5%']:.3f} -> {verdict}")

adf_report("price (level)",  price)    # expect NON-STATIONARY
adf_report("log return",     logret)   # expect STATIONARY

# 2) Autocorrelation: raw returns vs SQUARED returns (volatility clustering)
def lb_report(name, x, lags=20):
    out = acorr_ljungbox(x, lags=[lags], return_df=True)
    q, pv = out['lb_stat'].iloc[0], out['lb_pvalue'].iloc[0]
    print(f"[{name}] Ljung-Box Q({lags})={q:.2f} p={pv:.4f} -> "
          f"{'autocorrelation present' if pv < 0.05 else 'no autocorrelation (i.i.d.)'}")

lb_report("raw returns",           logret)        # expect ~i.i.d.
lb_report("squared returns",       logret**2)      # expect STRONG autocorrelation

# 3) Manual ACF of squared returns (stdlib-style, no extra deps)
def acf_manual(x, maxlag=10):
    x = x - x.mean()
    v0 = np.dot(x, x) / len(x)
    return [np.dot(x[:-k], x[k:]) / (len(x) - k) / v0 for k in range(1, maxlag + 1)]

print("ACF squared returns, lags 1..10:",
      [f"{a:.3f}" for a in acf_manual(logret**2, 10)])
```

**Expected output (verified):**
```
[price (level)] ADF=-1.349 p=0.6066 lags=0 crit(5%)=-2.863 -> NON-STATIONARY (fail to reject unit root)
[log return] ADF=-24.420 p=0.0000 lags=2 crit(5%)=-2.863 -> STATIONARY (reject unit root)
[raw returns] Ljung-Box Q(20)=23.07 p=0.2853 -> no autocorrelation (i.i.d.)
[squared returns] Ljung-Box Q(20)=244.36 p=0.0000 -> autocorrelation present
ACF squared returns, lags 1..10: ['0.044', '0.035', '0.127', '0.082', '0.031', '0.047', '0.028', '0.078', '0.027', '0.062']
```
The level fails to reject the unit root; log returns reject it; raw returns pass Ljung–Box (no linear autocorrelation) while squared returns fail it decisively (volatility clustering), exactly the stylized facts below.

**Live-data variant (data source pointer):** replace the synthetic block with, e.g.,
`import yfinance as yf; px = yf.download("SPY", start="2015-01-01")["Close"]; logret = np.log(px).diff().dropna().values`.
Always state the vendor, ticker, and date range; free tiers have rate limits and may contain splits/dividend adjustments that must be handled (use adjusted close).

## Assumptions & limitations
- **ADF has low power against near-unit-root processes.** When `γ` is close to but below 0, ADF frequently fails to reject the null, mislabeling a stationary-but-highly-persistent series as non-stationary (S62 notes the p-value is approximate near the boundary — prefer comparing the statistic to the printed critical values when p is marginal).
- **Lag/regression specification matters.** Choosing `'ct'` when there is no trend, or too few/many lags, changes the result. `autolag='AIC'` is a reasonable default but not infallible.
- **Structural breaks** (regime shifts, crises) induce apparent non-stationarity even in a "stationary-around-shift" series; ADF is not break-robust.
- **Stationarity describes the sample window only.** A series stationary over 2000 days need not stay so; non-stationarity is a recurring, time-varying property (regime dependence).
- **Stationary ≠ predictable.** White noise is stationary yet unforecastable. Passing ADF does not imply a profitable signal exists.
- **Ljung–Box on heavy-tailed returns:** its χ² reference is asymptotically justified; with fat tails and small `n` the p-values are approximate. Use it as a diagnostic, not a final arbiter.

## Empirical evidence
- **Cont (2001)** surveyed independent studies and codified the *stylized facts* of asset returns: (i) **weak or no linear autocorrelation in raw returns**, (ii) **strong, slowly decaying autocorrelation in absolute/squared returns** (volatility clustering), and (iii) non-Gaussian, fat-tailed marginal distributions (S63). These hold across many markets, instruments, and eras.
- **Wilshire 5000 daily returns** (econometrics-with-r, S64): the sample ACF of returns is near zero ("little autocorrelation … difficult to predict using an AR model"), while the series visibly clusters; a fitted **GARCH(1,1)** has persistence `α₁ + β₁ ≈ 0.99`, a direct quantitative confirmation of volatility clustering.
- **Efficient-market implication:** at the *daily* horizon, linear return predictability is largely absent (consistent across Cont 2001 and the Wilshire example). This is a robust, well-replicated finding — not folklore.
- **Nuance / horizon dependence:** the "no autocorrelation" fact is strongest at short (intraday–daily) horizons. At *multi-month* horizons, well-documented effects appear — short-horizon reversal (days–weeks) and momentum (6–12 months) — and at *very long* horizons mean-reversion in valuation multiples emerges. These do not contradict the daily-stylized-fact; they underscore that autocorrelation is horizon-dependent (S63 framework; see also strategy-catalog / 04-quant-and-factors entries).

## Conflicting views
- **The ADF null-reversal trap.** The most common mistake is treating a *large* p-value as "stationary." Because H₀ is *unit root present*, a large p-value means you **cannot reject non-stationarity** (S65 explicitly flags this as the standard analyst error). Decision rule: `p < 0.05` → stationary; `p ≥ 0.05` → non-stationary (or inconclusive).
- **ADF vs KPSS disagreement.** KPSS has the *opposite* null (process is trend-stationary) (S67). Possible outcomes: both say non-stationary → non-stationary; both say stationary → stationary; KPSS stationary + ADF non-stationary → **trend-stationary** (detrend); KPSS non-stationary + ADF stationary → **difference-stationary** (difference). Using only one test can misclassify trend- vs difference-stationarity.
- **"All models need stationarity."** Contested in ML circles: tree/boosting models are less sensitive to level non-stationarity than linear/ARIMA models, yet stable feature–target relationships still argue for stationarizing inputs. Treat as a modeling choice with trade-offs, not an absolute law.

## Common mistakes
1. **Reversing the ADF null** — concluding "stationary" from `p > 0.05`. (See Conflicting views.)
2. **Testing prices instead of returns** — price levels almost always fail ADF; that is expected, not informative. Test log returns.
3. **Single-test reliance** — running ADF alone and ignoring KPSS; use both to separate trend- vs difference-stationarity.
4. **Reading ADF p as a tradability certificate** — stationarity is a statistical property, not alpha.
5. **Testing only raw returns for autocorrelation** — the real signal in equities is in *squared/absolute* returns (volatility clustering); ignoring it misses the dominant dependence.
6. **Treating "stationary in-sample" as "stationary out-of-sample"** — regimes shift; re-test on rolling/expanding windows.
7. **Wrong `regression` spec or ignoring `model_df` in Ljung–Box** when applied to model residuals (understating dof biases the test).

## Further reading
**Tier 1 (authoritative / primary)**
- S63 — Cont, R. (2001), "Empirical properties of asset returns: stylized facts and statistical issues," *Quantitative Finance* 1(2):223–236. https://www.stat.rice.edu/~dobelman/courses/texts/stylized.cont.2001.pdf (canonical stylized-facts paper; also cites Engle 1982, Bollerslev 1986, Campbell–Lo–MacKinlay 1997).
- S62 — statsmodels, `adfuller` API reference (null hypothesis, return tuple, MacKinnon p-values). https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html
- S66 — statsmodels, `acorr_ljungbox` API reference (Ljung–Box statistic, `model_df`, i.i.d. null). https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html
- S67 — statsmodels, "Stationarity and detrending (ADF/KPSS)" notebook (KPSS opposite null; 4 outcome cases; differencing). https://www.statsmodels.org/stable/examples/notebooks/generated/stationarity_detrending_adf_kpss.html
- Engle, R. (1982), "Autoregressive Conditional Heteroskedasticity," *Econometrica* 50:987–1007; Bollerslev, T. (1986), "Generalized ARCH," *J. Econometrics* 31:307–327 (primary ARCH/GARCH sources, cited in S64).

**Tier 2 (reputable practitioner)**
- S65 — machinelearningplus, "Augmented Dickey Fuller Test" (ADF regression, the null-reversal warning). https://machinelearningplus.com/time-series/augmented-dickey-fuller-test
- S64 — *Introduction to Econometrics with R*, Ch. 16.4 "Volatility Clustering and ARCH/GARCH" (Wilshire 5000 worked GARCH(1,1)). https://www.econometrics-with-r.org/16.4-volatility-clustering-and-autoregressive-conditional-heteroskedasticity.html

**Leads / further (verify before asserting)**
- MITRE (2023), "Revisiting Cont's Stylized Facts for Modern Stock Markets" (arXiv:2311.07738) — replication of Cont's 11 facts on Dow-30 intraday data; useful secondary confirmation. https://arxiv.org/abs/2311.07738
- López de Prado, M., *Financial Machine Learning* (Cambridge, 2018) — emphasizes non-stationarity as a core reason ML underperforms in finance (background; consult primary for specifics).
