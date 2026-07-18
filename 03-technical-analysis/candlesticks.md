---
title: Candlestick Patterns (Evidence Grade)
topic_id: 03-technical-analysis/candlesticks
tags: [technical-analysis, candlesticks, chart-patterns, market-efficiency, japanese-charting]
last_updated: 2026-07-18
confidence: contested
sources: [S201, S202, S203, S204, S88, S93, S190, S191]
---

## TL;DR
- A candlestick is just an OHLC bar drawn as a "body" (open–close) plus "shadows" (high/low); it is a *visualization*, not a signal. The construction is robust and useful (S203, S204).
- As standalone trading systems, candlestick patterns **fail to beat random/buy-and-hold after proper bootstrap testing** in developed large-cap equity markets (Marshall, Young & Rose 2006, S201; Sullivan, Timmermann & White 1999 bootstrap, S88).
- A handful of studies find *short-lived, pattern-specific, market-specific* predictive ability (e.g., a statistically significant 5-day excess return after a shooting star in one NYSE sample, Yatrakis & Williams 2008, S202). Treat this as **emerging**, not robust.
- The realistic edge (if any) comes from using patterns *in context* (trend, support/resistance, volume) as a timing filter — not as a clairvoyant system. Net-of-cost profitability is contested.

## Core explanation

### What a candlestick is
A candlestick depicts the four prices of one period (day, hour, minute): **open (O), high (H), low (L), close (C)**. The wide central rectangle is the **real body** — it is black/red when `C < O` (bearish) and white/green when `C > O` (bullish). The thin lines above and below are the **shadows** (or wicks), showing the period's high and low (Investopedia, S203; StockCharts, S204). The technique was developed by Japanese rice merchants in the 1700s (Munehisa Homma, Dojima rice exchange) and popularized in the West by Steve Nison in the late 1980s/early 1990s (Yatrakis & Williams 2008, S202).

### Common patterns (mechanics)
All are defined by the *shape* and, critically, by the *trend context* in which they appear:

- **Doji** — `O ≈ C`; open and close virtually equal. Conveys indecision / tug-of-war between buyers and sellers (StockCharts, S204).
- **Hammer** — price sells off after the open then rallies to close well above the intraday low; looks like a "square lollipop" with a long lower shadow. Bullish *only when it forms during a decline* (StockCharts, S204; Investopedia, S203).
- **Hanging Man** — *identical shape to a hammer* but forms during an advance; it is the bearish counterpart (StockCharts, S204). Same candle, opposite implication — context is everything.
- **Shooting Star** — small body near the low with a long *upper* shadow; a bearish reversal at the end of an uptrend (Yatrakis & Williams 2008, S202).
- **Bullish/Bearish Engulfing** — a small body day whose body is *completely engulfed* by the next day's body, which closes in the opposite direction of the prevailing trend (StockCharts, S204; Investopedia, S203).
- **Harami** — a small body day entirely *contained within* the prior day's body, opposite color; **Harami Cross** uses a doji for the second day (Investopedia, S203).
- **Morning Star / Evening Star** — three-day reversals (bullish / bearish): a long trend-day, a gapped narrow day, then a strong close back across the midpoint of the first day (Investopedia, S203).

### The evidence question
Two separate claims get conflated:
1. **Informativeness** — do patterns carry *any* statistical information about future returns? Lo, Mamaysky & Wang (2000, S190) showed that formally detected head-and-shoulders and other patterns *do* alter the conditional distribution of subsequent returns (a real, weak effect).
2. **Tradable, net-of-cost profitability** — can you make money trading them? This is where the academic record is largely negative for standalone use.

## Math / formulas

A candle is the 4-tuple `(O, H, L, C)` with `L ≤ min(O, C) ≤ max(O, C) ≤ H`. Derived quantities:

- Real body: `B = |C − O|`
- Upper shadow: `U = H − max(O, C)`
- Lower shadow: `D = min(O, C) − L`

Heuristic detectors (thresholds are conventions, not laws):

- **Hammer** (bullish, in a downtrend): `D ≥ k·B` (often `k = 2`), `U` small, and `B > 0`.
- **Bullish engulfing**: prior candle bearish (`C_prev < O_prev`), current bullish (`C_cur > O_cur`), and `O_cur ≤ O_prev` and `C_cur ≥ C_prev` (current body covers prior body).
- **Doji**: `B ≤ ε·(H − L)` for a small `ε` (e.g., 0.05–0.1).

Note there is **no single canonical parameterization**; the lack of fixed rules is itself a source of the data-snooping problem (see below).

## Worked example / code

Pure-standard-library detector (Python 3.14, no dependencies). It injects one bullish engulfing and one hammer into a synthetic random-walk series and confirms detection. Data source: synthetic (deterministic via `random.seed(42)`) — this snippet demonstrates *logic*, not a market claim.

```python
import random
from dataclasses import dataclass

@dataclass
class Candle:
    o: float; h: float; l: float; c: float
    def body(self): return abs(self.c - self.o)
    def upper_shadow(self): return self.h - max(self.o, self.c)
    def lower_shadow(self): return min(self.o, self.c) - self.l

def is_hammer(c, body_min=0.5, shadow_mult=2.0, max_upper_frac=0.3):
    b = c.body()
    if b < body_min: return False
    ls, us = c.lower_shadow(), c.upper_shadow()
    return (ls >= shadow_mult * b) and (us <= max_upper_frac * (ls + b))

def is_bullish_engulfing(prev, cur):
    if not (prev.c < prev.o): return False   # prev bearish
    if not (cur.c > cur.o): return False      # cur bullish
    return (cur.o <= prev.o) and (cur.c >= prev.c)  # body fully covers

def make_series(n=40, seed=42):
    random.seed(seed); price = 100.0; out = []
    for _ in range(n):
        o = price; c = o + random.uniform(-1.5, 1.5)
        h = max(o, c) + random.uniform(0.1, 1.2)
        l = min(o, c) - random.uniform(0.1, 1.2)
        out.append(Candle(o, h, l, c)); price = c
    return out

s = make_series(40, seed=42)
s[9]  = Candle(o=98.0,  h=98.5, l=95.0, c=95.5)   # bearish
s[10] = Candle(o=95.0,  h=101.0, l=94.8, c=100.8) # bullish, engulfs
s[20] = Candle(o=102.0, h=102.3, l=96.0, c=101.3) # hammer

hammers, eng = [], []
for i, c in enumerate(s):
    if is_hammer(c): hammers.append(i)
for i in range(1, len(s)):
    if is_bullish_engulfing(s[i-1], s[i]): eng.append(i)

print("hammers:", hammers, "| engulfings:", eng)
```

Verified output (Python 3.14):

```
Detected hammer indices : [20]
Detected engulfing indices: [2, 5, 10, 16, 18, 24, 29, 32, 38]
Injected bullish engulfing at index 10 -> detected: True
Injected hammer at index 20 -> detected: True
Doji flagged as hammer (should be False): False
```

**Important self-check:** the random series throws off *nine* "engulfing" signals with no edge at all. This is exactly why raw pattern counts prove nothing — you must test against a null (bootstrap), as Sullivan et al. (1999, S88) and Marshall et al. (2006, S201) did.

## Assumptions & limitations
- **Patterns are visual, not statistical:** there is no single canonical definition; thresholds are judgment calls, which inflates the number of "patterns" you can test (multiple testing).
- **Context dependence:** a hammer and a hanging man are the *same shape*; the implication flips with the trend. Ignoring context produces garbage signals.
- **Stationarity:** any edge is regime-dependent and non-stationary; a pattern that "worked" in one decade need not work in the next (Park & Irwin 2007, S93, find US technical-rule profitability faded after the late 1980s).
- **Costs dominate churn:** candlestick systems typically trade frequently; bid–ask, commissions, and market impact (see KB 08-backtesting-methodology, 09-market-microstructure) can erase gross signals.
- **Survivorship / look-ahead:** naive backtests over current-index members or using signals computed with future information overstate results (KB 15-pitfalls-and-antipatterns).

## Empirical evidence
- **Robust (negative for standalone use):** Marshall, Young & Rose (2006, S201) test candlestick trading strategies on Dow Jones Industrial Average component stocks (1992–2002) using a bootstrap that randomizes the open/high/low/close series. They conclude candlestick technical analysis "does not create value for investors" in informationally efficient markets; a companion study finds the same for the Japanese equity market (1975–2004).
- **Robust (data-snooping):** Sullivan, Timmermann & White (1999, S88) apply a bootstrap "reality check" to technical rules and show much of the apparent significance vanishes once you account for the fact that the rules were *selected* on the same data.
- **Meta-evidence:** Park & Irwin (2007, S93) survey 92 modern technical-analysis studies — many show profitability, but the US-equity edge is concentrated in pre-late-1980s samples and is stronger in FX and emerging markets.
- **Emerging (positive, narrow):** Yatrakis & Williams (2008, S202) examine the **shooting star** across 257 NYSE stocks (March–April 2005) over 20 subsequent trading days and report a *small but statistically significant excess return over the five days following the pattern* — a short-lived weak-form anomaly. Single pattern, single window, not net-of-cost; treat as suggestive.
- **Informativeness vs profitability (nuance):** Lo, Mamaysky & Wang (2000, S190) find patterns carry genuine *conditional-distribution* information, yet that is distinct from net tradable profit (corroborated by CFA Institute's TA review, S89/S191).
- **Unverified leads (Tier 3, do NOT assert):** several emerging-market studies (e.g., Taiwan Pacific-Basin 2014; a 2025 Nifty-IT student study) report pattern "success rates" of 50–70%, but these are gross, single-sample, and not opened as primaries here — flagged for verification.

## Conflicting views
- **Practitioners (Nison, StockCharts, Investopedia):** candlesticks are a powerful, time-tested read on sentiment and reversal risk; best used with confirmation (volume, support/resistance, indicators).
- **Efficient-market academics:** candlestick patterns are largely a *selection* artifact; after bootstrap adjustment and transaction costs there is little to no persistent edge in liquid developed markets (S201, S88).
- **Resolution:** the conflict is mostly about *scope*. Pattern **informativeness** (real) ≠ **standalone system profitability** (weak/contested) ≠ **net-of-cost edge** (mostly fails). The defensible position: candlesticks are a useful *descriptive/contextual* tool, not a predictive system on their own.

## Common mistakes
1. **Standalone trading:** treating a pattern as a buy/sell order without trend, support/resistance, or volume confirmation.
2. **Ignoring context:** calling a hammer bullish when it appears in an uptrend (it's then a hanging man) — same candle, wrong read.
3. **Pattern snooping:** testing 70+ named patterns and their variants, then reporting only the winners (this is exactly the multiple-testing trap Sullivan et al. 1999 warn about).
4. **Neglecting costs:** backtesting gross signals; frequent candlestick trading is killed by spreads/slippage (KB 08/09).
5. **Overfitting parameters:** tuning shadow/body thresholds to history; non-stationary regimes break it.
6. **Survivorship/look-ahead in backtests:** testing on live-index members or with forward-looking signals (KB 15).

## Further reading
- Marshall, B.R., Young, M.R. & Rose, L.C. (2006), "Candlestick technical trading strategies: Can they create value for investors?" *Journal of Banking & Finance* 30(8):2303–2323 — https://ideas.repec.org/a/eee/jbfina/v30y2006i8p2303-2323.html (S201, Tier 1)
- Yatrakis, P. & Williams, A.A. (2008), "Candlestick charts," *Business Quest* — https://www.westga.edu/~bquest/2008/candlestick08.pdf (S202, Tier 2)
- Investopedia, "Candlestick Chart: Definition and the Basics" — https://www.investopedia.com/terms/c/candlestick.asp (S203, Tier 2)
- StockCharts ChartSchool, "Candlestick Pattern Dictionary" — https://chartschool.stockcharts.com/table-of-contents/chart-analysis/candlestick-charts/candlestick-pattern-dictionary (S204, Tier 2)
- Sullivan, R., Timmermann, A. & White, H. (1999), "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap," *Journal of Finance* 54(5) — https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1647-1691.html (S88, Tier 1; reuse)
- Park, C.-H. & Irwin, S.H. (2007), "What Do We Know about the Profitability of Technical Analysis," *Journal of Economic Surveys* 21(4) (S93, Tier 1/2; reuse)
- Lo, A.W., Mamaysky, H. & Wang, J. (2000), "Foundations of Technical Analysis," *Journal of Finance* 55(4) (S190, Tier 1; reuse)
- Nison, S. (1991/1992), *Japanese Candlestick Charting Techniques* (seminal practitioner text; not a URL — cite as book).
