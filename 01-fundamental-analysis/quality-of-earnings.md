---
title: Quality of Earnings & Red Flags
topic_id: 01-fundamental-analysis/quality-of-earnings
tags: [fundamental-analysis, earnings-quality, accruals, red-flags, beneish, sloan-anomaly, forensic-accounting]
last_updated: 2026-07-18
confidence: robust
sources: [S43, S44, S45, S46, S47, S48, S49]
---

## TL;DR
- "Quality of earnings" asks whether reported net income is backed by cash and sustainable, or manufactured by aggressive accrual accounting. Analysts treat a high ratio of cash flow from operations (CFO) to net income as a rough proxy for quality (S44).
- The single most replicated empirical finding is the **Sloan (1996) accrual anomaly**: earnings driven by accruals persist less than earnings driven by cash, and high-accrual firms earn lower future returns (S43).
- The **Beneish M-Score** (8 financial ratios) flags firms with a statistical profile matching historical earnings manipulators; a score above −1.78 is the standard "likely manipulator" cut (S45, S46). It is a screening tool, not proof of fraud.
- Red flags cluster around revenue recognition, expense capitalization, reserve/allowance manipulation, and cash-flow/earnings divergence. These are corroborated across CFA curriculum material and practitioner forensic guides (S44, S47, S48).
- Application caveat: the live trading edge of the simple accrual strategy has materially weakened since ~2002 (S49) — treat these as risk/forensic screens, not standalone alpha.

## Core explanation
**Plain language.** A company's reported profit (net income) is built from two very different ingredients:
1. **Cash** — money actually received or paid.
2. **Accruals** — non-cash accounting entries (revenue earned but not yet collected, expenses incurred but not yet paid, estimates for bad debts, depreciation, etc.) required by accrual accounting.

Both increase net income this period, but they do not have the same durability. Cash-based earnings tend to repeat; accrual-based earnings often reverse. "Quality of earnings" is the discipline of separating the two and judging how much of this period's profit is real, repeatable, and supported by cash.

**Precise.** Under accrual accounting, Net Income ≈ Cash Flow from Operations + Accruals (the non-cash and timing difference between the two). Accruals embed managers' estimates and judgments, which creates both legitimate smoothing and a channel for bias. When accruals are large relative to cash flows, reported earnings are more likely to contain estimates that will later reverse, and (historically) the market has under-weighted this distinction.

Two complementary lenses:
- **Sustainability lens (Sloan 1996):** decompose earnings into cash and accrual components; the accrual component has lower persistence.
- **Manipulation lens (Beneish 1999):** build a multivariate profile of firms that *have* manipulated; screen current firms against it.

## Math / formulas

### 1. Accruals (Sloan 1996)
Balance-sheet (statement-of-changes) accruals, the most common definition:

```
BS_ACC = (ΔCA − ΔCash) − (ΔCL − ΔSTD − ΔITP) − Dep
```
where ΔCA = change in current assets, ΔCash = change in cash & equivalents, ΔCL = change in current liabilities, ΔSTD = change in debt in current liabilities, ΔITP = change in income taxes payable, Dep = depreciation & amortization expense.

A normalized **accruals ratio** = BS_ACC / Average Total Assets. High positive values → low-quality earnings (S43). (Cash-flow-statement accruals, CFO − NI, give the same sign.)

### 2. CFO / Net Income screen
```
Earnings-quality ratio = CFO / Net Income
```
A persistently low or negative ratio (NI ≫ CFO) is a classic warning sign that profits are not converting to cash (S44, S47).

### 3. Beneish M-Score (S45, S46)
Eight indices, combined with the published coefficients:

```
M = −4.840 + 0.920·DSRI + 0.528·GMI + 0.404·AQI
           + 0.892·SGI  + 0.115·DEPI − 0.172·SGAI
           − 0.327·LVGI + 4.679·TATA        # some reproductions use 4.697 for TATA
```

| Var | Definition | Rising = red flag? |
|---|---|---|
| DSRI | (Recv_t/Rev_t) / (Recv_{t-1}/Rev_{t-1}) | Receivables growing faster than revenue → revenue inflation |
| GMI | GM_{t-1} / GM_t (GM = (Rev−COGS)/Rev) | Falling gross margin → pressure to manipulate |
| AQI | [1−(CA_t+PP&E_t)/TA_t] / [1−(CA_{t-1}+PP&E_{t-1})/TA_{t-1}] | More deferred cost capitalized as assets |
| SGI | Rev_t / Rev_{t-1} | High growth → more incentive to manipulate |
| DEPI | DepRate_{t-1} / DepRate_t (DepRate = Dep/(Dep+PP&E)) | Slower depreciation → inflated profit |
| SGAI | (SGA_t/Rev_t) / (SGA_{t-1}/Rev_{t-1}) | SG&A rising faster than revenue |
| LVGI | (Debt_t/TA_t) / (Debt_{t-1}/TA_{t-1}) | Rising leverage → pressure |
| TATA | (Income from cont. ops_t − CFO_t) / TA_t | Large accruals = strongest manipulation signal |

**Interpretation:** M > −1.78 → "likely manipulator"; M < −2.22 → "unlikely"; between → gray zone (S45, S46). Beneish's own out-of-sample test flagged Enron before its collapse (S45).

## Worked example / code
Pure-Python (stdlib only, Python 3.11+) illustration of the two screens. Replace the illustrative figures with real 10-K data pulled from SEC EDGAR (https://www.sec.gov/edgar/searchedgar/companysearch) or a financial-data API (e.g., Financial Modeling Prep, SimFin, or `pandas-datareader` against Yahoo). State your data source explicitly when you run it for real.

```python
# quality_of_earnings_screens.py  (Python 3.11+, no third-party deps)
# Illustrative numbers only — substitute real 10-K line items for live use.

def accruals_ratio(cur, prev):
    dCA   = cur["ca"]   - prev["ca"]
    dCash = cur["cash"] - prev["cash"]
    dCL   = cur["cl"]   - prev["cl"]
    dSTD  = cur["std"]  - prev["std"]   # debt in current liabilities
    dITP  = cur["itp"]  - prev["itp"]   # income taxes payable
    dep   = cur["dep"]
    bs_acc = (dCA - dCash) - (dCL - dSTD - dITP) - dep
    avg_ta = (cur["ta"] + prev["ta"]) / 2.0
    return bs_acc / avg_ta

def cfo_to_ni(cfo, ni):
    return cfo / ni if ni else float("nan")

def beneish_m(cur, prev):
    dsri = (cur["rec"]/cur["rev"]) / (prev["rec"]/prev["rev"])
    gmi  = ((prev["rev"]-prev["cogs"])/prev["rev"]) / ((cur["rev"]-cur["cogs"])/cur["rev"])
    aqi  = (1-(cur["ca"]+cur["ppe"])/cur["ta"]) / (1-(prev["ca"]+prev["ppe"])/prev["ta"])
    sgi  = cur["rev"]/prev["rev"]
    dep_rate_t  = cur["dep"]/(cur["dep"]+cur["ppe"])
    dep_rate_p  = prev["dep"]/(prev["dep"]+prev["ppe"])
    depi = dep_rate_p/dep_rate_t
    sgai = (cur["sga"]/cur["rev"]) / (prev["sga"]/prev["rev"])
    lvgi = (cur["debt"]/cur["ta"]) / (prev["debt"]/prev["ta"])
    tata = (cur["ico"]-cur["cfo"]) / cur["ta"]
    return (-4.840 + 0.920*dsri + 0.528*gmi + 0.404*aqi
            + 0.892*sgi + 0.115*depi - 0.172*sgai
            - 0.327*lvgi + 4.679*tata)

prev = dict(ca=1000, cash=200, cl=500, std=50, itp=20, dep=80, ta=2000,
            rec=300, rev=2000, cogs=1200, ppe=900, sga=400, debt=700, ico=150, cfo=250)
cur  = dict(ca=1200, cash=180, cl=560, std=55, itp=18, dep=85, ta=2300,
            rec=450, rev=2300, cogs=1450, ppe=950, sga=500, debt=850, ico=170, cfo=240)

print("Accruals ratio :", round(accruals_ratio(cur, prev), 4))
print("CFO / NI       :", round(cfo_to_ni(cur["cfo"], cur["ico"]), 4))
print("Beneish M-Score:", round(beneish_m(cur, prev), 4))
```

Running this prints an M-Score around −2.0 (gray zone) for the illustrative inputs — confirming the mechanics. For a real screen, plug in consecutive fiscal years and compare M across your universe; empirically, ~only a small fraction exceed −1.78.

## Assumptions & limitations
- **Accruals are not fraud.** Large accruals can be legitimate (e.g., working-capital growth in a scaling business). The Sloan and Beneish models are *statistical* screens, not verdicts.
- **Two years of clean data required.** Beneish needs t and t−1; restatements break the indices.
- **Coefficients are sample-specific.** Beneish's weights were estimated on 1980s–1990s U.S. firms; industry, era, and accounting-regime (GAAP vs IFRS) shifts reduce precision (S46).
- **Markets adapt.** The Sloan anomaly's *trading* edge has decayed (see Empirical evidence); screens are better as risk filters than as alpha (S49).
- **Audits ≠ assurance of quality.** Even clean audit opinions miss going-concern and manipulation risk; the CFA blog cites UK Audit Reform Lab finding auditors flagged going-concern uncertainty in only ~25% of major failures (S44).
- **Non-stationarity.** What flags manipulation in one regime may not in another; recompute and re-validate periodically.

## Empirical evidence
- **Sloan (1996) — robust, primary (S43).** Using 1962–1991 Compustat data, Sloan shows the accrual component of earnings is significantly *less persistent* than the cash component, and that stock prices behave as if investors "fixate" on earnings, failing to price the accrual/cash split fully until it hits future earnings. High-accrual firms earn negative future abnormal returns; low-accrual firms earn positive ones, concentrated around subsequent earnings announcements. The original hedge portfolio earned roughly double-digit annualized abnormal returns in-sample.
- **Beneish (1999) — robust as a forensic flag (S45, S46).** The M-Score correctly identifies a large share of known manipulators in holdout samples; Cornell students applied it to flag Enron in 1998, years before its 2001 collapse (S45). However, as a *forward* trading signal its standalone edge is weak/folklore.
- **Accrual anomaly decay — contested/emerging (S49).** Quantpedia summarizes that the simple accruals long-short "generated significant excess returns consistently for over four decades until 2002, but has apparently weakened in the subsequent period" (citing Mohanram) and that earnings-quality signals "stopped working in the mid-2000s but since the end of 2008 has staged a remarkable rebound" (citing Bender & Nielsen). Quantpedia rates the anomaly's live validity as **Weak** with out-of-sample backtests showing materially negative performance — a likely in-sample data-mining artifact.

## Conflicting views
- **Is the accrual anomaly "real" alpha or a statistical artifact?** Sloan (1996) documents a strong in-sample effect; later work (Mohanram; Bender & Nielsen, via S49) finds it weakened/recovered depending on period — suggesting regime dependence and possible original overfitting. Practitioners disagree on whether it survives transaction costs and crowding today.
- **Do high accruals mean "bad" or "growing"?** A benign reading: high accruals reflect genuine expansion (receivables/inventory build). An aggressive reading: they reflect manipulation. The same number needs business context — hence the Beneish multi-factor approach and the CFO/NI check.
- **Beneish TATA coefficient.** Reproductions differ slightly: 4.679 (most-cited original) vs 4.697 (MarketXLS, S46). Immaterial to ranking but worth noting for exact replication.
- **"Higher CFO/NI is always better"** — contested. A very high ratio can signal aggressive cash acceleration (e.g., stretching payables) rather than quality; context matters (S47, S48).

## Common mistakes
- **Treating accruals as fraud.** Most large accruals are legitimate; use them as a flag for *investigation*, not a sell signal.
- **Single-metric decisions.** Don't rely on CFO/NI or M-Score alone; triangulate with revenue-recognition red flags and sector context.
- **Ignoring restatements/look-ahead.** Computing these on *future-restated* data injects look-ahead bias; always use the data *as reported* at the time.
- **Survivorship bias in backtests.** Screening a current index ignores delisted/failed firms where manipulation actually concentrates; this inflates historical screen performance.
- **Forgetting taxes & costs.** Any accrual-based trade must net transaction costs, shorting fees, and taxes; the decay evidence (S49) shows naive implementations lose money out-of-sample.
- **Mixing GAAP/IFRS without adjustment.** Classification differences (e.g., interest/dividends in the cash-flow statement) change accrual computations across regimes (cf. financial-statements.md).

## Further reading
- S43 (Tier 1, primary): Sloan, R.G. (1996), "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" *The Accounting Review* 71(3):289–315. https://www.cuhk.edu.hk/acy2/workshop/June2009Wasley/1996TAR).pdf
- S44 (Tier 1, practitioner/reputable): CFA Institute, "Quality of Earnings: A Critical Lens for Financial Analysts" (Enterprising Investor, Mar 2026). https://rpc.cfainstitute.org/blogs/enterprising-investor/2025/quality-of-earnings-a-critical-lens-for-financial-analysts
- S45 (Tier 2, reputable): Investopedia, "Beneish Model: Definition, Examples, and M-Score Calculation" (updated Feb 2026). https://www.investopedia.com/terms/b/beneishmodel.asp — cites Beneish (1999), *Financial Analysts Journal* 55(5).
- S46 (Tier 2, practitioner): MarketXLS, "Beneish M-Score" (8-variable formulas + coefficients). https://marketxls.com/blog/beneish-m-score
- S47 (Tier 2, CFA-aligned): Soleadea, "CFA Level 1: Issues and Red Flags" (financial reporting quality). https://soleadea.org/cfa-level-1/issues-red-flags
- S48 (Tier 1, prior KB sources reusable): SEC, "Beginners' Guide to Financial Statements" (S29) and "How to Read a 10-K" (S30/S31) — for where to pull the raw line items.
- S49 (Tier 2, quant summary): Quantpedia, "Accrual Anomaly." https://quantpedia.com/strategies/accrual-anomaly
- Primary Beneish paper (citation only, paywalled): Beneish, M.D. (1999), "The Detection of Earnings Manipulation," *Financial Analysts Journal* 55(5):24–36.
- Companion KB articles: `01-fundamental-analysis/financial-statements.md`, `01-fundamental-analysis/ratio-analysis.md`.
