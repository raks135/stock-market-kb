---
title: Macroeconomic Regimes, Interest Rates, and the Business Cycle
topic_id: 11-macro-and-regimes/rates-business-cycles-sector-rotation
tags: [macro, business-cycle, yield-curve, interest-rates, inflation, sector-rotation, regimes, NBER]
last_updated: 2026-07-18
confidence: robust
sources: [S130, S131, S132, S133, S134, S135, S136, S137, S138]
---

## TL;DR
- A U.S. **recession is an NBER call** — a broad, deep, persistent decline in activity — **not** the popular "two consecutive quarters of negative GDP" rule. NBER announcements also arrive with a long lag (the Apr-2020 trough was dated Jul-2021), so they are useless for real-time trading (S130).
- Long-term interest rates are a **discount-rate input to every valuation**: rising real rates mechanically depress equity values, and the effect is *larger* for long-duration (high expected-growth) stocks. But the move can be offset by the growth news that caused rates to rise (S132).
- The **yield-curve slope** (10y–3m or 10y–2y) is a statistically real recession harbinger, but it gives long, noisy lead times (often 6–18 months) and is not a golden rule (S133, S138).
- **Sector rotation** (cyclicals early-cycle, defensives late-cycle) is intuitive and episode-supported, but its *exploitable* edge is contested and the cycle is only known in hindsight (S134).
- Headline macro variables are **weak equity-return predictors out-of-sample**: Goyal–Welch (2008) found most fail to beat the historical mean. Treat macro as *risk context*, not a timing signal (S135).

## Core explanation
Macroeconomics describes the "weather" in which individual stocks operate. Three channels matter most to an equity investor:

1. **The business cycle** — the alternating expansion and contraction of aggregate economic activity. The NBER's Business Cycle Dating Committee is the arbiter of U.S. peaks and troughs. Its recession definition is qualitative: a "significant decline in economic activity that is spread across the economy and that lasts more than a few months," judged on three criteria — **depth, diffusion, and duration** (S130). It explicitly does *not* use the "two consecutive quarters of negative real GDP" rule (the 2001 recession, for example, did not have two such quarters) (S130).

2. **The discount-rate / rates channel** — equity value is the present value of future cash flows. The discount rate embeds the risk-free rate. When long-term rates rise, the present value of distant cash flows falls. This is why rate moves hit growth/long-duration stocks hardest (S132).

3. **The inflation & policy channel** — inflation feeds into nominal rates. When a central bank runs a *countercyclical* policy (raising rates as inflation rises), higher inflation translates into a higher discount rate and lower equity values; classical monetary theory predicts a negative stock-return/inflation correlation under such regimes (S137).

"Regimes" are persistent states of the world (expansion vs. recession; calm vs. stressed volatility; low vs. high inflation). Detecting them matters because factor performance, correlations, and optimal positioning all shift across regimes — but the detection itself is noisy and backward-looking.

## Math / formulas

**Yield-curve spread (recession signal).**
$$s_t = y_t^{\text{long}} - y_t^{\text{short}}$$
Inversion ⇔ $s_t < 0$. Academic work typically uses the 10-year minus 3-month Treasury spread; many market participants watch 10-year minus 2-year (S133).

**Discount-rate sensitivity (Gordon / constant-growth).**
$$P = \frac{D_1}{r - g}, \qquad \frac{\partial P}{\partial r} = -\frac{D_1}{(r-g)^2} = -\frac{P}{r-g}$$
So the elasticity is
$$\frac{\%\Delta P}{\%\Delta r} \approx -\frac{1}{r-g}$$
Higher expected growth $g$ ⇒ larger magnitude ⇒ **growth stocks are more rate-sensitive**. With $r=8\%,\,g=3\%$, a 1% (100 bp) rise in $r$ cuts price by roughly 20%; with $g=1\%$ the hit is ~14% (S132).

**Inflation–discount channel.** Under a countercyclical central bank,
$$i \approx r^{\text{real}} + \mathbb{E}[\pi] + \text{reaction to } \pi\uparrow \;\Rightarrow\; \text{discount rate} \uparrow \;\Rightarrow\; PV \downarrow$$
IMF (2021) confirms a negative real-stock-return/inflation relation that strengthens with more countercyclical policy; in its panel, the interaction `expected inflation × countercyclical-policy dummy` carries a significantly negative coefficient (≈ −4.5, p<0.01) (S137).

**Markov-switching regime model (Hamilton 1989).** Let the unobserved state $s_t \in \{0,1\}$ follow a first-order Markov chain with transition matrix
$$P = \begin{pmatrix} p_{00} & p_{01} \\ p_{10} & p_{11} \end{pmatrix}, \quad p_{ij} = \Pr(s_t=j \mid s_{t-1}=i)$$
and the observation (e.g., return or GDP growth) have a regime-dependent distribution, e.g. $r_t \sim \mathcal{N}(\mu_{s_t}, \sigma^2_{s_t})$. Parameters are estimated by (quasi-)maximum likelihood / EM (Baum–Welch); the most-likely state path by the Viterbi algorithm (S136). The novelty vs. a one-off structural break is that switches are *recurrent and autocorrelated in time* (S136).

**Sector-rotation map (heuristic).** Early cycle (recovery): cyclicals — Consumer Discretionary, Technology, Financials, Industrials. Mid/late cycle: maturing growth, Energy, Materials. Late cycle / recession: defensives — Utilities, Consumer Staples, Health Care. The cycle is driven by three sub-cycles: the corporate-profit cycle, the credit cycle, and the inventory cycle (S134).

## Worked example / code
Two reproducible, **pure-stdlib** demos (Python 3, no external packages). Part 1 flags yield-curve inversions from a short yield series; Part 2 builds a simple **volatility-regime detector** (rolling standard deviation + top-quartile "stressed" cutoff) — a real practitioner filter standing in for a full Markov-switching model.

```python
import math, random

# ---- Part 1: 10y-2y Treasury spread flag (illustrative yields, %). ----
# Concept: Investopedia (10y-3m academic, 10y-2y investor proxy), CNBC 2022.
ten_year = [1.5, 1.6, 1.9, 2.3, 2.5, 2.33, 2.5, 2.8, 3.0, 2.9]
two_year = [1.2, 1.3, 1.5, 1.9, 2.2, 2.337, 2.4, 2.6, 2.7, 2.95]
spread = [round(a - b, 3) for a, b in zip(ten_year, two_year)]
inverted = [s < 0 for s in spread]
print("10y-2y spread (%):", spread)
print("inverted flags:   ", inverted)

# ---- Part 2: heuristic volatility-regime detector (rolling std + top quartile). ----
def rolling_std(x, win=12):
    out = []
    for i in range(len(x)):
        seg = x[max(0, i + 1 - win):i + 1]
        m = sum(seg) / len(seg)
        out.append(math.sqrt(sum((s - m) ** 2 for s in seg) / len(seg)))
    return out

# Synthetic monthly returns: 120 calm months then 40 crisis (high-vol, negative) months.
random.seed(42)
calm = [random.gauss(0.010, 0.008) for _ in range(120)]
crisis = [random.gauss(-0.010, 0.040) for _ in range(40)]
rets = calm + crisis

vol = rolling_std(rets, win=12)
threshold = sorted(vol)[int(0.75 * len(vol))]      # flag highest-vol quartile as "stressed"
regime = [1 if v > threshold else 0 for v in vol]  # 1 = high-vol / "stressed"
crisis_hit = sum(1 for i in range(120, 160) if regime[i] == 1)
calm_hit = sum(1 for i in range(120) if regime[i] == 0)
print(f"\nStressed (top-quartile) vol threshold: {threshold:.4f}")
print(f"True crisis months (last 40): {crisis_hit}/40 flagged high-vol")
print(f"True calm   months (first120): {calm_hit}/120 flagged low-vol")
```

**Verified output (Python 3.14, seed 42):**
```
10y-2y spread (%): [0.3, 0.3, 0.4, 0.4, 0.3, -0.007, 0.1, 0.2, 0.3, -0.05]
inverted flags:    [False, False, False, False, False, True, False, False, False, True]

Stressed (top-quartile) vol threshold: 0.0094
True crisis months (last 40): 39/40 flagged high-vol
True calm   months (first120): 120/120 flagged low-vol
```
The detector recovers the stressed block almost perfectly — illustrating that a simple volatility filter separates regimes, but the single missed month shows the boundary is fuzzy (a real limitation, not a bug).

**Data source.** Replace the synthetic returns with real series from **FRED** (Federal Reserve Economic Data, fred.stlouisfed.org): e.g., `DGS10`/`DGS2`/`DGS3MO` for yields, `SP500` for returns, and NBER/BCDM recession dummies for labels. All are free and live.

## Assumptions & limitations
- **Non-stationarity.** Every relationship here (rate→valuation, curve→recession, inflation→returns, factor performance) is *sample-dependent* and can break (S135, S137).
- **NBER lag.** Recession dates are announced months-to-years after the fact (Apr-2020 trough → Jul-2021 call), so they cannot drive real-time decisions (S130).
- **Curve signal needs persistence.** A brief "flash" inversion is not the signal; practitioners want a *sustained* inversion, and the chosen maturity pair changes the read (S133, S138).
- **Discount-rate channel assumes stable cash-flow expectations.** If rates rise *because* growth expectations rose, the cash-flow uplift can offset the discount-rate drag — the "facile" higher-rates-are-bad story is incomplete (S132).
- **Sector rotation needs hindsight.** Correctly placing "today" in the cycle is the hard part; mistiming costs the spread (S134).
- **Regime detectors lag.** Rolling-window and MSM filters identify regimes after they begin; they are risk-management aids, not crystal balls.

## Empirical evidence
- **Business cycle.** NBER has dated U.S. cycles since 1854; expansions are the normal state and most recessions are brief, though the recovery to prior peak can be long (e.g., payroll employment did not exceed its pre-2007-12 peak until 2014) (S130, S131).
- **Yield curve.** Inversions have preceded every U.S. recession since the late 1950s. CNBC (2022), citing Bespoke, reports a 2s10y inversion implies a >2/3 chance of recession within a year and >98% within two years — but with long, variable leads (163–571 days ahead of the last three recessions) and at least one false alarm (1998) (S138). Academic studies favor the 10y–3m spread; some argue the 3m–10y is the more accurate forecaster (S133, S138).
- **Rates & valuation.** Damodaran's framework shows PE ratios fall as rates rise, with growth stocks falling more — consistent with the $-1/(r-g)$ elasticity. He stresses the Fed does not "set" long rates; inflation and real growth do (S132).
- **Inflation & equities.** IMF (2021), using 71 economies over 35 years, finds real stock returns are negatively related to inflation, *more so* under countercyclical policy and in inflation-targeting regimes; the effect vanishes at the Zero Lower Bound (S137). This aligns with the classic Fama (1981) result that the raw inflation–return correlation is negative but partly a proxy for real-activity swings.
- **Sector rotation.** The intuition (cyclicals lead early, defensives lead late) is widely taught (S134). A 2020 Journal of Asset Management study found sector-rotation strategies can beat benchmarks in the US and Europe, but results depend heavily on the switching signal and costs (mixed/emerging evidence).
- **Macro return predictability.** Goyal–Welch (2008) tested 17 variables claimed to time the equity premium and found **none reliably beat the historical mean out-of-sample**; Welch's 2023 update across ~45 variables concluded "70–80% poof" and that he could not confidently recommend market timing (S135). This is one of the most robust negative findings in empirical finance.

## Conflicting views
- **"Higher rates are always bad for stocks"** vs. Damodaran: the net effect depends on *why* rates rise; growth-driven rate rises can leave indexes resilient (S132).
- **Yield-curve maturity pair.** 10y–2y (most-watched) vs. 10y–3m (academic) vs. 3m–10y (arguably most accurate); each gives different timing and false-signal rates (S133, S138).
- **Sector rotation: free lunch or folklore?** Intuitive and episode-supported, but the exploitable alpha is contested once costs and mistiming are counted (S134).
- **Macro timing: possible or futile?** Goyal–Welch say futile out-of-sample (S135); others argue specific signals (credit conditions, short-interest, nearness-to-high) show weak but real OOS power. The weight of evidence favors humility (S135).
- **Inflation hedge.** Stocks are *not* a reliable inflation hedge in the short run; the negative relation is strongest under countercyclical policy and can flip across regimes (S137).

## Common mistakes
- **Using the "two quarters of negative GDP" rule as the recession definition.** It is a press shorthand, not the NBER standard (S130).
- **Treating an inversion as a precise sell signal.** Leads are long and variable; the S&P 500 has historically been *up* 6–18 months after inversions before peaking (S138).
- **Conflating correlation with causation on inflation.** The negative stock/inflation link is partly a real-activity proxy and regime-dependent (S137).
- **Assuming sector rotation is easy.** The cycle is labeled only in hindsight; acting on a guessed cycle position is a coin flip dressed as analysis (S134).
- **Using macro variables as market-timing signals.** Out-of-sample they mostly fail; size positions accordingly (S135).
- **Ignoring regime non-stationarity.** A factor or correlation that held last cycle can invert next cycle — backtests that don't respect regimes overstate edge (ties to KB 05-stats, 08-backtesting, 15-pitfalls).

## Further reading
- **S130** NBER, *Business Cycle Dating Procedure: FAQ* — https://www.nber.org/research/business-cycle-dating/business-cycle-dating-procedure-frequently-asked-questions (Tier 1)
- **S131** St. Louis Fed, *All About the Business Cycle* — https://www.stlouisfed.org/publications/page-one-economics/2023/03/01/all-about-the-business-cycle-where-do-recessions-come-from (Tier 1)
- **S132** Damodaran, *Interest Rates, Earning Growth and Equity Value* (Musings on Markets, 2021) — https://aswathdamodaran.blogspot.com/2021/03/rates-growth-and-value-investment.html (Tier 1)
- **S133** Investopedia, *Inverted Yield Curve* — https://www.investopedia.com/terms/i/invertedyieldcurve.asp (Tier 2)
- **S134** Fidelity, *Intro to Sector Rotation Strategies* — https://www.fidelity.com/learning-center/trading-investing/markets-sectors/intro-sector-rotation-strats (Tier 2)
- **S135** Goyal & Welch (2008), *A Comprehensive Look at the Empirical Performance of Equity Premium Prediction*, RFS 21(4); Welch (2023) update — https://ivo-welch.org/research/presentations/99-stanford-prediction.pdf (Tier 1)
- **S136** Hamilton (1989), *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle*, Econometrica 57(2); Kuan (2002) lecture notes — https://homepage.ntu.edu.tw/~ckuan/pdf/Lec-Markov_note_spring%202010.pdf (Tier 1 / Tier 2)
- **S137** IMF Working Paper 2021/219, *Stock Returns and Inflation Redux* — https://www.elibrary.imf.org/view/journals/001/2021/219/article-A001-en.xml (Tier 1)
- **S138** CNBC, *2-year tops 10-year — yield curve inversion* (2022) — https://www.cnbc.com/2022/03/31/2-year-treasury-yield-tops-10-year-rate-a-yield-curve-inversion-that-could-signal-a-recession.html (Tier 2)
- Related KB: 03-technical-analysis (trend/momentum), 04-quant-and-factors (Fama–French, factors), 05-stats-and-ml (stationarity, regimes), 06-portfolio-construction, 08-backtesting-methodology, 15-pitfalls (look-ahead, non-stationarity).
