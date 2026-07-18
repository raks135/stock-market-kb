---
title: Momentum & Value Premiums — Robust or Fading?
topic_id: 04-quant-and-factors/momentum-value-premiums
tags: [factors, momentum, value, premiums, empirical, cross-sectional, time-series]
last_updated: 2026-07-18
confidence: contested
sources: [S92, S91, S164, S165, S214, S215, S216, S217, S218, S219, S163, S168, S220]
---

## TL;DR
The momentum premium is one of the most robust, pervasive findings in all of empirical asset pricing — it survives across ~150 years of US data, every major equity market, and eight asset classes, though it carries severe left-tail crash risk. The value premium is **empirically documented to have shrunk** in US large caps since ~1991 (big-value ~4.3%→0.6%/yr, small-value ~7%→4%/yr per Fama–French 2020), but the decline is statistically clouded by the factor's huge volatility, so "fading" and "not dead" are both defensible. Practitioners should treat value as *cyclical and currently cheap*, and combine value with momentum because the two are negatively correlated (a genuine diversifier).

## Core explanation

Two of the most studied equity "anomalies" are:

- **Value** — cheap stocks (high book-to-market, earnings-to-price, or cash-flow-to-price) tend to outperform expensive "growth" stocks.
- **Momentum** — stocks that have performed well over the past 3–12 months tend to keep performing well over the next few months (cross-sectional momentum, Jegadeesh & Titman 1993), and the same past-return predictor works *across* asset classes as a time-series signal (Moskowitz, Ooi & Pedersen 2012).

Both are "premiums" in the sense that a zero-cost long–short portfolio (long the winners / short the losers, or long value / short growth) has earned positive average excess return. The contested question is whether these premiums are *structural* (persistent, compensation for risk or behavioral bias) or *fading* (arbitraged away or eroded by publication and crowding).

**The evidence splits by factor:**

- **Momentum** is robust. Asness, Moskowitz & Pedersen (2013, S214) find significant value *and* momentum premia in **all eight** of the asset classes they study (US/UK/European/Japanese equities, equity-index futures, government bonds, currencies, commodities). Baltussen et al. (2026, S218) extend US equity momentum back to **1866** and find an ~8–9%/yr long–short premium that survives 4,000+ portfolio specification choices. MSCI (S219) calls momentum "one of the strongest generators of excess returns." Its main weakness is **crash risk**, not disappearance (see below).
- **Value** is contested. Fama & French themselves (2020, S215) document a sharp US shrinkage after 1991 yet cannot statistically reject that the out-of-sample premium is zero, because monthly value-premium volatility (~2.9% for Big Value) is so high that 28 years is not enough data to be sure. CFA Institute's five-factor revisit (S165) notes HML lost roughly half its cumulative edge after 2007. The "value is dead" camp (AQR 2020, S163; Swedroe 2023, S217) counters that the value *spread* is at historically wide levels (>4 SD per AQR) and that value has repeatedly been declared dead before (e.g., 2000) only to roar back.

A key, often-underappreciated fact: **value and momentum are negatively correlated** (S214; MSCI S219). An equal-weighted combination of the two earns the diversification benefit and — per Asness et al. (S214) — is largely *immune to funding-liquidity risk*, which loads positively on momentum but negatively on value.

## Math / formulas

**Cross-sectional momentum (Jegadeesh & Titman 1993, S92).** At each rebalance, rank stocks by past return over a formation period (typically 3–12 months, skipping the most recent month to avoid short-term reversal), form:

```
WML_t = (1/N) Σ winners_t − (1/N) Σ losers_t
```

where winners are the top decile/quintile by prior return and losers the bottom. JT (1993) document ~12.0%/yr (compounded) on 6-month/6-month US portfolios, 1965–1989, not explained by market beta.

**Time-series momentum (Moskowitz, Ooi & Pedersen 2012, S91).** A single asset's signal is simply `sign(r_{t−12→t})`; go long if the past 12-month excess return is positive. Significant in 58/58 futures contracts.

**Value long–short (Fama–French HML).** Sort on book-to-market equity (B/M); HML = small+big high-B/M minus small+big low-B/M. FF (2005, S164) report VMG/HML averaging ~0.40%/mo (1926–2004). FF (2020, S215) split the sample:

| Portfolio | 1963–1991 (1st half) | 1991–2019 (2nd half) |
|---|---|---|
| Big Value premium vs Market | **+4.3%/yr** (0.36%/mo, t=2.91) | **+0.6%/yr** (0.05%/mo, t=0.24) |
| Small Value premium vs Market | **+7.0%/yr** (0.58%/mo, t=3.19) | **+4.0%/yr** (0.33%/mo, t=1.52) |

The full-period (1963–2019) average is still reliably positive, but the *decline* in the means is only ~1.4 standard errors — statistically indistinguishable from zero (S215).

**Annualization.** `annual ≈ monthly_mean × 12` (arithmetic) or `(1+monthly_mean)^12 − 1` (geometric); the tables above use the ×12 convention.

## Worked example / code

Faithful statistical-power demonstration using the **exact** monthly moments Fama & French (2020, S215, Table 1) report for the *Big Value* portfolio. The point it makes: even a true 0.31%/month decline is usually *invisible* in 28 years of data because of the factor's volatility. Library: Python standard library only (always reproducible). Data source: F&F "The Value Premium" (Chicago Booth Paper 20-01), Table 1 — first-half mean 0.36%/mo, second-half mean 0.05%/mo, full-sample monthly std 2.94%, 336 months per half.

```python
import random, math

# Fama & French (2020), "The Value Premium", Big Value monthly premium
mu1, mu2 = 0.36, 0.05   # monthly %, true half-period means (BV, Table 1)
sigma    = 2.94         # monthly % std deviation (BV full-sample, Table 1)
n        = 336          # months per 28-year half-period

# Analytic standard error of the difference in means
se = sigma * math.sqrt(2 / n)
t_analytic = (mu1 - mu2) / se
print(f"True monthly decline = {mu1-mu2:.2f}%   SE = {se:.3f}%   t = {t_analytic:.2f}")

# Monte Carlo: each half-period sample mean ~ N(true_mean, sigma^2/n) (CLT, exact
# for normal draws). Draw sample means directly; difference d ~ N(mu1-mu2, 2*sigma^2/n).
random.seed(42)
N = 200_000
diffs, ts = [], []
for _ in range(N):
    m1 = random.gauss(mu1, sigma / math.sqrt(n))
    m2 = random.gauss(mu2, sigma / math.sqrt(n))
    d  = m1 - m2
    ts.append(d / se)          # sd of difference is exactly `se`
    diffs.append(d)

not_sig = sum(1 for t in ts if abs(t) < 1.96) / N
diffs.sort()
lo, hi = diffs[int(0.025*N)], diffs[int(0.975*N)]
print(f"Simulated P(|t|<1.96) = {not_sig:.2f}  (decline 'invisible' this often)")
print(f"95% CI of monthly decline = [{lo:.3f}, {hi:.3f}] %")
print(f"Zero inside 95% CI: {lo <= 0 <= hi}")
```

Expected output (verified, seed 42):

```
True monthly decline = 0.31%   SE = 0.227%   t = 1.37
Simulated P(|t|<1.96) = 0.71  (decline 'invisible' this often)
95% CI of monthly decline = [-0.13, 0.75] %
Zero inside 95% CI: True
```

Interpretation: a real 0.31%/month erosion of the value premium is *statistically undetectable* about 71% of the time over a 28-year window, and the 95% confidence interval straddles zero. This is precisely why Fama & French conclude we "cannot confidently conclude that the expected value premium … declines or even disappears" (S215) — the shrinkage is economically large but statistically ambiguous. (This is a power simulation using reported moments, not a market return simulation.)

## Assumptions & limitations

- **Backtests ≠ forward returns.** Both premia were *discovered* (published 1992–1993). McLean & Pontiff (2010) document that anomalies often weaken post-publication; Chicago Booth (S216) explicitly notes the value premium's shrinkage is "consistent with … academic research destroying stock-return predictability postpublication."
- **Transaction costs matter, especially for momentum.** Momentum is high-turnover; net-of-cost edge is materially smaller than gross (ties to KB 08/15 on costs and survivorship).
- **Regime dependence.** Momentum crashes in "panic states" (after market declines, high volatility — Daniel & Moskowitz 2016, S220); value is pro-cyclical and suffers in long growth rallies (e.g., 2008–2020 US large-cap).
- **Factor definitions vary.** "Value" via B/M vs E/P vs EV/EBITDA; "momentum" via 6/6 vs 12/1 vs time-series — magnitudes shift (S218 shows Sharpe ranging 0.38–0.94 across 4,000+ specs).
- **Sample and data vintage sensitivity.** Akey et al. (2026, see KB 04 Fama–French article) show factor returns are revision-sensitive to CRSP data vintage.

## Empirical evidence

**Momentum — strong, multi-source, long-horizon:**
- Jegadeesh & Titman (1993, S92): ~12.0%/yr cross-sectional, 1965–1989; robust to beta.
- Moskowitz, Ooi & Pedersen (2012, S91): significant time-series momentum in 58/58 futures; persists ~1 year.
- Asness, Moskowitz & Pedersen (2013, S214): value *and* momentum premia significant in all 8 asset classes; negatively correlated with each other.
- Baltussen et al. (2026, S218): 1866–2024 US long–short momentum ~8–9%/yr, $1 → $10,000+, t-stats far above convention; 4,000+ specs all positive Sharpe (median 0.61).
- MSCI (S219): MSCI World Momentum >13%/yr annualized over ~40 years; "one of the strongest generators of excess returns."

**Value — documented shrinkage, contested interpretation:**
- Fama & French (2020, S215): big-value premium 4.3%→0.6%/yr, small-value 7%→4%/yr across the two 28-year halves; cannot reject OOS-zero.
- CFA Institute (2022, S165): HML lost ~half its cumulative edge post-2007; RMW (quality) the most consistent post-1963 factor.
- AQR (2020, S163): value spread >4 SD, "down a decade ≠ −2σ event," value not dead.
- Swedroe/Morningstar (2023, S217): after the 2000 "value is dead" call, 2000–2007 small-value returned 16.2%/yr vs S&P 500's 1.7%; global small-value outperformed outside the US 2008–2023; wide valuation spread predicts *higher* future value premium.

**Diversification property:**
- Value–momentum correlation is low/negative both within and across asset classes (S214; MSCI S219) — combining them is a genuine diversifier and, per S214, removes most funding-liquidity risk exposure.

**Crash risk (momentum's failure mode):**
- Daniel & Moskowitz (2016, S220): momentum returns are negatively skewed; crashes occur in panic states after market declines / high volatility; a dynamic (vol-forecast) momentum strategy roughly doubles alpha and Sharpe.
- Baltussen et al. (S218): maximum drawdown as large as **−88%** for traditional price momentum; left-skewed, fat-tailed.

## Conflicting views

- **"Value is dead" vs "value is not dead."** F&F (2020) empirically show the US premium shrank and cannot be distinguished from zero post-1991 (S215). AQR (S163) and Swedroe (S217) argue the shrinkage is a cyclical drawdown within a still-alive premium, citing the historically wide valuation spread and prior false death-declarations. *Resolution:* both can be true — the *average* premium is lower and noisier, but the *current* starting valuation is favorable. Asness (2022, S168) also shows value is **not** merely an interest-rate bet (long-run HML↔10y-yield correlation ~0.10).
- **Risk vs mispricing.** Rational/Risk-based theories say premia compensate for bad states (value loads on distress/liquidity risk; momentum crashes in crises). Behavioral theories cite under-reaction (momentum) and over-extrapolation/distress neglect (value). Asness et al. (S214) note *neither* family fully explains value appearing in currencies, bonds, and commodities.
- **Is momentum even a distinct factor?** Recent "factor momentum" work (e.g., 2020 AEA paper, *Factor Momentum and the Momentum Factor*) argues individual-stock momentum merely aggregates the autocorrelations of other factors — a challenge to momentum as an independent risk source. (Flagged for Verify: primary not directly opened this iteration.)
- **Statistical threshold.** Whether a "real" premium needs |t| ≈ 3 (Harvey–Liu–Zhu factor-zoo bar, see KB 08) raises the bar further for calling any single premium robust (ties to KB 05/08).

## Common mistakes

1. **Declaring a factor "dead" from a 10–15 year drawdown.** Value was declared dead in 2000, then outperformed massively; the 2008–2020 US large-cap value slump is one regime, not proof of demise (S217).
2. **Ignoring momentum crash risk.** Standalone price momentum can lose >50–88% in a single rebound (S218, S220); size position and consider vol-scaling or combining with value.
3. **Forgetting costs and capacity.** Quoted premia are usually *gross*; momentum's turnover and value's small-cap weighting erode net returns (KB 08/13).
4. **Confusing correlation with causation in "rates killed value."** AQR (S168) finds at most a mild relationship; don't over-attribute value's pain to the rate environment.
5. **Backtest overfitting / p-hacking.** With 300+ "factors" in the literature (KB 08), a single significant premium is weak evidence; demand multiple independent replications and a |t|≈3 bar.
6. **Survivorship / look-ahead contamination.** Premiums computed on current-index members or with future-looking fundamentals are inflated (KB 13/15).
7. **Treating value and momentum as substitutes.** They are *complements* — negative correlation makes the combo superior (S214, S219).

## Further reading

- Asness, Moskowitz & Pedersen (2013), "Value and Momentum Everywhere," *Journal of Finance* 68(3):929–985 — https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf (S214)
- Fama, E.F. & French, K.R. (2020), "The Value Premium," Chicago Booth Paper 20-01 — https://ssrn.com/abstract=3525096 (S215)
- Jegadeesh, N. & Titman, S. (1993), "Returns to Buying Winners and Selling Losers," *Journal of Finance* 48(1):65–91 (S92)
- Moskowitz, T., Ooi, Y.H. & Pedersen, L.H. (2012), "Time Series Momentum," *Journal of Financial Economics* 104(2):228–250 (S91)
- Baltussen, Dom, Van Vliet & Vidojevic (2026, forthcoming JPM), "Momentum factor investing: Evidence and evolution," summary at CFA Enterprising Investor — https://rpc.cfainstitute.org/blogs/enterprising-investor/2025/momentum-investing-a-stronger-more-resilient-framework-for-long-term-allocators (S218)
- Daniel, K. & Moskowitz, T.J. (2016), "Momentum Crashes," *Journal of Financial Economics* 122(2):221–247 — https://ideas.repec.org/a/eee/jfinec/v122y2016i2p221-247.html (S220)
- Asness, C. (2020), "Is (Systematic) Value Investing Dead?" AQR — https://www.aqr.com/Insights/Perspectives/Is-Systematic-Value-Investing-Dead (S163)
- MSCI, "Factor Focus: Momentum" — https://www.msci.com/documents/1296102/1339060/Factor+Factsheets+Momentum.pdf (S219)
- Related KB entries: 04 Fama–French factors, 14 value & quality strategies, 05 stationarity/overfitting, 08 deflated Sharpe / multiple-testing, 13 data hygiene, 15 pitfalls.
