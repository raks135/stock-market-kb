---
title: Discounted Cash Flow (DCF) Valuation — FCFF, FCFE, WACC, and Terminal Value
topic_id: 02-valuation/dcf
tags: [valuation, dcf, fcff, fcfe, wacc, terminal-value, intrinsic-value, free-cash-flow, gordon-growth]
last_updated: 2026-07-18
confidence: robust
sources: [S50, S51, S52, S53, S54, S55, S56, S57]
---

## TL;DR
- DCF values an asset as the **present value of its expected future cash flows**, discounted at a rate that reflects their risk. Intrinsic value = PV of FCFF discounted at WACC (firm) or PV of FCFE discounted at the cost of equity (equity) [S50, S51].
- Use **FCFF (unlevered)** discounted at **WACC** to get enterprise value, then subtract debt for equity value; or use **FCFE (levered)** discounted at the cost of equity directly. They should agree under a constant-leverage, consistent-discount-rate assumption [S50, S55].
- **Terminal value dominates:** for a typical 5-year forecast it is ~75% (a 10-year forecast ~50%) of total value, so the perpetuity/exit-multiple assumptions matter enormously [S53, S57, S56].
- Three-bucket rating: the *method* is **robust** (textbook, regulator-adjacent, near-universal analyst use); the *inputs* (WACC, growth, margins) are **emerging/folklore** — small assumption changes swing value wildly. Always present a sensitivity grid, never a single point estimate.

## Core explanation
Discounted cash flow (DCF) valuation rests on one idea: the value of any asset today equals the present value of the cash flows its owner expects to receive, discounted to reflect that those cash flows are risky and occur in the future. The CFA curriculum states it plainly: "the intrinsic value of a security [is] the present value of its expected future cash flows" [S50]. Damodaran frames the same point: "the value of an asset is the present value of the expected cash flows on that asset, discounted at a rate that reflects the riskiness of those cash flows" [S51].

There are two parallel implementations:
- **Value the firm, then back out equity (FCFF / WACC).** Free cash flow to the firm (FCFF, "unlevered" FCF) is the cash available to *all* capital providers (debt + equity). Discount it at the weighted average cost of capital (WACC) to get enterprise/firm value; subtract the market value of debt (and add cash/non-operating assets) to reach equity value [S50, S55].
- **Value equity directly (FCFE / cost of equity).** Free cash flow to equity (FCFE, "levered" FCF) is what's left for *common shareholders* after debt service and net borrowings. Discount it at the required return on equity (usually CAPM) [S50, S55].

A survey of practicing analysts (Pinto, Robinson & Stowe 2019, cited in the CFA reading) found 78.8% use a DCF approach and 86.9% of those use a discounted free-cash-flow model; FCFF models are used roughly twice as often as FCFE models [S50]. So DCF is not an academic curiosity — it is the workhorse of equity valuation.

**Why a terminal value is unavoidable.** You cannot forecast cash flows to infinity. Standard practice builds an explicit forecast of ~5–10 years, then "closes" the model with a terminal value capturing all cash flows thereafter [S52, S53]. This is where most of the value lives (see Empirical evidence), which is why terminal-value assumptions dominate the output.

## Math / formulas

**Two cash-flow definitions (starting from net income) [S50]:**
```
FCFF = NI + NCC + Int·(1 − t) − FCInv − WCInv
FCFE = NI + NCC        − FCInv − WCInv + NetBorrowing
```
where NCC = non-cash charges (e.g., depreciation), Int·(1−t) = after-tax interest, FCInv = fixed-capital investment, WCInv = working-capital investment. Bridge: `FCFE = FCFF − Int·(1−t) + NetBorrowing`. FCFF can also be built from EBIT or CFO:
```
FCFF = EBIT·(1 − t) + Dep − FCInv − WCInv
FCFF = CFO + Int·(1 − t) − FCInv
```

**Valuation equations (general/infinite form) [S50]:**
```
Firm value      = Σ_{t=1..∞} FCFF_t / (1 + WACC)^t
Equity value    = Firm value − Market value of debt (+ non-operating assets)
Equity value    = Σ_{t=1..∞} FCFE_t  / (1 + r)^t          (r = cost of equity)
```

**Constant-growth (Gordon) special case [S50]:**
```
Firm value   = FCFF_1 / (WACC − g) = FCFF_0·(1+g) / (WACC − g)
Equity value = FCFE_1  / (r − g)   = FCFE_0·(1+g)  / (r − g)
```
Requires `g < discount rate`, else the model blows up.

**Two-stage model (explicit forecast of n years + terminal value) [S50]:**
```
Firm value = Σ_{t=1..n} FCFF_t/(1+WACC)^t  +  [ FCFF_{n+1} / (WACC − g) ] / (1+WACC)^n
```
with `FCFF_{n+1} = FCFF_n·(1+g)`.

**WACC [S50, S54]:**
```
WACC = (E/V)·r_e + (D/V)·r_d·(1 − t)
```
`r_e` = cost of equity (CAPM: `r_e = r_f + β·(E[R_m] − r_f)`) [S51, S54]; `r_d` = pre-tax cost of debt (yield to maturity on comparable debt); `E, D` = market values of equity and debt; `V = E + D`; `t` = marginal tax rate.

**Terminal value — two methods [S52, S53, S57]:**
```
Gordon growth:   TV = FCFF_n·(1+g) / (WACC − g)
Exit multiple:   TV = Final-year EBITDA × Exit EV/EBITDA multiple
```
The terminal value must itself be discounted back `n` years. As a sanity check, always cross-imply one method's input from the other:
```
Implied g        = (TV·WACC − FCFF_n) / (TV + FCFF_n)
Implied multiple = TV / Final-year EBITDA
```

## Worked example / code
A self-contained, stdlib-only two-stage DCF (FCFF/WACC) with **both** terminal-value methods, an equity-value bridge, an implied-growth sanity check, and a WACC×g sensitivity grid. Numbers are illustrative but internally consistent. In practice replace the forecast arrays with your own and pull WACC inputs from market data (β from a data vendor, r_f from Treasury yields, ERP from e.g. Damodaran's published series).

```python
#!/usr/bin/env python3
# Run: python3 dcf_demo.py   (Python 3.10+, no external dependencies)
# Illustrative two-stage DCF: FCFF discounted at WACC, two terminal-value methods.

# --- CAPM cost of equity & WACC inputs ---
rf, mrp, beta = 0.04, 0.055, 1.15          # risk-free, equity risk premium, levered beta
cost_of_equity = rf + beta * mrp            # = 0.10325
pre_tax_kd, tax = 0.05, 0.21
E_mv, D_mv = 600.0, 400.0                   # market values of equity & debt ($m)
wacc = (E_mv/(E_mv+D_mv))*cost_of_equity + (D_mv/(E_mv+D_mv))*pre_tax_kd*(1-tax)

# --- explicit FCFF forecast, years 1..5 ($m) ---
fcff = [40.0, 46.0, 53.0, 61.0, 70.0]
n = len(fcff)

# --- terminal value: Gordon growth (must have g < WACC) ---
g = 0.025
tv_gordon = fcff[-1] * (1 + g) / (wacc - g)
pv_explicit = sum(f / (1+wacc)**t for t, f in enumerate(fcff, 1))
pv_tv_gordon = tv_gordon / (1 + wacc)**n
firm_value = pv_explicit + pv_tv_gordon
equity_value_gordon = firm_value - D_mv

# --- terminal value: exit EV/EBITDA multiple ---
ebitda_n, exit_mult = 110.0, 9.0
tv_exit = ebitda_n * exit_mult
pv_tv_exit = tv_exit / (1 + wacc)**n
equity_value_exit = (pv_explicit + pv_tv_exit) - D_mv

# FCFE bridge (illustrative, net borrowing = 0): FCFE = FCFF - Int(1-t)
int_after_tax = D_mv * pre_tax_kd * (1 - tax)
fcfe = [f - int_after_tax for f in fcff]

# sanity check: implied perpetuity growth from the exit-multiple TV
implied_g = (tv_exit * wacc - fcff[-1]) / (tv_exit + fcff[-1])

shares = 20.0  # million shares outstanding
print(f"WACC={wacc:.4f}  CostOfEquity={cost_of_equity:.4f}")
print(f"PV explicit FCFF={pv_explicit:.1f}  TV(Gordon)={tv_gordon:.1f}")
print(f"PV(TV) as % of firm value={pv_tv_gordon/firm_value:.1%}")
print(f"Equity value (Gordon)={equity_value_gordon:.1f}  -> price ${equity_value_gordon/shares:.2f}")
print(f"Equity value (Exit 9x)=${equity_value_exit:.1f}  -> price ${equity_value_exit/shares:.2f}")
print(f"FCFE yr5={fcfe[-1]:.1f} (bridge: FCFF - Int(1-t)={fcff[-1]:.1f}-{int_after_tax:.1f})")
print(f"Implied g from exit TV={implied_g:.4f}  (cf. Gordon g={g})")

# --- sensitivity grid: equity value vs WACC and g (Gordon method) ---
print("\nEquity value ($m) sensitivity [WACC x g]:")
header = "WACC\\g  " + "  ".join(f"{x:.1%}" for x in [0.02,0.025,0.03])
print(header)
for w in [0.07, 0.08, 0.09]:
    row = []
    for gg in [0.02, 0.025, 0.03]:
        tv = fcff[-1]*(1+gg)/(w-gg)
        ev = sum(f/(1+w)**t for t,f in enumerate(fcff,1)) + tv/(1+w)**n - D_mv
        row.append(f"{ev:7.1f}")
    print(f"{w:.1%}  " + "  ".join(row))

assert wacc > g and cost_of_equity > g, "need discount rate > growth rate"
```
**Expected (verified) output:** WACC≈0.0778, TV≈81% of firm value, equity value (Gordon)≈$747m (≈$37.4/share), equity value (9x exit)≈$493m (≈$24.6/share), implied g from the exit TV≈0.66%. The two terminal-value methods disagree by a wide margin — exactly why you cross-check and present a range, not a single number.

**Data source for real numbers:** pull historical FCFF inputs from the company's **Form 10-K** (Item 8 audited statements via SEC EDGAR: `https://www.sec.gov/edgar/searchedgar/companysearch`, or the XBRL endpoint `https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`, CIK zero-padded to 10 digits, with a descriptive User-Agent). Pull β, r_f, and market values from a market-data vendor (see 13-data-and-tooling). WACC/ERP reference series: Damodaran's NYU pages (e.g., `https://pages.stern.nyu.edu/~adamodar/`).

## Assumptions & limitations
- **Forecast accuracy degrades with horizon.** Beyond ~5–10 years, projections are guesses; this is precisely why the terminal value carries most of the weight [S52, S53].
- **Constant-growth constraint:** the Gordon model requires `g < WACC` (and `g < r` for FCFE). Violating it produces negative or infinite value — a common error [S52, S57].
- **Terminal growth cannot exceed the economy.** Practitioners bound `g` between long-run inflation (≈2–3%) and historical GDP growth (≈4–5%); assuming `g > ~5%` literally claims the firm outgrows the entire economy forever [S57]. Damodaran notes the *excess returns* (ROC vs cost of capital) embedded in `g` matter as much as `g` itself [S56].
- **WACC assumes a stable capital structure** and uses *market-value* weights, which are themselves a function of the value you're solving for — a mild circularity. If leverage is expected to change, the single-WACC approach is wrong and an iterated/APV treatment is needed [S50, S51].
- **CAPM for the cost of equity is itself contested** (see 04-quant-and-factors: CAPM). The discount rate is an assumption, not a fact.
- **Going-concern only.** DCF is weak or unusable for distressed firms, pre-revenue biotech, highly cyclical firms at the wrong point in the cycle, firms in the middle of restructuring, or land-rich firms (most value is non-operating real estate) [S51].
- **Net income / EBITDA are NOT cash flow.** The CFA reading explicitly warns against using NI, EBIT, EBITDA, or CFO as the discounted cash-flow proxy — they double-count or omit parts of the stream [S50].
- **Non-operating assets** (excess cash, marketable securities, non-core holdings) must be valued separately and added to operating-asset value [S50].

## Empirical evidence
- **Near-universal practitioner use.** A study of practicing analysts (Pinto, Robinson & Stowe 2019) found ~78.8% use DCF and ~92.8% use market multiples; among DCF users, 86.9% use a discounted free-cash-flow model [S50]. This is a usage/frequency fact, not a claim that DCF is "correct" in any given case.
- **Terminal value is the dominant component.** Multiple practitioner sources quantify it: ~75% of value in a 5-year DCF and ~50% in a 10-year DCF [S53, S57]. Damodaran shows the proportion rises with the firm's growth rate and can exceed 100% for high-growth/negative-early-FCF firms (early dilution via equity issuance) [S56]. He argues this is *not* a flaw — it mirrors how equity investors actually earn returns (mostly capital appreciation, not dividends: ~85% of US stock returns 1996–2015 were price appreciation) [S56].
- **Sensitivity is the empirical headline.** Because terminal value dominates, 1 percentage-point changes in `g` or WACC swing value by double-digit percentages; this is reproducible in any spreadsheet and is the central practical risk of DCF, not a debated anomaly.

## Conflicting views
- **Perpetuity growth vs exit multiple.** Academics favor the Gordon/perpetuity method (theoretically clean, internally consistent); investment bankers and practitioners prefer the exit multiple (market-anchored, easier to defend) [S52]. Best practice is to compute both and reconcile (cross-imply `g` or multiple) [S57].
- **"A high terminal-value share means the DCF is broken."** A common myth; Damodaran argues the opposite — if the terminal value is *not* the majority of value, that is the real warning sign [S56].
- **"High terminal value ⇒ early-stage assumptions don't matter."** Also false: Damodaran shows varying the high-growth-period assumptions (growth rate and return on equity) materially changes the terminal value itself, so early assumptions still drive the result [S56].
- **DCF vs relative valuation on "assumptions."** Some analysts claim multiples avoid fundamental assumptions; Damodaran counters that any multiple (P/E, EV/EBITDA) embeds implicit growth, risk, and payout assumptions, so relative valuation is *not* assumption-free [S51].

## Common mistakes
- **Mismatching cash flows and discount rates** — discounting FCFF at the cost of equity, or FCFE at WACC. FCFF→WACC, FCFE→cost of equity [S51]. This is the single most common (and most damaging) DCF error.
- **Using net income, EBIT, or EBITDA as the cash flow** instead of properly constructed FCFF/FCFE [S50].
- **Terminal growth ≥ discount rate** (model explodes) or **g > long-run GDP** (economically impossible) [S52, S57].
- **Forgetting the bridge to equity:** computing firm/enterprise value and forgetting to subtract net debt (and add cash/non-operating assets) before comparing to market cap [S50].
- **Single point estimate.** Presenting one price from one set of assumptions; always show a sensitivity grid and a range [S53, S57].
- **Garbage in, garbage out.** DCF inherits every forecast error; a precise-looking output from shaky inputs is false precision.
- **Ignoring the mid-year convention** (cash flows assumed mid-year, not year-end) — a ~few-% effect that matters in comparables.
- **Survivorship/look-ahead in any "DCF beats the market" backtest:** see 15-pitfalls-and-antipatterns. A DCF is a *valuation* tool, not a guaranteed alpha signal.

## Further reading
- [S50] CFA Institute, *Free Cash Flow Valuation* (2026 CFA L2 Equity Valuation refresher) — https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/free-cash-flow-valuation (Tier 1)
- [S51] Damodaran, A., *Discounted Cashflow Valuation: Problems and Solutions* (NYU Stern) — https://pages.stern.nyu.edu/~adamodar/New_Home_Page/problems/dcfprob.htm (Tier 1)
- [S52] Investopedia, *Terminal Value (TV) Definition and Formula* (updated May 2025) — https://www.investopedia.com/terms/t/terminalvalue.asp (Tier 2)
- [S53] Wall Street Prep, *Terminal Value (DCF)* — https://www.wallstreetprep.com/knowledge/terminal-value (Tier 2)
- [S54] Investopedia, *Weighted Average Cost of Capital (WACC)* — https://www.investopedia.com/terms/w/wacc.asp (Tier 2)
- [S55] Corporate Finance Institute, *FCFF vs FCFE* — https://corporatefinanceinstitute.com/resources/valuation/fcff-vs-fcfe (Tier 2)
- [S56] Damodaran, A., *Myth 5.5: The Terminal Value ate my DCF!* (Musings on Markets, 2016) — https://aswathdamodaran.blogspot.com/2016/11/myth-55-terminal-value-ate-my-dcf.html (Tier 1)
- [S57] Macabacus, *Terminal Value in DCF* — https://macabacus.com/valuation/dcf-terminal-value (Tier 2)

### Verify tasks spawned
- [ ] VERIFY: cross-sectional empirical evidence on whether DCF-derived intrinsic values predict future market prices better than multiples (out-of-sample); most practitioner claims are anecdotal — seek a peer-reviewed test (e.g., journal studies on DCF vs comparables forecast accuracy) before asserting predictive power.
- [ ] VERIFY: the "75% terminal value" figure for a *specific* forecast length — WSP/Macabacus quote ~75% (5-yr) and ~50% (10-yr); confirm against an independent practitioner/academic source and note it is illustrative, not a law.
