---
title: Feature Engineering & ML Pitfalls in Finance
topic_id: 05-stats-and-ml/feature-engineering-ml-pitfalls
tags: [machine-learning, feature-engineering, leakage, fractional-differentiation, cross-validation, non-stationarity, overfitting]
last_updated: 2026-07-18
confidence: contested
sources: [S250, S251, S252, S253, S72, S68, S80, S62, S67]
---

## TL;DR
- In financial ML the *features and labels* usually matter more than the choice of algorithm; raw prices are poor inputs and raw returns barely predict (low signal-to-noise).
- The recurring failure modes are **not** "the model is too simple" but **leakage** (label/feature information from the future), **non-stationarity** (features decay), **wrong cross-validation** (standard k-fold leaks on time series), and **research-through-backtesting** (tuning until a backtest looks good).
- Discipline beats algorithms: use path-dependent labeling (triple-barrier), purged/embargoed CV, fractional differentiation to preserve memory while gaining stationarity, and *feature-importance analysis* as the research tool rather than the backtest.
- These pitfalls compound the overfitting/data-snooping problems covered in `05-stats-and-ml/overfitting-lookahead.md` and `08-backtesting-methodology/deflated-sharpe-multiple-testing.md`. A clean backtest still does not imply a future edge.

## Core explanation
Feature engineering is the process of transforming raw market, fundamental, and alternative data into predictive variables (features) and outcomes (labels) for a supervised model. In trading, "models struggle to extract stable predictive structure from raw prices alone" (S252) — prices are integrated (I(1)) and dominated by unforecastable news, so the value is in *derived* variables: volatility, momentum, liquidity, valuation spreads, and microstructure signatures.

Why feature engineering is the crux:
- **Low signal-to-noise.** Expected returns are hard to measure; most variation is noise (S250). A feature that captures even a small stable structure beats a fancy model fed with raw prices.
- **Non-stationarity.** The data-generating process shifts (regimes, microstructure changes, competitor arbitrage). A feature that worked in 2010 may be gone by 2020.
- **Leakage is easy and fatal.** Financial labels are *path-dependent* (a trade opened at t is marked by the price path until exit). If any feature, label, or CV fold borrows information from the future, the model "predicts" perfectly and fails live.

López de Prado (S251) lists ten reasons ML funds fail; the directly feature/label/CV-related ones are: **chronological (time-bar) sampling** → use the volume clock; **integer differentiation** → use fractional differentiation; **fixed-time-horizon labeling** → use the triple-barrier method; **learning side and size simultaneously** → use meta-labeling; **cross-validation leakage** → use purging and embargoing; **walk-forward backtesting** → use combinatorial purged CV; and the overarching **research-through-backtesting** → use feature-importance analysis.

## Math / formulas

**Labeling — triple-barrier method (S251 #5; S252 §3).** For each observation at time t, define three barriers:
- a horizontal profit-take at `p_t · (1 + h)`,
- a horizontal stop-loss at `p_t · (1 - h)`,
- a vertical expiration at `t + Δt`.
The label is `y = +1` if the profit-take is hit first, `y = -1` if the stop-loss is hit first, and `y = sign(r_{t+Δt})` (or 0) if expiration is reached first. This respects the *path*, unlike a fixed-horizon sign label `y = sign(r_{t+h})` (S252).

**Meta-labeling (S251 #6).** Train a primary model for the *side* (high recall), then a secondary model on `{(X, 1_{primary correct})}` to decide *whether* to bet and size it — separating direction from timing/sizing.

**Fractional differentiation (S251 #4; S252 §5).** The backshift operator `B` gives integer difference `(1-B)X_t = X_t - X_{t-1}`. The fractional weight uses the binomial expansion
`(1-B)^d = Σ_{k≥0} (d choose k)(-B)^k`, with weights `w_0 = 1`, `w_k = -w_{k-1}(d-k+1)/k`.
A feature `f_t = Σ_k w_k X_{t-k}` is *stationary* for `0 < d < 1` while **retaining memory** (S252). This trades off the stationarity required by most predictors against the memory destroyed by full `d=1` differencing.

**Purged & embargoed CV (S251 #8; S252 §7; S253).** In standard k-fold, a training point whose *event window* (the price path from trade time to exit time) overlaps a test point's window leaks future information into training. *Purging* removes training observations whose labels overlap test labels; *embargoing* drops the `L` periods after a test fold when a feature needs an `L`-day lookback (e.g., a 63-day realized-volatility feature requires embargoing the first ~63 days of the following fold — S253). Combinatorial purged CV (CPCV) builds `binom(N,k)` train/test splits to synthesize many backtest paths (S252 §12; S253).

**Feature importance (S252 §8).** Mean Decrease in Impurity (MDI, tree-only, penalizes collinear features), Mean Decrease in Accuracy (MDA, permutation-based OOS, any classifier), Single Feature Importance (SFI), and a PCA sanity check via weighted Kendall-τ against MDI/SFI.

## Worked example / code
Data source: **synthetic** daily returns (i.i.d. normal, μ=0, σ=1%, Box–Muller via `random.gauss`, seed 42). Deliberately null — it demonstrates the *leakage mechanism*, not a market claim. Pure standard library (no numpy/sklearn needed); runs on Python 3.11+.

```python
import random, math, statistics
random.seed(42)

# synthetic returns + price path (random walk, NULL market data)
N = 4000
rets = [random.gauss(0.0, 0.01) for _ in range(N)]
prices = []
c = 100.0
for r in rets:
    c *= (1.0 + r); prices.append(c)

# Label at t = sign of NEXT-day return r[t+1]  (what we want to predict)
# "Leaky" feature z_t = r[t+1]  (NOT knowable at t -> target leakage)
# "Honest" feature x_t = r[t]    (contemporaneous, knowable at t)
labels, leaky, honest = [], [], []
for t in range(N - 1):
    labels.append(1 if rets[t + 1] > 0 else -1)
    leaky.append(rets[t + 1]); honest.append(rets[t])

def acc(feat):
    return sum(1 for i in range(len(labels))
               if (1 if feat[i] > 0 else -1) == labels[i]) / len(labels)

def acc_shuf(feat, frac=0.3, seed=7):
    rng = random.Random(seed); idx = list(range(len(labels))); rng.shuffle(idx)
    test = idx[:int(len(idx)*frac)]
    return sum(1 for i in test if (1 if feat[i] > 0 else -1) == labels[i]) / len(test)

print("leaky  acc full/shuffle:", round(acc(leaky),4), round(acc_shuf(leaky),4))
print("honest acc full/shuffle:", round(acc(honest),4), round(acc_shuf(honest),4))

# Fractional differentiation: stationarity vs memory trade-off
def fracdiff(d, x, L=120):
    w = [1.0]
    for k in range(1, L): w.append(-w[-1]*(d-k+1)/k)
    return [sum(w[k]*x[t-k] for k in range(min(t+1, L))) for t in range(len(x))]

def acf1(x):
    m = statistics.mean(x); xc = [v-m for v in x]
    num = sum(xc[i]*xc[i-1] for i in range(1, len(xc)))
    return num / sum(v*v for v in xc)

for d in [0.0, 0.5, 1.0]:
    f = fracdiff(d, prices)
    print(f"d={d:<3} std={statistics.pstdev(f):.3f} ACF(1)={acf1(f):.4f}")
```

Verified output (this repo, Python 3.14.4):
```
leaky  acc full/shuffle: 1.0 1.0          # leakage survives shuffled CV!
honest acc full/shuffle: 0.5019 0.5046    # no signal, as expected for i.i.d. returns
d=0.0  std=21.669 ACF(1)=0.9991           # price: non-stationary, full memory
d=0.5  std=2.638  ACF(1)=0.7222           # partial memory retained
d=1.0  std=1.787  ACF(1)=-0.0022          # returns: stationary, no memory
```
**Read-out:** (A) the leaky feature scores 100% *even after a shuffled train/test split* — because the leakage is per-row (z_t literally contains the label's sign), so ordinary CV cannot detect it. This is why "backtesting/shuffled-CV looks great" is not evidence. (B) `d=0` (price) is non-stationary (ACF≈1); `d=1` (returns) is stationary but throws away all memory; an intermediate `d≈0.5` keeps most of the series while cutting autocorrelation — the fractional-differentiation idea in practice. A formal ADF/KPSS check is in `05-stats-and-ml/stationarity-adf-autocorrelation.md`.

## Assumptions & limitations
- **Stationarity is assumed, never guaranteed.** Most predictors want stationary inputs; fractional differentiation only *approximates* it and the optimal `d` itself drifts (S251 #4; S252 §5, §17 structural breaks).
- **Labels are path- and assumption-dependent.** Triple-barrier results change with the choice of `h` (profit/stop widths) and `Δt`; meta-labels inherit primary-model error.
- **Feature importance is relative, not causal.** MDI/MDA are corrupted by collinearity (mitigate with PCA); importance ≠ a tradable edge (S252 §8).
- **Sample size.** With hundreds of candidate characteristics (Green, Hand & Zhang count ~330 stock-level predictors; Harvey, Liu & Zhu study 316 "factors" — both cited in S250), traditional methods break down as `P → N`; ML helps via regularization but needs large `N` and is still subject to the factor-zoo / multiple-testing critique (see S72 and `15-pitfalls-and-antipatterns/data-snooping-phacking.md`).
- **Leakage is structural in finance.** Event-time vs trade-time overlap, backfilled fundamentals, and long-lookback features all leak unless explicitly purged/embargoed (S251 #8; S253).

## Empirical evidence
- **ML can add value (S250, Tier 1).** Gu, Kelly & Xiu (2020) compare methods on the canonical equity risk-premium problem (cross-section and time series). A neural-network market-timing strategy earns an **out-of-sample Sharpe of 0.77 vs 0.51 for buy-and-hold**; a value-weighted long–short decile strategy using NN forecasts earns an **OOS Sharpe of 1.35, more than doubling** a leading regression-based strategy. All methods agree the dominant predictive signals are **momentum, liquidity, and volatility** variations. The gains are attributed to nonlinear predictor interactions missed by linear regressions.
- **But ML funds mostly fail (S251, Tier 1).** López de Prado argues the failures are methodological (the ten pitfalls above), not algorithmic — e.g., it takes roughly **20 backtest iterations to "discover" a false strategy** at a 5% false-positive rate, which the ASA flags as scientific misconduct.
- **Strength of evidence:** the *existence* of ML predictability OOS is robust (replicated across methods and asset classes in S250); the *magnitude and persistence* of any single edge is contested and regime-dependent. Backtests ≠ future (see `08-backtesting-methodology/deflated-sharpe-multiple-testing.md`).

## Conflicting views
- **"ML works / beats classical methods"** (S250) vs **"most ML funds fail / it's overfitting"** (S251). Reconciliation: the *method* can work, but success is driven by **process discipline** (meta-strategy pipeline, feature-importance research, purged CV, deflated statistics) rather than the algorithm. A lone quant iterating on a backtest reproduces Pitfall #1/#2.
- **Trees/networks vs linear models.** S250 shows trees and neural nets win on OOS R²; traditionalists note linear models are interpretable, cheaper, and less prone to spurious nonlinearities. The *characteristics-are-covariances* and shrinkage literatures (e.g., Kozak, Nagel & Santosh 2020, cited in S250) suggest much of the ML gain is dimension reduction, not magic.
- **Fractional vs integer differentiation.** Practitioners split on how much memory to retain; there is no universal `d` (S251 #4; S252 §5).

## Common mistakes
1. **Target leakage** — including any future-knowable quantity (next return, forward earnings, a label derived from the price path) in `X`. Detectable only by *audit*, not by shuffled CV (demonstrated above).
2. **Shuffled/time-ignorant CV on a time series** — standard k-fold leaks via overlapping event windows; use purged + embargoed (and ideally combinatorial) CV (S251 #8; S253).
3. **Forgetting feature lookbacks** — a 63-day volatility feature leaks into the next fold unless you embargo the first ~63 days (S253).
4. **Integer differentiation by default** — `returns = diff(prices)` destroys memory; prefer fractional differentiation when the signal is in slow-moving levels (S251 #4).
5. **Fixed-horizon labeling** — `sign(r_{t+h})` ignores stops/expirations and the path; use triple-barrier (S251 #5).
6. **Researching through the backtest** — tuning parameters until SR looks good (Bailey & López de Prado DSR/PSR, S68/S80; `08-backtesting-methodology/deflated-sharpe-multiple-testing.md`). Use feature importance (S252 §8) and *never* let a backtest modify the strategy.
7. **Ignoring costs, capacity, and regime** — an in-sample edge can vanish after transaction costs (`08-backtesting-methodology/transaction-costs-slippage-walkforward.md`) or once arbitraged away (non-stationarity).
8. **Too many correlated features** — collinearity inflates importance estimates and variance; reduce dimensionality or PCA-rotate (S252 §8; §6).

## Further reading
- **Tier 1 (primary):** Gu, Kelly & Xiu (2020), *Empirical Asset Pricing via Machine Learning*, RFS 33(5):2223–2273 — https://dachxiu.chicagobooth.edu/download/ML.pdf (open access) [S250]
- **Tier 1 (primary):** López de Prado (2018), *The 10 Reasons Most Machine Learning Funds Fail*, GARP whitepaper — https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf [S251]
- **Tier 2:** López de Prado, *Advances in Financial Machine Learning* (Wiley, 2018) — executive summary notes https://reasonabledeviations.com/notes/adv_fin_ml [S252]
- **Tier 2:** QuantInsti, *Cross Validation in Finance: Purging, Embargoing, Combination* — https://blog.quantinsti.com/cross-validation-embargo-purging-combinatorial [S253]
- **Tier 1/2:** Harvey, Liu & Zhu (2016) factor-zoo / multiple-testing context — see S72 in `STATE/sources.md` and `15-pitfalls-and-antipatterns/data-snooping-phacking.md`
- **In-repo cross-links:** `05-stats-and-ml/stationarity-adf-autocorrelation.md` (formal ADF/KPSS), `05-stats-and-ml/overfitting-lookahead.md`, `08-backtesting-methodology/deflated-sharpe-multiple-testing.md`, `08-backtesting-methodology/transaction-costs-slippage-walkforward.md`, `15-pitfalls-and-antipatterns/data-snooping-phacking.md`
- **Code:** mlfinlab ( fracdiff, triple-barrier, purged CV implementations); `timeseriescv` (CPCV) — https://github.com/sam31415/timeseriescv
