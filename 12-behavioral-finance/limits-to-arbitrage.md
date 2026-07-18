---
title: Limits to Arbitrage
topic_id: 12-behavioral-finance/limits-to-arbitrage
tags: [behavioral, arbitrage, market-efficiency, mispricing, short-selling, agency, noise-trader-risk, factor-premiums]
last_updated: 2026-07-18
confidence: contested
sources: [S142, S336, S337, S338, S339, S340, S147, S241]
---

## TL;DR
- Textbook arbitrage is riskless and capital-free; real arbitrage needs capital, is risky, and is conducted by a small set of specialized agents using *other people's money* (Shleifer & Vishny 1997, S142).
- Three structural frictions stop mispricings from being instantly eliminated: **fundamental risk** (no perfect hedge), **noise-trader risk** (prices can move further against you before reverting), and **implementation/agency costs** (shorting, financing, performance-based capital withdrawal).
- The dangerous result: arbitrageurs are *most constrained exactly when the mispricing is largest* — when prices diverge further, their investors withdraw capital, forcing them to sell into losses (S142).
- Practical implication: a "cheap" stock can get cheaper for years; convergence is not guaranteed on your horizon, and you can be forced out before it happens. Size for survival, not for the theoretical edge.

## Core explanation

The efficient-market story relies on arbitrage to drag prices back to fundamental value. The textbook definition — "the simultaneous purchase and sale of the same, or essentially similar, security in two different markets for advantageously different prices" (Sharpe & Alexander, quoted in S142) — requires **no capital and bears no risk**: you collect the spread up front and your future cash flows net to zero.

Shleifer & Vishny (1997, S142) show this description fails in three ways that matter:
1. **Real arbitrage needs capital.** Even a near-riskless Bund futures cross-exchange trade ties up good-faith margin; if prices diverge *further* before converging, the arbitrageur must post more margin or be liquidated. Deep pockets turn "probability-one" profit into "if you survive."
2. **Real arbitrage is risky.** Most trades are *risk arbitrage* — the hedge is imperfect, fundamentals can shift, and the convergence horizon is uncertain.
3. **Real arbitrage is delegated.** The "brains" (specialized arbitrageurs) are separated from the "money" (endowments, funds, banks) by an agency relationship. The capital providers cannot see the trade; they only observe *returns*. When a trade loses money because the mispricing deepened, they rationally infer the manager is unskilled and pull capital — *precisely when the trade needs more.*

This is why anomalies (value, momentum, closed-end-fund discounts, the idiosyncratic-volatility puzzle) can persist for years instead of being arbitraged away in seconds.

### The taxonomy of limits
- **Fundamental risk** (S142, S340): the arbitrageur cannot always find a perfect substitute. Long Pepsi / short Coke when Coke is "expensive" still leaves each name's own fundamentals exposed; bad news on Pepsi hurts the long leg regardless of the mispricing.
- **Noise-trader risk** (De Long, Shleifer, Summers & Waldmann 1990, S340): irrational investors' beliefs are unpredictable. If you buy because a stock is underpriced, pessimists may become *more* pessimistic and drive it lower before it recovers. The risk that opinions worsen is itself a cost that deters rational arbitrage — so "prices can diverge significantly from fundamental values even in the absence of fundamental risk" (S340, abstract).
- **Implementation costs** (S142, S341): shorting carries borrow fees ("short rebate"), sometimes 10–20% annualized; transaction costs, financing, and capacity all bleed the spread.
- **Agency / performance-based capital** (S142): the feedback loop where losses trigger withdrawals, shrinking the arbitrageur's ability to hold or add — the mechanism that makes arbitrage "ineffective in extreme circumstances" (S142).

## Math / formulas

**Shleifer–Vishny agency model (S142).** Three agents: noise traders set a stochastic sentiment shock `s_t`; arbitrageurs know fundamental value `V` (but not `s_t` perfectly); *investors* supply capital based on the arbitrageur's *past returns*, not expected future edge. The core comparative-static result:

> Arbitrageurs using their own capital increase positions as mispricing widens. Arbitrageurs using **other people's money** do the opposite when capital is performance-based: a deeper mispricing means a mark-to-market loss today, which reduces capital tomorrow, which forces a *smaller* position exactly when the opportunity is biggest.

Formally, in their two-period setup the arbitrageur chooses position `x` to maximize expected payoff net of the probability of capital withdrawal. The withdrawal probability rises with the interim loss, so the optimal `x` is **decreasing in the depth of the mispricing** under delegated, performance-based capital. S142 prove arbitrage "becomes ineffective in extreme circumstances, when prices diverge far from fundamental values" — arbitrageurs "might bail out of the market when their participation is most needed."

**De Long et al. noise-trader risk (S340).** In an overlapping-generations model, noise traders' stochastic misperceptions create a risk that rational arbitrageurs must bear. Because risk-averse arbitrageurs are averse to this risk, they bid prices *away* from fundamentals; noise traders, by bearing the risk they themselves create, can earn a **higher expected return** than rational investors. Closed-end-fund underpricing and excess volatility are direct implications.

**Stambaugh–Yu–Yuan arbitrage asymmetry (S337).** Combine arbitrage *risk* (idiosyncratic volatility, IVOL) with the fact that **buying is easier than shorting**. With long-only capital `L` and long-short capital `B`, mispricing of asset `i` resolves roughly as

```
α_i(long-only)  ≈ (A·L + B) · y_i · σ²_ε,i / (L + B)
α_i(shorted)    ≈ A·B · y_i · σ²_ε,i / B
```

where `y_i` is noise-trader demand and `σ²_ε,i` the idiosyncratic variance. Because less capital sits on the short side, **overpricing persists more than underpricing**, and high-IVOL overpriced stocks stay the most overpriced — producing the empirically observed *negative* IVOL–return relation (S337).

## Worked example / code

Illustrative simulation of the S142 "worst when most needed" mechanism. A fundamental `V=100` is known to the arbitrageur but not to capital providers. Price first diverges (becomes underpriced to −35), then reverts. We compare an *unconstrained* arbitrageur (own capital) with a *performance-based* one (investors shrink his tradable book after any loss).

Data source: synthetic path, seed-fixed, stdlib only (no external data). This demonstrates the *mechanism*, not a market prediction.

```python
import random
random.seed(7)

V = 100.0
T = 80
prices = []
for t in range(T):
    if t < 3:
        dev = -50.0 * (t / 3)                      # 0 -> -50: fast adverse drop while building
    elif t < 55:
        dev = -50.0                                # flat cheap: mispricing PERSISTS
    else:
        dev = -50.0 + 50.0 * ((t - 55) / (T - 55)) # -50 -> 0: correction
    prices.append(V + dev)

def simulate(performance_based):
    pos = 0.0
    cash = 0.0
    cum_pnl = 0.0
    for t in range(T):
        cap_mult = 1.0
        if performance_based and t > 0:
            mtm = pos * (prices[t] - prices[t - 1])
            cum_pnl += mtm
            cap_mult = max(0.25, 1.0 + cum_pnl / 200.0)
        max_pos = 10.0 * cap_mult
        target = max(-max_pos, min(max_pos, (V - prices[t]) / 5.0))
        trade = target - pos
        pos = target
        cash -= trade * prices[t]
    return cash + pos * prices[-1]

def position_at(performance_based, t_peak):
    pos = 0.0
    cash = 0.0
    cum_pnl = 0.0
    for t in range(T):
        cap_mult = 1.0
        if performance_based and t > 0:
            mtm = pos * (prices[t] - prices[t - 1])
            cum_pnl += mtm
            cap_mult = max(0.25, 1.0 + cum_pnl / 200.0)
        max_pos = 10.0 * cap_mult
        target = max(-max_pos, min(max_pos, (V - prices[t]) / 5.0))
        trade = target - pos
        pos = target
        cash -= trade * prices[t]
        if t == t_peak:
            return pos
    return pos

nav_unc = simulate(False)
nav_pb  = simulate(True)
pos_unc = position_at(False, 30)
pos_pb  = position_at(True, 30)

print(f"Final NAV  unconstrained (own capital) : {nav_unc:8.2f}")
print(f"Final NAV  performance-based capital    : {nav_pb:8.2f}")
print(f"Position during CHEAP flat (t=30)      : unconstrained = {pos_unc:.2f} shares")
print(f"Position during CHEAP flat (t=30)      : performance-based = {pos_pb:.2f} shares")
print(f"Share of the opportunity captured by PB : {100*nav_pb/max(nav_unc,1e-9):5.1f}%")
```

Output (CPython 3.14.4, seed 7):

```
Final NAV  unconstrained (own capital) :    92.53
Final NAV  performance-based capital    :   -13.68
Position during CHEAP flat (t=30)      : unconstrained = 10.00 shares
Position during CHEAP flat (t=30)      : performance-based =  2.50 shares
Share of the opportunity captured by PB : -14.8%
```

The performance-based arbitrageur's book is cut to its 0.25 floor during the adverse drop and he is *forced to sell 4.17 shares at the bottom* (price 50, bought earlier at 83 and 67) — realizing the loss precisely when the trade is most right. By the time the mispricing corrects, he holds only 2.50 shares versus the unconstrained arbitrageur's 10.00, and ends the *identical, ultimately-correct* trade with a **loss** (−13.68) while the unconstrained earns +92.53. That is the S142 result in one number: arbitrageurs are most constrained when mispricing is largest.

## Assumptions & limitations
- The S142 model assumes investors observe only returns, not the trade — a reasonable proxy for delegated asset management but not literal for every setting.
- "Limits to arbitrage" explains *why* mispricings can persist; it does **not** by itself prove a *tradable* edge. The friction that stops professionals from correcting a price also stops you.
- The simulation is a mechanism illustration with a hand-built path; it is not a fitted market model and makes no quantitative claim about real convergence speeds.
- Agency models assume short horizons and risk aversion; long-horizon, patient capital (e.g., some endowments, Berkshire-style balance sheets) is *less* constrained — which is exactly why it can harvest limits-to-arbitrage premia.

## Empirical evidence
- **Closed-end fund discounts (Lee, Shleifer & Thaler 1991, S338).** Discounts on closed-end funds move with *individual-investor sentiment*, co-move across funds, and are most sensitive for small funds — establishing the discount as a sentiment index and a canonical "limits-to-arbitrage" exhibit (the fund holds the same assets as its NAV, yet trades at a persistent discount).
- **Costly arbitrage is real (Pontiff 1996, 2006, S339).** Pontiff documents that arbitrage costs — especially idiosyncratic risk, the "single largest cost faced by arbitrageurs" (S339 abstract) — explain why some anomalies are only partially corrected.
- **The idiosyncratic-volatility puzzle (Stambaugh, Yu & Yuan 2015, S337).** The IVOL–return relation is *negative* among overpriced stocks but *positive* among underpriced stocks; the negative side dominates because short-side arbitrage is weaker. The effect is stronger for hard-to-short stocks (low institutional ownership) and following high investor sentiment — direct, large-sample confirmation of arbitrage asymmetry.
- **Limits in action: the 2007 quant crisis (Khandani & Lo 2010, S241).** Coordinated deleveraging of similar long/short equity factor portfolios produced a temporary but violent dislocation; arbitrageurs were *forced sellers* into the widening spread, the real-world version of S142's forced liquidation.

## Conflicting views
- **"Limits to arbitrage" vs "it's just risk compensation."** Critics note that many supposed "limits" (e.g., shorting costs, idiosyncratic risk) are compensations for *real* risks, not frictions that invalidate EMH. The debate is over *magnitude*: are the frictions large enough to explain persistent anomalies, or are anomalies small, transient, and mostly risk-based?
- **Are limits shrinking?** More arbitrage capital and better technology have reduced some frictions (execution, data). But shorting constraints, agency-driven redemptions, and noise-trader risk are structural, not technological — and the 2007 and 2020 episodes show they reappear under stress.
- **Overuse caution.** "Limits to arbitrage" is sometimes invoked to rationalize *any* persistent spread; it is a necessary, not sufficient, condition for a tradable anomaly. A spread that persists because of genuine risk (carry, liquidity) is not "irrational."
- **Noise-trader-risk critique (S340).** Some argue noise traders should *lose* money and disappear (Friedman 1953; Fama 1965). De Long et al. show they can *earn more* by bearing the risk they create — but the empirical size of this edge remains contested.

## Common mistakes
- **"It's cheap, so it must converge."** Convergence is not contractual; it can take years or never arrive on your horizon. Keynes: *"markets can remain irrational longer than you can remain solvent"* (paraphrased; debated attribution, S341).
- **Ignoring the short side.** Many anomalies are long-only "cheapness" plays; the short leg that would complete the arbitrage is blocked by borrow costs, Reg SHO fails-to-deliver, or simply unavailable. You are not the arbitrageur — you're holding the constrained long.
- **Undersizing the gap, oversizing the edge.** Because the worst case is "mispricing deepens," position sizing must survive a multi-sigma adverse move, not just the expected reversion.
- **Conflating academic long–short returns with implementable ones.** See `06-portfolio-construction/factor-portfolios-smart-beta.md`: the long-short premium and the tradable ETF return differ by costs, shorts, and capacity.
- **Treating limits as a bullish signal.** A wide discount or a stretched factor is a *risk* that can widen, not a free option.

## Further reading
- **[Tier 1]** Shleifer, A. & Vishny, R.W. (1997), "The Limits of Arbitrage," *Journal of Finance* 52(1):35–55 — S142 (full text opened).
- **[Tier 1]** De Long, J.B., Shleifer, A., Summers, L.H. & Waldmann, R. (1990), "Noise Trader Risk in Financial Markets," *JPE* 98(4):703–738 — S340 (full text opened).
- **[Tier 1]** Stambaugh, R.F., Yu, J. & Yuan, Y. (2015), "Arbitrage Asymmetry and the Idiosyncratic Volatility Puzzle," *Journal of Finance* 70(5):1903–1948 — S337 (full text opened).
- **[Tier 1]** Lee, C., Shleifer, A. & Thaler, R. (1991), "Investor Sentiment and the Closed-End Fund Puzzle," *Journal of Finance* 46(1):75–109 — S338 (abstract opened).
- **[Tier 1]** Pontiff, J. (2006), "Costly Arbitrage and the Myth of Idiosyncratic Risk," *Journal of Accounting and Economics* 42:35–52 — S339 (abstract opened).
- **[Tier 1]** Khandani, A. & Lo, A. (2010), "What Happened to the Quants in August 2007?" — S241 (full text opened; limits in action).
- **[Tier 2]** Alpha Architect (2014), "Introduction to Behavioral Finance — Part 2: Limits of Arbitrage" — S341 (full text opened; practitioner taxonomy).
- **[Tier 1]** Lakonishok, Shleifer, Vishny (1992) herding — S147 (link to crowding in `12-behavioral-finance/cognitive-biases-sentiment-crowding.md`).
