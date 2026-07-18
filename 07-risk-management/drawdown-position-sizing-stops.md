---
title: Drawdown, Position Sizing, and Stop-Losses
topic_id: 07-risk-management/drawdown-position-sizing-stops
tags: [risk management, drawdown, maximum drawdown, Calmar, position sizing, stop-loss, R-multiple]
last_updated: 2026-07-18
confidence: contested
sources: [S275, S276, S277, S278, S279, S280, S281, S282]
---

## TL;DR
- **Drawdown** (peak-to-trough loss) is the risk measure that actually frightens capital away; it scales differently from volatility and is **path-dependent**, so VaR/volatility alone understate it.
- **Position sizing** is the single most consequential risk lever: the fraction you risk per trade, not the entry signal, drives whether you survive a normal losing streak. Fixed-fractional ("1% risk") sizing is the workhorse.
- **Stop-losses are contested.** Under a random walk a stop-loss only *reduces* expected return (it is an insurance premium); it adds value *only* in trending/positive-autocorrelation regimes, and large-sample equity studies find **no net value** for mechanical stop-losses on the S&P 500.

## Core explanation

### Drawdown
A **drawdown** at time *t* is the decline from the running peak of a portfolio's value to the current value:

```
DD(t) = (V_peak(t) − V(t)) / V_peak(t),   V_peak(t) = max_{0 ≤ s ≤ t} V(s)
```

The **Maximum Drawdown (MDD)** is the largest such decline over the sample. MDD is a *path-dependent* measure: two portfolios with identical mean and volatility can have very different MDDs depending on the order of returns. Because most investors experience the path (not just the average), and because large drawdowns trigger redemptions and career risk, MDD is the risk statistic that matters most to allocators (S278, S275).

### Position sizing
Position sizing answers "how big?" for each bet. The most common disciplined rule is **fixed-fractional / percent-risk sizing**: risk a fixed fraction *f* of equity on each trade, where "risk" means the loss you would take if your stop is hit.

```
Shares = Risk$ / (Entry × StopDistanceFraction)
       = (Equity × f) / (Entry × StopFraction)
```

Volatility-based variants size so that the dollar risk equals a fixed fraction of a volatility measure (e.g., *k × ATR*), shrinking the position when volatility expands. The crucial, often-misunderstood fact: **position size determines drawdown depth**. Risking 10% per trade can halve an account in ~7 consecutive losses; risking 2% needs ~34 (math below). This is why sizing—not the signal—is the dominant determinant of survival.

### Stop-losses
A stop-loss is an order/rule to liquidate once a position falls by a preset amount. Academically it is best understood as a **path-dependent, trend-following overlay** (S276, S277). Under a pure random walk the optimal strategy is buy-and-hold, so any stop can only *diminish* expected return—it is an insurance premium paid to cap downside. It pays off *only* when returns exhibit positive serial correlation (momentum/trend), which is weak and short-lived in liquid large-cap equities.

## Math / formulas

**Drawdown & related ratios**
- `MDD = max_t (V_peak(t) − V(t)) / V_peak(t)`  (reported as a negative or positive magnitude)
- `Calmar = CAGR / |MDD|`  (higher is better) — S280
- `Sterling = CAGR / (|MDD| − threshold)`  (e.g., threshold = 10%), designed so a small MDD does not blow up the ratio
- **CDaR** (Conditional Drawdown-at-Risk, Chekhlov–Uryasev–Zabarankin, cited in S278): the mean of the worst `(1 − β)·100%` of drawdowns. A coherent, optimization-ready drawdown risk measure.

**Expected MDD under Brownian motion** (Magdon-Ismail & Atiya 2004, S275). For a portfolio value following `dx = μ dt + σ dW` (arithmetic, no reinvestment), the expected MDD has a phase transition in its scaling with horizon *T*:
- Profitable (μ > 0): `E(MDD)/σ → (0.63519 + 0.5·ln T + ln(μ/σ)) / (μ/σ)`, scaling ≈ linearly with `√T` at long horizons.
- Breaking even (μ = 0): `E(MDD) ≈ 1.2533 σ √T`.
- Losing (μ < 0): `E(MDD) → −μT − σ²/μ` (approaches total loss).

Define the √T-scaled Sharpe `Shrp = μ/σ`. Then `E(MDD)/σ = 2·Qp(T²·Shrp²) / Shrp`, where `Qp` is a universal integral tabulated in the paper. This quantifies the well-known fact that **higher Sharpe ⇒ proportionally smaller expected drawdown**.

**Normalized Calmar** (S275). Because the plain Calmar depends on the evaluation window *T*, comparing two funds' Calmars is only valid over identical horizons. For a base horizon `τ` (recommended τ = 1 year):

```
Calmar(τ) = γ_τ(T, Shrp) × Calmar,
γ_τ(T, Shrp) = [ (1/T)·Qp(T²Shrp²) ] / [ (1/τ)·Qp(τ²Shrp²) ]
```

**Position sizing**
- Fixed-fractional: `Risk$ = Equity × f`; `Shares = Risk$ / (Entry × StopFraction)`.
- ATR-based: `Shares = Risk$ / (k × ATR)` with `k` a multiple (e.g., 2).
- Consecutive-loss survival: after *n* losing trades each costing fraction *f*, `Equity_n = Equity_0 × (1 − f)^n`. Losses to halve: `n_half = ln(0.5)/ln(1 − f)`.

**Stop-loss as trend filter** (Acar & Toffel 2000/2001, S276, S277). For an AR(1) return process `X_t = α X_{t−1} + ε_t`, a conditional stop-loss with exit on the first negative mark-to-market has expected excess return `E(Sc) ≈ (α σ)/π` over the no-stop strategy. The stop *helps* iff `α > 0` (positive autocorrelation). Empirically, daily equity autocorrelation is "mostly below 0.04" (S277 abstract), so the condition is rarely met in liquid equities.

## Worked example / code

Pure standard-library Python (no third-party packages, runs on CPython 3.14). Data are **synthetic, seeded geometric Brownian motion** — this is a pedagogical illustration of the mechanics, *not* a market claim.

```python
import math, random

# ---------- 1. Synthetic equity curve (seeded; NOT market data) ----------
random.seed(42)
mu_a, sig_a, T, steps = 0.10, 0.15, 10.0, 2520   # 10y daily, drift 10%, vol 15%
dt = T / steps
V = 1000.0
equity = []
for _ in range(steps):
    z = random.gauss(0.0, 1.0)
    V *= math.exp((mu_a - 0.5*sig_a**2)*dt + sig_a*math.sqrt(dt)*z)
    equity.append(V)

# ---------- 2. Drawdown, MDD, Calmar ----------
peak = equity[0]
mdd = 0.0
for v in equity:
    peak = max(peak, v)
    dd = (peak - v) / peak
    mdd = max(mdd, dd)
cagr = (equity[-1]/equity[0])**(1.0/T) - 1.0
calmar = cagr / mdd
print(f"Final wealth : {equity[-1]:.2f}")
print(f"CAGR         : {cagr*100:.2f}%")
print(f"Max Drawdown : {mdd*100:.2f}%")
print(f"Calmar       : {calmar:.2f}")

# ---------- 3. Recovery math ----------
loss = 0.50
gain_needed = 1.0/(1.0-loss) - 1.0
print(f"A {loss*100:.0f}% drawdown needs a {gain_needed*100:.0f}% gain to recover.")

# ---------- 4. Fixed-fractional position sizing ----------
equity0 = 100_000.0
f = 0.01                      # risk 1% of equity
entry, stop_pct = 100.0, 0.05 # entry $100, stop 5% below
risk_usd = equity0 * f
shares = risk_usd / (entry * stop_pct)
print(f"Risk$/trade   : ${risk_usd:.0f}")
print(f"Shares (1% R) : {shares:.0f}  (notional ${shares*entry:,.0f})")

# ---------- 5. Consecutive-loss survival ----------
for frisk in (0.02, 0.05, 0.10):
    n_half = math.log(0.5)/math.log(1-frisk)
    print(f"Risk {frisk*100:.0f}%/trade -> {n_half:.1f} consecutive losses to halve account")

# ---------- 6. Magdon-Ismail E(MDD) approximation vs simulation ----------
shrp = mu_a/sig_a
E_MDD_over_sig = (0.63519 + 0.5*math.log(T) + math.log(shrp))/shrp
E_MDD = E_MDD_over_sig * sig_a
print(f"E[MDD] (MIA asympt, mu=.10 sig=.15 T=10y) ~ {E_MDD*100:.1f}%  (simulated MDD above: {mdd*100:.1f}%)")
```

Expected output (deterministic given seed 42, verified on CPython 3.14.4):
```
Final wealth : 1889.08
CAGR         : 6.58%
Max Drawdown : 38.09%
Calmar       : 0.17
A 50% drawdown needs a 100% gain to recover.
Risk$/trade   : $1000
Shares (1% R) : 200  (notional $20000)
Risk 2%/trade -> 34.3 consecutive losses to halve account
Risk 5%/trade -> 13.5 consecutive losses to halve account
Risk 10%/trade -> 6.6 consecutive losses to halve account
E[MDD] (MIA asympt, mu=.10 sig=.15 T=10y) ~ 31.1%  (simulated MDD above: 38.1%)
```
The simulated MDD (38.1%) exceeds the asymptotic Gaussian expectation (31.1%) because a single 10-year path is one draw from a wide distribution—exactly the point that MDD is a *realized* tail statistic, not a stable parameter, and that fat tails/jumps make real drawdowns worse than the Brownian prediction. Pin versions: Python 3.14.4; no third-party libs.

## Assumptions & limitations
- **Drawdown depends on measurement frequency and path.** Daily MDD ≥ monthly MDD for the same period; comparing MDDs requires identical frequency and horizon (S278, S275).
- **E(MDD) formulas assume Brownian motion** (i.i.d. normal increments, no jumps, no reinvestment in the arithmetic form). Real equity returns have fat tails, volatility clustering, and jumps, so realized MDDs are typically *worse* than the Gaussian prediction—as the simulation shows.
- **Calmar is not time-homogenizable** without the normalization above; a 3-year Calmar of 2.0 is not comparable to a 10-year Calmar of 2.0 (S275).
- **Stop-loss analysis ignores costs in the pure theory** (Acar & Toffel explicitly note slippage/trading costs would worsen results); with real frictions, mechanical stops fare even worse.
- **Position-sizing math assumes the stop is actually filled near the intended price**—gaps, illiquidity, and limit-order slippage break this, especially in crashes when you most need the protection.
- **Sizing rules are not alpha.** They control *survival and scale*, not expected return; optimal f / Kelly still require a positive-expectancy signal.

## Empirical evidence
- **Drawdown is the dominant risk investors feel.** Large drawdowns drive fund redemptions and forced deleveraging; MDD is "the risk measure of choice for many money management professionals" (S275). CFA Institute notes normality assumptions imply the S&P 500 should have had ~1.3 months of −15%+ returns in 85 years vs. the ~10 observed—volatility alone massively understates real drawdown risk (S278).
- **Stop-losses reduce expected return under random walk.** Acar & Toffel (2000) show the stop-loss payoff under drifted Brownian motion only shifts mass to the insurer's loss; "path-dependent strategies such as the stop-loss rule can only diminish earnings" relative to buy-and-hold (S276).
- **Stop-losses help only with positive autocorrelation.** The same authors' AR(1) analysis gives `E(Sc) ≈ ασ/π`; since observed daily equity autocorrelation is mostly < 0.04, the condition is rarely satisfied in liquid large caps (S277).
- **No net value for mechanical stops on the S&P 500.** Clare, Seaton, Smith & Thomas (2013) test simple trend-following rules on the S&P 500 (1952–2011) and conclude "there is no value in stop loss rules"; adding percentage stop-losses to 200-day breakout strategies *lowers* Sharpe ratios (e.g., 200-day breakout Sharpe 0.56 with no stop vs. 0.54/0.49 at 12%/15% stops, and negative at tight 3–5% stops) (S279, Tables 4–5).
- **Trend-following as a whole can add value** (200-day MA beats buy-and-hold on risk-adjusted basis in that study), which is consistent with the "stop = trend filter" interpretation: the *trend rule* helps, the *stop* overlay does not.

## Conflicting views
- **"Stops protect capital" vs. "stops are a drag."** Practitioners treat stops as essential discipline (and they do cap a *single* catastrophic loss and curb the disposition effect—see the behavioral article). Academics show that, net of the trend/timing content, a pure stop is an insurance premium that lowers expected return and only pays off when trends exist (S276, S277, S279).
- **Asset-class dependence.** Stop-loss/trend overlays are far more defensible in trending, lower-efficiency markets (commodities, FX, some CTAs) than in liquid large-cap equities where autocorrelation is near zero (S279 vs. the CTA/trend-following literature it cites).
- **Drawdown vs. volatility as the optimization target.** Variance is path-independent and analytically tractable; drawdown is what investors care about but is hard to optimize. CDaR and similar drawdown-risk measures exist but are less standard (S278).

## Common mistakes
- **Ignoring the recovery asymmetry.** A −50% drawdown needs +100% to break even; −20% needs only +25%. Sizing to keep MDD small is the only reliable defense.
- **Stop too tight → whipsaw.** Tight stops get hit by noise, realize many small losses, and convert a winning strategy into a losing one after costs.
- **Confusing stop-loss with risk control in crashes.** Stops assume continuous liquidity; in gap/flash events the fill is far below the stop, so realized loss >> intended risk.
- **Risking too much per trade.** 10%/trade can halve an account in ~7 losses—well within any normal strategy's losing streak. Disciplined managers use 0.5–2%.
- **Comparing Calmar ratios across different windows** without normalization (S275).
- **Treating optimal-f / Kelly sizing as tradable edge.** It maximizes geometric growth *given a known, stable edge*; in practice the edge is estimated with error and optimal f is anchored to the worst historical loss, which is not the worst possible loss (Vince critique, S282).

## Further reading
- S275 — Magdon-Ismail, M. & Atiya, A.F. (2004), "An Analysis of the Maximum Drawdown Risk Measure," *Risk* 17(10). https://www.cs.rpi.edu/~magdon/ps/journal/drawdown_RISK04.pdf
- S276 — Acar, E. & Toffel, R. (2000), "Stop-loss and Investment Returns," Faculty and Institute of Actuaries. https://www.actuaries.org.uk/system/files/documents/pdf/stop-loss-and-investment-returns.pdf
- S277 — Acar, E. & Toffel, R. (2001), "On the effectiveness of stop-loss rules. An analytical framework based on Brownian motion," SSRN 3087196. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3087196
- S278 — Ramani, P. (CFA) (2013), "Sculpting Investment Portfolios: Maximum Drawdown and Optimal Portfolio Strategy," CFA Institute Inside Investing. https://blogs.cfainstitute.org/insideinvesting/2013/02/12/sculpting-investment-portfolios-maximum-drawdown-and-optimal-portfolio-strategy
- S279 — Clare, A., Seaton, J., Smith, P.N. & Thomas, S. (2013), "Breaking into the blackbox: Trend following, stop losses and the frequency of trading — the case of the S&P500," *Journal of Asset Management* 14(3):182–194. https://openaccess.city.ac.uk/id/eprint/17842/
- S280 — Calmar ratio definition. https://journalplus.co/learn/glossary/calmar-ratio
- S281 — Luxalgo, "5 Position Sizing Methods for High-Volatility Trades." https://www.luxalgo.com/blog/5-position-sizing-methods-for-high-volatility-trades
- S282 — Van Tharp Institute, position sizing / R-multiple framework (practitioner, lead only). https://vantharpinstitute.com/van-tharp-teaches-position-sizing-strategies-and-risk-management
- Cross-references: `07-risk-management/var-cvar.md` (tail risk), `06-portfolio-construction/risk-parity-kelly-sizing.md` (Kelly/risk-parity sizing), `12-behavioral-finance/cognitive-biases-sentiment-crowding.md` (disposition effect that stops counteract), `15-pitfalls-and-antipatterns/data-snooping-phacking.md` (overfitting stop parameters).
