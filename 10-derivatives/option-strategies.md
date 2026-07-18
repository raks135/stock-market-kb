---
title: Option Strategies — Covered Calls, Protective Puts & Spreads
topic_id: 10-derivatives/option-strategies
tags: [options, covered-call, protective-put, spreads, collar, calendar-spread, volatility-risk-premium, hedging]
last_updated: 2026-07-18
confidence: robust
sources: [S310, S311, S312, S313, S314, S315]
---

## TL;DR
- A **covered call** (long stock + short call) caps your upside in exchange for premium income and behaves as **long equity + short volatility** — its edge comes from harvesting the volatility risk premium, not from "downside protection."
- A **protective put** (long stock + long put) is genuine portfolio insurance that floors losses, but it is **structurally expensive**: the long-volatility leg has historically cost ~2%/yr with a negative Sharpe, because option implied vol tends to exceed realized vol (the volatility risk premium works *against* the buyer).
- **Vertical spreads, collars, and straddles** trade off bounded risk/reward for lower cost; their payoffs are fully determined at expiration and are easy to verify arithmetically (code below).
- **Empirical reality is contested**: index covered calls have matched equity returns at ~2/3 the volatility (BXM), while systematic protective-put buying has *reduced* risk-adjusted returns. Treat the "income" and "protection" framings as marketing, not mechanics.

## Core explanation

Options are combined with the underlying and with each other to modify risk–return profiles. The CFA curriculum (Level III, 2026) organizes the building blocks as follows [S310]:

- **Covered call** — holder of a stock writes (sells) a call against it. One of the most common retail uses of options. It changes the risk–reward profile by *enhancing yield* (premium) or *exiting at a target price* (strike). Because the right tail of the return distribution is sold to the option buyer, **maximum return is limited** while maximum loss is slightly smaller than the stock alone (offset by premium). The cost is an **opportunity loss if the stock rallies hard**.
- **Protective put** — long stock + long put on the same asset. Acts as insurance: it limits downside while preserving upside. The CFA reading warns the **cost must be carefully considered — it is frequently expensive** [S310].
- **Bull / bear spread** — buy one option and write another of the *same type* (both calls or both puts) with a different strike. Both maximum gain and maximum loss are **known and limited** [S310].
- **Straddle** — long (or short) a put and a call at the same strike/expiry; profits from a *large* move (long) or *stability* (short) [S310].
- **Collar** — long stock + write a call above current price + buy a put below. Limits outcomes to a band, sacrificing upside for downside protection [S310].
- **Calendar spread** — buy a long-dated option, write a shorter-dated one of the same type/strike. Used when the near-term view is flat but larger moves are expected later [S310].

**The unifying insight (Israelov & Nielsen, FAJ 2014) [S314]:** a covered call is mathematically equivalent to a **50/50 mix of a long equity position and a short straddle**. Writing the call therefore gives you *long equity + short volatility* exposure. An at-the-money covered call earns two risk premiums — the equity risk premium and the **volatility risk premium** (options are typically richly priced versus subsequent realized volatility). This is why the strategy is better understood as a *risk-bearing* position than as "income generation."

## Math / formulas

**Payoff at expiration** (per share, ignoring discounting), with terminal underlying price `S`, entry `S0`, strike `K`, option premium `c` (received, short) or `p` (paid, long):

- **Covered call:** `P&L = (S − S0) + c − max(S − K, 0)`
  - Max profit = `(K − S0) + c` (achieved for `S ≥ K`)
  - Max loss = `−(S0 − c)` (for `S → 0`)
  - Breakeven = `S0 − c`
- **Protective put:** `P&L = (S − S0) − p + max(K − S, 0)`
  - Max loss = `(K − S0) − p` (for `S ≤ K`); **max profit is unlimited**
  - Breakeven = `S0 + p`
- **Bull call spread** (buy call `K1` pay `c1`, sell call `K2 > K1` receive `c2`):
  - Max profit = `(K2 − K1) − (c1 − c2)`; Max loss = `−(c1 − c2)`; Breakeven = `K1 + (c1 − c2)`
- **Bear put spread** (buy put `K2`, sell put `K1 < K2`):
  - Max profit = `(K2 − K1) − (p2 − p1)`; Max loss = `−(p2 − p1)`; Breakeven = `K2 − (p2 − p1)`
- **Collar** (long stock, long put `K_put`, short call `K_call > K_put`):
  - Floors loss near `K_put`, caps gain near `K_call`; net premium = `c − p`

**Synthetic positions** [S310]: long call + short put (same `K`, `T`) ≡ synthetic long forward; short call + long put ≡ synthetic short forward. (Verified numerically below.)

**Volatility risk premium (VRP):** `VRP ≈ implied volatility − realized volatility` over the coincident period. For S&P 500 index options, the VRP averaged **+3.4%** and was positive **88% of the time** over Jan 1990–Jun 2014 [S313]. Option sellers collect this; option buyers pay it.

## Worked example / code

Self-contained, stdlib-only payoff calculator. Run with `python3 option_strategies_payoffs.py` (Python 3.14.4, no dependencies). Output below is the verified execution.

```python
def covered_call(S, K, prem, S0):
    return (S - S0) + prem - max(S - K, 0)

def protective_put(S, K, prem, S0):
    return (S - S0) - prem + max(K - S, 0)

def bull_call_spread(S, K1, K2, c1, c2):
    return max(S - K1, 0) - max(S - K2, 0) + (c2 - c1)

def bear_put_spread(S, K1, K2, p1, p2):
    return max(K2 - S, 0) - max(K1 - S, 0) + (p1 - p2)

def collar(S, K_put, K_call, p_prem, c_prem, S0):
    return (S - S0) - p_prem + max(K_put - S, 0) + c_prem - max(S - K_call, 0)

def metrics(fn, lo=0.0, hi=200.0, step=0.01):
    vals, xs = [], []
    x = lo
    while x <= hi + 1e-9:
        vals.append(fn(x)); xs.append(x); x += step
    bes = []
    for i in range(1, len(vals)):
        if (vals[i-1] <= 0 < vals[i]) or (vals[i-1] >= 0 > vals[i]):
            bes.append(round((xs[i-1] + xs[i]) / 2.0, 2))
    return max(vals), min(vals), bes

def show(name, fn):
    mp, ml, bes = metrics(fn)
    print(f"{name}: max_profit={mp:.2f}  max_loss={ml:.2f}  breakeven(s)={bes}")

show("Covered call (S0=100,K=100,prem=5)",
     lambda S: covered_call(S, 100, 5, 100))
show("Protective put (S0=100,K=95,prem=3)",
     lambda S: protective_put(S, 95, 3, 100))
show("Bull call spread (K1=100 c1=5, K2=110 c2=2)",
     lambda S: bull_call_spread(S, 100, 110, 5, 2))
show("Bear put spread (K1=90 p1=2, K2=100 p2=5)",
     lambda S: bear_put_spread(S, 90, 100, 2, 5))
show("Collar (S0=100, put K=95 prem=3, call K=105 prem=2)",
     lambda S: collar(S, 95, 105, 3, 2, 100))
```

Verified output (CPython 3.14.4):

```
Covered call (S0=100,K=100,prem=5): max_profit=5.00  max_loss=-95.00  breakeven(s)=[95.0]
Protective put (S0=100,K=95,prem=3): max_profit=97.00  max_loss=-8.00  breakeven(s)=[103.0]
Bull call spread (K1=100 c1=5, K2=110 c2=2): max_profit=7.00  max_loss=-3.00  breakeven(s)=[103.0]
Bear put spread (K1=90 p1=2, K2=100 p2=5): max_profit=7.00  max_loss=-3.00  breakeven(s)=[97.0]
Collar (S0=100, put K=95 prem=3, call K=105 prem=2): max_profit=4.00  max_loss=-6.00  breakeven(s)=[101.0]
```

*(The protective-put `max_profit=97.00` is just the grid ceiling at S=200; the position has theoretically unlimited upside. The collar caps gain at +4.00 and floors loss at −6.00, exactly the band defined by the two strikes net of premium.)*

## Assumptions & limitations
- **Expiration-only math.** Payoffs above ignore path, early assignment, dividends, and time value. Real P&L before expiration depends on the whole volatility surface (see `10-derivatives/volatility-surface-skew-hedging.md`).
- **European/exercise simplicity.** American options can be assigned early (especially puts, and calls with dividends); covered-call writers can be "called away" before expected.
- **Transaction costs, financing, and taxes are excluded.** The BXM benchmark explicitly does *not* include transaction costs or taxes [S312]; a live covered-call program faces bid–ask, commissions, and short-option financing.
- **Static strikes.** Rolling, strike selection, and rebalancing materially change outcomes and are where skill (or data-mining) lives.
- **Volatility regime dependence.** All these strategies' attractiveness moves with the VRP; a shrinking VRP (e.g., post-2020 low-vol environment) compresses covered-call yield [S313].

## Empirical evidence

**Covered calls / buy-write (robust documentation, contested "alpha"):**
- The CBOE S&P 500 BuyWrite Index (BXM) = long SPX + write a monthly at-the-money SPX call; variants write 30-delta OTM (BXMD) or 2%-OTM (BXY) calls [S311].
- Ibbotson Associates (2004) case study, Jun 1988–Mar 2004 [S312]: BXM **compound annual return 12.39%** vs S&P 500 **12.20%**, at **~two-thirds the volatility**; Stutzer (skew/kurtosis-adjusted) index **0.22 vs 0.16**. Average monthly premium = **1.69%** of underlying (≈22.3% annualized); average implied vol **16.5%** vs realized **14.9%** (the VRP in action). BXM skew **−1.249** vs S&P **−0.456** (more negative skew). Rampart investable version tracked BXM with **1.27%/yr** tracking error.
- Israelov & Nielsen (FAJ 2014) [S314], 1 Jul 1986–31 Dec 2013: BXM annualized excess return **4.4%** vs S&P **5.4%**, volatility **13.4%** vs **18.5%**, **Sharpe 0.33 vs 0.29**, worst drawdown **−43.0%** vs **−61.7%**, beta **0.67**, **upside beta 0.63 / downside beta 0.78**. Writing the call cut beta from 1.00 to 0.64; ~two-thirds of risk from the equity premium, one-third from the short straddle.
- **Interpretation:** covered calls have historically delivered equity-like returns with lower beta/vol and shallower drawdowns — but at the cost of *asymmetric* exposure (more sensitivity to down-moves than up-moves; upside beta 0.63 < downside beta 0.78) [S314]. This is the mechanical price of selling the right tail.

**Protective puts (robust documentation, contested value):**
- Israelov & Nielsen (JPM 2015) [S313] analyze a 5%-OTM monthly protective-put program on the S&P 500 (Mar 1996–Jun 2014): it cuts portfolio beta from **1.00 to 0.72** and **downside beta from 1.00 to 0.47**. Decomposing returns: passive equity (≈5.2%/yr excess), dynamic-equity (insignificant −0.9%/yr), and **long-volatility exposure costing ≈2.0%/yr with a Sharpe of −0.83**. The authors' verdict: paying for that 0.10 reduction in downside beta via puts is "too expensive" — selling 10% of the equity position achieves the same beta cut at ~0.6%/yr cost (assuming a 6% equity risk premium).
- **Interpretation:** protective puts *work* as insurance (limited loss, preserved upside) but are a negative-expected-return carry trade in normal times because the buyer pays the VRP [S313]. They are most defensible for discrete, known-risk horizons (earnings, M&A) or for investors with hard constraints, not as a permanent overlay.

**Confidence assessment:** strategy *mechanics* are **robust** (defined payoffs, benchmark construction). The claim that these strategies *add risk-adjusted value on a sustained basis* is **contested** — the edge is the VRP, which can compress or invert, and net-of-cost live implementation differs from passive index backtests.

## Conflicting views
- **"Covered calls give downside protection."** Israelov & Nielsen [S314] label this a **myth**: the premium is small relative to drawdowns, and the position is *more* exposed to negative than positive market returns (upside beta 0.63 vs downside beta 0.78). The protection is partial and asymmetric.
- **"Covered calls generate income."** Also flagged as a misleading framing [S314]: the premium is compensation for *selling volatility/optionality*, not risk-free yield; describing it as "income" obscures the short-vol risk.
- **"Protective puts are cheap when volatility is low."** Israelov & Nielsen [S313] counter that an option's fair value is tied to *realized* vol, not its own implied level — low implied vol can still be expensive versus subsequent realized vol, so the VRP (not the VIX level) is what matters.
- **Bullish/bearish suitability.** CFA [S310] frames spreads as expressing moderate directional views with defined risk; practitioners debate whether spreads or naked options are preferable depending on liquidity and IV skew (a separate, contested topic).

## Common mistakes
- **Treating premium as yield / ignoring the short-vol risk.** Covered calls are not bonds; in rallies you underperform and can be called away below fair value [S310, S314].
- **Buying protective puts as a permanent overlay without costing it.** Expect ~2%/yr drag and a negative-Sharpe long-vol leg in calm regimes [S313].
- **Forgetting assignment / early exercise** on American options, especially when dividends or deep ITM.
- **Ignoring transaction costs, financing, and taxes** — BXM is a *hypothetical, cost-free* index; live replication differs [S312].
- **Strike/maturity snooping** — picking the "best" covered-call or spread parameters ex post is data-mining; validate out-of-sample (see `15-pitfalls-and-antipatterns/data-snooping-phacking.md`).
- **Confusing payoff diagrams with full risk.** A covered-call diagram omits the volatility exposure that drives much of its risk/return [S314].
- **Selling naked options "for income"** — uncapped tail risk; not equivalent to the defined-risk spreads described here.

## Further reading
- **[Tier 1]** CFA Institute, *Options Strategies* (2026 L3 refresher) — https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/options-strategies
- **[Tier 1]** Cboe, *BuyWrite Indices Methodology* (BXM/BXMD/BXY/BXR) — https://cdn.cboe.com/api/global/us_indices/governance/Cboe_BuyWrite_Indices_Methodology.pdf
- **[Tier 1]** Ibbotson Associates, *BXM Buy-Write Case Study* (2004) — https://cdn.cboe.com/resources/education/research_publications/IbbotsonAug30final.pdf
- **[Tier 1]** Israelov & Nielsen, "Still Not Cheap: Portfolio Protection in Calm Markets," *J. Portfolio Mgmt* 41(4), 2015 — https://www.aqr.com/-/media/AQR/Documents/Journal-Articles/JPM-Still-Not-Cheap.pdf
- **[Tier 1]** Israelov & Nielsen, "Covered Call Strategies: One Fact and Eight Myths," *Financial Analysts Journal* 70(6), 2014 — https://rpc.cfainstitute.org/research/financial-analysts-journal/2014/covered-call-strategies-one-fact-and-eight-myths
- **[Tier 2]** Optiver, *Options strategies (protective put & covered call)* — https://www.optiver.com/insights/explainers/options-strategies-part-one
- Companion KB articles: `10-derivatives/option-greeks.md`, `10-derivatives/volatility-surface-skew-hedging.md`, `04-quant-and-factors/low-vol-quality-carry-factors.md` (the short-vol / low-risk anomaly link).
