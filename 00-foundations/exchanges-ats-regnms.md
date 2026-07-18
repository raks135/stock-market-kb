---
title: Exchanges, ATS / Dark Pools, and Regulation NMS Basics
topic_id: 00-foundations/exchanges-ats-regnms
tags: [market-structure, regulation, reg-nms, ats, dark-pools, nbbo, exchanges]
last_updated: 2026-07-18
confidence: robust
sources: [S1, S20, S21, S22, S23, S24, S25, S26, S27, S28]
---

## TL;DR
- U.S. equities trade on two broad venue types: **lit exchanges** (NYSE, Nasdaq, Cboe, IEX, etc. — self-regulatory organizations) and **alternative trading systems (ATSs)**, including **dark pools**, which are broker-dealer–operated venues that need not display pre-trade interest.
- **Regulation NMS (2005)** is the backbone rule set: Rule 610 (access), Rule 611 (order protection / no trade-throughs, which creates the NBBO), Rule 612 (minimum tick size), and the Market Data Rules (consolidated quotes/trades + execution-quality disclosure).
- Off-exchange trading is now the majority of volume (Nasdaq: >50% in Nov 2024–Jan 2025), but most of that growth is **bilateral/internalizer** flow, not dark pools — dark-pool share has been roughly rangebound since ~2019.
- The regime is **actively changing**: 2024 amendments cut the access-fee cap and introduced a half-penny tick for tight-spread stocks; in June 2026 the SEC **proposed** (not yet adopted) rescinding the Order Protection Rule. Treat current structure as contested/evolving.

## Core explanation
### Venues: lit exchanges vs. ATS vs. dark pools
Historically, U.S. stock trades occurred only on exchanges such as the NYSE and Nasdaq (S22). Two SEC rulemakings changed this: **Regulation ATS** (adopted 1998) and **Regulation NMS** (adopted 2005) enabled a proliferation of competing venues (S22). Today the landscape splits into:

- **Lit exchanges / "lit" venues** — Traditional exchanges (NYSE, Nasdaq, Cboe, IEX, etc.) are self-regulatory organizations (SROs) that **display** pre-trade bids and offers into the public, consolidated quote stream used to price stocks (S22).
- **Alternative Trading Systems (ATSs)** — Trading venues that let securities be bought and sold **outside** traditional exchanges. An ATS must register as a broker-dealer and file an initial operation report (Form ATS; for NMS stocks, the newer **Form ATS-N**) before operating, and is subject to Regulation ATS (Rules 300–303) (S20). ATSs are operated by FINRA-member firms and are overseen by both the SEC and FINRA (S21).
- **Dark pools** — A subset of ATSs, often called "dark pools of liquidity," designed to handle large institutional block trades **anonymously**. They are "dark" because they do **not broadcast pre-trade data** — the presence, price, and size of buy/sell orders are hidden, unlike lit venues (S21, S22). They report trades *after* execution, so they contribute to price discovery only ex-post (S21).

The rationale for dark pools is reducing **market impact**: an institution trying to sell 500,000 shares on a lit exchange would likely have to work the order in smaller pieces, tipping its hand and pushing the price against itself; a dark pool lets it seek a counterparty without broadcasting intent (S21).

### Regulation NMS — the four pillars
Reg NMS (adopted April 2005, Exchange Act Release No. 34-51808) modernized the national market system. Its core provisions are (S23, corroborated by S24):

1. **Rule 610 — Access Rule.** Requires fair and non-discriminatory access to quotations, sets a **cap on access fees** that an exchange may charge to trade against a protected quote, and (via Rule 610(e)) requires SROs/FINRA to adopt rules discouraging members from displaying quotations that **lock or cross** protected quotations (S23, S28).
2. **Rule 611 — Order Protection Rule (the "trade-through rule").** Requires each trading center to establish, maintain, and enforce written policies reasonably designed to **prevent trade-throughs** — executions at prices inferior to "protected quotations" displayed by other trading centers. This is what operationalizes the **National Best Bid and Offer (NBBO)** (S23, S24).
3. **Rule 612 — Minimum Pricing Increment (the "sub-penny rule").** Prohibits displaying/ranking/accepting quotations in NMS stocks in increments smaller than **$0.01** for stocks priced at or above $1.00 (and $0.0001 for sub-dollar stocks) (S23, S28).
4. **Market Data Rules** (amendments to the joint-industry plans; Rules 604/605/606). Mandate consolidated dissemination of quotations and transactions — i.e., the **NBBO** — and require disclosure of **order execution quality (Rule 605)** and **order routing (Rule 606)** (S23).

### NBBO, protected quotes, and trade-throughs
- **National Best Bid and Offer (NBBO)** = the highest displayed bid and the lowest displayed offer for a security **across all trading centers**, as consolidated into a single national stream (S23). The NBBO is what brokers are generally expected to beat or match for customer orders.
- A **protected quotation** is an automated, immediately-and-automatically accessible best bid or best offer of an SRO trading facility (or ADF) that is displayed in the consolidated stream (S23).
- A **trade-through** is executing a trade at a price worse than a protected quotation on another venue (S23). Rule 611 forbids this.
- **Intermarket Sweep Orders (ISOs):** the most-used exception to Rule 611. An ISO lets the destination venue execute immediately at the limit price or better, *provided* it simultaneously routes additional ISOs to sweep the full displayed size of any better-priced protected quotations. This both respects price priority and enables "best-price" routing (S23).

### How dark-pool trades are reported
All trade data for listed stocks executed on ATSs (including dark pools) must be submitted to a **FINRA Trade Reporting Facility (TRF)** and published on the **consolidated tape**. FINRA also publishes weekly per-ATS volume (with a 2–4 week delay) to enhance transparency (S21). So dark pools are **not** unregulated or invisible post-trade — only their *pre-trade* interest is hidden (S20, S21).

## Math / formulas
### NBBO definitions
$$
\text{NBB} = \max_{v \in \text{venues}} (\text{bid}_v), \qquad
\text{NBO} = \min_{v \in \text{venues}} (\text{ask}_v)
$$
$$
\text{NBBO spread} = \text{NBO} - \text{NBB}
$$
A customer marketable order should receive a price **at least as good as** the NBBO; executing at a worse price is a *trade-through* (prohibited under Rule 611 absent an exception).

### Tick-size assignment under the 2024 amendments (Rule 612)
For NMS stocks priced ≥ $1.00, the minimum quoting increment is set by the stock's **Time-Weighted Average Quoted Spread (TWACS)**:
$$
\text{TWACS} = \frac{\sum_t (\text{NBO}_t - \text{NBB}_t)\cdot \Delta t_t}{\sum_t \Delta t_t}
$$
where each unique NBB/NBO pair is weighted by how long it prevailed during regular trading hours (S28). Assignment (S28):

| Min increment | Price ≥ $1.00 | TWACS (eval. period) |
|---|---|---|
| $0.01 | yes | > $0.015 |
| $0.005 (half-penny) | yes | ≤ $0.015 |
| $0.0001 | < $1.00 | n/a |

### Access-fee caps (Rule 610, as amended 2024)
| Access-fee cap | Price ≥ $1.00 | Price < $1.00 |
|---|---|---|
| $0.001 / share (10 mils) | yes | — |
| 0.1% of quote | — | yes |

Down from the prior $0.003/share (30 mils) cap for ≥$1.00 stocks (S25, S28).

## Worked example / code
The snippet below illustrates **NBBO construction and a trade-through check** using synthetic multi-venue quotes. Real consolidated NBBO requires a SIP or vendor feed (e.g., CTA/CQ plans, or commercial APIs such as Polygon, Alpaca, IEX); `yfinance` returns a *consolidated last sale / single-venue quote*, **not** venue-level NBBO, so do not mistake it for the protected quote stream.

```python
# Data source: illustrative synthetic venue quotes (NOT live consolidated NBBO).
# For production NBBO, subscribe to a SIP/vendor feed (CTA, UTP, Polygon, IEX, etc.).
# Reproducible with the Python standard library only (no third-party deps required).
# Verified on: CPython 3.11.

# Each entry = one protected quotation on one venue (price, size in shares)
book = [
    {"venue": "XNYS",   "bid": 100.10, "bid_sz": 800,  "ask": 100.20, "ask_sz": 700},
    {"venue": "XNAS",   "bid": 100.11, "bid_sz": 1200, "ask": 100.19, "ask_sz": 1000},
    {"venue": "ARCX",   "bid": 100.09, "bid_sz": 500,  "ask": 100.21, "ask_sz": 600},
    {"venue": "BATS",   "bid": 100.10, "bid_sz": 900,  "ask": 100.22, "ask_sz": 800},
    {"venue": "DARK_A", "bid": 100.12, "bid_sz": 2000, "ask": 100.18, "ask_sz": 1500},
]

nbb_row = max(book, key=lambda r: r["bid"])
nbo_row = min(book, key=lambda r: r["ask"])
nbb, nbo = nbb_row["bid"], nbo_row["ask"]
print(f"NBB = {nbb} @ {nbb_row['venue']} (sz {nbb_row['bid_sz']})")
print(f"NBO = {nbo} @ {nbo_row['venue']} (sz {nbo_row['ask_sz']})")
print(f"NBBO spread = {nbo - nbb:.4f}")

# Trade-through check: a market buy routed to DARK_A at its ask of 100.18
candidate_venue, candidate_price = "DARK_A", 100.18
if candidate_price > nbo:
    print(f"TRADE-THROUGH: {candidate_venue} ask {candidate_price} > NBO {nbo} "
          f"-> prohibited under Rule 611 absent an exception (e.g., ISO sweep).")
else:
    print(f"OK: {candidate_venue} ask {candidate_price} <= NBO {nbo}.")
```
*(If you prefer pandas, the same logic works with `pandas==2.2.2`: build a DataFrame from the `book` rows and use `.max()/.min()` on the bid/ask columns.)*
This prints the NBBO, the inside spread, and flags any execution that would violate Rule 611's price-priority backstop.

## Assumptions & limitations
- **NBBO reflects displayed, accessible size only.** A protected quote has limited posted size; sweeping a large order may exhaust it, requiring ISO routing to the next best venue (S23). "Best displayed price" ≠ "best executable price for the whole order."
- **Dark-pool prices benchmark off lit markets.** Dark pools generally must execute at prices *at least as good* as the public NBBO (per the Order Protection Rule), so they free-ride on lit-venue price discovery (S21).
- **Consolidated data has latency.** The SIP/consolidated tape lags the fastest proprietary feeds; "protected" status can be stale at HFT timescales (see S1 on fragmentation/HFT).
- **Reg NMS is not static.** The figures above (half-penny tick, $0.001 access cap) reflect 2024 amendments whose compliance dates have been phased and partly extended via exemptive relief into 2026–2027, and a 2026 *proposal* could rescind Rule 611 (see below). Verify current effective dates against the SEC release.
- **Off-exchange ≠ dark pool.** Conflating the two misstates where liquidity resides (see Common mistakes).

## Empirical evidence
- **Dark-pool growth (historical):** dark pools rose from ~4% of overall equity volume in 2008 to ~15% in 2013 (CRS, S22). More recent academic work (Irvine, 2023, cited by AEA) places **off-exchange** share at 47.2% of U.S. equity volume in Jan 2021 — but note that is *off-exchange broadly*, not dark pools alone.
- **Recent off-exchange dominance:** Nasdaq's chief economist reports off-exchange share **topped 50%** in November 2024 and stayed above 50% in Dec 2024–Jan 2025, and exceeded 45% across all market caps since 2019. Crucially, the *growth* since ~2019 is driven by **bilateral/internalizer** flow, while **dark-pool (ATS) share has been roughly rangebound** (S27).
- **Rule 610/612 amendments upheld:** The D.C. Circuit denied challenges to the 2024 access-fee/tick-size amendments (Oct 2025), and the SEC estimated the half-penny tick would apply to ~1,800 stocks (~66% of share volume, ~43% of dollar volume) (S25, S28).
- **Strength of evidence:** Venue-definition and Reg NMS mechanics are **robust** (direct SEC/FINRA/CRS primary sources). Volume-share claims are **robust** but fast-moving; always re-check the latest FINRA/Nasdaq data before quoting a percentage.

## Conflicting views
- **Does Rule 611 (Order Protection) help or hurt?** *Robust-benefit view:* it protects price priority, acts as a backstop to best execution, and incentivizes traders to post competitive displayed liquidity (S23; S26 background). *Critique:* it has been blamed for **increasing fragmentation** and connectivity costs (forcing brokers to connect to many venues) and may have **pushed volume to dark/off-exchange** venues where competition is on speed/fees rather than displayed liquidity (S24; S1 context).
- **Dark pools: efficiency vs. transparency.** Proponents: lower trading costs, enable large blocks without moving the market, improve execution for institutions (S21, S22). Critics / regulators (incl. former SEC Chair Mary Jo White): they may **impair price discovery** and raise fairness concerns; enforcement actions (e.g., the 2014 NY AG suit against Barclays over misrepresented HFT activity in its dark pool) illustrate the risk of opaque, mislabeled flow (S22).
- **2026 proposed rescission of Rule 611 (and 610(e)).** The SEC (June 11, 2026) **proposed** rescinding these rules, arguing today's automated, interconnected markets make mandatory order protection obsolete and that it added cost/complexity and venue proliferation; best-execution duties would remain as the safeguard (S26). Independent analysis (Sidley) counters that it is **unclear** whether rescission would actually reduce fragmentation or costs, and warns it could undermine displayed liquidity, confuse investors via locked/crossed markets under the Vendor Display Rule, and weaken confidence in market data (S26). **Status: proposal only — not adopted; comments due Aug 17, 2026.**

## Common mistakes
1. **"Off-exchange" = "dark pools."** Wrong. Most off-exchange growth is bilateral/internalizer flow; dark-pool ATS share has been flat since ~2019 (S27).
2. **"Dark pools are unregulated."** Wrong. They are broker-dealer ATSs overseen by SEC + FINRA, file Form ATS-N, and must report trades to a FINRA TRF for the consolidated tape (S20, S21).
3. **Assuming NBBO is fully executable at size.** The protected quote has limited displayed size; large orders need ISO sweeps across venues (S23).
4. **Treating Reg NMS as settled.** It is under active revision (2024 amendments live; 2026 rescission *proposed*). Build systems against the *current* effective rules, not a textbook from 2006.
5. **Using a single-venue quote as "the NBBO."** Retail tickers/yfinance show a consolidated last or one venue's quote; true NBBO requires aggregating all protected quotes via a SIP/vendor feed.

## Further reading
- **[Tier 1]** SEC, *Regulation of NMS Stock Alternative Trading Systems* (Form ATS-N, dark pools) — https://www.sec.gov/rules-regulations/2018/07/regulation-nms-stock-alternative-trading-systems
- **[Tier 1]** SEC Division of Trading & Markets, *FAQs on Rule 610 and Rule 611 of Reg NMS* — https://www.sec.gov/divisions/marketreg/nmsfaq610-11.htm
- **[Tier 1]** FINRA, *Can You Swim in a Dark Pool?* — https://www.finra.org/investors/insights/can-you-swim-dark-pool
- **[Tier 1]** Congressional Research Service, *Dark Pools in Equity Trading: Policy Concerns and Recent Developments* (R43739) — https://www.everycrsreport.com/reports/R43739.html
- **[Tier 1]** SEC Chair Atkins, *Statement on Minimum Pricing Increments and Access Fee Caps* (Oct 2025, D.C. Circuit uphold) — https://www.sec.gov/newsroom/speeches-statements/atkins-101525-statement-regarding-minimum-pricing-increments-access-fee-caps
- **[Tier 1]** SEC, *Equity Market Structure Literature Review Part II: HFT* (fragmentation/HFT context) — https://www.sec.gov/marketstructure/research/hft_lit_review_march_2014.pdf
- **[Tier 2]** Investopedia, *Order Protection Rule* — https://www.investopedia.com/terms/o/order-protection-rule.asp
- **[Tier 2]** Davis Polk, *Reg NMS Resized* (Rule 612 half-penny, Rule 610 fee cap detail) — https://www.davispolk.com/insights/client-update/reg-nms-resized-sec-adjusts-tick-sizes-lowers-access-fees-and-accelerates
- **[Tier 2]** Sidley, *SEC Proposes Rescission of the Order Protection Rule* (Jun 2026) — https://www.sidley.com/en/insights/newsupdates/2026/06/sec-proposes-rescission-of-the-order-protection-rule
- **[Tier 2]** Nasdaq, *Off-Exchange Trading Increases Across All Types of Stocks* — https://www.nasdaq.com/articles/exchange-trading-increases-across-all-types-stocks
