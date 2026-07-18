---
title: Maker-Taker Pricing, Payment for Order Flow (PFOF), and High-Frequency Trading (HFT)
topic_id: 09-market-microstructure/maker-taker-pfof-hft
tags: [market-microstructure, maker-taker, payment-for-order-flow, PFOF, HFT, high-frequency-trading, reg-nms, best-execution]
last_updated: 2026-07-18
confidence: contested
sources: [S1, S5, S25, S26, S28, S296, S297, S298, S300, S301]
---

## TL;DR
- **Maker-taker** is the dominant equity-venue pricing model: exchanges pay a *rebate* to traders who post resting limit orders (makers) and charge a *fee* to those who hit them (takers). It attracts liquidity provision but also steers routing toward rebate-rich venues and tilts the profit mix toward fast limit-order traders.
- **Payment for order flow (PFOF)** is a broker's compensation from a wholesaler/market-maker for routing client orders to it. It underwrites commission-free retail trading but creates a structural conflict with the broker's best-execution duty (SEC v. Robinhood, 2020: $65M penalty for inferior execution tied to high PFOF rates).
- **HFT** is a *large subset* of algorithmic trading (often >50% of US equity volume). The evidence is genuinely **contested**: in normal times HFT narrows spreads and adds price discovery; in stress it withdraws depth and amplifies moves (Flash Crash 2010). Treat "HFT is good" and "HFT is toxic" as both partially true.

## Core explanation
### Maker-taker pricing
A trading venue's *matching engine* fills orders by priority (typically price-time). Traders who submit resting **limit orders** that add size to the book are **makers**; traders who submit **market orders** that consume that size are **takers**. Under maker-taker, the venue **rebates** makers (e.g., a fraction of a cent per share) and **charges** takers a fee (O'Hara 2015, S5; Investopedia, S296). Island ECN introduced the model in 1997 and it is now the dominant pricing structure in US equity markets (S5). The net spread between taker fees and maker rebates is the exchange's revenue.

Variants exist: **taker-maker** (rebate to the market-order side, fee to limit-order side — historically used to attract *less toxic* retail flow), and **subscription** ("all-you-can-trade" monthly fee) venues (S5). Exchanges also differentiate rebates by *where* a maker posts (at/join/outside NBBO) to incentivize quoting at the touch (S5).

### Payment for order flow (PFOF)
PFOF is compensation a broker-dealer receives for directing customer orders to a particular market maker or venue. The Exchange Act defines it in **Rule 10b-10(d)(8)** as "any monetary payment, service, property, or other benefit that results in remuneration, compensation, or consideration to a broker-dealer in return for the routing of customer orders" (SEC, In re Robinhood, 2020, S298). It is *legal* provided the broker still satisfies its **best-execution** duty and discloses terms in **Rule 606** quarterly reports (S298; S297).

PFOF is the economic engine behind zero-commission retail brokers: when commissions fell in the mid-2010s, PFOF became a primary revenue source (S297). A 2022 study cited by Investopedia found roughly **65% of broker PFOF revenue came from options, ~30% from non-S&P 500 stocks, and only ~5% from S&P 500 stocks** — because options spreads are wider and more profitable to internalize (S297).

### High-frequency trading (HFT)
HFT is a *strategy-based, computer-driven* style characterized by extreme speed (latency measured in milliseconds down to nanoseconds), co-location, very short holding periods (often flat by day-end), and high order-cancel rates (often >90% of messages cancelled; the SEC found 23% of cancelled orders and 38% of cancelled quotes occur within 50 ms of placement, S5). The SEC estimates HFT is **typically >50% of volume** in US-listed equities (S1). Crucially, HFT is a *subset* of algorithmic trading, not identical to it (S1).

## Math / formulas
**Maker-taker round-trip cost (per share).** For a trader who both provides and takes liquidity:

- Maker rebate received: `−r` (negative = cash in)
- Taker fee paid: `+f`
- Exchange net revenue per share traded: `f − r` (the "exchange spread")

A pure liquidity **taker** pays `f` per share taken; a pure **maker** earns `r` per share posted. Because HFT can post and cancel limit orders faster than anyone, limit-order trading is less risky for them, so maker rebates are "a substantial source of profit for high frequency traders" (S5).

**Reg NMS access-fee cap.** Rule 610(c) caps the per-share/per-order access fee a trading center may charge. The **2024 amendments lowered the cap from $0.003 to $0.001 per share** (Davis Polk summary of the 2024 rule, S28; SEC Atkins statement, S25). The access fee is the fee a venue charges others to access its quotations — distinct from, but related to, the maker-taker taker fee.

**HFT share of volume.** Let `V_HFT` = shares attributed to HFT accounts in a proprietary dataset; HFT share `= V_HFT / V_total`. SEC staff note these figures "typically exceeded 50%" (S1). Proxy-based estimates from public data are noisier and can capture non-HFT algorithmic flow (S1).

## Worked example / code
The snippet below is **synthetic/illustrative** (stdlib only, seed fixed). It demonstrates the central microstructure narrative from Kirilenko et al. (2014, S300): HFT firms normally *supply* top-of-book depth, but when they withdraw in stress the book is thinner, so an identical aggressive sell order moves price **more**. This is the mechanism behind "HFT adds liquidity in calm markets, removes it in stress."

```python
import random
random.seed(42)

def market_impact(hft_present, sweep_shares=50_000,
                  depth_hft=10_000, depth_stress=4_000,
                  tick=0.01, mid=100.0):
    """Ticks moved and % price impact when `sweep_shares` hits a one-sided book.
    HFT normally supplies ~60% of resting depth; in stress that depth is pulled."""
    depth = depth_hft if hft_present else depth_stress
    remaining = sweep_shares
    ticks_moved = 0.0
    while remaining > 0 and ticks_moved < 100:
        take = min(remaining, depth)
        remaining -= take
        ticks_moved += take / depth
    impact_pct = ticks_moved * tick / mid * 100.0
    return ticks_moved, impact_pct

calm_t, calm_p = market_impact(True)
str_t,  str_p  = market_impact(False)
print(f"Calm   (HFT supplying depth 10k/level): {calm_t:.1f} ticks, impact {calm_p:.3f}%")
print(f"Stress (HFT withdrawn,  depth 4k/level): {str_t:.1f} ticks, impact {str_p:.3f}%")
print(f"Liquidity-withdrawal amplification = {str_p/calm_p:.2f}x")
```

**Data source:** synthetic book; magnitudes chosen only to illustrate the *direction* of the effect, not a market claim. Run on CPython 3.14.4 →

```
Calm   (HFT supplying depth 10k/level): 5.0 ticks, impact 0.050%
Stress (HFT withdrawn,  depth 4k/level): 12.5 ticks, impact 0.125%
Liquidity-withdrawal amplification = 2.50x
```

## Assumptions & limitations
- **Maker-taker**: assumes price-time priority and that rebates actually change routing behavior. Evidence (Battalio, Corwin & Jennings 2013, cited in S5) shows routing *is* materially influenced by rebate size — so the model is not neutral.
- **PFOF**: assumes "internalization" by a wholesaler yields at least NBBO; legally it must, but *price improvement* vs *true best available* can differ, and the conflict of interest is structural, not eliminated by the NBBO floor (S298).
- **HFT**: "HFT" is not a single strategy — it spans market-making, statistical arbitrage, and predatory tactics (spoofing, layering, momentum ignition), all grouped under one label (S5). Aggregated effects mask this heterogeneity.
- **Reg NMS**: the 2024 access-fee cap and any 2026 rescission proposal (S26) are regulatory specifics that change over time; this article reflects the state as of mid-2026.
- **Backtests/estimates**: HFT-share and PFOF-mix figures depend heavily on dataset and definition; proxy-based numbers are fragile (S1).

## Empirical evidence
**Maker-taker**
- Island introduced maker-taker in 1997; it is now dominant in US equities (S5). Rebates are a "substantial source of profit" for HFT (S5).
- Routing decisions of retail brokers are "greatly influenced by the size of the rebates offered by the trading venues" (Battalio, Corwin & Jennings 2013, cited in S5).
- 2024 Reg NMS amendments cut the access-fee cap to $0.001/share (S28, S25).

**PFOF**
- Legal and widespread; required disclosures via Rule 606; best-execution duty enforced (S298).
- SEC (2020) found Robinhood's "commission-free" model delivered *inferior* execution vs competitors, with PFOF its single largest revenue source, and imposed a **$65M penalty** for best-execution failures (S298).
- PFOF mix is options-heavy (~65% of broker PFOF revenue) because options spreads are wider (S297).

**HFT — the contested core**
- *For (liquidity/quality):* There is "general, but not universal, agreement that HFT market making enhances market quality by reducing spreads and enhancing informational efficiency" (Jones 2012; Brogaard, Hendershott & Riordan 2013; Menkveld 2013, cited in S5). Brogaard, Hendershott & Riordan (2014, RFS) find HFT **stabilize prices during transitory shocks** and that HFT **limit orders provide most price discovery** (S301). Industry HFT profits fell from ~$5B (2009) to ~$1B (2013), suggesting the edge is competed away (S5).
- *Against (fragility):* Kirilenko, Kyle, Samadi & Tuzun (2014, S300) conclude HFT **did not cause** the May 6, 2010 Flash Crash but **contributed** to it by "demanding immediacy" — aggressively removing the last contracts at the best bid and re-quoting one tick down, imposing an "immediacy absorption" cost on slower traders, especially in stress. The joint CFTC-SEC (2010) report traced the trigger to a **$4.1B E-mini S&P 500 sell order** (Waddell & Reed) amplified by algorithmic activity (S300); it recommended short-lived trading pauses (circuit breakers). Jarrow & Protter (2012) model a "dysfunctional role" for HFT in electronic markets (cited in S5).

## Conflicting views
- **HFT net effect.** "HFT improves liquidity and price discovery" (Brogaard/Hendershott/Riordan, Menkveld) vs "HFT is a source of fragility that withdraws exactly when needed" (Kirilenko & Kyle). The resolution is **regime-dependent**: HFT is a net liquidity *supplier* in calm markets and a net liquidity *withdrawer* in stress (S300, S5).
- **Maker-taker.** Encourages dense, competitive limit-order books (good) vs distorts routing toward rebate capture and can subsidize predatory limit-order strategies (S5; S296).
- **PFOF.** Enables commission-free trading and often *price improvement* for retail (S297; S298) vs an inherent conflict of interest where the broker's profit can override client best execution (S298; S297). The EU is phasing PFOF out by 2026; the SEC has proposed restrictions/transparency but not an outright ban (S297).
- **Policy.** Reg NMS Rule 610 access-fee cap was cut to $0.001 (S28); a 2026 SEC proposal would **rescind Rule 611** (order protection) and Rule 610(e) (sub-penny pricing) — contested and proposal-stage (S26).

## Common mistakes
1. **Conflating HFT with all algorithmic trading.** HFT is a fast, strategy-based subset; institutional execution algorithms (VWAP/TWAP) are not HFT (S1, S5).
2. **Assuming PFOF = worse prices always.** Many retail orders receive *price improvement* vs NBBO; the risk is the *marginal* incentive to route to the highest payer rather than the best executor (S298).
3. **Treating "HFT share >50%" as a verdict.** It describes volume, not welfare; the same firms can be liquidity suppliers at noon and liquidity withholders at 2:45 pm on a crash day (S300).
4. **Believing maker-taker is neutral.** Rebates actively shape where orders go and which strategies profit (S5).
5. **Ignoring the NBBO floor's limits.** Best execution is a *process* duty, not a per-trade guarantee; the Robinhood case shows disclosure + NBBO compliance can still coexist with systematically inferior net prices (S298).

## Further reading
- SEC Division of Trading & Markets, *Equity Market Structure Literature Review Part II: High-Frequency Trading* (Mar 2014) — S1.
- O'Hara, M., "High frequency market microstructure," *Journal of Financial Economics* (2015) — S5.
- Kirilenko, A., Kyle, A., Samadi, M. & Tuzun, T., "The Flash Crash: The Impact of High-Frequency Trading on an Electronic Market" (2014) — S300.
- SEC, *In re Robinhood Financial LLC*, Admin. Proceeding File No. 3-20171, Rel. 10906 (Dec 2020) — S298.
- Brogaard, J., Hendershott, T. & Riordan, R., "High-Frequency Trading and Price Discovery," *RFS* 27(8):2267–2306 (2014) — S301.
- Investopedia, "Understanding Maker-Taker Fees" — S296; "Payment for Order Flow (PFOF)" — S297.
- Davis Polk, "Reg NMS Resized" (2024 amendments) — S28; Sidley Austin, "SEC Proposes Rescission of the Order Protection Rule" (2026) — S26.
