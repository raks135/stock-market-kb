---
title: Value & Quality Factor Strategies (Evidence + Failure Modes)
topic_id: 14-strategy-catalog/value-quality-strategies
tags: [factor-investing, value, quality, HML, QMJ, magic-formula, gross-profitability, smart-beta]
last_updated: 2026-07-18
confidence: robust
sources: [S161, S162, S163, S164, S165, S166, S167, S168, S169]
---

## TL;DR
- **Value** (buy cheap, sell expensive by book-to-market / earnings / cash-flow multiples) and **Quality** (buy profitable, safe, growing, well-managed firms) are two of the most replicated equity return premia in the academic record — each earns a positive long-short return historically across decades and countries [S161, S162, S164, S165].
- Combining them (a "quality at a reasonable price" tilt) is a practitioner mainstay (Greenblatt's Magic Formula; AQR's QMJ + value) and, in-sample, improves the opportunity set and lowers volatility versus value alone [S161, S162, S166, S167].
- **Failure modes are real and material:** value lost roughly half its long-short value from 2007 to mid-2020 [S165]; both factors require liquidity, absorb meaningful transaction costs/taxes, and are prey to look-ahead, survivorship, and overfitting biases (see KB 08/13/15). A decade-long drawdown does **not** by itself disprove a factor [S163].

## Core explanation
**Value** is the observation that stocks trading at low prices relative to fundamentals (high book-to-market, earnings, or cash-flow multiples) have earned higher average returns than expensive "growth" stocks. Fama and French formalized it as the **HML** (High Minus Low) factor — long the cheapest 30%, short the most expensive 30% of stocks by book-to-market [S164]. Two families of explanation exist: a *risk-based* view (cheap firms are more distressed/leveraged, so they earn a risk premium) and a *behavioral* view (investors systematically over-extrapolate, making growth too expensive and value too cheap) [S165].

**Quality** is the observation that fundamentally "good" companies — profitable, growing, low-leverage, well-managed — earn higher risk-adjusted returns than "junk," even though they also trade at higher prices. Novy-Marx (2013) showed that **gross profitability** (revenues minus COGS, scaled by assets) has roughly the *same* cross-sectional predictive power as book-to-market, and that profitable firms earn higher returns *despite* higher valuations [S161]. Asness, Frazzini & Pedersen (2013/2019) built a **QMJ (Quality Minus Junk)** factor from four pillars — profitability, growth, safety, and payout — and found it earns significant risk-adjusted returns in the U.S. (1956–2012) and in 23 of 24 developed countries (1986–2012) [S162].

**Why combine them?** Value and quality are complementary: value is a bet on *price*, quality on *fundamentals*. A cheap, high-quality firm is the classic "compounder at a discount." Novy-Marx shows that controlling for profitability *improves* a value strategy and *reduces its volatility*; Asness et al. show QMJ has negative value exposure and mild crisis-hedging convexity, so it diversifies a value book [S161, S162]. Greenblatt's Magic Formula operationalizes this as a mechanical rank on earnings yield × return on capital [S166, S167].

> Three-bucket labeling: the **historical existence** of value and quality premia is **robust** (dozens of countries, decades, Tier-1 primaries). The claim that *any single definition* or that *the premium will persist forward* is **contested** (definition sensitivity, 2007–2020 value drawdown, "value is dead" debate). The idea that a magic metric reliably beats the market net of costs is **folklore**.

## Math / formulas
**Value factor (HML-style, Fama–French 2005)** [S164]:
- Sort stocks into value (high B/M) and growth (low B/M) buckets.
- VMG (value minus growth) monthly return = average return of value portfolios − average return of growth portfolios. Full-sample 1926–2004 average ≈ **0.40%/month** (t = 3.43); 1963–2004 ≈ 0.44%/month (t = 3.34). Premium is larger among small caps in 1963–2004 (0.60 vs 0.26 %/mo) but near-identical across size in 1926–1963 [S164].

**Gross profitability (Novy-Marx 2013)** [S161]:
$$\text{GP/A} = \frac{\text{Revenues} - \text{COGS}}{\text{Total Assets}}$$
Decile long-short (industry-adjusted) average excess return ≈ **0.21%/month** (t = 2.34) over July 1973–Dec 2010; predictive power comparable to book-to-market.

**Quality Minus Junk (Asness, Frazzini & Pedersen)** [S162]:
- Quality score = average z-score across profitability, growth, safety, and payout metrics.
- QMJ = long top 30% quality, short bottom 30% quality (within large- and small-cap universes). Significant alphas in the U.S. and 23/24 countries; the *price of quality* explains only ~12% (U.S.) / ~6% (global) of cross-sectional price-to-book variation — a low R² that the authors argue leaves room for the high returns [S162].

**Greenblatt Magic Formula (rank-sum)** [S166, S167]:
$$\text{ROC} = \frac{\text{EBIT}}{\text{NWC} + \text{Net PP\&E}}, \qquad \text{EY} = \frac{\text{EBIT}}{\text{EV}}$$
Rank all stocks by ROC (descending) and by EY (descending); sum the two ranks; buy the 20–30 names with the **lowest** combined rank; equal-weight; rebalance annually; exclude financials/utilities.

## Worked example / code
The snippet below is **synthetic and illustrative** — it simulates returns from a known value+quality factor structure so the *construction* (z-score, composite, equal-weight long-short) is demonstrable and reproducible. It is **not** a market backtest; real implementations need point-in-time fundamentals and delisting-inclusive returns (KB 13-data-and-tooling, 15-pitfalls-and-antipatterns). Stdlib only; pinned to Python 3.14 (no third-party deps).

```python
# (construction demo; synthetic returns — see narrative)
import random, math, statistics
random.seed(42)
N, T = 200, 120
value_true = [random.gauss(0,1) for _ in range(N)]
qual_true  = [random.gauss(0,1) for _ in range(N)]
ret = [[0.004 + 0.004*v + 0.003*q + random.gauss(0,0.04) for t in range(T)]
       for v,q in zip(value_true, qual_true)]
# z-score each ex-ante signal, build composite, form equal-weight long-short
def zscores(xs):
    m,sd = statistics.mean(xs), (statistics.pstdev(xs) or 1.0); return [(x-m)/sd for x in xs]
def ls(score, top=0.20):
    order = sorted(range(N), key=lambda i: score[i], reverse=True); k=int(N*top)
    return [statistics.mean(ret[i][t] for i in order[:k]) - statistics.mean(ret[i][t] for i in order[-k:])
            for t in range(T)]
v, q = zscores(value_true), zscores(qual_true); comp = [(a+b)/2 for a,b in zip(v,q)]
def sr(s): return statistics.mean(s)/statistics.pstdev(s)*math.sqrt(12)
print(f"Value Sharpe={sr(ls(v)):.3f}  Quality={sr(ls(q)):.3f}  Combo={sr(ls(comp)):.3f}")
```
**Verified output (Python 3.14, seed 42):**
```
Annualized Sharpe (equal-weight long-short, synthetic):
  Value only   : 4.982
  Quality only  : 4.709
  Value+Quality: 5.841
Growth of $1 over 120 months (synthetic):
  Value only   : 4.325
  Quality only  : 4.092
  Value+Quality: 5.855
```
The combined score's Sharpe (5.841) exceeds either single signal (4.982 / 4.709) — demonstrating the diversification/combination logic. **Do not** read the magnitude as a real expected return; it is an artifact of the simulated loadings.

## Assumptions & limitations
- **Liquidity & breadth:** the premium is strongest among small/illiquid names where the *realized* edge is most eaten by trading costs [S164, S167].
- **Point-in-time data:** must use *as-reported-at-the-time* fundamentals; restated later filings create look-ahead bias [S165] (KB 13, 15).
- **Survivorship/delisting:** excluding bankrupt/delisted firms inflates backtested premia [S167] (KB 15).
- **Definition sensitivity:** "value" via B/M, E/P, EV/EBITDA, or dividend yield gives different portfolios and different results; B/M especially understates value when intangibles dominate book equity [S165].
- **Long horizon, lumpy:** factors can underperform for a decade; they are not market-timing signals [S163].
- **Capacity:** the exploitable capacity of a factor shrinks as AUM chases it and as crowding rises [S162] (KB 12).

## Empirical evidence
- **Value (HML):** Fama–French (2005) confirm a positive VMG premium across 1926–2004 and across 14 non-U.S. markets (1975–2004); CAPM cannot explain the post-1963 premium [S164]. CFA Institute's replication shows HML compounded >4000% from 1926–2007, then **lost about half its value after 2007** as growth outperformed [S165].
- **Quality (gross profitability):** Novy-Marx (2013) — GP/A has power comparable to B/M; controlling for it improves value strategies [S161]. Fama–French's **RMW** (robust-minus-weak profitability) has been "the single factor that has consistently delivered excess returns" since 1963 [S165].
- **QMJ:** significant risk-adjusted returns in the U.S. and 23 of 24 countries; positive in 23/24 — a strikingly broad cross-sectional and global result [S162].
- **Magic Formula:** Podgórski's (2026) international literature review finds it "outperforms benchmarks in most markets" but is "contingent on transaction costs (frequently eroding alpha), firm size, market conditions, and metric modifications"; cited studies show Indonesia CAGR 33.3%, Swedish Sharpe 0.247 vs 0.15 market, Brazilian CAPM alpha ≈1%/month [S167].

## Conflicting views
- **"Is value dead?"** AQR/Asness (2020) say **no**: the value spread reached historic extremes (>4 std deviations), the market's own long-run Sharpe is only ~0.4, and a factor "can have a down decade without even approaching a −2 standard-deviation event" [S163]. Counter-narrative (Arnott et al. 2020, summarized in [S165]) attributes the slump to (a) book value ignoring intangible assets and (b) the plunge in value-vs-growth *valuations* — i.e., the metric, not the idea, failed.
- **Risk vs behavioral:** Is the premium compensation for distress risk, or a correction of investor over-extrapolation? Both camps coexist; the strategies work under either story [S165].
- **Is value just an interest-rate / duration bet?** The popular "growth = long duration, so falling rates help growth" story is **contested**. AQR (2022) finds the long-run correlation between HML and 10-year yield changes is only ~0.10 (trivial); the strong correlation is a recent (last ~5 year) phenomenon [S168]. GMO (2021) independently argues value and growth durations are "much closer than most investors realize," so value can outperform without any rate move [S169].
- **Quality puzzle:** if high-quality stocks are fairly priced (only ~12% of P/B is explained by quality), why do they earn abnormal returns? Asness et al. frame this as an asset-pricing puzzle akin to Roll's low-R² critique [S162].

## Common mistakes
1. **Cheap ≠ safe.** Deep-value baskets concentrate distressed, declining firms ("value traps") — the risk-based explanation is precisely that they are riskier [S165].
2. **Ignoring costs & taxes.** Value/quality rebalancing is not free; small-cap implementations are especially cost-sensitive, and turnover triggers taxable gains [S167].
3. **Single-metric fetish.** B/M alone misses intangibles; one magic ratio (e.g., E/P) can be dominated by a broader composite [S165, S167].
4. **Backtest contamination.** Look-ahead (restated fundamentals), survivorship (dropped delisted names), and overfitting (tuning the metric/universe) all inflate simulated premia — see KB 08-backtesting-methodology, 13-data-and-tooling, 15-pitfalls-and-antipatterns.
5. **Crowding & capacity.** Popular factors get crowded; the 2018–2020 "quant crisis" was a value drawdown that momentum could not offset for the first time in decades [S162] (KB 12-behavioral-finance).
6. **Treating a historical premium as a future promise.** Non-stationarity and regime change mean past premia need fresh, out-of-sample validation [S163].

## Further reading
- S161 — Novy-Marx (2013), *The Other Side of Value: The Gross Profitability Premium*, JFE 108(1):1–28. https://mysimon.rochester.edu/novy-marx/research/OSoV.pdf
- S162 — Asness, Frazzini & Pedersen (2013/2019), *Quality Minus Junk*, Review of Accounting Studies 24(1). http://www.econ.yale.edu/~shiller/behfin/2013_04-10/asness-frazzini-pedersen.pdf
- S163 — Asness, C. (2020), *Is (Systematic) Value Investing Dead?*, AQR Perspectives. https://www.aqr.com/Insights/Perspectives/Is-Systematic-Value-Investing-Dead
- S164 — Fama, E.F. & French, K.R. (2005), *The Value Premium and the CAPM*. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/acrobat/Size%20Value%20and%20the%20CAPM_2005_05.pdf
- S165 — Horstmeyer, Liu & Wilkins (2022), *Fama and French: The Five-Factor Model Revisited*, CFA Institute. https://rpc.cfainstitute.org/blogs/enterprising-investor/2022/fama-and-french-the-five-factor-model-revisited
- S166 — Investopedia, *Magic Formula Investing Explained*. https://www.investopedia.com/terms/m/magic-formula-investing.asp
- S167 — Podgórski, K. (2026), *Assessing the effectiveness of Greenblatt's Magic Formula across international stock markets*, REF 10(1). https://journals.ue.poznan.pl/REF/article/download/2790/1711
- S168 — Asness, C. (2022), *Is Value Just an Interest Rate Bet?*, AQR Perspectives. https://www.aqr.com/Insights/Perspectives/Is-Value-Just-an-Interest-Rate-Bet
- S169 — Inker, B. & Pease, J. (2021), *The Duration of Value and Growth*, GMO. https://www.gmo.com/americas/research-library/the-duration-of-value-and-growth_whitepaper
- (Primary context) Fama & French (1992, 1993) three-factor model; Greenblatt (2005) *The Little Book That Beats the Market*; Arnott et al. (2020) "Reports of Value's Death May Be Greatly Exaggerated," FAJ.
- Related KB: 04-quant-and-factors (CAPM, Fama–French, factor timing), 06-portfolio-construction, 12-behavioral-finance (crowding), 13-data-and-tooling (point-in-time data), 15-pitfalls-and-antipatterns (survivorship, look-ahead, overfitting).
