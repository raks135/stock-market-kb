---
title: Momentum & Trend-Following Strategies
topic_id: 14-strategy-catalog/momentum-trend-following-strategies
tags: [momentum, trend-following, time-series-momentum, cross-sectional-momentum, managed-futures, CTA, strategy-catalog]
last_updated: 2026-07-18
confidence: contested
sources: [S363, S364, S365, S366, S91, S215, S218, S220]
---

## TL;DR
Momentum exists in two distinct flavors: **cross-sectional** ("buy past winners, sell past losers" in equities, Jegadeesh & Titman 1993) and **time-series / trend-following** ("go long what has risen, short what has fallen" across asset classes, Moskowitz-Ooi-Pedersen 2012; Hurst-Ooi-Pedersen 2017). The phenomenon is one of the most replicated in all of asset pricing — profitable across ~137 years, 67 markets, and every one of 58 futures contracts studied. But the *live, net-of-cost* edge is **contested**: cross-sectional momentum has decayed since the 2000s, time-series momentum was roughly flat-to-negative after 2008 (Baltas & Kosowski 2017), and both crash violently at market bottoms (Daniel & Moskowitz 2016). Treat momentum as a real, well-documented anomaly with negative skewness and heavy regime dependence — not a free lunch.

## Core explanation

**Cross-sectional momentum (relative strength).** Sort stocks on their return over a past formation window (typically 3–12 months, skipping the most recent month to avoid short-term reversal) and hold the long–short portfolio of past winners minus past losers for 3–12 months. Jegadeesh & Titman (1993) document ~1% per month over 1965–1989 for this "12-1 month" strategy, and show the abnormal returns are *not* explained by market beta or size. The effect partially reverses after ~12 months (winners give back >half the gain over the following two years).

**Time-series momentum / trend-following (absolute momentum).** For each asset, take a long position if its trailing excess return is positive, short if negative, and vol-scale the position to a constant risk target. Moskowitz, Ooi & Pedersen (2012) show 12-month time-series momentum is positive — not just on average but *for every one of 58 futures contracts* across equities, bonds, commodities, and currencies. Hurst, Ooi & Pedersen (2017) extend this to 1880–2016 across 67 markets and find it profitable in essentially every decade. This is the engine behind managed-futures / CTA funds (Baltas & Kosowski 2013, 2017).

The two are **structurally different** (Baltas & Kosowski 2017): cross-sectional momentum is a zero-cost long–short that captures the *spread* between winners and losers and relies on cross-sectional return dispersion; time-series momentum relies on *serial correlation* (autocorrelation) in each asset's own returns and is typically implemented with leverage and vol-scaling.

## Math / formulas

**Cross-sectional (Jegadeesh–Titman 1993).** For stock *i* at time *t*, formation return
$$r^{form}_{i,t} = \prod_{k=1}^{J}\left(1+r_{i,t-k}\right)-1$$
Rank stocks on $r^{form}$, form decile portfolios, and hold the long–short **WML** (winners minus losers) portfolio for *K* months. Standard choice: skip the most recent month (12-1) to avoid one-month reversal.

**Time-series momentum (Moskowitz-Ooi-Pedersen 2012; Hurst-Ooi-Pedersen 2017).** For asset *a* at rebalance *t*, with lookback *L*:
$$\text{signal}_{a,t} = \text{sign}\!\left(\sum_{\tau=1}^{L} r_{a,t-\tau}\right), \qquad w_{a,t} = \text{signal}_{a,t}\,\frac{\sigma^{\*}}{\sigma_{a,t}}$$
where $\sigma^{\*}$ is the volatility target (Hurst et al. use 10% annualized) and $\sigma_{a,t}$ is the trailing realized volatility. The Hurst et al. (2017) "trend factor" combines equal-weighted 1-, 3-, and 12-month signals, rebalanced monthly, aggregated across markets and scaled to 10% ex-ante volatility.

**Why it can work (mechanism).** A strategy that is long an asset exactly when its trailing return is positive is, in expectation, long assets whose returns are positively autocorrelated. See the worked example: TSM profit rises monotonically with the return autocorrelation it harvests, and is flat-to-negative when autocorrelation is zero (volatility drag from being always fully exposed with a random sign).

## Worked example / code

Runnable illustration (numpy 2.5.1; synthetic data — **not** a market claim). It holds the noise path fixed and varies only the autocorrelation $\rho$, isolating momentum's fuel:

```python
# file: 14-strategy-catalog/_demo_momentum.py  (run: .venv/bin/python _demo_momentum.py)
import numpy as np

rng = np.random.default_rng(42)
T = 360                                 # 30y of monthly observations
target_vol = 0.10 / np.sqrt(12)         # monthly vol target ~2.89% (10% annualized)
base = rng.normal(0.0, 0.04, T)         # SAME noise for every rho -> isolates autocorrelation

def make_ar1(rho):
    x = np.zeros(T)
    for t in range(1, T):
        x[t] = rho * x[t - 1] + base[t]
    return x

def tsm_returns(rets, lookback=12):
    out = np.zeros(len(rets))
    for t in range(lookback, len(rets)):
        signal = np.sign(np.sum(rets[t - lookback:t]))
        vol = np.std(rets[t - lookback:t], ddof=1)
        vol = vol if vol > 1e-9 else 1e-9
        out[t] = signal * (target_vol / vol) * rets[t]
    return out

print(f"{'rho':>5} | {'TSM cum P&L':>12} | {'ann. Sharpe':>12}")
for rho in [0.0, 0.10, 0.20, 0.30]:
    pnl = tsm_returns(make_ar1(rho))
    cum = (np.prod(1.0 + pnl) - 1.0) * 100.0
    shr = np.mean(pnl) / np.std(pnl, ddof=1) * np.sqrt(12)
    print(f"{rho:5.2f} | {cum:11.1f}% | {shr:12.2f}")
```

Verified output (CPython 3.14.4 / numpy 2.5.1):
```
 rho | TSM cum P&L | ann. Sharpe
 0.00 |      -22.4% |       -0.02
 0.10 |       -7.0% |        0.03
 0.20 |        2.8% |        0.06
 0.30 |       31.5% |        0.14
```
Read: TSM profit rises with the return autocorrelation it harvests; at $\rho=0$ it is flat-to-negative (volatility drag), not a market edge. Data source: synthetic AR(1) — illustrative only.

## Assumptions & limitations

- **Requires return autocorrelation / trends.** Momentum has no edge on i.i.d. returns (the demo's $\rho=0$ case). In range-bound, mean-reverting, or high-correlation regimes it underperforms (Hurst et al. 2017 find TSM performs *best in low-correlation environments*; Baltas & Kosowski 2017 link post-2008 weakness to rising cross-market correlations).
- **Transaction costs dominate.** Time-series momentum is high-turnover; Baltas & Kosowski (2017) estimate ~1.0–1.85% annual cost, and the post-GFC (2009–2013) window is *negative after costs* (about −1.4% return, Sharpe −0.09). Cross-sectional momentum's edge shrinks sharply net of costs and is sensitive to the short side.
- **Survivorship & look-ahead bias** in naive backtests: see `15-pitfalls-and-antipatterns/survivorship-bias.md` and the look-ahead deep dive. Use point-in-time, delisting-inclusive data.
- **Non-stationarity.** The premium is not constant; cross-sectional momentum in particular has decayed (see empirical evidence and `04-quant-and-factors/momentum-value-premiums.md`).
- **Capacity limits** in futures (Baltas & Kosowski 2017 find no strong constraint 1984–2013, but post-2008 AUM growth is a live concern).

## Empirical evidence

- **Cross-sectional (Jegadeesh & Titman 1993, S363).** 1965–1989: relative-strength portfolios earn ~1%/month over 3–12-month holding periods; abnormal returns are *not* due to systematic risk or a common-factor lead-lag effect, but are consistent with delayed reaction to firm-specific information; part of the gain reverses in months 13–36.
- **Time-series, 58 futures (Moskowitz-Ooi-Pedersen 2012, S91).** 12-month time-series momentum profits are positive for *every one of 58 liquid contracts* across equity index, currency, commodity, and bond futures, with little exposure to standard risk factors.
- **137-year, 67-market (Hurst-Ooi-Pedersen 2017, S364).** 1880–2016: time-series momentum profitable in essentially every decade; positive in 8 of 10 major stress periods; best in low-correlation regimes. Authors argue this longevity makes pure data-mining unlikely.
- **Costs & post-GFC (Baltas & Kosowski 2017, S365).** Naive TSM Sharpe ~1.0–1.15 before costs, ~1.0–1.05 after costs (full 1984–2013 sample); **post-GFC (2009–2013) Sharpe ≈ 0 before costs and negative after costs**. Volatility-estimator and trading-rule refinements cut turnover ~36% with no significant performance penalty; a correlation-adjusted variant outperforms, especially post-2008.
- **Decay of the equity premium (Fama & French 2020, S215; Baltussen et al. 2026, S218).** Cross-sectional momentum remains statistically significant over the long run but its *net-of-cost, out-of-sample* US large-cap edge has faded since the 2000s — consistent with the replication-crisis debate in `06-portfolio-construction/factor-portfolios-smart-beta.md`.
- **Momentum crashes (Daniel & Moskowitz 2016, S366).** Momentum returns are **negatively skewed**: crashes occur in "panic" states — after market declines with high volatility — and coincide with abrupt market rebounds. In 1927–2013 the two worst months (Jul–Aug 1932) saw the past-loser decile return +232% while winners returned only +32%; in Mar–May 2009 losers rose +163% vs +8% for winners. The loser portfolio's up-market beta exceeds its down-market beta (−1.51 vs −0.70, t=4.5), so momentum behaves like a **written call option on the market** in bear markets. A volatility-scaled dynamic version roughly doubles the static strategy's alpha and Sharpe.

## Conflicting views

- **Is momentum a market inefficiency or a risk premium?** *Behavioral:* Jegadeesh & Titman (1993) frame it as underreaction to firm-specific news; Hong & Stein (1999) model gradual information diffusion; Hurst et al. (2017) cite anchoring, herding, and the disposition effect, plus non-profit-seeking flow (central banks, corporate hedging) as trend sources. *Risk-based:* Daniel & Moskowitz (2016) show momentum's crashes are partly explained by time-varying conditional betas and volatility risk (a partial risk story); Grundy & Martin (2001, discussed in Daniel & Moskowitz 2016) attribute performance to dynamic factor exposure; Conrad & Kaul (1998) argue time-varying expected returns can account for momentum profits. The literature has **not settled** the source — most practitioners treat it as an empirically robust anomaly whose economic cause is mixed.
- **Is the edge still alive?** Cross-sectional momentum's US large-cap edge has clearly decayed post-2000 (S215, S218), yet remains significant over the full ~90-year sample; time-series momentum delivered weak/negative net-of-cost performance in 2009–2013 (S365) but strong long-run and crisis-diversification results (S364). Net conclusion: **robust in existence, contested in forward tradability and net-of-cost magnitude**.
- **Cross-sectional vs time-series are not the same trade.** Baltas & Kosowski (2017) emphasize they exploit different return properties (cross-sectional dispersion vs serial correlation) and can diverge; do not assume one implies the other.

## Common mistakes

- **Ignoring costs / turnover.** A gross-Sharpe of ~1.0 can vanish after 1–2% annual cost (Baltas & Kosowski 2017); backtests that skip financing, roll, or rebalancing costs overstate edge.
- **Survivorship & look-ahead in backtests.** Using current index membership or restated fundamentals injects look-ahead; see the `15-pitfalls-and-antipatterns` series. The 137-year result (S364) is impressive precisely because it uses *expanding* historical universes, not a fixed modern index.
- **Treating momentum as alpha without crash risk.** The negative skew and written-call behavior (S366) mean a few months can erase years of gains — size for tail risk, consider vol-scaling.
- **Over-leverage in calm regimes.** Low realized vol invites leverage that amplifies the next crash; the dynamic vol-targeted approach (S366) is one mitigation.
- **Conflating trend-following with technical analysis.** TSM is a systematic, rules-based risk premia strategy with a 137-year evidential base; casual chart-reading is a different (far weaker) claim — see `03-technical-analysis/`.

## Further reading

- **[Tier 1]** Jegadeesh, N. & Titman, S. (1993). "Returns to Buying Winners and Selling Losers." *Journal of Finance* 48(1): 65–91. https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf (S363)
- **[Tier 1]** Moskowitz, T., Ooi, Y.H. & Pedersen, L.H. (2012). "Time Series Momentum." *Journal of Financial Economics* 104(2): 228–250. https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf (S91)
- **[Tier 1]** Hurst, B., Ooi, Y.H. & Pedersen, L.H. (2017). "A Century of Evidence on Trend-Following Investing." *Journal of Portfolio Management* 44(1): 15–29. https://fairmodel.econ.yale.edu/ec439/hurst.pdf (S364)
- **[Tier 1]** Baltas, N. & Kosowski, R. (2017). "Demystifying Time-Series Momentum Strategies." https://www.cmegroup.com/education/files/demystifiing-time-series-momentum-strategies.pdf (S365)
- **[Tier 1]** Daniel, K. & Moskowitz, T.J. (2016). "Momentum Crashes." *Journal of Financial Economics* 122(2): 221–247. https://www.nber.org/system/files/working_papers/w20439/w20439.pdf (S366)
- **[Tier 1]** Fama, E. & French, K. (2020). "The Value Premium." (cross-sectional momentum decay context) (S215)
- **[Tier 1]** Baltussen, G. et al. (2026). "Momentum Everywhere, 1866–2024." (long-run robustness) (S218)
- **[Tier 2]** AQR / Asness-Moskowitz-Pedersen (2013). "Value and Momentum Everywhere." (cross-asset integration) (S214)
- Internal: `03-technical-analysis/trend-support-momentum.md`, `04-quant-and-factors/momentum-value-premiums.md`, `06-portfolio-construction/factor-portfolios-smart-beta.md`, `08-backtesting-methodology/transaction-costs-slippage-walkforward.md`, `15-pitfalls-and-antipatterns/`.
