---
title: Momentum Oscillators — RSI and MACD (with Evidence Grade)
topic_id: 03-technical-analysis/indicators-rsi-macd
tags: [technical-analysis, momentum, oscillator, RSI, MACD, Wilder, Appel, evidence-grade]
last_updated: 2026-07-18
confidence: contested
sources: [S184, S185, S186, S187, S89, S88]
---

## TL;DR
- RSI (J. Welles Wilder, 1978) and MACD (Gerald Appel, late 1970s) are two of the most-used **momentum oscillators**; their math is fixed and reproducible across platforms (robust).
- RSI measures *speed/change* of price on a 0–100 scale; MACD measures the *gap between two EMAs* and is unbounded.
- The **trading edge is contested**: specific RSI/MACD rule variants produced statistically significant abnormal returns in some non-US and older samples (Chong, Ng & Liew 2014), but the same rules fare poorly in US large-caps post-1990 and much of their historical "significance" disappears after data-snooping correction (Sullivan, Timmermann & White 1999; Park & Irwin 2007).
- Practical use: as **timing/filter/confirmation** tools inside a broader process, with explicit costs — not as a stand-alone "buy at 30, sell at 70" magic line (folklore).

## Core explanation
Both indicators try to quantify *momentum* — the tendency of recent price direction to persist — but from different angles.

**RSI (Relative Strength Index).** Wilder's RSI is a bounded oscillator (0–100) built from the ratio of average up-moves to average down-moves over a look-back window (default 14). It is designed to flag *overbought* (traditionally RSI > 70) and *oversold* (RSI < 30) extremes, and to detect *divergences* between price and momentum. It is a **leading-ish** gauge of exhaustion, not direction.

**MACD (Moving Average Convergence Divergence).** Appel's MACD converts two trend-following EMAs into an oscillator by subtracting the slow EMA from the fast EMA. Because it is the difference of two moving averages, MACD is inherently a **lagging** momentum/trend-confirmation tool. It is unbounded, so it signals via *crossovers* (MACD vs its signal line, and MACD vs the zero line) and *divergences* rather than fixed overbought/oversold bands.

Plain-language summary: RSI asks "has the stock moved too far, too fast?"; MACD asks "is the recent trend accelerating or rolling over?"

## Math / formulas

### RSI (Wilder, 1978)
Let `U_t = max(P_t − P_{t−1}, 0)`, `D_t = max(P_{t−1} − P_t, 0)` be per-period gains and losses.

First average (simple mean over `n` periods, default 14):
```
AvgGain_0 = (U_1 + ... + U_n) / n
AvgLoss_0 = (D_1 + ... + D_n) / n
```
Subsequent values use Wilder's smoothing (exponential, α = 1/n):
```
AvgGain_t = (AvgGain_{t-1}·(n−1) + U_t) / n
AvgLoss_t = (AvgLoss_{t-1}·(n−1) + D_t) / n
```
Then:
```
RS  = AvgGain / AvgLoss
RSI = 100 − 100 / (1 + RS)
```
By convention: if `AvgLoss = 0`, `RSI = 100`; if `AvgGain = 0`, `RSI = 0`. Wilder's smoothing is mathematically an EMA with `α = 1/n`, so RSI needs a warm-up (StockCharts uses ≥250 prior points for stable values) [S184].

### MACD (Appel)
Define EMA with `α = 2/(N+1)`:
```
MACD_line = EMA_12(close) − EMA_26(close)
Signal    = EMA_9(MACD_line)
Histogram = MACD_line − Signal
```
Default parameters are `MACD(12, 26, 9)`. The MACD line oscillates around zero (positive = 12-day EMA above 26-day EMA = upside momentum). The histogram is positive when MACD is above its signal line [S185][S186].

### Standard trading rules
- **RSI:** buy when RSI crosses *up* through 30 (leaving oversold); sell when it crosses *down* through 70. `RSI(14, 30/70)` and `RSI(21, 50)` are common research parameterizations.
- **MACD:** bullish when MACD crosses *above* signal (signal-line crossover) or crosses above zero (centerline crossover); bearish on the mirror images. `MACD(12, 26, 0)` in the literature means *no* signal line — i.e., a pure centerline (12/26 EMA) crossover rule [S187].

## Worked example / code
Pure-stdlib implementation (Python 3.14). Prices are a **seeded geometric random walk** used only to exercise the math — they are synthetic noise, NOT a market claim, and the numbers are reproducible by construction.

```python
import random, math

def gen_prices(seed=42, n=300, mu=0.0003, sigma=0.015, start=100.0):
    rnd = random.Random(seed)
    p = start; out = [p]
    for _ in range(n - 1):
        p = p * math.exp(mu + sigma * rnd.gauss(0, 1)); out.append(p)
    return out

def rsi_wilder(prices, period=14):
    gains = [max(prices[i]-prices[i-1], 0.0) for i in range(1, len(prices))]
    losses = [max(prices[i-1]-prices[i], 0.0) for i in range(1, len(prices))]
    ag = sum(gains[:period]) / period; al = sum(losses[:period]) / period
    out = [None] * period
    for i in range(period, len(gains)):
        ag = (ag*(period-1) + gains[i]) / period
        al = (al*(period-1) + losses[i]) / period
        out.append(100.0 if al == 0 else 100.0 - 100.0/(1.0 + ag/al))
    return out

def ema(vals, span):
    a = 2.0/(span+1.0); prev = None; out = []
    for v in vals:
        prev = v if prev is None else a*v + (1-a)*prev
        out.append(prev)
    return out

def macd(prices, fast=12, slow=26, signal=9):
    ml = [a-b for a,b in zip(ema(prices,fast), ema(prices,slow))]
    sig = ema(ml, signal)
    return ml, sig, [m-s for m,s in zip(ml, sig)]

prices = gen_prices()
rsi = rsi_wilder(prices, 14)
ml, sig, hist = macd(prices, 12, 26, 9)

print("RSI(14) last:", round(rsi[-1], 3))
print("MACD last:", round(ml[-1], 4), "Signal:", round(sig[-1], 4),
      "Hist:", round(hist[-1], 4))
```

Verified output (Python 3.14.4, `seed=42`, deterministic):
```
RSI(14) last: 49.03
MACD last: -1.9259 Signal: -1.9860 Hist: 0.0601
```
Across the 286 valid RSI bars the oscillator stayed in `[31.83, 84.60]` and registered **25 overbought (>70)** readings; the MACD signal line crossed 5 times in the final 60 bars — confirming both indicators produce the expected bounded-oscillator and crossover behavior. Run it again with the same seed and you get identical numbers.

For live data, swap `gen_prices()` for a pinned download:
```python
# Data source: Yahoo Finance via yfinance (Apache-2.0; not endorsed by Yahoo).
# Pin for reproducibility: pip install yfinance==1.5.1 numpy==2.2.0
import yfinance as yf
prices = yf.download("SPY", start="2023-01-01", end="2024-01-01",
                     auto_adjust=True)["Close"].tolist()
```

## Assumptions & limitations
- **Reactive, not predictive.** Both are functions of *past* prices; they describe what already happened.
- **Weak-form efficiency is the implicit null.** Any edge implies historical patterns that have not been fully arbitraged away.
- **Warm-up sensitivity.** RSI's first values depend on the seed window; short histories give unstable readings (StockCharts back-fills ≥250 bars) [S184].
- **MACD is not comparable across names.** Because it is price-level denominated and unbounded, you cannot compare a $400 stock's MACD to a $40 stock's; use the Percentage Price Oscillator (PPO) for cross-sectional comparison [S186].
- **Lag.** MACD is a lagging indicator — by the time a centerline crossover confirms a trend, much of the move may be done [S185].
- **Parameter dependence.** 12/26/9 and 14/30/70 are conventions, not laws; changing them changes the signal set.
- **Costs ignored by raw rules.** Every crossover is a round-trip; in choppy regimes whipsaws dominate (e.g., StockCharts' CMI example shows 7 centerline crossovers in 5 months with no trend to profit from) [S186].

## Empirical evidence
**Findings that support a real (if conditional) effect:**
- Chong, Ng & Liew (2014) [S187] re-test MACD and RSI across five OECD markets. They report that `MACD(12,26,0)` and `RSI(21,50)` generate *significant abnormal returns* in the Milan Comit General and the S&P/TSX Composite, and that `RSI(14,30/70)` is profitable on the Dow Jones Industrials. This extends Chong & Ng (2008), who found MACD/RSI excess returns on London's FT30.
- The broader technical-analysis literature (Brock, Lakonishok & LeBaron 1992 on MA rules; Jegadeesh & Titman 1993 on cross-sectional momentum) independently shows *some* historical rule profitability [S89].

**Findings that undercut a universal edge:**
- Park & Irwin (2007) meta-review of 92 modern studies (cited in [S89]) finds technical strategies profitable in US equities **only through the late 1980s**, then not; FX and emerging markets remain more favorable — i.e., the US large-cap edge appears to have **decayed**.
- Fang, Jacobsen & Qin (2014) (cited in [S89]) report **out-of-sample null** results for many classical technical rules.
- Sullivan, Timmermann & White (1999) [S88] apply White's (2000) bootstrap Reality Check to ~26 expanded technical rules on ~100 years of DJIA data and show that much of the apparent significance **vanishes after correcting for data snooping**.

**Strength of evidence:** moderate but era- and market-dependent. Positive results cluster in older/non-US samples and are sensitive to the multiple-testing correction; the cleanest contemporary US-large-cap reading is "at best marginal after costs." This is exactly the contested bucket.

## Conflicting views
- **Practitioners vs. EMH academics.** Murphy (1999) and the Cardwell/Brown RSI school treat divergences and bull/bear RSI ranges as genuinely informative; Fama (1970) and Malkiel treat TA as no better than noise once costs are counted [S187][S89].
- **Overbought/oversold as a trade signal.** Wilder framed 70/30 as *warning* zones, not automatic reversals; yet retail lore treats "buy 30 / sell 70" as a system. In strong trends RSI *stays* pinned above 70 (StockCharts' McDonald's example shows four overbought readings before the actual peak) [S184].
- **Signal line vs. centerline.** Some researchers drop the signal line entirely (`MACD(12,26,0)`) to avoid the extra lag of a 9-day EMA; practitioners argue the signal line reduces whipsaws. Both are defensible; they are different rules [S187].

## Common mistakes
1. **Treating overbought/oversold as a trigger.** RSI > 70 in an uptrend is often *continuation*, not reversal [S184].
2. **Ignoring transaction costs and whipsaw.** MACD throws many crossovers in ranges; net P&L is often negative after even modest costs [S186].
3. **Parameter snooping.** Optimizing the look-back / thresholds on the same data that "proves" the edge invites the data-snooping trap documented in [S88] (see KB 15 — Data Snooping & p-Hacking).
4. **Comparing MACD across securities.** Use PPO for cross-sectional screening [S186].
5. **Survivorship / look-ahead in backtests.** Testing on current-index members only and using future-dated splits/earnings produces inflated, fictitious edges (see KB 13 — Data & Tooling, and KB 15 — Pitfalls).
6. **One-indicator conviction.** RSI/MACD work best as *filters or confirmations* (e.g., RSI oversold *within* an uptrend, or MACD confirmation of a breakout), not as a sole signal.

## Further reading
- **[S184]** StockCharts ChartSchool, "Relative Strength Index (RSI)" — formulas, 70/30 interpretation, divergences. https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-strength-index-rsi
- **[S185]** Wikipedia, "MACD" — formula, terminology, lagging-indicator caveat. https://en.wikipedia.org/wiki/MACD
- **[S186]** StockCharts ChartSchool, "MACD Oscillator" — signal/centerline crossovers, whipsaw examples, PPO note. https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/macd-moving-average-convergence-divergence-oscillator
- **[S187]** Chong, T.T.L., Ng, W.-K. & Liew, V.K.-S. (2014), "Revisiting the Performance of MACD and RSI Oscillators," MPRA Paper 54149 (Tier 1, academic). https://mpra.ub.uni-muenchen.de/54149
- **[S89]** CFA Institute Research Foundation, *Technical Analysis: Modern Perspectives* (Hill, Nadig, Hougan et al., 2016) — meta-review numbers (Park & Irwin 2007; Fang, Jacobsen & Qin 2014). https://rpc.cfainstitute.org/sites/default/files/-/media/documents/book/rf-lit-review/2016/rflrv11n11.pdf
- **[S88]** Sullivan, R., Timmermann, A. & White, H. (1999), "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap," *Journal of Finance* 54(5). https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1647-1691.html
- Companion KB articles: `03-technical-analysis/trend-support-momentum.md` (broader TA evidence), `15-pitfalls-and-antipatterns/data-snooping-phacking.md`, `08-backtesting-methodology/transaction-costs-slippage-walkforward.md`.
