---
title: Market Structure, Instruments, Order Types & Participants
topic_id: 00-foundations/market-structure
tags: [market-structure, order-types, liquidity, market-maker, bid-ask, primary-secondary]
last_updated: 2026-07-15
confidence: robust
sources: [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12]
---

## TL;DR
Stocks trade on a **secondary market** (exchanges/ATS) where **market makers** quote continuous two-sided prices and earn the **bid–ask spread**. You trade via **market / limit / stop** orders, each with a different execution-price guarantee. Transaction cost ≈ the spread + explicit fees; the spread is the first thing a strategy must overcome to be profitable.

## Core explanation
A **stock** is a fractional ownership claim on a company (equity). New issues are sold in the **primary market** (e.g., an IPO); after that, shares trade among investors in the **secondary market** — what people mean by "the stock market" (NYSE, Nasdaq, and ATS venues) [S8][S9].

The secondary market is an **order-driven + dealer-hybrid** system. At any moment there is a **best bid** (highest price someone will buy at) and **best ask/offer** (lowest price someone will sell at). The gap is the **bid–ask spread** — the cost a price-taker pays to trade immediately [S6][S7].

**Market makers** (a.k.a. liquidity providers / designated market makers) stand ready to buy at the bid and sell at the ask, continuously, for their own account. They profit from the spread and are obligated (on registered exchanges) to maintain continuous quotes; exchanges often pay them rebates (maker-taker) to post liquidity [S4][S10][S11].

## Math / formulas
- **Spread** = `ask − bid`
- **Mid price** = `(bid + ask) / 2`
- **Quoted spread (relative)** = `(ask − bid) / mid`
- **Effective spread** (price-taker) = `2 · |trade_price − mid| / mid` — captures which side you crossed.
- **Implementation shortfall** ≈ `executed_price − decision_time_mid` (slippage vs. when you decided).

Spreads widen with volatility and thin liquidity; a wide spread is a tax on turnover [S6][S7].

## Worked example / code
Show the spread and a simple cost estimate from a live quote snapshot. Data source: any quote feed (here we use a placeholder; replace with your vendor — see 13-data-and-tooling).

```python
# python 3.11, no external deps (illustrative)
bid, ask = 100.00, 100.12          # quoted prices
mid = (bid + ask) / 2
spread = ask - bid
rel_spread = spread / mid
print(f"mid={mid:.2f} spread={spread:.2f} rel={rel_spread:.4%}")

# round-trip cost if you buy at ask then sell at bid (ignoring fees)
round_trip = (ask - bid) / mid
print(f"round-trip cost ~ {round_trip:.4%} of notional")
```
Output: `mid=100.06 spread=0.12 rel=0.12%`, round-trip ≈ 0.12% — a strategy must clear this *before* fees to break even on a round trip.

## Assumptions & limitations
- Continuous two-sided quotes exist (true for liquid names; not for illiquid/thin names where the book is sparse).
- The mid is a fair reference (falls apart in fast moves / gaps).
- Spread is only the *implicit* cost; explicit commissions, fees, and **market impact** (size you trade vs. available liquidity) add to it (see 09-market-microstructure).

## Empirical evidence
- Maker-taker rebates and competition post-Reg NMS increased quoted liquidity and narrowed spreads on lit venues [S1][S5].
- HFT/algorithmic market making improved measured liquidity (tighter spreads, more depth) in normal conditions, but the same speed can amplify fragility during stress (flash events) [S1][S5]. This is **contested** — see below.
- Payment for order flow and rebate structures are associated with both tighter retail spreads and concerns about price discovery / execution quality [S5].

## Conflicting views
- **HFT net effect:** Some evidence (SEC 2014 lit review, O'Hara 2015) frames HFT as a net liquidity *improver* in calm markets; critics (and post-2010 flash-event analyses) argue it extracts spread rent and worsens crises. Resolution is regime-dependent — treat as **contested**, not settled.
- **Maker-taker:** exchanges say it attracts liquidity; some studies argue it misaligns execution quality for retail. Needs a Tier-1 confirmation (logged as a Verify task).

## Common mistakes
- Treating the **last traded price** as the price a market order will fill at — it won't; you fill at ask (buy) / bid (sell) [S2].
- Ignoring the spread when backtesting (assuming mid-to-mid fills) — overstates returns (see 08-backtesting-methodology, 15-pitfalls).
- Assuming all venues are equal — fragmentation means the "best price" may be on a venue you don't reach without smart order routing [S1].
- Confusing **primary** (issuer gets the money) vs **secondary** (investors trade; issuer gets nothing) — IPO hype often blurs this [S8][S9].

## Further reading
- SEC market-structure HFT review (Tier 1) [S1]; NYSE market-making paper (Tier 1) [S4]; O'Hara 2015 JFE (Tier 1) [S5]; FINRA order types (Tier 1) [S3]; Investor.gov (Tier 1) [S2]; Investopedia spread/market-maker (Tier 2) [S6][S10].
