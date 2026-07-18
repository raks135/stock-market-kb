---
title: Option Greeks — Delta, Gamma, Vega, Theta, Rho
topic_id: 10-derivatives/option-greeks
tags: [options, greeks, black-scholes, hedging, derivatives, risk-management]
last_updated: 2026-07-18
confidence: robust
sources: [S127, S128, S129, S130]
---

## TL;DR
- The **Greeks** are the partial derivatives of an option's price with respect to the inputs that drive it: **Delta** (spot), **Gamma** (curvature of delta), **Vega** (volatility), **Theta** (time), **Rho** (interest rate). They let a trader isolate and hedge each risk separately.
- Under the Black–Scholes model the closed-form formulas are textbook-certain and easy to compute, but they rest on assumptions (constant volatility, lognormal returns) that **break in reality** — which is why every desk recalibrates implied vol off the **volatility surface** rather than treating sigma as constant.
- Practical use: **delta-hedge** to neutralize spot risk, watch **gamma** (it explodes near expiry at-the-money and is the source of hedging cost), and remember Vega/Rho are usually quoted **per 1%** move (divide the raw derivative by 100). A common and dangerous myth: "delta = probability of expiring ITM" — only approximately true under restrictive conditions.

## Core explanation
An option's fair value depends on several moving inputs at once: the underlying price S, volatility σ, time to expiry T, the risk-free rate r, and (for dividend-paying underlyers) the dividend yield q. If all inputs shift together the price move is a tangled mess. The Greeks linearize that mess: each Greek is the **sensitivity of the option price to a small change in one input, holding the others fixed**.

Formally, if V is the option value, the first-order Greeks are the first partial derivatives (∂V/∂S, ∂V/∂σ, ∂V/∂t, ∂V/∂r) and Gamma is the second derivative (∂²V/∂S²). Higher-order cross-derivatives (vanna, charm, vomma, …) exist but are beyond this article's scope; see S127 for the full taxonomy.

In plain terms:
- **Delta (Δ)** — "how much does my option price move if the stock moves $1?" It is also the **hedge ratio**: to delta-hedge a short call you hold Δ shares per option.
- **Gamma (Γ)** — "how fast does delta itself change as the stock moves?" Gamma is the **convexity** of the option. Long options are long gamma (good when the stock moves a lot); short options are short gamma (bad — losses accelerate).
- **Vega (𝒱)** — "how much does the price move if implied volatility rises 1%?" Same for calls and puts.
- **Theta (Θ)** — "how much value bleeds out each day as time passes?" Usually negative (options are wasting assets), but not always.
- **Rho (ρ)** — "how much does the price move if the risk-free rate rises 1%?" Usually the least important for short-dated options.

**Order of the Greeks.** Delta, Vega, Theta, Rho are first-order; Gamma is second-order (the derivative of Delta). Delta, Gamma and (to a lesser extent) Vega are the "big three" that option desks manage actively; Rho is often ignored for short maturities because its effect is small (S127, S130).

## Math / formulas
We use the **Black–Scholes–Merton** framework with a continuous dividend yield q (Hull's formulation; the Columbia notes in S129 derive the same objects). Define:

$$d_1 = \frac{\ln(S/K) + (r - q + \sigma^2/2)\,\tau}{\sigma\sqrt{\tau}}, \qquad d_2 = d_1 - \sigma\sqrt{\tau}$$

where τ = T (time to expiry in years), and N(·) is the standard-normal CDF, φ(x) = e^{−x²/2}/√(2π) its density.

| Greek | Call | Put |
|---|---|---|
| **Delta** | e^{−qτ} N(d₁) | e^{−qτ}[N(d₁) − 1] = −e^{−qτ} N(−d₁) |
| **Gamma** (same) | e^{−qτ} φ(d₁) / (S σ √τ) | same |
| **Vega** (same) | S e^{−qτ} φ(d₁) √τ | same |
| **Theta** (per year) | − S e^{−qτ} φ(d₁)σ / (2√τ) − r K e^{−rτ} N(d₂) | − S e^{−qτ} φ(d₁)σ / (2√τ) + r K e^{−rτ} N(−d₂) |
| **Rho** | K τ e^{−rτ} N(d₂) | −K τ e^{−rτ} N(−d₂) |

**Units / scaling traps (folklore-prone):**
- Vega as written above is the change per **1.00** (100 percentage points) change in σ. For "per 1% change" **divide by 100**.
- Rho above is per **1.00** change in r; for "per 1% change" **divide by 100**.
- Theta above is the change per **year**; divide by 365 (calendar) or 252 (trading days) for per-day decay. Different vendors also flip the sign convention, so always confirm whether Θ is "decay per day passing" (negative) or "gain if time increases" (positive) (S128).

**Delta–Put parity:** with q = 0, Δ_call − Δ_put = 1 exactly (S128). With dividends it is e^{−qτ}, close to 1 unless q or τ is large.

**Taylor approximation (why the Greeks matter):** for a small move ΔS in spot and Δσ in vol,
$$V(S+\Delta S,\sigma+\Delta\sigma) \approx V + \Delta S\cdot\Delta + \tfrac12(\Delta S)^2\Gamma + \Delta\sigma\cdot\text{Vega}$$
(S129 derives this from Itô/Taylor; "dollar gamma" = ½ S² Γ appears in the delta-hedging P&L below.)

## Worked example / code
**Scenario (all BS inputs):** S=100, K=100 (at-the-money), τ=0.5 yr, r=5%, q=0, σ=20%. European call.

Computed Greeks: Δ = 0.598, Γ = 0.0274, Vega (per 1%) = 0.2736, Θ (per day) = −0.0222, Rho (per 1%) = 0.2644.
Note the ATM call delta is **0.598, not 0.50** — positive interest rates lift call delta above 0.5 (the put delta is −0.402, and 0.598 − (−0.402) = 1.000, exactly the parity relation). With r = 0 the ATM call delta would be ≈ 0.5.

Runnable, dependency-free Python (stdlib `math` only; the conventional pinned alternative is `scipy==1.13` + `scipy.stats.norm.cdf`). Data source: model inputs are user-supplied; for live numbers pull S, r, q, σ (implied) from a market-data vendor (see KB 13-data-and-tooling).

```python
import math

def N(x):  # standard normal CDF (stdlib only; scipy.stats.norm.cdf is the pinned alt)
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def phi(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

def bs_greeks(S, K, T, r, q, sigma, kind="call"):
    tau = max(T, 1e-12)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    if kind == "call":
        delta = math.exp(-q * tau) * N(d1)
        rho   = K * tau * math.exp(-r * tau) * N(d2)
        theta = (-S * math.exp(-q * tau) * phi(d1) * sigma) / (2.0 * math.sqrt(tau)) \
                - r * K * math.exp(-r * tau) * N(d2)
    else:
        delta = math.exp(-q * tau) * (N(d1) - 1.0)
        rho   = -K * tau * math.exp(-r * tau) * N(-d2)
        theta = (-S * math.exp(-q * tau) * phi(d1) * sigma) / (2.0 * math.sqrt(tau)) \
                + r * K * math.exp(-r * tau) * N(-d2)
    gamma = math.exp(-q * tau) * phi(d1) / (S * sigma * math.sqrt(tau))
    vega  = S * math.exp(-q * tau) * phi(d1) * math.sqrt(tau)
    return dict(delta=delta, gamma=gamma, vega_per_1pct=vega/100.0,
                theta_per_day=theta/365.0, rho_per_1pct=rho/100.0)

g = bs_greeks(100, 100, 0.5, 0.05, 0.0, 0.20, "call")
print({k: round(v, 4) for k, v in g.items()})
# -> {'delta': 0.5977, 'gamma': 0.0274, 'vega_per_1pct': 0.2736,
#     'theta_per_day': -0.0222, 'rho_per_1pct': 0.2644}
```

Verified behavior (this code executed during authoring): ATM call delta 0.5977, put delta −0.4023, parity Δ_call − Δ_put = 1.000; Gamma and Vega identical for call and put; deep-ITM call delta → 1.00, deep-OTM → 0.00. A Taylor repricing test (S+1, σ+1%) gave error ≈ $0.0025 on a $7.77 price, confirming the Greeks are internally consistent.

## Assumptions & limitations
- **Black–Scholes assumptions** (S129): constant volatility, lognormal/Gaussian returns with no jumps, continuous trading, no transaction costs, constant r and q, European exercise. In reality (a) volatility is **not constant** — the implied-volatility surface is skewed/smiled (see below); (b) returns have fatter tails and occasional jumps; (c) American options (most single-stock options) allow early exercise, so BS is only approximate.
- **Greeks are local and dynamic.** They are valid for *small* moves *right now*; they change as S, t, σ move. A hedge computed once is stale within minutes. This is the core reason hedging is done repeatedly (discrete rebalancing), which introduces replication error.
- **Constant-vol trap.** BS Greeks are computed at a *single* σ. Real desks compute Greeks off the **volatility surface** (σ as a function of strike and maturity). Using a flat σ misprices skew-sensitive risks.
- **Transaction costs ignored.** Delta hedging assumes costless, continuous trading; real rebalancing incurs spreads, impact, and borrow costs (ties to KB 08-backtesting & 09-microstructure).

## Empirical evidence
- **The volatility surface is real and persistent.** The Columbia lecture notes (S129) show the Eurostoxx-50 implied-vol surface (Nov 2007): implied vol is **higher for lower strikes** (the "skew"/"smile"), most pronounced at short maturities, and inverts (short-dated vol spikes) in market stress. If BS were correct the surface would be flat — it is not, which is *why* traders quote BS implied vol and BS Greeks but calibrate σ to the surface.
- **Delta hedging P&L depends on realized vs implied vol, not on the forecast.** S129 derives the continuous-hedging result:
  $$\text{P\&L} = \int_0^T \tfrac12 S_t^2\,\Gamma_t\,(\sigma^2_{\text{imp}} - \sigma^2_t)\,dt$$
  A seller of options makes money when realized vol < implied vol (and vice versa); the "dollar gamma" ½ S² Γ is always positive for a long call/put and drives the path-dependent P&L. This is the empirical backbone of the volatility-risk-premium / variance-risk-premium strategies (see KB 14-strategy-catalog).
- **Rho is empirically minor for short maturities** (S127): a 1% rate move moves a short-dated option's value only a few cents, which is why desks routinely ignore it.

## Conflicting views
- **"Delta equals the probability of expiring in-the-money."** This is the most pervasive **folklore** (S127 lists delta as only a *proxy* for probability). Under BS with r = q = 0 and short maturity it is approximately true, but with non-zero rates/dividends or longer maturities the mapping breaks — delta can exceed the risk-neutral ITM probability. Treat it as a rough intuition, never as an equality.
- **"Theta is always negative."** Usually true for long options, but S128 notes **not all** options have negative theta — deep-ITM European puts (high r) or positions with large positive dividend effects can show positive theta. Don't hard-code the sign.
- **Model choice for the Greeks themselves.** The "Greeks" are model-dependent. BS Greeks, sticky-strike/local-vol Greeks, and stochastic-vol Greeks (e.g., Heston) can differ materially for the same option, especially in tails. Practitioners standardize on BS *implied* Greeks for communication but may hedge with a richer model (S129 emphasizes more sophisticated models are used in practice).

## Common mistakes
1. **Forgetting the /100 on Vega and Rho.** Reporting raw Vega (per 100%-point move) as if it were per 1% overstates the sensitivity by 100×.
2. **Treating Greeks as static.** Recomputing only at trade entry; in reality they must be re-marked continuously. Gamma especially explodes near expiry ATM.
3. **Delta-hedging without costing.** A "perfect" delta hedge in backtests ignores bid-ask, impact, and borrow — the real P&L is dominated by hedging frictions (KB 08/09).
4. **Hedging with flat σ.** Ignoring the skew means under-hedging downside tail risk; the 1987 crash and every vol-skew episode punished this.
5. **Confusing sign conventions for Theta.** Some platforms report Θ positive for long options (gain if time increases); others negative. Always confirm.
6. **Using BS Greeks on American options as if exact.** Early-exercise premium is ignored; use a tree/finite-difference pricer for accurate American Greeks.

## Further reading
- **S129 (Tier 1, opened):** M. Haugh, *The Black-Scholes Model* (Columbia IEOR E4706 lecture notes) — derivation, delta hedging, dollar gamma, vol-surface weaknesses. https://www.columbia.edu/~mh2078/FoundationsFE/BlackScholes.pdf
- **S128 (Tier 2, opened):** Macroption, *Black-Scholes Formulas (d1, d2, Greeks)* — exact formula reference with sign/units caveats. https://www.macroption.com/black-scholes-formula
- **S127 (Tier 2, opened):** Wikipedia, *Greeks (finance)* — full taxonomy incl. second/third-order Greeks. https://en.wikipedia.org/wiki/Greeks_(finance)
- **S130 (Tier 2, opened):** Investopedia, *Understanding Greeks in Finance* — practitioner intuition. https://www.investopedia.com/terms/g/greeks.asp
- **Hull, J.C., *Options, Futures, and Other Derivatives* (Pearson)** — the canonical textbook reference for the BS Greeks and hedging (further reading; not directly opened as URL).
- Next in KB: 10-derivatives/volatility-surface-skew-hedging (skew, term structure, hedging bases) and 10-derivatives/option-strategies (covered call, protective put, spreads).
