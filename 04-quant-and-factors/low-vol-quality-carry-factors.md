---
title: Low-Volatility, Quality, and Carry Factors
topic_id: 04-quant-and-factors/low-vol-quality-carry-factors
tags: [factors, low-volatility, quality, carry, smart-beta, beta, anomaly]
last_updated: 2026-07-18
confidence: contested
sources: [S221, S222, S223, S224, S225, S162, S227]
---

## TL;DR
- Three "alternative" equity factors — **low-volatility** (low-vol/min-vol), **quality**, and **carry** — each show a robust, multi-decade, multi-country premium that *contradicts* the simple CAPM prediction that more risk = more return.
- Low-vol: high-beta / high-vol stocks have historically earned *lower* risk-adjusted (and often lower absolute) returns than low-beta/low-vol stocks. BAB framework (Frazzini & Pedersen 2014) shows a zero-cost long-low-beta / short-high-beta factor earned ~0.7 Sharpe in US data 1926–2011 and positive Sharpe in 18 of 19 developed markets.
- Quality (QMJ, Asness-Frazzini-Pedersen): safe, profitable, growing, well-managed firms beat "junk" with significant risk-adjusted returns in the US and ~23/24 countries.
- Carry (Koijen-Moskowitz-Pedersen-Vrugt 2018): an asset's forward-looking yield ("carry") predicts returns across equities, bonds, currencies, commodities, credit, and options; diversified carry Sharpe ≈ 1.2.
- **Bucket labels:** mechanics & existence = **robust**; each as a *distinct, risk-based* premium = **contested**; the claim that any is a free lunch = **folklore**.
- Practical failure modes: sector/size/style concentration (low-vol often loads on utilities/staples/value), leverage & shorting costs (BAB needs shorts), non-stationarity, and the fact that much of "low-vol" is reproducible by simply de-risking (holding less equity + cash).

## Core explanation

### Low-volatility (the "low-risk" / betting-against-beta effect)
The Capital Asset Pricing Model predicts a *positive, linear* security market line: higher beta ⇒ higher expected return. Empirically the relation is **too flat or inverted**. Baker, Bradley & Wurgler (2011, S221) sort NYSE/AMEX/NASDAQ stocks into volatility and beta quintiles (CRSP, Jan 1968–Dec 2008, top-1000-by-cap universe). A dollar in the **lowest-volatility** quintile grew to **$59.55** vs **$0.58** for the highest-volatility quintile (no costs); for beta, $60.46 vs $3.77. The high-risk portfolios also had *larger* drawdowns — so they were not even compensated with higher risk-adjusted return. Ang, Hodrick, Xing & Zhang (2006, S224) independently find that stocks with high *idiosyncratic* volatility earn "abysmally low returns," unexplained by size, book-to-market, or momentum.

Frazzini & Pedersen (2014, S222, "Betting Against Beta") supply the leading *structural* explanation: many investors (mutual funds, pensions, individuals) face **leverage constraints**, so instead of levering low-beta assets they *overweight high-beta assets*. This bids up high-beta prices ⇒ low alpha / low returns on high-beta, and conversely makes low-beta assets cheap. Their **BAB factor** is long leveraged low-beta assets, short high-beta assets, sized to zero market beta and self-financing. Matching US data 1926–2011, the BAB factor shows ~11% vol, ~8% annual excess return (Sharpe ≈ 0.7). BAB delivers positive Sharpe ratios in **18 of 19 MSCI developed countries** (ScienceDirect abstract, S222).

### Quality (QMJ)
Asness, Frazzini & Pedersen (2013/2019, S162, "Quality Minus Junk") define a *quality* security as one an investor should pay more for, all else equal: **safe** (low risk, low earnings volatility, low leverage), **profitable** (high margins, high ROE/ROA, low accruals), **growing** (asset/earnings growth), and **well-managed** (low agency costs, high payout). A **QMJ** long-short factor (long top-30%-quality, short bottom-30%-junk) earns significant risk-adjusted returns in the US and across **23 of 24 countries**. High-quality stocks *do* carry higher prices, but only modestly, so the quality tilt remains profitable. (See also the 14-strategy-catalog value-quality entry for the profitability/quality premium evidence.)

### Carry
Koijen, Moskowitz, Pedersen & Vrugt (2018, S223, "Carry") generalize the currency "carry trade" to *any* asset: **carry = the return on a (synthetic) futures position if prices stay unchanged**. Return = carry + expected price appreciation + unexpected shock. Carry is model-free and observable ex ante. They show carry predicts returns **cross-sectionally and in time series** for global equities, government bonds, currencies, commodities, credit, and options; a single-asset-class carry portfolio averages **Sharpe ≈ 0.8**, and a **diversified cross-asset carry portfolio ≈ 1.2**. Carry is *not* explained by value, momentum, or time-series momentum, and it "captures many of these predictors," suggesting a unifying framework. The premium is only *partly* explained by recession/liquidity/volatility risk — i.e., it is not a clean risk premium.

## Math / formulas

**Low-vol sorting / BAB.** Let βᵢ be stock i's beta. The BAB factor holds low-beta stocks leveraged to beta 1 and shorts high-beta stocks de-levered to beta 1:
- US calibration (S222): long **$1.4** of low-beta stocks, short **$0.7** of high-beta stocks, with risk-free offset to make it self-financing and ~zero beta.

**Quality (QMJ).** Composite score z = weighted average of standardized quality measures (profitability, growth, safety, payout); QMJ = long top quality − short bottom quality, typically cap-weighted within each bucket (S162).

**Carry (general).** For an asset with futures price F and spot S, or yield differential y:
- carry ≈ (F − S)/S  (for assets where roll/yield defines carry), or the forward premium in currencies.
- Expected return ≈ carry + expected price appreciation. High carry ⇒ higher expected return, on average, across asset classes (S223).

**Empirical magnitude (US BAB, S222, Table C1 "Data" column, 1926–2011):**
| Portfolio | Ann. vol | Ann. excess ret | Sharpe |
|---|---|---|---|
| Low-risk (β≈0.7) | 18% | 11% | ≈ 0.61 |
| High-risk (β≈1.3) | 35% | 12% | ≈ 0.34 |
| BAB factor | 11% | 8% | ≈ 0.73 |

The low-risk asset has *both* lower vol and (roughly) comparable-or-higher raw return ⇒ higher Sharpe — the inversion.

## Worked example / code
Illustrative, **stdlib-only** Monte Carlo calibrated to the documented inversion (low-vol earns higher Sharpe). It is a teaching device, NOT a market claim — real backtests require point-in-time CRSP/Compustat data (see 13-data-and-tooling). Run with `python3` (no dependencies).

```python
import random, math
random.seed(42)  # reproducibility

# Stylized simulation of the low-risk anomaly.
# Each stock i gets a true annual vol and an EXPECTED ANNUAL excess return that
# DECREASES with vol (the empirical inversion documented by S221/S222):
#   mu_ex = 0.14 - 0.12 * vol
N, MONTHS = 300, 60 * 12
stocks = []
for i in range(N):
    vol = 0.10 + 0.50 * (i / (N - 1))      # 10% .. 60% annual vol
    mu_ex = 0.14 - 0.12 * vol               # higher vol -> LOWER expected return
    stocks.append((vol, mu_ex))

def norm():
    u1, u2 = random.random(), random.random()
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

# monthly returns ~ N(mu_ex/12, vol/sqrt(12))
rets = [[s[1] / 12 + (s[0] / math.sqrt(12)) * norm() for _ in range(MONTHS)]
        for s in stocks]

# Each month: rank by trailing 12m realized vol, form 5 equal-weight quintiles,
# hold 1 month, rebalance.
port = [[] for _ in range(5)]
for t in range(12, MONTHS):
    vols = []
    for s in range(N):
        w = rets[s][t - 12:t]
        m = sum(w) / 12
        var = sum((x - m) ** 2 for x in w) / 11
        vols.append(math.sqrt(var))
    order = sorted(range(N), key=lambda s: vols[s])
    q = N // 5
    for k in range(5):
        members = order[k * q:(k + 1) * q] if k < 4 else order[k * q:]
        port[k].append(sum(rets[s][t] for s in members) / len(members))

def ann_sharpe(xs):
    n = len(xs); mu = sum(xs) / n
    sd = math.sqrt(sum((x - mu) ** 2 for x in xs) / (n - 1))
    return (mu / sd) * math.sqrt(12)

for k in range(5):
    xs = port[k]
    cum = 1.0
    for x in xs: cum *= (1 + x)
    cagr = cum ** (1 / (len(xs) / 12)) - 1
    print(f"Q{k+1} (low->high vol): CAGR={cagr*100:5.2f}%  AnnSharpe={ann_sharpe(xs):.2f}")
```

Expected output (seed 42): the lowest-volatility quintile shows the **highest** annualized Sharpe and the highest CAGR; the highest-vol quintile shows the lowest of both — reproducing the documented inversion qualitatively. (Exact numbers vary with the random draw but the ordering is robust by construction.) **Caveat:** the simulated Sharpe (~5.8 for Q1) is *inflated* versus the real-world BAB Sharpe of ≈0.7 (S222 Table C1) because this toy Monte Carlo assumes a perfectly stable, noiseless vol→return relation, zero costs, and no regime change. It illustrates the *direction* of the effect only — do not read the magnitude as a tradable edge.

## Assumptions & limitations
- **Low-vol assumes the historical vol/return inversion persists** — it is a statistical regularity, not an arbitrage. Regime change can flip it (e.g., long stretches where growth/cyclical names lead).
- **BAB requires shorting high-beta stocks** and leverage on low-beta stocks; both incur financing, borrow, and capacity costs that erode the zero-cost ideal (see 08-backtesting-methodology transaction costs).
- **Low-vol/min-vol indices embed unintended tilts** (FTSE Russell 2015, S225): size (smaller, less-liquid names), sector (utilities, staples, low-beta defensives), reduced diversification, and illiquidity — these, not "low vol" per se, may drive returns and add hidden risk.
- **Quality and low-vol overlap**: both favor profitable, stable, low-leverage firms; much of low-vol's premium is partly a quality tilt (Asness et al. note the complementarity via S162).
- **Carry embeds crisis risk**: carry strategies lose money in global recessions, liquidity crunches, and volatility spikes (S223) — the premium compensates for crash/liquidity risk only partially.
- **Survivorship / look-ahead**: any quintile backtest must use point-in-time, delisting-inclusive data or it overstates results (see 13-data-and-tooling, 15-pitfalls survivorship).

## Empirical evidence
- **Low-vol robust across studies & eras**: Baker-Bradley-Wurgler (S221) 1968–2008; Ang et al. (S224) idiosyncratic-vol effect; Frazzini-Pedersen (S222) BAB positive in 18/19 developed markets; Wikipedia (S227) notes the anomaly holds "in most markets studied." Strength: **strong, multi-source, multi-country.**
- **Quality robust**: QMJ significant in US + 23/24 countries (S162); "price of quality" fell to a low in the dot-com bubble, and a low price of quality predicts higher future QMJ returns. Strength: **strong.**
- **Carry robust across asset classes**: Sharpe ≈ 0.8 per class, ≈ 1.2 diversified; rejects uncovered-interest-parity / expectations-hypothesis in favor of time-varying risk premia (S223). Strength: **strong and unusually broad (it spans asset classes).**
- **Common caveat**: all three are documented on *historical* data; out-of-sample decay and period-dependence are real (consistent with the factor-zoo / multiple-testing warnings in 08-backtesting-methodology and 15-pitfalls data-snooping).

## Conflicting views
- **Is low-vol a "factor" or just leverage/de-risking?** Critics: you can replicate most of low-vol's risk reduction by simply holding *less* equity plus cash, cheaper and with no shorting. The "excess return" may be largely a **quality + value tilt** and a bet on low interest-rate sensitivity (FTSE Russell 2015, S225). Proponents (Frazzini-Pedersen, S222): BAB is a distinct, economically-motivated premium rewarding those who supply leverage/liquidity to constrained investors; it is not subsumed by standard factors.
- **CAPM contradiction — settled or not?** The inversion is well documented (S221, S224, S222, S227) and is a genuine challenge to the textbook CAPM (see also 04-capm-beta Roll's critique). Whether it reflects *behavioral* mispricing (lottery-demand for high-vol stocks, Baker-Bradley-Wurgler) or *rational* leverage constraints is debated.
- **Carry: risk or anomaly?** Koijen et al. (S223) show recession/liquidity/volatility risk *partly* explain carry but "none fully explains" the premium — leaving room for both risk-based and behavioral (limits-to-arbitrage) stories.
- **Period dependence**: the low-vol effect was strongest pre-2000s in many studies; its recent live performance has been noisier and subject to severe drawdowns during growth/cyclical rallies. Treat historical Sharpe as an upper bound, not a forecast.

## Common mistakes
- Treating low-vol as "free downside protection" — min-vol still falls in bear markets; it reduces *volatility*, not *loss probability* to zero.
- Ignoring the embedded sector/size/quality tilts when attributing performance.
- Running BAB/carry backtests without realistic shorting, financing, and capacity costs (the high-beta/short leg is the expensive one).
- Assuming these factors are independent — low-vol, quality, and (sometimes) value are **correlated** and collectively can concentrate in defensives.
- Overfitting a "quality" composite to past winners (data snooping — see 15-pitfalls data-snooping).
- Using survivorship-biased or look-ahead data and believing the resulting Sharpe (see 15-pitfalls survivorship / look-ahead).

## Further reading
- S221 Baker, Bradley & Wurgler (2011), "Benchmarks as Limits to Arbitrage: Understanding the Low-Volatility Anomaly," *FAJ* 67(1):40–54 — https://pages.stern.nyu.edu/~jwurgler/papers/faj-benchmarks.pdf
- S222 Frazzini & Pedersen (2014), "Betting Against Beta," *JFE* 111:1–25 — https://pages.stern.nyu.edu/~lpederse/papers/BettingAgainstBeta.pdf ; ScienceDirect abstract — https://www.sciencedirect.com/science/article/pii/S0304405X13002675
- S223 Koijen, Moskowitz, Pedersen & Vrugt (2018), "Carry," *JFE* 127:197–225 — https://www.sciencedirect.com/science/article/abs/pii/S0304405X17302908
- S224 Ang, Hodrick, Xing & Zhang (2006), "The Cross-Section of Volatility and Expected Returns," *JF* 61:259–299 — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=681343
- S162 Asness, Frazzini & Pedersen (2013/2019), "Quality Minus Junk," *Review of Accounting Studies* 24(1) — http://www.econ.yale.edu/~shiller/behfin/2013_04-10/asness-frazzini-pedersen.pdf
- S225 FTSE Russell (2015), "Low Volatility or Minimum Variance: An 'eyes wide open' discussion" — https://research.ftserussell.com/products/downloads/Low-Vol-Whitepaper.pdf
- S227 Wikipedia, "Low-volatility anomaly" — https://en.wikipedia.org/wiki/Low-volatility_anomaly
- Related KB: 04-capm-beta (Roll's critique), 04-fama-french-factors, 04-momentum-value-premiums, 14-strategy-catalog/value-quality-strategies, 13-data-and-tooling, 08-backtesting-methodology, 15-pitfalls-and-antipatterns.
