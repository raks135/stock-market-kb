---
title: Inflation, Yields & Equity Valuation
topic_id: 11-macro-and-regimes/inflation-yields-equity-valuation
tags: [macro, inflation, interest-rates, yields, valuation, fed-model, equity-duration, discount-rate]
last_updated: 2026-07-18
confidence: contested
sources: [S320, S321, S322, S323, S324, S325, S326, S327, S328]
---

## TL;DR
- Two robust mechanics drive the rate–valuation link: (1) the **discount-rate channel** — lower required returns raise the present value of distant cash flows; and (2) **equity duration** — equities are long-duration assets, so their prices are *more* sensitive to rate moves precisely when rates are low.
- The popular **"Fed model"** (compare E/P to the nominal 10y Treasury yield) is fallacious as a predictive tool: it compares a *real* quantity (earnings yield) to a *nominal* one, and fails out-of-sample [S321].
- Inflation is a **long-run wash but a short-run tax** on equities: the cross-section of studies finds a negative stock–inflation relation at business-cycle horizons and a roughly neutral one over decades [S324]. Moderate inflation (2–4%) has historically been benign for US stocks; high inflation (>4%) has not [S325].
- A third, behavioral channel — **inflation illusion** (discounting real cash flows at nominal rates) — explains much historical mispricing and is corroborated by two independent opened primaries [S323, S324].

## Core explanation

### The discount-rate channel (robust)
A stock is the present value of its future cash flows. When the required return (discount rate) falls, every future dollar is worth more today. Because equity cash flows are far in the future, the effect is large and non-linear. This is the cleanest, least-contested mechanism linking yields to valuations.

### Equity duration (robust framing, contested magnitudes)
Debt has a well-known duration; equities do too. Under a constant-growth (Gordon) model the *discount-rate duration* of a stock is `DDR = 1/(k − g)` [S327]. As the discount rate `k` falls, duration lengthens — meaning **low-rate environments make equities *more*, not less, sensitive to further rate moves** [S327]. Empirically, Golez & Koudijs (2025) show that after 1945 expected-return changes drive >90% of aggregate price variation (vs. ~50/50 before 1945), and that this rise in "equity duration" tracks the secular fall in payout ratios [S328]. This is why "growth" stocks are often described as the longest-duration assets in the market.

### Inflation: three distinct channels
1. **Cash-flow / real-economy channel.** Unexpected or high inflation can depress *real* earnings growth (margin compression, uncertainty, policy tightening), which mechanically lowers fair value [S320, S324].
2. **Discount-rate channel.** Inflation raises nominal required returns (and, via the Fisher effect, nominal risk-free rates), which lowers the PV of cash flows [S320].
3. **Inflation-illusion / money-illusion channel (Modigliani–Cohn 1979).** If investors discount *real* cash flows with *nominal* discount rates, equities become underpriced when inflation is high and overpriced when it is low. Campbell & Vuolteenaho (2004) decompose the S&P 500 dividend yield and find that **the level of inflation explains almost 80% of the time-series variation in stock-market mispricing**, consistent with this hypothesis [S323]. The CFA Institute literature review reaches the same conclusion about the money-illusion mechanism [S324].

### The "Fed model" (contested)
Practitioners often assert stocks are "cheap" when the earnings yield `E/P` exceeds the 10-year Treasury yield `Y`, and "expensive" otherwise, justifying high P/E multiples when rates are low [S321]. Asness (2003) shows this is **logically flawed**: `E/P` is a *real* quantity (nominal earnings already embed inflation), while `Y` is *nominal*. The correct comparison is `E/P` versus the *real* (TIPS) yield [S321]. The Fed model works as a *descriptive* story for how investors have set P/E multiples only when conditioned on perceived volatility, but has essentially no *predictive* power for future long-term returns [S321]. Campbell & Vuolteenaho independently label it a behavioral description, not a rational valuation rule [S323].

## Math / formulas

**Constant-growth (Gordon) dividend model**
```
P0 = D1 / (r − g) = D0(1+g) / (r − g),   r > g
```
Implied dividend yield: `D/P = r − g`. Implied earnings yield (no-payout distinction, illustrative): `E/P ≈ (r − g)/(1+g)`.

**Inflation neutrality (Fisher, via the DDM) [S324]**
Let nominal discount rate `r = R + i` (approx, Fisher 1930; `R` = real rate, `i` = expected inflation) and nominal growth `g = G + i` (`G` = real growth). Then
```
P0 = D0(1+G+i) / (R + i − (G + i)) = D0(1+G) / (R − G)
```
so **expected inflation cancels out** *if and only if* (a) inflation is correctly anticipated, (b) nominal `r` and `g` both move one-for-one with `i`, and (c) the *real* required return `R` and *real* growth `G` are unaffected by inflation. Equity prices are inflation-neutral only under these three conditions; each is frequently violated [S324].

**Equity (discount-rate) duration [S327]**
```
DDR0 = ∫₀^∞ t·E[~c_t]·e^(−k t) dt  /  P0 ,   with P0 = ∫₀^∞ E[~c_t]·e^(−k t) dt
```
For the Gordon model, `DDR = 1/(k − g)`. Lower `k` ⇒ longer duration ⇒ greater sensitivity to subsequent rate changes.

**Campbell–Shiller log-linear present-value identity (intuition)**
`log(P_t) − log(D_t) ≈ const + Σ ρ^j E_t[ (Δd_{t+1+j}) − r_{t+1+j} ]` — i.e. the price–dividend (and hence P/E) ratio is a function of expected *real* cash-flow growth and expected *real* returns, not of nominal rates per se. This is the framework Sharpe (1999) extends with analyst earnings forecasts to study inflation [S320].

## Worked example / code
Pure-stdlib illustration of the two robust mechanics: equity duration expands as rates fall, and the Fed-model fallacy (real E/P compared to nominal yield). **Data: synthetic/illustrative; no external data required. Verified on CPython 3.14.4.**

```python
# Equity duration & the discount-rate channel (Gordon model)
def equity_duration(k, g, D0=1.0):
    DDR = 1.0 / (k - g)                  # Schroeder & Esterer (Gordon case)
    P0  = D0 * (1 + g) / (k - g)
    return DDR, P0

kA, gA = 0.09, 0.04                       # higher-rate regime
kB, gB = 0.05, 0.03                       # lower-rate regime (same ~4-5pp real spread)
dA, pA = equity_duration(kA, gA)
dB, pB = equity_duration(kB, gB)
print(f"High-rate: k={kA:.02f} g={gA:.02f} -> duration={dA:.1f}y  P0={pA:.2f}")
print(f"Low-rate:  k={kB:.02f} g={gB:.02f} -> duration={dB:.1f}y  P0={pB:.2f}")
print(f"Duration expands {dB/dA:.2f}x as rates fall; price rises {pB/pA-1:+.1%}")

# P/E sensitivity to the discount rate (illustrative constant-growth P/E = (1+g)/(r-g))
def pe(r, g):
    return (1 + g) / (r - g)

r1, r2, g = 0.08, 0.06, 0.02             # discount rate drops 2pp
print(f"\nP/E at r={r1:.02f}: {pe(r1,g):.1f}")
print(f"P/E at r={r2:.02f}: {pe(r2,g):.1f}  ({(pe(r2,g)/pe(r1,g)-1):+.1%} for a 2pp drop in r)")

# The Fed-model fallacy: compare a REAL earnings yield to a NOMINAL bond yield
nominal_y = 0.04                          # 10y Treasury
inflation = 0.02
real_y    = nominal_y - inflation         # ~Fisher approximation (TIPS proxy)
ep = 1.0 / pe(r2, g)                      # real earnings yield from the equity model
print(f"\nE/P (real, from equity model) = {ep:.4f}")
print(f"Nominal 10y Y = {nominal_y:.4f} -> Fed model says {'CHEAP' if ep>nominal_y else 'EXPENSIVE'}")
print(f"Real (TIPS) Y = {real_y:.4f} -> correct comparison says {'CHEAP' if ep>real_y else 'EXPENSIVE'}")
```

Expected output (mechanics, not market forecasts):
```
High-rate: k=0.09 g=0.04 -> duration=20.0y  P0=20.80
Low-rate:  k=0.05 g=0.03 -> duration=50.0y  P0=51.50
Duration expands 2.50x as rates fall; price rises +147.6%

P/E at r=0.08: 17.0
P/E at r=0.06: 25.5  (+50.0% for a 2pp drop in r)

E/P (real, from equity model) = 0.0392
Nominal 10y Y = 0.0400 -> Fed model says EXPENSIVE
Real (TIPS) Y = 0.0200 -> correct comparison says CHEAP
```
The last block is the key teaching point: comparing a real earnings yield to a nominal bond yield (the Fed model) falsely flags equities as "expensive" when inflation is positive, because the nominal yield embeds expected inflation that the real earnings yield does not.

## Assumptions & limitations
- The Gordon/DDM mechanic requires `r > g` in perpetuity and stable growth — violated for negative or hyper-growth firms, and `g` must stay below the discount rate or value is infinite.
- Inflation-neutrality holds **only** if inflation is anticipated and real `R` and `G` are unchanged (seldom true; high inflation correlates with higher real risk premia and lower real growth) [S324].
- The equity-duration figures are model-dependent (Gordon / residual-income assumptions); the *qualitative* "low rates ⇒ longer duration ⇒ more rate-sensitivity" is robust, but exact year-counts are illustrative [S327, S328].
- All empirical inflation/return statistics are in-sample historical averages; **past inflation regimes need not repeat**, and the 1948–2020 US sample is one realization.
- The code uses no live data; it demonstrates mechanics only, not a tradable signal.

## Empirical evidence
- **Sharpe (Fed, 1999)** using analyst forecasts in a Campbell–Shiller framework: P/E ratios are strongly negatively related to expected inflation; a 1pp rise in expected inflation is associated with ~1pp higher required *real* stock return and therefore ~20% lower stock prices — but the inflation component of returns is largely shared with long-bond yields, so expected inflation has little effect on the *equity premium* [S320].
- **Campbell & Vuolteenaho (2004):** inflation explains ~80% of the time-series variation in estimated stock-market mispricing, supporting the Modigliani–Cohn inflation-illusion story [S323].
- **Asness (2003):** the Fed model is a failed predictive tool; `E/P` is real and should be compared to real yields; the model has descriptive power only when conditioned on volatility [S321].
- **AllianceBernstein (2021):** since 1948, US stocks returned ~2.7%/quarter when inflation was 2–4%, falling to ~1.0%/quarter when inflation exceeded 4% [S325].
- **MSCI Barra (2008):** US equities returned ~7.6%/yr vs ~4% CPI since 1970 (long-run hedge), but failed to beat inflation in several shorter windows; value/earnings-yield and commodity-producer exposures were resilient in the 1970s inflation episodes [S326].
- **Arnott & Ryan (2001):** at 2000 valuation levels, forward real equity returns were estimated near 3.2% vs an 8.4% historical real return, with the forward equity risk premium near zero/negative — a duration-and-yield argument about diminishing forward returns [S322].
- **CFA Institute review (Wilcox 2012):** synthesizes the literature — a negative stock–inflation relation at business-cycle horizons (Bodie 1976; Fama & Schwert 1977) vs rough long-run neutrality (Siegel; Jaffe & Mandelker 1976) [S324].

## Conflicting views
- **Is the Fed model valid?** Practitioners/strategists use it routinely; Asness (2003) and Campbell–Vuolteenaho (2004) show it is logically inconsistent (real vs nominal) and has no out-of-sample return-predictive power [S321, S323]. The "debate" is essentially settled among academics; it survives as a descriptive story.
- **Do stocks hedge inflation?** Long-run: roughly yes (MSCI, Siegel). Short-run: clearly no (Bodie, Fama–Schwert). The resolution is horizon-dependent [S324, S326].
- **Do low rates justify high multiples?** The discount-rate/duration channel says yes in level; but Asness warns the *nominal*-rate justification is wrong (compare to real rates), and Arnott & Ryan warn that very high multiples imply very low forward returns regardless of the rate level [S321, S322].
- **Is the inflation–valuation link rational or behavioral?** Inflation-illusion (Modigliani–Cohn; Campbell–Vuolteenaho) vs a fully rational dynamic-general-equilibrium explanation (Wei 2010, cited in Wilcox 2012) that can generate a positive dividend-yield/inflation correlation without money illusion [S323, S324].

## Common mistakes
- **Fed-model error:** comparing a real earnings yield `E/P` to a nominal Treasury yield `Y`. Use real (TIPS) yields for any yield-based cheapness claim [S321].
- **"Low rates justify any multiple":** duration rises as rates fall, but that does not make an infinite multiple rational; `r > g` must hold and forward returns compress as multiples expand [S322].
- **Treating equities as a short-horizon inflation hedge:** they are not; the negative business-cycle-horizon relation is well documented [S324].
- **Forgetting nominal earnings already embed inflation:** a firm with pricing power grows nominal earnings with inflation, which is exactly why the real/real comparison cancels inflation [S324].
- **Hindsight/survivorship:** "stocks always beat inflation" leans on the long US sample and ignores episodes (1973–74, 1977–80, 2022) where real returns were sharply negative [S326].

## Further reading
- **Tier 1 (primary/opened):** Sharpe (1999), *Reexamining Stock Valuation and Inflation*, Federal Reserve FEDS paper [S320]; Asness (2003), *Fight the Fed Model*, JPM/AQR [S321]; Campbell & Vuolteenaho (2004), *Inflation Illusion and Stock Prices*, AER/NBER w10263 [S323]; Wilcox (2012), *Equity Valuation and Inflation: A Review*, CFA Institute Research Foundation [S324]; Schroeder & Esterer, *A new measure of equity and cash flow duration* (working paper) [S327].
- **Tier 2 (practitioner/opened):** Arnott & Ryan (2001), *The Death of the Risk Premium*, JPM/Research Affiliates [S322]; AllianceBernstein (2021), *Stocks Can Surmount a Return of Inflation* [S325]; MSCI Barra (2008), *Hedging Inflation with Equities* [S326]; Golez & Koudijs (2025), *Equity duration and predictability*, Journal of Finance (via Alpha Architect summary) [S328].
- **Foundational (cited, not opened this iteration):** Modigliani & Cohn (1979), *Inflation, Rational Valuation, and the Market*; Campbell & Shiller (1988), *Stock Prices, Earnings, and Expected Dividends*; Ritter & Warr (2002), *The Decline of Inflation and the Bull Market of 1982–1999*; Bhamra, Kuehn & Strebulaev (2023), *High Inflation: Low Default Risk and Low Equity Valuations*, RFS (peer-reviewed; abstract seen, full text not opened — flag before asserting magnitudes).
