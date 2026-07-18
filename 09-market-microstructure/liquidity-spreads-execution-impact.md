---
title: Liquidity, Spreads, Execution, and Market Impact
topic_id: 09-market-microstructure/liquidity-spreads-execution-impact
tags: [market-microstructure, liquidity, bid-ask-spread, market-impact, execution, implementation-shortfall, almgren-chriss, roll-spread, kyle-lambda, square-root-impact]
last_updated: 2026-07-18
confidence: robust
sources: [S119, S120, S121, S122, S123, S124, S125, S126, S75, S76, S79]
---

## TL;DR
- **Liquidity has three dimensions** — tightness (how cheap to trade), depth (how much size a price absorbs), and resiliency (how fast prices recover). A "liquid" market is tight, deep, and resilient [S121].
- **The bid–ask spread compensates the dealer for two things**: a *transitory* component (order processing, inventory carrying, monopoly rent) and an *adverse-selection* component (trading against better-informed investors) [S123].
- **Roll's (1984) implied spread** `s = 2√(-cov(ΔPₜ,ΔPₜ₋₁))` estimates the *effective* spread from price reversals alone — but it **understates the true spread** whenever adverse selection exists, because that component does not produce reversals [S119, S123].
- **Executing a large order moves price** via *temporary* impact (decays) plus *permanent* impact (stays). The Almgren–Chriss (2000/01) linear model gives a closed-form efficient frontier of schedules trading off expected cost vs variance [S120].
- **Average price impact of a "metaorder" scales with √Q, not Q** (square-root law) — so cost *per share* keeps falling as you split a bigger order [S79].
- **Measure execution with implementation shortfall (Perold 1988)** = paper-portfolio return minus actual return from decision to fill; VWAP/TWAP/arrival-price are *benchmarks*, not costs [S125, S126].

## Core explanation
Market microstructure studies how the rules and mechanics of trading turn buy/sell intentions into prices. Three quantities matter to a practitioner:

1. **Liquidity** — the ease of trading a position at a predictable price. The classic tripartite definition (tracing to Kyle 1985 and Harris 1990, surveyed in BIS CGFS 1999) is: *tightness* = the cost of immediately changing position (the spread/commissions); *depth* = the trade size the book absorbs before price moves; *resiliency* = how quickly price reverts to equilibrium after a shock [S121].
2. **The bid–ask spread** — the gap between the best buy (bid) and sell (ask) prices. It is the dealer's compensation and the most visible transaction cost. It is *not* a single economic cost: Glosten–Harris (1988) decompose it into a **transitory component** (inventory, clearing, monopoly rent — revenue from random order flow) and an **adverse-selection component** (the extra widening needed because some counterparties are informed). The adverse-selection piece is *permanent* in price; the transitory piece induces negative serial correlation in trade prices [S123].
3. **Market impact / execution** — when *you* trade, you consume liquidity and move the price against yourself. Impact is split into temporary (reverts) and permanent (stays) parts. How you slice and time the order (the execution *schedule*) determines the realized cost; this is the domain of optimal-execution theory (Almgren–Chriss) and transaction-cost analysis (implementation shortfall).

### Spread measures (all three are used in practice)
- **Quoted spread** = ask − bid (the headline, often meaningless if you cannot trade at it).
- **Effective spread** = 2 × |trade price − midquote at the trade| — what you actually paid relative to the marketable price [S75].
- **Realized spread** = 2 × (trade price − midquote *some time after* the trade) — the liquidity provider's net revenue after price reverts; isolates the transitory component from the adverse-selection component [S75, S123].

## Math / formulas

### Roll's (1984) implicit spread [S119]
In an informationally efficient market with a constant effective spread `s`, successive price changes are negatively autocorrelated (a buy at the ask is followed, on no news, by a fall back toward the mid). The first-order serial covariance satisfies `cov(ΔPₜ, ΔPₜ₋₁) = −s²/4`, hence the **implicit (effective) spread**:

```
s_eff = 2 × sqrt( − cov(ΔPₜ, ΔPₜ₋₁) )      (requires cov < 0)
```

This needs *only* a price series (no quote data). Caveats: it assumes efficiency and stationarity, and it **captures only the transitory component** — if adverse selection is present, Glosten (1987, in S123) shows serial-covariance estimators *understate* the total spread.

### Glosten–Harris (1988) decomposition [S123]
A two-component asymmetric-information model estimated from transaction prices separates:
- **Transitory component** `s_tr`: inventory costs, clearing fees, specialist monopoly power. Induces negative serial correlation (caught by Roll).
- **Adverse-selection component** `s_as`: compensates the dealer for losses to informed traders; has a *permanent* effect on price, so it does **not** generate reversals.

Empirically on 1981–83 NYSE data, the authors could **not reject** that a substantial part of spreads was due to adverse selection, and the adverse-selection piece rises with order size (consistent with Kyle 1985 and Glosten–Milgrom 1985). Huang & Stoll (1997) later extend this to a three-way split (order processing / inventory / adverse selection) [S124].

### Kyle (1985) lambda / market depth [S122]
In Kyle's canonical insider-trading model the competitive market maker sets the price as a linear function of net order flow `y`:

```
p = p* + λ · y ,      depth = 1/λ
```

where `λ` (the "Kyle lambda") is the price impact per unit of order flow and **market depth = 1/λ** is the market's ability to absorb quantity without moving price. A larger `λ` (thinner market) means each trade moves price more [S122, referenced in S120/S121].

### Almgren–Chriss (2000/01) execution model [S120]
Liquidate `X` shares by time `T` in `N` intervals of length `τ`. Price follows an arithmetic random walk plus market impact:

```
S_k = S_{k-1} + σ τ^{1/2} ξ_k − τ · g(n_k/τ)          (permanent impact g)
S̃_k = S_{k-1} − h(n_k/τ)                              (execution price, temporary impact h)
```

With **linear** impact functions `g(v) = γ v` and `h(v) = ε·sgn(n) + η v`:

```
Expected cost   E(x) = ½ γ X² + ε·X + (η − ½γτ)·τ·Σ n_k²
Variance        V(x) = σ² τ · Σ x_k²
```

where `x_k` is shares held after interval `k` and `n_k = x_{k−1} − x_k`. Optimal schedules minimize `E(x) + λ·V(x)` (λ = risk aversion). The solution is monotone and explicit:

```
x_k = X · sinh(κ (N−k)) / sinh(κ N),     κ = arccosh( 1 + λσ² / (2(η − ½γτ)) )
```

Higher λ ⇒ trade faster up-front (lower delay/opportunity cost, higher impact); λ = 0 ⇒ constant-rate "naïve" schedule. The curvature of the cost–variance frontier at its minimum is a *measure of liquidity* [S120].

### Square-root law of market impact [S79]
Across stocks, futures, FX, options and even Bitcoin, the *average* price impact `I` of a metaorder of total size `Q` (with daily volume `V`) obeys, for moderate participation rates:

```
I(Q) ≈ σ · sqrt( Q / V )        equivalently   ΔP/P ∝ sqrt(Q)
```

Impact depends on **total** volume traded and barely on the *schedule* — slicing a fixed `Q` into more, smaller child orders does not materially shrink total impact (it mainly changes the temporary-vs-permanent split and timing risk). This contradicts a naïve linear (Kyle-style) `ΔP ∝ Q` and is one of the most robust empirical regularities in microstructure [S79, S76].

## Worked example / code
Pure **standard-library Python** (no third-party install needed — runs with `python3` on any 3.x). Data: a synthetic price path (reproducible, seed 42) used only to *illustrate the mechanics*, not a market claim.

```python
import math, random

# ---------- (1) Roll implicit spread ----------
rng = random.Random(42)
eff_spread = 0.05                      # true effective half-spread in $ (illustrative)
h = eff_spread / 2.0
mid = 100.0
P = [mid]
for _ in range(20000):
    mid += rng.gauss(0, 0.10)          # efficient-value random walk (the unobserved mid)
    sign = 1.0 if rng.random() < 0.5 else -1.0   # trade at ask (+) or bid (-)
    P.append(mid + h * sign)           # recorded trade price bounces around the mid
dP = [P[i] - P[i-1] for i in range(1, len(P))]
cov = sum(dP[i]*dP[i-1] for i in range(1, len(dP))) / len(dP)   # population serial cov
roll_spread = 2*math.sqrt(-cov) if cov < 0 else float('nan')
print(f"Roll implicit spread = {roll_spread:.4f}  (true eff spread used = {eff_spread:.2f})")

# ---------- (2) Almgren-Chriss optimal liquidation ----------
X, T, N = 1_000_000, 5.0, 50          # shares, days, intervals
tau = T / N
sigma = 0.95 / math.sqrt(252) * 50     # $/share per sqrt(day); S0=50
eps = 0.0625                           # half-spread ($/share)
gamma = 2.5e-7                         # permanent impact coeff ($/share)/share
eta = 2.5e-6                           # temporary impact coeff ($/share)/(share/day)

def schedule(lam):
    A = (eta - 0.5*gamma*tau) * tau             # cost weight on n_k^2
    if lam == 0.0:                              # constant-rate (naive) limit: r -> 1
        x = [X*(N-k)/N for k in range(N+1)]
    else:
        B = lam * sigma**2 * tau                # risk-aversion term
        c = 2.0 + B/A
        r = (c + math.sqrt(c*c - 4.0)) / 2.0
        x = [X * (r**k - r**(2*N - k)) / (1.0 - r**(2*N)) for k in range(N+1)]
    n = [x[k-1] - x[k] for k in range(1, N+1)]  # shares sold each step (n_1..n_N)
    E = 0.5*gamma*X**2 + eps*X + A*sum(v*v for v in n)
    V = sigma**2 * tau * sum(v*v for v in x)
    return x, n, E, V

for lam in (0.0, 1e-6, 1e-5):
    x, n, E, V = schedule(lam)
    first = n[0]/X*100
    print(f"lambda={lam:.0e}: first-interval sells {first:5.1f}% of X | E[cost]=${E:,.0f} | V[cost]=${V:,.0f}")
```

Expected output (reproducible): `lambda=0.0` → constant-rate 2.0%-per-step, lowest expected cost, largest variance; rising `lambda` front-loads the schedule (first interval sells a growing share) and lowers variance at the expense of expected cost. Roll implicit spread prints ~0.05 (matches the injected `eff_spread` because this synthetic path has *no* adverse-selection component — exactly Roll's assumption; add informed trades and the estimate drifts below the true total spread, per S123).

## Assumptions & limitations
- **Roll's measure** assumes informational efficiency and stationarity; it ignores the adverse-selection component, so on real equities it *understates* the true spread [S119, S123].
- **Almgren–Chriss** assumes an arithmetic random walk with independent increments, linear impact, and a single risk-averse agent; it ignores serial correlation, news clusters, and information leakage. Static optimal schedules can be suboptimal when these hold [S120].
- **Square-root law** holds for *moderate* participation rates; at very high participation or in stressed, gapping markets, impact can be super-linear and the law breaks (capacity/fragility) [S79, S76].
- **Implementation shortfall** requires a precisely defined *decision/arrival price*; sloppy timestamps or benchmark gaming (e.g., delaying into low-volume periods to beat VWAP) distort the number [S125].

## Empirical evidence
- **Spread decomposition**: Glosten–Harris (1988) on 250 NYSE stocks (1981–83) find a significant adverse-selection component that grows with trade size; the permanent/transitory split mirrors Holthausen–Leftwich–Mayers block-study results [S123].
- **Execution cost**: institutional TCA shows implicit costs (impact + delay) dominate explicit costs (commissions); the Plexus Group cited delay as the single largest IS component in Asian equity trades (≈84 of 153 bps in 2004) [S125, S76].
- **Square-root impact**: replicated across asset classes, geographies and 1995→2014 windows; it also holds in option markets [S79].
- **Three-bucket labeling**: *robust* — liquidity tri-dimensionality, spread decomposition, Roll estimator, Almgren–Chriss linear model, square-root law, implementation shortfall. *Emerging/folklore* — precise numerical impact coefficients (η, γ, Kyle λ) are market-, stock-, and regime-specific; the "optimal" schedule is model-dependent.

## Conflicting views
- **Roll vs Glosten–Harris**: Roll's covariance estimator is simple and data-light, but Glosten–Harris argue it *cannot* recover the total spread when adverse selection exists — the two schools disagree on what the number means [S119 vs S123].
- **Linear (Kyle) vs square-root impact**: Kyle's linear `ΔP ∝ y` is analytically convenient but empirically contradicted by the concave √Q law; modern optimal-execution work uses square-root or transient-impact specifications instead [S79, S120].
- **Spread as a "cost"**: quoted spread overstates real cost for patient limit-order traders and understates it for urgent market-order takers; "the spread" is not one number [S75, S123].

## Common mistakes
- Treating the **quoted spread** as the cost you pay (you usually cross it or trade inside it; effective spread is what matters) [S75].
- Using **VWAP as a cost** — it is a *benchmark*; a fill "below VWAP" can still be a terrible decision-price execution [S125].
- Ignoring **permanent impact** in cost models (treating all impact as temporary/reversible) — overstates how cheap aggressive trading is [S120].
- Believing **more slicing always lowers impact** — square-root law says total impact depends on Q, not the number of child orders [S79].
- **Backtesting execution** with look-ahead (using end-of-bar VWAP you could not have known) or ignoring capacity — see `08-backtesting-methodology` [S76].

## Further reading
- [S119] Roll, R. (1984), "A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market," *JF* 39(4):1127–1139. https://www.bauer.uh.edu/rsusmel/phd/roll1984.pdf
- [S123] Glosten, L. & Harris, L. (1988), "Estimating the Components of the Bid/Ask Spread," *JFE* 21:123–142. https://www.acsu.buffalo.edu/~keechung/MGF743/Readings/B3%20Glosten%20and%20Harris%2C%201988%20JFE.pdf
- [S120] Almgren, R. & Chriss, N. (2000/01), "Optimal Execution of Portfolio Transactions." https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf
- [S121] Muranaga, J. & Shimizu, T. (1999), "Market Microstructure and Market Liquidity," BIS CGFS. https://www.bis.org/publ/cgfs11mura_a.pdf
- [S126] Perold, A.F. (1988), "The Implementation Shortfall: Paper versus Reality," *J. Portfolio Management* 14(1):4–9 (referenced in S120).
- [S125] O'Connell, R. (2026), "Implementation Shortfall: Perold Framework," ryanoconnellfinance.com. https://ryanoconnellfinance.com/implementation-shortfall
- [S79] Bouchaud, J-P. (2024), "The Square-Root Law of Market Impact." https://bouchaud.substack.com/p/the-square-root-law-of-market-impact
- [S75] CFA Institute (2026), "Trading Costs and Electronic Markets" (refresher reading). https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets
- [S76] Graham Capital Management (2017), "Transaction Costs" research note. https://www.grahamcapital.com/wp-content/uploads/2023/08/Transaction-Costs_GCM-Research-Note_Jul-17.pdf
- [S122] Kyle, A.S. (1985), "Continuous Auctions and Insider Trading," *Econometrica* 53:1315–1336 (primary; referenced in S120/S121 — exact λ algebra not re-derived here; Verify).
- [S124] Huang, R.D. & Stoll, H.R. (1997), "The Components of the Bid-Ask Spread: A General Approach," *RFS* 10(4):995–1034 (three-way extension of S123; Verify exact split).
