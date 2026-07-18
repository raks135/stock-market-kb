---
title: Risk Parity and Kelly Sizing
topic_id: 06-portfolio-construction/risk-parity-kelly-sizing
tags: [portfolio-construction, risk-parity, equal-risk-contribution, kelly-criterion, position-sizing, leverage, fractional-kelly]
last_updated: 2026-07-18
confidence: robust
sources: [S261, S262, S263, S264]
---

## TL;DR
- **Risk parity** (a.k.a. equal-risk-contribution, ERC) builds a portfolio so that *every* holding contributes the same amount to total risk, instead of the same dollar weight. It needs no expected-return estimates, but almost always requires **leverage** on low-volatility assets to reach an equity-like volatility target — that leverage is both its engine and its main vulnerability.
- **Kelly sizing** tells you the bet fraction that maximizes long-run *geometric* wealth growth (`f* = p − q/b` for a binary bet; `f* = (μ−r)/σ²` per asset). Full Kelly is optimal only if your edge and odds are *exactly* known — in practice everyone uses **fractional Kelly** because full Kelly produces brutal drawdowns and is hyper-sensitive to estimation error.
- Both methods are mathematically robust; their **live outperformance is contested** and depends entirely on the quality of your risk/return estimates and on transaction costs, regime stability, and capacity.

## Core explanation

### Risk parity (equal risk contribution)
Traditional 60/40 tips ~90%+ of portfolio *risk* into equities (see worked example: a 60/40 of 15%-vol stocks and 6%-vol bonds carries 98% of its risk in the equity sleeve). Risk parity fixes this by equalizing each asset's **risk contribution** (RC) rather than its weight. The idea was popularized by Bridgewater's "All Weather" in the 1990s (Qian 2005 names the concept; Choueifaty & Coignard 2008 pursue the parallel "maximum diversification" idea) and formalized by Maillard, Roncalli & Teiletche (2008/2010) as the ERC portfolio.

Plain version: you compute, for each asset, how much of the portfolio's total volatility is "caused" by that asset, then adjust weights until all assets cause the same amount. Because low-volatility assets (e.g., bonds) get *larger* weights, the raw risk-parity portfolio is low-vol; to make it competitive on return, practitioners **leverage** the whole portfolio (or the bond sleeve) up to a target volatility. That leverage is the reason risk parity is often described as "owning more of what's less risky."

### Kelly criterion
The Kelly criterion maximizes the expected logarithm of wealth, i.e. the long-run geometric growth rate. For a binary bet that pays `b`-to-1 on a win with win-probability `p`, the optimal fraction of bankroll to wager is `f* = p − q/b` (with `q = 1−p`). For a security with expected excess return `μ−r` and variance `σ²`, the continuous approximation is `f* = (μ−r)/σ²`. In a multi-asset setting the growth-optimal portfolio is proportional to `Σ⁻¹(μ−r·1)` — the same tangency/maximum-Sharpe portfolio from mean-variance theory (Markowitz 1959; Thorp). Kelly is the sizing rule, not a signal: it assumes you already have an edge.

## Math / formulas

### Risk contributions
Let `w` be weights, `Σ` the covariance matrix, and `σ(w) = √(wᵀΣw)` the portfolio volatility. The **marginal contribution to risk** of asset `i` is
`MCTR_i = ∂σ/∂w_i = (Σw)_i / σ(w)`.
The **total risk contribution** is `RC_i = w_i · MCTR_i = w_i (Σw)_i / σ(w)`, and by Euler's homogeneous-function theorem `Σ_i RC_i = σ(w)`.

**ERC optimization problem** (long-only): find `w` with `Σ_i w_i = 1`, `w_i ≥ 0`, and `RC_i = RC_j` for all `i, j`. A convenient equivalent is `w_i (Σw)_i = w_j (Σw)_j`.

Key theoretical ranking (Maillard et al. 2008/2010, Appendix A.3):
`σ_mv ≤ σ_erc ≤ σ_1/n`
i.e. ERC volatility sits between the minimum-variance portfolio and the equal-weight (1/N) portfolio. ERC is a "middle ground": more diversified in risk than min-variance (which over-concentrates), more risk-balanced than 1/N (which can be risk-concentrated when assets differ in volatility).

The **maximum-diversification portfolio** (Choueifaty & Coignard 2008) instead maximizes the *diversification ratio* `DR = (wᵀσ_vec) / σ(w)`; it is a tangency portfolio on the efficient frontier and tends to concentrate in fewer, low-correlation names. CFA Institute's analytic study (2013) finds, on 1,000 U.S. stocks (1968–2012), that on pure risk-minimization **min-variance > risk parity > max-diversification** — risk parity is not the lowest-vol portfolio, but it is far better diversified in *risk* than a cap/equal-weight book and uses the whole universe rather than a concentrated subset.

### Kelly
- Binary, lose-entire-wager: `f* = p − q/b`.
- Binary with partial loss `l` and gain `g` (investment form): `f* = p/l − q/g`.
- Continuous single asset: `f* = (μ − r)/σ²` (symmetric return distribution assumed).
- **Fractional Kelly**: bet `c·f*` with `0 < c < 1`. Thorp shows the growth rate relative to full Kelly is `g(cf*)/g(f*) = c(2−c)`. So half-Kelly (`c=0.5`) keeps **75%** of the growth rate while roughly halving variance and drawdown.
- Betting **more than** full Kelly (`c>1`) *reduces* expected growth and sharply raises the probability of ruin / deep drawdown.

## Worked example / code
Data below is an **illustrative synthetic covariance** (equity 15% vol, bonds 6% vol, correlation −0.20); it is chosen to echo a 60/40-like universe and is **not** a real dataset. Run with the repo `.venv` (`numpy>=2.5.1`, `scipy>=1.18.0`).

```python
import numpy as np
from scipy.optimize import minimize
import math, random

# ---- Long-only Equal-Risk-Contribution (ERC) solver ----
def erc_solver(cov):
    n = cov.shape[0]
    def obj(w):
        s = math.sqrt(float(w @ cov @ w))
        rc = w * (cov @ w) / s
        return float(np.var(rc))          # equal RCs => variance of RCs = 0
    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
    bnds = [(1e-6, 1.0)] * n
    res = minimize(obj, np.full(n, 1/n), method="SLSQP",
                   bounds=bnds, constraints=cons,
                   options={"maxiter": 1000, "ftol": 1e-12})
    return res.x

# Illustrative equities/bonds covariance (NOT real data)
vol_eq, vol_b, rho = 0.15, 0.06, -0.20
cov = np.array([[vol_eq**2, rho*vol_eq*vol_b],
                [rho*vol_eq*vol_b, vol_b**2]])
w_erc = erc_solver(cov)
sig = math.sqrt(float(w_erc @ cov @ w_erc))
rc = w_erc * (cov @ w_erc) / sig

print("ERC weights (eq, bond):", np.round(w_erc, 4))   # [0.2857 0.7143]
print("ERC portfolio vol     :", round(sig, 4))         # 0.0542
print("ERC risk contributions:", np.round(rc, 4))       # [0.0271 0.0271]  EQUAL

w_6040 = np.array([0.6, 0.4])
s60 = math.sqrt(float(w_6040 @ cov @ w_6040))
rc60 = w_6040 * (cov @ w_6040) / s60
print("60/40 vol:", round(s60, 4))                      # 0.0884
print("60/40 RC :", np.round(rc60, 4))                  # [0.0868 0.0016]  ~98% in equity

# ---- Kelly examples ----
p, q, b = 0.60, 0.40, 1.0
print("Kelly binary p=0.6,b=1 :", round(p - q/b, 4))    # 0.20
mu, r, sigma = 0.10, 0.06, 0.16
print("Kelly continuous (mu-r=4%, sig=16%):", round((mu-r)/sigma**2, 4))  # 1.5625 -> leverage
for c in [1.0, 0.5, 0.25, 1.5]:
    print(f"  fractional {c}: growth-ratio c(2-c) = {c*(2-c):.3f}")

# Coin-toss wealth paths: full vs over- vs under-bet (seed=7, 200 flips, p=0.6,b=1)
def path(p, b, f, n, seed=0):
    rnd = random.Random(seed); W = 1.0; xs = [W]
    for _ in range(n):
        W *= (1 + f*b) if (rnd.random() < p) else (1 - f); xs.append(W)
    return xs
for f in [0.2, 0.4, 0.1]:
    xs = path(0.6, 1.0, f, 200, seed=7)
    peak = xs[0]; mdd = 0.0
    for x in xs:
        peak = max(peak, x); mdd = max(mdd, (peak - x)/peak)
    print(f"  f={f}: final={xs[-1]:.1f}  maxDD={mdd:.1%}")
```

**Verified output**
```
ERC weights (eq, bond): [0.2857 0.7143]
ERC portfolio vol     : 0.0542
ERC risk contributions: [0.0271 0.0271]
60/40 vol: 0.0884
60/40 RC : [0.0868 0.0016]          # ~98% of risk sits in equities
Kelly binary p=0.6,b=1 : 0.2
Kelly continuous (mu-r=4%, sig=16%): 1.5625   # >1 => requires leverage
  fractional 1.0: growth-ratio c(2-c) = 1.000
  fractional 0.5: growth-ratio c(2-c) = 0.750
  fractional 0.25: growth-ratio c(2-c) = 0.438
  fractional 1.5: growth-ratio c(2-c) = 0.750
  f=0.2 (full):   final=3234.9  maxDD=75.8%
  f=0.4 (2x):     final=2932.5  maxDD=98.2%   # overbetting -> lower wealth, near-ruin
  f=0.1 (half):   final=150.7  maxDD=47.9%   # calmer, lower growth
```
The 60/40 vs ERC contrast is the whole point: equal *weights* leave equal-*risk* massively unequal; ERC rebalances until each sleeve carries the same risk. Note ERC's raw vol (5.4%) is below 60/40's (8.8%) — reaching 60/40's risk would require ~1.6× leverage, which is exactly the role leverage plays in real risk-parity mandates.

## Assumptions & limitations
- **Risk parity assumes the covariance matrix is known and stable.** In practice `Σ` is estimated with error and is non-stationary; leverage amplifies estimation error. If correlations spike toward +1 in a crisis (the classic "all correlations go to 1" effect), the diversification that risk parity relies on partially collapses exactly when you are most leveraged.
- **Kelly assumes known, stationary `p`/`b`/`μ`/`σ`.** Wikipedia and Thorp both stress "garbage in, garbage out": ex-post growth-optimal weights can differ *fantastically* from ex-ante predictions when inputs are estimated. Thorp's own estimate of the S&P 500 Kelly fraction is ~117% — i.e. it *requires* leverage, and a small error in the mean/variance inputs swings the number enormously.
- **Full Kelly has enormous drawdowns** (75.8% in the 200-flip run above, and realistically worse over longer horizons). That is why practitioners use fractional Kelly (half or quarter). The simulation also shows 2×-Kelly *underperforms* full Kelly on terminal wealth in this seed — overbetting is punished.
- **Costs & capacity:** both methods trade; ERC rebalances and can turn over frequently, and the leverage in risk parity carries financing cost. Backtests that ignore financing, spreads, and capacity overstate live results (see KB 08-backtesting-methodology).
- **Leverage/regulatory constraints:** many investors (pensions, mutual funds) cannot use the leverage risk parity mathematically requires, so they implement "almost-risk-parity" with bounded weights.

## Empirical evidence
- **Mechanics, not magic:** ERC volatility genuinely lies between min-variance and 1/N (`σ_mv ≤ σ_erc ≤ σ_1/n`, Maillard et al. 2008/2010, proven). On 1,000 U.S. stocks (1968–2012) the CFA Institute analytic study confirms risk parity uses the *whole* universe (unlike min-variance, which concentrates) and sits between min-variance and max-diversification on risk minimization (S262).
- **Risk-parity live performance is contested.** Practitioner backtests (e.g., Bridgewater All Weather variants) often show risk parity beating 60/40 on a risk-adjusted basis over long windows, and some report All Weather beating 60/40 in the majority of rolling 20-year periods — but these are *single-manager/practitioner* backtests (Tier-3 leads), sensitive to the leverage assumption, rebalancing frequency, and the bond bull market of 1980–2020. The low-rate environment that made bond leverage cheap has reversed, so historical RP edge is **not** a forward guarantee. Treat any "RP beats 60/40" claim as emerging/folklore until you see a cost-and-leverage-inclusive, out-of-sample study.
- **Kelly growth optimality is proven** (Kelly 1956; Breiman 1961; Thorp): among strategies with the same information, the growth-optimal one eventually dominates almost surely. The catch is the premise "same information" — which never holds with estimated inputs. Real-world "Kelly" is therefore always fractional.

## Conflicting views
- **Is risk parity a free lunch or a leverage bet?** Proponents (Bridgewater, many asset managers) argue it is robust diversification that works across regimes. Skeptics note it is largely a *bet on stable low rates / low bond volatility* — leverage on bonds — and that its 2008–2020 success rode a 40-year bond bull market; the CFA analytic study even ranks min-variance *ahead* of risk parity on raw risk minimization, implying RP's appeal is diversification breadth, not minimal volatility.
- **Kelly: full or fractional?** Theory says full Kelly maximizes growth; practitioners (Thorp foremost) recommend fractional because full Kelly's drawdowns and sensitivity to estimation error are intolerable in reality. "More than Kelly" is universally cautioned against (Thorp: `c>1` lowers growth and raises ruin).
- **Kelly vs mean-variance:** they coincide at the tangency portfolio when inputs are known, but mean-variance optimizes *expected return per unit variance* (a single-period utility view) while Kelly optimizes *long-run geometric growth* (a multi-period log-utility view). For a single sequential bet stream, Kelly is the coherent choice; for one-period utility, MV/Sharpe is.

## Common mistakes
1. **Confusing equal weight with equal risk.** A 60/40 book is nowhere near risk-balanced (≈98% of risk in equities in the example). Rebalancing to equal *weights* does not equalize risk.
2. **Using full Kelly on estimated edges.** Plugging noisy `μ`/`σ` into `f*=(μ−r)/σ²` gives explosive, leverage-requiring sizes (e.g., 117% / 156%). Almost always use half or quarter Kelly.
3. **Ignoring the leverage in risk parity.** Presenting ERC weights (e.g., 28% equity / 71% bonds, vol 5.4%) as "the portfolio" without noting it must be ~1.6× levered to match 60/40 risk misrepresents the strategy and hides financing cost and margin risk.
4. **Assuming correlations hold in crises.** RP's diversification benefit is weakest exactly when leverage is highest and correlations rise.
5. **Backtesting without costs/capacity.** Both methods churn; naive backtests overstate live Sharpe (see KB 08 / 15).

## Further reading
- S261 (T1, primary): Maillard, S., Roncalli, T. & Teiletche, J. (2008/2010), *On the properties of equally-weighted risk contributions portfolios* — https://www.thierry-roncalli.com/download/erc.pdf
- S262 (T1): CFA Institute RPC Digest, *Risk Parity, Maximum Diversification, and Minimum Variance: An Analytic Perspective* (2013) — https://rpc.cfainstitute.org/research/cfa-digest/2013/11/risk-parity-maximum-diversification-and-minimum-variance-an-analytic-perspective-digest-summ
- S263 (T2): Wikipedia, *Kelly criterion* (binary, investment, continuous, multi-asset, fractional, criticism) — https://en.wikipedia.org/wiki/Kelly_criterion
- S264 (T1, primary): Thorp, E.O. (2006), *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market*, in Zenios & Ziemba (eds.) *Handbook of Asset and Liability Management* — https://gwern.net/doc/statistics/decision/2006-thorp.pdf
- Qian, E. (2005), *Risk Parity Portfolios* (PanAgora / EDHEC) — originating risk-parity concept (cited in S261/S262).
- Choueifaty, Y. & Coignard, Y. (2008), *Toward Maximum Diversification*, JPM 34(4) — maximum-diversification portfolio.
- Damodaran, A., *Betas by Sector* / leverage notes — for linking risk parity to the leverage that equalizes risk — https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/Betas.html
- Cross-refs in this KB: 06 mean-variance-efficient-frontier, 07 var-cvar, 08 transaction-costs-slippage-walkforward, 15 data-snooping-phacking.
