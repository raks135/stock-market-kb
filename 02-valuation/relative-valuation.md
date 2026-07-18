---
title: Relative Valuation — Trading Comparables and Valuation Multiples
topic_id: 02-valuation/relative-valuation
tags: [valuation, relative-valuation, comparables, multiples, pe, peg, pb, ps, ev-ebitda, enterprise-value]
last_updated: 2026-07-18
confidence: robust
sources: [S58, S59, S60, S61]
---

## TL;DR
- Relative valuation ("comps") values an asset by comparing a **standardized multiple** (value ÷ a fundamental) against the same multiple for comparable firms or a benchmark (sector, index, own history) [S58, S59]. It assumes the **law of one price**: similar assets should trade at similar multiples once fundamentals are controlled for [S58].
- The four most-used multiples are **P/E, P/B, P/S (equity-side)** and **EV/EBITDA, EV/EBIT, EV/Sales (firm-side)**. Match the numerator's claimholder to the denominator's (equity value ÷ equity earnings; enterprise value ÷ firm earnings) or the multiple is meaningless [S59, S61].
- Three-bucket rating: the *method* is **robust** (used in an estimated ~85% of equity research reports per Damodaran [S59]); its *output* is **emerging/folklore** — a comps number is a *relative* judgment about what the market currently pays, not an intrinsic value, and it inherits every bias in the peer group's prices [S59].
- Critical guardrails: use **median not mean** (distributions are skewed) [S59]; control for leverage/growth/risk differences [S58, S59]; never treat a low multiple as "cheap" without checking why [S59]; and remember relative valuation can only tell you what the market prices *similar* assets at today — it says nothing about absolute correctness.

## Core explanation
In intrinsic (DCF) valuation you estimate cash flows and discount them. In **relative valuation** you do something simpler and far more common: you take the asset's market price, divide it by some fundamental (earnings, book value, sales, EBITDA), and compare that ratio — the *multiple* — to the same ratio for comparable assets. If the target's multiple is below the peer median after controlling for differences, it is flagged "relatively undervalued," and vice versa [S58, S59].

Damodaran's definition is crisp: "In relative valuation, the value of an asset is compared to the values assessed by the market for similar or comparable assets... compare the standardized value or multiple for the asset being analyzed to the standardized values for comparable assets, controlling for any differences between the firms that might affect the multiple, to judge whether the asset is under or over valued" [S59]. The CFA curriculum frames the same idea as the **method of comparables**, whose economic rationale is the law of one price [S58].

Why it dominates practice:
- It requires **less information** than DCF and is faster to compute [S59].
- Portfolio managers are judged on a *relative* basis, so a number expressed in peer-relative terms fits how they are evaluated [S59].
- It reflects **current market mood**, which is exactly what you want if you are issuing, selling, or trading against today's price (e.g., an IPO) [S59].

The flip side: because the benchmark is *market prices*, relative valuation can never tell you an asset is absolutely mispriced — only that it is priced differently from its peers. If the whole sector is in a bubble, every "fair" comp says "fair." Damodaran puts it bluntly: "There are no similar assets. Every asset is unique... If you don't control for fundamental differences in risk, cashflows and growth across firms when comparing how they are priced, your valuation conclusions will reflect your flawed judgments rather than market misvaluations" [S59].

## Math / formulas

**The multiple is a ratio of value to a fundamental [S58, S59]:**
```
Multiple = Value / Fundamental
  Value      ∈ {Equity Value (market cap), Enterprise Value (EV)}
  Fundamental∈ {EPS, Book Equity, Sales, EBITDA, EBIT, CF, ...}
```

**Enterprise value (the firm-side numerator) [S59, S61]:**
```
EV = Market Value of Equity (market cap)
   + Market Value of Debt
   + Market Value of Preferred
   + Non-controlling (minority) Interests
   − Cash and Cash Equivalents
```
(Net debt = total debt − cash is the common shortcut; prefer full EV when minorities/preferred exist.)

**The big multiples [S58, S59, S61]:**

| Multiple | Numerator | Denominator | Best when |
|---|---|---|---|
| P/E (trailing) | Price | TTM EPS | Profitable, stable-earnings firms |
| P/E (forward) | Price | Next-yr EPS | Forward-looking views |
| PEG | P/E | Consensus EPS growth % | High-growth comparison |
| P/B | Price | Book value per share | Asset-heavy / financials |
| P/S | Price | Sales per share | Low/negative earnings, early stage |
| EV/EBITDA | EV | EBITDA | Comparing across leverage; capex-heavy |
| EV/EBIT | EV | EBIT | Capex differences matter |
| EV/Sales | EV | Revenue | Negative EBITDA, varying leverage |

**The matching rule (definitional test) [S59]:** both numerator and denominator must belong to the same claimholders. Equity value ÷ equity earnings (P/E, P/B, P/S). Firm value (EV) ÷ firm earnings (EBITDA, EBIT, Sales). *Mixing them — e.g., P/EBITDA — is a category error* because EBITDA accrues to all capital providers, not just equity [S61]. Hence EV/EBITDA is preferred to P/EBITDA [S58].

**Justified (fundamentals-implied) multiples** — derived by algebra from a DCF model, these tell you what multiple is *consistent* with a firm's growth, risk, and payout, and let you compare a market multiple to fundamentals [S58, S59]:
```
Justified P/E  ≈ Payout Ratio · (1 + g) / (r − g)        (constant-growth DDM/FCFE)
Justified P/B  = (ROE − g) / (r − g)
Justified P/S  ↑ with net profit margin, growth; ↓ with required return r
```
where `g` = expected growth, `r` = required return (cost of equity), `ROE` = return on equity. A market P/E *above* its justified P/E (given your fundamentals) suggests overvaluation relative to those fundamentals — but note it still only compares to your own assumptions [S58].

**PEG [S58]:** `PEG = (P/E) / (EPS growth rate in %)`. Stocks with lower PEG are, all else equal, more attractive; it rescales P/E by growth so a high-P/E fast-grower is not automatically "expensive."

**Central-tendency of a peer group [S58, S59]:** use the **median** (robust to skew and outliers); the **harmonic mean** is technically correct for ratios like P/E when averaging across firms (because you are averaging price/earnings, the denominator should be summed), and the arithmetic mean is acceptable only as a rough gauge. Damodaran warns peer-multiple distributions are typically right-skewed, so the mean overstates the "typical" multiple [S59].

## Worked example / code
A self-contained, library-free comps table. Data source: a practitioner would pull `market cap`, `total debt`, `cash`, `EBITDA`, `net income`, `book equity`, and `sales` from each peer's 10-K/10-Q via **SEC EDGAR** (or a vendor such as Capital IQ, FactSet, or Bloomberg). Here we hard-code a small peer set so the snippet runs offline and is fully reproducible.

```python
# relative_valuation_demo.py  (pure stdlib; Python 3.10+)
# Data source for real use: SEC EDGAR / Capital IQ / FactSet / Bloomberg.

def enterprise_value(market_cap, total_debt, cash, preferred=0.0, minority=0.0):
    return market_cap + total_debt + preferred + minority - cash

# Peer group (illustrative $ millions). Replace with live filings data.
peers = [
    # name,          mkt_cap, debt, cash, ebitda, ni,   book_eq, sales
    ("Peer_A",        4000,  800,  300,   600,   350,   1200,   3000),
    ("Peer_B",        9000, 1500,  500,  1200,   800,   3000,   7000),
    ("Peer_C",        2500,  400,  200,   400,   180,    800,   2000),
    ("Peer_D",       15000, 3000,  900,  2100,  1300,   5000,  11000),
]

rows = []
for name, mc, d, c, eb, ni, be, sa in peers:
    ev = enterprise_value(mc, d, c)
    rows.append({
        "name": name, "EV": ev, "EBITDA": eb, "NI": ni, "BookEq": be, "Sales": sa,
        "EV_EBITDA": ev / eb,
        "PE": mc / ni,
        "PB": mc / be,
        "PS": mc / sa,
    })

def median(xs):
    s = sorted(xs); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

med = {k: median([r[k] for r in rows]) for k in ("EV_EBITDA", "PE", "PB", "PS")}
print("Peer median multiples:", {k: round(v, 2) for k, v in med.items()})

# Target company (the one we are valuing), $ millions
target = {"mkt_cap": 6000, "debt": 1000, "cash": 400,
          "ebitda": 900, "ni": 500, "book_eq": 1800, "sales": 4500}
t_ev = enterprise_value(target["mkt_cap"], target["debt"], target["cash"])

# Apply peer medians to target fundamentals -> implied values
implied_equity_ev_ebitda = med["EV_EBITDA"] * target["ebitda"] - target["debt"] + target["cash"]
implied_equity_pe        = med["PE"] * target["ni"]
implied_equity_pb        = med["PB"] * target["book_eq"]
implied_equity_ps        = med["PS"] * target["sales"]

print(f"Target actual market cap : ${target['mkt_cap']:.0f}m")
print(f"Implied equity via EV/EBITDA: ${implied_equity_ev_ebitda:.0f}m")
print(f"Implied equity via P/E      : ${implied_equity_pe:.0f}m")
print(f"Implied equity via P/B      : ${implied_equity_pb:.0f}m")
print(f"Implied equity via P/S      : ${implied_equity_ps:.0f}m")
```
Run with `python3 relative_valuation_demo.py`. The output brackets the target's actual $6,000m market cap with four independent implied values — the spread *between* the four is itself the key signal: a tight cluster near the actual price says the market is pricing the target consistently with peers; a wide spread says either the target or the peer median is mispriced (or the multiples measure different things). Note that the example uses clean, scrubbed figures; real comps require adjusting for non-recurring items, leverage, and fiscal-year-end differences ("calendarizing") before computing multiples [S61].

## Assumptions & limitations
- **Law of one price holds** — comparable assets trade at comparable multiples. This fails when the "comparables" are not truly comparable in fundamentals [S58, S59].
- **The benchmark is correct** — comps inherit the valuation of the peer group. In a sector-wide bubble, every "fair" comp is expensive in absolute terms [S59].
- **Multiples are estimated uniformly** — same accounting standards, same definitions (trailing vs forward EPS, LTM vs NTM EBITDA). Mixing GAAP and IFRS, or TTM with forward, silently breaks comparability [S59, S61].
- **Distributions are skewed** — using the mean instead of the median pulls the benchmark up by outliers [S59].
- **Negative or near-zero denominators** — P/E is undefined for loss-makers; P/B is meaningless when book value is near zero or negative; P/S ignores cost structure and can reward unprofitable revenue [S58].
- **Capital-structure mismatch** — P/E penalizes leveraged firms; EV/EBITDA neutralizes leverage but hides the risk that debt creates [S58, S61].
- **Single multiple ⇒ false precision** — one multiple captures one slice of value; the CFA and Damodaran both recommend triangulating several and, ideally, anchoring to a fundamentals-justified multiple [S58, S59].

## Empirical evidence
- **Pervasiveness:** Damodaran estimates roughly **85% of equity research reports** rely on a multiple/comparables, and over **50% of acquisition valuations** use multiples; even many "DCF" valuations back into a number first derived from a multiple, or set terminal value with a multiple [S59]. This is strong, practitioner-corroborated evidence that relative valuation is the dominant real-world method (robust, not contested).
- **Theoretical anchor:** The "justified multiple" algebra (P/E, P/B, P/S as functions of growth, risk, payout/margin) is derived directly from DCF and is standard in the CFA curriculum, confirming multiples are not arbitrary but encode the same fundamentals as intrinsic valuation [S58, S59].
- **Predictive / mean-reversion evidence (contested, treat as emerging):** A large academic literature finds broad market multiples such as the S&P 500 P/E (and Shiller CAPE) are **mean-reverting at long horizons** and explain a meaningful share of *long-horizon* (multi-year) future returns, with explanatory power rising with horizon (e.g., R² of ~20% or more at 4–5 year horizons in seminal work; see Campbell & Shiller 1998 and Weigand & Irons 2007 as representative citations). However, this is a *market-level* result, much weaker at the single-stock level and useless at short horizons. **I have not opened the primary papers for this claim — treat the single-stock version as unverified and see the Verify task below.**
- **Comparable-firm selection is the weak link:** empirically, analyst "comps" sets are chosen by sector membership, not by matched fundamentals, so reported "cheapness" often reflects omitted risk/growth differences rather than mispricing [S59]. This is a documented, robust limitation rather than a refutation.

## Conflicting views
- **"Comps are objective" vs "comps are circular."** Practitioners (WSP, Investopedia) present comps as a market-based, objective anchor [S60, S61]; Damodaran counters that most "DCF" valuations are really relative valuations in disguise and that the method inherits all market mood and bias, so it is only as objective as the peer group's prices [S59]. Resolution: comps are *consistent-with-market*, not *correct*.
- **Median vs mean for the benchmark.** CFA and most practitioners report both but emphasize the median for skewed distributions [S58]; some screens still quote the mean. Using the mean on a right-skewed multiple overstates "typical" [S59].
- **P/E vs EV/EBITDA as the default.** Retail and academia often default to P/E; investment-banking practice favors EV/EBITDA (capital-structure neutral) [S61]. Damodaran's sector table resolves this pragmatically: revenue multiples for retail, P/B for financials, PEG for tech, EV/EBITDA for infra [S59].
- **Is a low multiple "cheap"?** Intuition says yes; both CFA and Damodaran warn a low multiple usually reflects lower growth, higher risk, or lower quality — you must *explain the gap with fundamentals* before calling it cheap [S58, S59].

## Common mistakes
1. **Mismatched claimholders** — using P/EBITDA or EV/EPS. Keep equity multiples equity, firm multiples firm [S59, S61].
2. **Using the mean of a skewed multiple** instead of the median [S59].
3. **Comparing across inconsistent accounting/definitions** (TTM vs forward, GAAP vs IFRS, LTM vs fiscal) [S59, S61].
4. **Treating negative-earnings firms with P/E** — the ratio is undefined or misleading; switch to EV/EBITDA, P/S, or forward estimates [S58].
5. **Ignoring leverage in P/E** — a levered firm looks "cheaper" on P/E than an identical unlevered one; prefer EV/EBITDA for cross-capital-structure comparison [S58, S61].
6. **Reading "cheap" off a low multiple without a fundamentals story** [S58, S59].
7. **Letting the peer group define itself by sector alone** — true comparables match on risk, growth, and cash-flow pattern, not just GICS code [S59].
8. **Survivorship / look-ahead in backtests of "cheap-multiple" strategies** — historical comps screens that exclude delisted/RESTATED firms or use future information overstate the edge; always state the data window and survivorship handling.
9. **Single-multiple false precision** — report a range across several multiples and anchor to a justified multiple [S58, S59].

## Further reading
- **S58 (Tier 1)** — CFA Institute, *Market-Based Valuation: Price and Enterprise Value Multiples* (2026 CFA L2 Equity Valuation refresher): https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/market-based-valuation-price-enterprise-value-multiples — canonical definitions, justified multiples, normalization, method-of-comparables rationale.
- **S59 (Tier 1)** — Damodaran, A., *Relative Valuation* (NYU Stern exec-val notes, relval.pdf): https://pages.stern.nyu.edu/~adamodar/pdfiles/execval/relval.pdf — four-step deconstruction, definitional/descriptive/analytical/application tests, sector multiple-choice table, prevalence stats.
- **S60 (Tier 2)** — Investopedia, *Comparables Approach to Equity Valuation*: https://www.investopedia.com/articles/investing/080913/equity-valuation-comparables-approach.asp — accessible contrast with DCF/precedent/asset-based methods.
- **S61 (Tier 2)** — Wall Street Prep, *Comparable Company Analysis (Trading Comps)*: https://www.wallstreetprep.com/knowledge/comparable-company-analysis-comps — step-by-step peer selection, scrubbing/calendarizing, EV vs equity multiples, output conventions (min/25/median/mean/75/max).
- Related KB articles: `02-valuation/dcf.md` (intrinsic anchor), `01-fundamental-analysis/ratio-analysis.md` (the raw ratios behind the denominators), `01-fundamental-analysis/quality-of-earnings.md` (why reported EPS/book can distort multiples).
