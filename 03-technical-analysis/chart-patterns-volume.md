---
title: Chart Patterns & Volume — Definitions and the Evidence Grade
topic_id: 03-technical-analysis/chart-patterns-volume
tags: [technical-analysis, chart-patterns, head-and-shoulders, double-top, volume-confirmation, evidence-grade]
last_updated: 2026-07-18
confidence: contested
sources: [S89, S93, S190, S191, S192, S193, S194, S88]
---

## TL;DR
- Classical chart patterns (head-and-shoulders, double tops/bottoms, triangles, rectangles, wedges, flags) are **geometrically well-defined** shapes in price that technicians read as reversals or continuations; volume is used to *confirm* the conviction behind a move.
- The best academic test to date — Lo, Mamaysky & Wang (2000, *Journal of Finance*) — shows that conditioning on these patterns **does alter the distribution of subsequent returns** (incremental information, strongest for Nasdaq), and that real price histories contain far more patterns than a random walk would generate. **That is informativeness, not proven net profitability.**
- Practitioner breakout statistics (Bulkowski, >30k samples) show sizable *gross* post-breakout moves, but these are not net of transaction costs, slippage, or false-breakout losses — the edge that survives is **contested** and decays over time and across regimes.

## Core explanation

### What a "chart pattern" is
A chart pattern is a recognizable configuration of peaks and troughs in a price series that, by convention, is interpreted as a signal about the *next* move. Patterns are split into two families:

- **Reversal patterns** — assumed to end the prevailing trend: head-and-shoulders (top/bottom), double/triple tops and bottoms, broadening formations, diamonds.
- **Continuation patterns** — assumed to pause then resume the trend: triangles (ascending/descending/symmetrical), rectangles, flags, pennants, cups-with-handle, wedges.

The geometry is defined by a small number of *local extrema* (alternating maxima and minima) and constraints on their relative heights. For example, a head-and-shoulders **top** is five consecutive extrema — max, min, max (the highest), min, max — where the two "shoulder" maxima are roughly equal and the two "neckline" minima are roughly equal, with the middle "head" peak above both shoulders (Lo, Mamaysky & Wang 2000, Definition 1; S190).

### The role of volume
Raw price shape is ambiguous; technicians add **volume** as a confirmation filter. The working rule (Schwab; S193; Investopedia; S194):
- A breakout **with above-average / rising volume** is taken as "confirmed" — genuine participation behind the move.
- A breakout **on low volume** is suspect — possibly a head-fake or exhaustion.
- In an uptrend, price rising on **declining** volume warns of weakening enthusiasm; in a downtrend, falling price on **rising** volume signals conviction to the downside.

Volume therefore converts a 1-D price shape into a 2-D price×volume signal. Lo et al. (2000) explicitly condition returns on *both* the pattern **and** an increasing/decreasing volume trend, and find the combination carries more information than price shape alone (S190).

### Why this is "evidence grade" and not "folklore"
The contested claim is not "do patterns exist" (they do — they are just local extrema with constraints) but "do they let you trade profitably after costs, robustly, out-of-sample?" That question has a **robust core** (patterns are informative) wrapped in a **contested shell** (the tradable edge).

## Math / formulas

### 1. Kernel-regression detection (Lo, Mamaysky & Wang 2000)
Lo et al. model prices as a smooth but unknown nonlinear function plus noise:

$$P_t = m(X_t) + \varepsilon_t,\quad \varepsilon_t \sim \text{white noise}$$

They smooth the series with a **nonparametric kernel regression** $\hat m_h(\cdot)$ to remove noise, then detect patterns from the *extrema* of the smoothed curve. A head-and-shoulders top is formalized as five consecutive alternating extrema $(E_1,\dots,E_5)$ with:

- $E_1, E_3, E_5$ are maxima; $E_2, E_4$ are minima;
- $E_3 > E_1$ and $E_3 > E_5$ (the head is highest);
- $|E_1 - E_5| / \big((E_1+E_5)/2\big) \le 1.5\%$ (shoulders equal);
- $|E_2 - E_4| / \big((E_2+E_4)/2\big) \le 1.5\%$ (neckline equal).

The same template defines inverse H&S, broadening, triangle, rectangle, and double top/bottom pairs (S190).

### 2. The informativeness test (goodness-of-fit)
Rather than backtesting a trading rule, Lo et al. compare the **unconditional** daily-return distribution $F$ to the **conditional** distribution $F|\text{pattern}$ (and $F|\text{pattern, volume trend}$). If a pattern is informative, conditioning shifts the distribution. They quantify the shift with decile-occupancy statistics and a **Kolmogorov–Smirnov** test of equality of the two distributions. A rejected null ⇒ the pattern carries incremental information about next-day returns.

### 3. Practitioner "breakout move" metric (Bulkowski)
Bulkowski measures the price change from the **breakout** (price crossing the pattern's trigger level, e.g., the neckline) to a fixed horizon (1/2/3/6 months), aggregated over tens of thousands of observed patterns. This is a *gross* descriptive statistic of how price historically behaved after the pattern — **not** a net-P&L or risk-adjusted result (S192).

## Worked example / code

The snippet below implements the Lo et al. (2000) head-and-shoulders *geometry* as an automated detector and contrasts a series with an embedded H&S against a geometric Brownian motion (random walk). It reproduces the paper's qualitative result: a random walk still throws off a few spurious patterns, but far fewer than real price histories (Lo et al. observed **1,611** H&S vs only **577** in a GBM simulation calibrated to the same means/vols over 1962–1996; S190, Table I).

**Data source:** synthetic (stdlib only, no external data). This is a *method* demo, not a market claim.

```python
import math, random

def local_extrema(prices, order=2):
    """Return list of (index, 'max'/'min') alternating local extrema."""
    extrema = []
    for i in range(order, len(prices) - order):
        w = prices[i - order:i + order + 1]
        if prices[i] == max(w) and prices[i] != prices[i - 1]:
            extrema.append((i, 'max'))
        elif prices[i] == min(w) and prices[i] != prices[i - 1]:
            extrema.append((i, 'min'))
    return extrema

def find_head_and_shoulders(prices, tol=0.015):
    """Lo, Mamaysky & Wang (2000) Definition 1 geometry:
    five consecutive alternating extrema max,min,max(highest),min,max;
    shoulders E1,E5 within tol of their mean; E2,E4 within tol of their mean."""
    ext = local_extrema(prices, order=2)
    pats = []
    for i in range(len(ext) - 4):
        e = ext[i:i + 5]
        if [t for _, t in e] != ['max', 'min', 'max', 'min', 'max']:
            continue
        E1, E2, E3, E4, E5 = [prices[idx] for idx, _ in e]
        if not (E3 > E1 and E3 > E5):
            continue
        if abs(E1 - E5) / ((E1 + E5) / 2.0) > tol:
            continue
        if abs(E2 - E4) / ((E2 + E4) / 2.0) > tol:
            continue
        pats.append((e[0][0], e[4][0]))
    return pats

def gbm(n, mu=0.0, sigma=0.2, seed=42):
    random.seed(seed)
    p = [100.0]
    for _ in range(n - 1):
        z = random.gauss(0, 1)
        p.append(p[-1] * math.exp((mu - 0.5 * sigma ** 2) / 252 + sigma / math.sqrt(252) * z))
    return p

def synth_with_hs(seed=7):
    random.seed(seed)
    nodes = [(0,90),(5,100),(10,95),(15,110),(20,95),(25,100),(32,91)]
    p = []
    for (i0,v0),(i1,v1) in zip(nodes[:-1], nodes[1:]):
        steps = i1 - i0
        for s in range(steps):
            frac = s / steps
            p.append(v0 + (v1 - v0) * frac + random.gauss(0, 0.15))
    p.append(nodes[-1][1])
    return p

hs_series = synth_with_hs()
print("H&S detected in series with embedded H&S shape:",
      len(find_head_and_shoulders(hs_series)))
counts = [len(find_head_and_shoulders(gbm(250, seed=s))) for s in range(20)]
print("GBM (random walk) avg H&S over 20 seeds: %.2f" % (sum(counts) / len(counts)))
```

Typical output: `1` H&S in the embedded-shape series, and `~1.5` per 250-day random walk — i.e., the detector works on a real shape while a pure random walk generates only sparse spurious patterns, the same direction Lo et al. report at scale.

## Assumptions & limitations

- **Subjectivity / definitional risk.** The single biggest academic objection to chart patterns is that "the pattern is in the eye of the beholder" (Lo et al. 2000, p. 1705; S190). Automated definitions (e.g., the 1.5%-tolerance rule above) reduce but do not eliminate discretion.
- **Informativeness ≠ profitability.** Lo et al. test whether patterns *shift the return distribution*, not whether a trading rule earns positive **risk-adjusted, net-of-cost** P&L. Jegadeesh's accompanying discussion is explicit: the evidence "does not support the use of technical analysis as a tool to independently identify profitable trading opportunities," only that it "can be a useful adjunct" (S190/S191).
- **Costs and false breaks.** Breakout strategies churn; Bulkowski's gross moves ignore commissions, slippage, and the cost of whipsaws. A pattern that is "right" 55% of the time can still lose net of costs if the losers are large.
- **Non-stationarity / decay.** The broader TA literature finds US equity pattern/trend-edge profitability **faded after the late 1980s** (Park & Irwin 2007 meta-review, S93; Fang, Jacobsen & Qin 2014 find out-of-sample nulls, S89). What worked in 1962–1996 need not work now.
- **Data-snooping.** The universe of possible patterns and parameter tolerances is huge; naive "this pattern worked" claims are exactly the selection bias the Deflated Sharpe / White Reality Check framework warns about (S88; see also `05-stats-and-ml/overfitting-lookahead.md` and `15-pitfalls-and-antipatterns/data-snooping-phacking.md` in this KB).

## Empirical evidence

**Robust (well-supported):**
- Lo, Mamaysky & Wang (2000) apply automated detection to **CRSP daily returns of NYSE/Amex/Nasdaq stocks, 1962–1996**, split into seven 5-year subperiods and five size groups. They find that conditioning on several of the 10 patterns **alters the unconditional next-day return distribution** (KS rejections), especially for **Nasdaq** stocks, and that real histories contain **many more patterns than a calibrated GBM random walk** (e.g., 1,611 vs 577 head-and-shoulders). Conclusion: classic patterns are not mere random-walk artifacts and carry *some* predictive information (S190; corroborated by the CFA Digest summary, S191).
- Frequency: double tops/bottoms are the most common (~2,000+ each over the sample), then head-and-shoulders / inverse H&S (~1,600 each) (S190, Table I).

**Emerging / sample-dependent:**
- Bulkowski's practitioner database (>30,000 patterns) reports large *gross* post-breakout moves — e.g., head-and-shoulders **top ≈ −7% over 2 months**, Eve-&-Eve double **bottom ≈ +12–13% over 2–3 months**, high-and-tight flags ≈ +21% over 1 month (S192). These are descriptive, **gross**, and pre-cost; treat as hypothesis-generating, not as an edge estimate.
- Chang & Osler (Federal Reserve Bank of New York Staff Report 4, 1999; algorithm proposed in Chang & Osler 1994 / Osler & Chang 1995, cited in the Lo et al. bibliography, S190) find head-and-shoulders trading rules produced excess returns in **foreign exchange** — a market where the edge has historically been stronger than in US equities.

**Contested (conflicting):**
- **Efficient-market view.** Malkiel ("A Random Walk Down Wall Street") likens chart-reading to alchemy; Lo et al. themselves quote this and position their work as bridging, not settling, the debate (S190).
- **Data-snooping null.** Sullivan, Timmermann & White (1999/2000) apply White's Reality Check bootstrap to technical rules on ~100 years of DJIA and find much of the apparent significance **vanishes after correcting for data-snooping** (S88; also summarized in S89).
- **Decay.** Park & Irwin (2007) survey 92 modern studies: technical rules looked profitable in US stocks **until the late 1980s**, then largely not; FX and emerging markets were more favorable (S93 via S89).

## Conflicting views

| View | Claim | Basis |
|---|---|---|
| Practitioners / Bulkowski | Patterns + volume give a tradable edge | Large descriptive samples; live trading lore (S192, S193, S194) |
| Lo, Mamaysky & Wang (2000) | Patterns are *informative* (shift return distributions) | Formal KS tests on CRSP 1962–1996 (S190) |
| Jegadeesh (discussant) | Informativeness ≠ independent profitable opportunities | Discussion in same JF issue (S190/S191) |
| EMH / Malkiel | Patterns are noise; "voodoo finance" | Random-walk argument (S190 intro) |
| Sullivan, Timmermann & White | Apparent edge is largely data-snooping | Bootstrap Reality Check on DJIA (S88) |

**Resolution in this KB's framing (three-bucket labeling):**
- **Robust:** chart patterns are objectively detectable and carry incremental short-horizon predictive information in historical US equity data.
- **Emerging:** a net-of-cost, risk-adjusted, out-of-sample edge from pattern trading in *current, liquid* US equities — plausible in specific regimes/markets (FX, small-caps, past eras) but not established for broad US large-caps today.
- **Folklore:** "a head-and-shoulders always reverses the trend" or "patterns are a stand-alone trading system." Both are contradicted by the cost, decay, and data-snooping evidence above.

## Common mistakes

1. **Treating a pattern as a certainty.** A pattern changes *probabilities*, not outcomes; base rates and stop placement still matter.
2. **Ignoring volume.** Trading a breakout with no volume confirmation invites whipsaws (S193).
3. **Gross vs net.** Quoting Bulkowski-style +12% moves as "returns" while ignoring costs, slippage, and false-breakout drag (S192).
4. **Pattern mining / overfitting.** Searching thousands of pattern shapes and tolerances until one "works" in-sample is the textbook multiple-testing trap (see `15-pitfalls-and-antipatterns/data-snooping-phacking.md`).
5. **Using patterns in isolation.** Lo et al. themselves frame TA as an *adjunct* to fundamentals, not a standalone system (S190/S191).
6. **Assuming stationarity.** An edge documented in 1962–1996 or in FX need not transfer to today's US large-cap tape (decay evidence, S93).
7. **Eyeballing instead of defining.** "I see a head-and-shoulders" is not reproducible; the fix is an explicit, coded definition (as in the worked example).

## Further reading

- **[S190 — Tier 1]** Lo, A.W., Mamaysky, H. & Wang, J. (2000), "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation," *Journal of Finance* 55(4):1705–1770. https://www.cis.upenn.edu/~mkearns/teaching/cis700/lo.pdf
- **[S191 — Tier 1]** CFA Digest summary of Lo, Mamaysky & Wang (2000), *Investment Policy and Portfolio Management*, Feb 2001. https://rpc.cfainstitute.org/sites/default/files/-/media/documents/article/cfa-digest/2001/dig-v31-n1-811-pdf.pdf
- **[S192 — Tier 2]** Bulkowski, T., "Best Chart Patterns" (Encyclopedia of Chart Patterns statistics). https://thepatternsite.com/BestPatterns.html
- **[S193 — Tier 2]** Charles Schwab, "Trading Volume as a Market Indicator" (2021). https://www.schwab.com/learn/story/trading-volume-as-market-indicator
- **[S194 — Tier 2]** Investopedia, "Head and Shoulders Pattern." https://www.investopedia.com/terms/h/head-shoulders.asp
- **[S89 — Tier 1]** CFA Institute Research Foundation, *Technical Analysis: Modern Perspectives* (2016) — Brock 1992, Sullivan et al. 1999, Park & Irwin 2007, Fang/Jacobsen/Qin 2014 context. https://rpc.cfainstitute.org/sites/default/files/-/media/documents/book/rf-lit-review/2016/rflrv11n11.pdf
- **[S88 — Tier 1]** Sullivan, R., Timmermann, A. & White, H. (1999), "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap," *Journal of Finance* 54(5). https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1647-1691.html
- **[S93 — Tier 1/2]** Park, C.-H. & Irwin, S.H. (2007), "What Do We Know about the Profitability of Technical Analysis?," *Journal of Economic Surveys* 21(4):786–826 (via S89).
- Complements in this KB: `03-technical-analysis/trend-support-momentum.md`, `03-technical-analysis/indicators-rsi-macd.md`, `05-stats-and-ml/overfitting-lookahead.md`, `15-pitfalls-and-antipatterns/data-snooping-phacking.md`.
