---
title: Financial Ratio Analysis (Liquidity, Solvency, Profitability, Efficiency)
topic_id: 01-fundamental-analysis/ratio-analysis
tags: [fundamental-analysis, ratios, liquidity, solvency, profitability, efficiency, dupont, altman, piotroski]
last_updated: 2026-07-18
confidence: robust
sources: [S36, S37, S38, S39, S40, S41, S42]
---

## TL;DR
- Ratio analysis standardizes financial statements so you can compare companies of different sizes and track one company over time; the four workhorse families are **liquidity** (can it pay bills now?), **solvency/leverage** (can it survive long-term debt?), **profitability** (does it earn a return?), and **efficiency/activity** (does it use assets well?).
- A single ratio is almost never decisive: the CFA curriculum explicitly warns that ratios "tell what happened but not why" — always read them against peers (cross-sectional) and against the firm's own history (trend), and use industry-specific benchmarks (S36).
- Ratios are not just descriptive: academically, combinations of them predict **bankruptcy** (Altman Z-score, 1968 — Tier-1) and, applied as a screen, have historically separated winning from losing value stocks (Piotroski F-score, 2000 — Tier-1). Both are correlational/past-based and decay.
- Biggest traps: ratios rest on **historical accounting data** subject to inflation, accounting-policy changes, seasonality, and earnings management (S42). Backtests/predictive models ≠ guaranteed future results.

## Core explanation
Ratio analysis converts raw balance-sheet, income-statement, and cash-flow numbers into standardized metrics. The CFA Institute organizes the standard toolkit into five families; four are the focus here (valuation/market ratios such as P/E and P/B are covered under valuation):

1. **Liquidity ratios** — ability to meet *short-term* obligations. Major members: current ratio, quick (acid-test) ratio, cash ratio, defensive-interval ratio (S36, S37).
2. **Solvency (leverage/coverage) ratios** — ability to meet *long-term* obligations. Split into (a) **debt ratios** from the balance sheet (debt-to-assets, debt-to-capital, debt-to-equity, financial-leverage/equity-multiplier) and (b) **coverage ratios** from the income statement (interest coverage, fixed-charge coverage) (S36, S37).
3. **Profitability ratios** — ability to generate profit from revenue and assets. Includes return-on-sales margins (gross, operating, pretax, net) and returns on investment (operating ROA, ROA, ROE, return on invested capital). DuPont analysis decomposes ROE to show *why* it moved (S36, S37).
4. **Efficiency / activity ratios** — how well assets are used. Inventory turnover, days of inventory on hand (DOH), receivables turnover, days sales outstanding (DSO), payables turnover, cash conversion cycle, fixed-asset turnover, total-asset turnover (S36, S37, S39).

A recurring theme from the CFA reading: **"It is important to examine a variety of financial ratios — not a single ratio or category of ratios in isolation."** Ratios are indicators of some aspect of performance, "telling what happened but not why it happened" (S36). Interpretation requires a comparison basis — cross-sectional (vs peers) and time-series (vs own history) — plus industry-specific ratios because "aspects of performance that are considered important in one industry may be irrelevant in another" (S36).

## Math / formulas
All formulas below are the CFA Institute's standard definitions (S37), which are the canonical exam/curriculum definitions and align with common practice.

**Liquidity**
- Current ratio = Current assets ÷ Current liabilities
- Quick ratio = (Cash + Short-term marketable investments + Receivables) ÷ Current liabilities
- Cash ratio = (Cash + Short-term marketable investments) ÷ Current liabilities
- Defensive interval ratio = (Cash + Short-term marketable investments + Receivables) ÷ Daily cash expenditures

**Solvency — debt ratios (balance sheet)**
- Debt-to-assets = Total debt ÷ Total assets
- Debt-to-capital = Total debt ÷ (Total debt + Total shareholders' equity)
- Debt-to-equity = Total debt ÷ Total shareholders' equity
- Financial leverage ratio (equity multiplier) = Average total assets ÷ Average shareholders' equity
- *Total debt* = interest-bearing short- and long-term debt (excludes accounts payable, accrued expenses, etc.)

**Solvency — coverage ratios (income statement)**
- Interest coverage = EBIT ÷ Interest payments  (also called "times interest earned," TIE)
- Fixed charge coverage = (EBIT + Lease payments) ÷ (Interest payments + Lease payments)  (S37, S38)

**Profitability — margins**
- Gross profit margin = Gross profit ÷ Total revenue
- Operating profit margin = Operating profit ÷ Total revenue
- Net profit margin = Net income ÷ Total revenue

**Profitability — returns**
- ROA = Net income ÷ Average total assets
- Operating ROA = Operating income ÷ Average total assets
- ROE = Net income ÷ Average shareholders' equity
- Return on common equity = (Net income − Preferred dividends) ÷ Average common shareholders' equity
- Return on invested capital (ROIC, after tax) = [EBIT × (1 − Effective tax rate)] ÷ (Average interest-bearing debt + Average shareholders' equity)  (S37)

**DuPont decomposition (3-way and 5-way)**
- 3-way: ROE = Net profit margin × Total asset turnover × Financial leverage = (NI/Revenue) × (Revenue/Avg total assets) × (Avg total assets/Avg equity)
- Hence ROE = ROA × Leverage (S36, S37).
- 5-way (extended): ROE = Tax burden × Interest burden × EBIT margin × Asset turnover × Financial leverage, where Tax burden = NI/EBT, Interest burden = EBT/EBIT (S36). This isolates operating vs financing vs tax drivers.

**Efficiency / activity**
- Inventory turnover = COGS ÷ Average inventory; DOH = Days in period ÷ Inventory turnover
- Receivables turnover = Total revenue ÷ Average receivables; DSO = Days in period ÷ Receivables turnover
- Payables turnover = Purchases ÷ Average trade payables; Days of payables = Days in period ÷ Payables turnover
- Cash conversion cycle = DOH + DSO − Days of payables
- Total asset turnover = Total revenue ÷ Average total assets
- Fixed asset turnover = Total revenue ÷ Average net fixed assets  (S37, S39)

## Worked example / code
The snippet below computes the standard ratios from an illustrative set of statement figures. **Data source:** synthetic/illustrative numbers sized to resemble a mid-cap manufacturer; for real analysis pull the same line items from a company's 10-K (Item 8 audited statements) via the SEC EDGAR API (see Further reading). Versions are pinned; the computation is pure Python so it runs without external data dependencies.

```python
# ratio_analysis_demo.py
# Pinned: python==3.11, pandas==2.2.2, numpy==1.26.4  (only stdlib used below)
# Data source: illustrative figures (replace with 10-K line items from SEC EDGAR).
from __future__ import annotations

# Illustrative FY figures (USD millions) for "Example Mfg Co."
fs = {
    "cash":                    120.0,
    "st_investments":           30.0,
    "receivables":            180.0,
    "inventory":              200.0,
    "current_assets":         650.0,
    "total_assets":          1500.0,
    "current_liabilities":    400.0,
    "total_debt":             600.0,   # interest-bearing only
    "total_equity":           900.0,
    "avg_total_assets":      1450.0,
    "avg_equity":            880.0,
    "avg_inventory":         190.0,
    "avg_receivables":       175.0,
    "revenue":               2000.0,
    "cogs":                  1300.0,
    "gross_profit":          700.0,
    "operating_income":      250.0,
    "ebit":                  250.0,
    "interest_expense":       45.0,
    "net_income":            150.0,
    "daily_cash_expenses":    12.0,
}

def ratios(fs):
    out = {}
    out["current_ratio"]   = fs["current_assets"] / fs["current_liabilities"]
    out["quick_ratio"]     = (fs["cash"] + fs["st_investments"] + fs["receivables"]) / fs["current_liabilities"]
    out["cash_ratio"]      = (fs["cash"] + fs["st_investments"]) / fs["current_liabilities"]
    out["debt_to_assets"]  = fs["total_debt"] / fs["total_assets"]
    out["debt_to_equity"]  = fs["total_debt"] / fs["total_equity"]
    out["equity_multiplier"]= fs["avg_total_assets"] / fs["avg_equity"]
    out["interest_coverage"]= fs["ebit"] / fs["interest_expense"]
    out["gross_margin"]    = fs["gross_profit"] / fs["revenue"]
    out["operating_margin"]= fs["operating_income"] / fs["revenue"]
    out["net_margin"]      = fs["net_income"] / fs["revenue"]
    out["roa"]             = fs["net_income"] / fs["avg_total_assets"]
    out["roe"]             = fs["net_income"] / fs["avg_equity"]
    out["asset_turnover"]  = fs["revenue"] / fs["avg_total_assets"]
    out["inventory_turnover"] = fs["cogs"] / fs["avg_inventory"]
    out["receivables_turnover"] = fs["revenue"] / fs["avg_receivables"]
    # DuPont 3-way check: ROE ~= net_margin * asset_turnover * equity_multiplier
    dupont_roe = (fs["net_income"]/fs["revenue"]) * (fs["revenue"]/fs["avg_total_assets"]) * (fs["avg_total_assets"]/fs["avg_equity"])
    out["dupont_roe_check"] = dupont_roe
    return out

if __name__ == "__main__":
    for k, v in ratios(fs).items():
        print(f"{k:20s} = {v:7.3f}")
```

Expected output (rounded): current_ratio ≈ 1.625, quick_ratio ≈ 0.825, cash_ratio ≈ 0.375, debt_to_assets ≈ 0.400, debt_to_equity ≈ 0.667, equity_multiplier ≈ 1.648, interest_coverage ≈ 5.556, gross_margin ≈ 0.350, operating_margin ≈ 0.125, net_margin ≈ 0.075, roa ≈ 0.103, roe ≈ 0.170, asset_turnover ≈ 1.379, inventory_turnover ≈ 6.842, receivables_turnover ≈ 11.429, dupont_roe_check ≈ 0.170 (ties to ROE). This demonstrates the DuPont identity ties out and that ROE of ~17% is driven by modest margins, healthy turnover, and moderate leverage — not by any single factor.

## Assumptions & limitations
- **Historical by construction.** Ratios are computed from past financial statements and "do not necessarily represent future company performance" (S42). A strong ratio today says little if the business model is shifting.
- **Accounting-policy sensitivity.** LIFO vs FIFO, depreciation methods, capitalization vs expensing, lease accounting, and revenue-recognition choices all move the numerator/denominator. Changes in policy make pre/post comparisons invalid unless restated (S42). (See also `01-fundamental-analysis/financial-statements.md` on accruals and estimates.)
- **Inflation & comparability.** Across periods, unadjusted nominal figures aren't comparable under inflation; cross-country comparisons are distorted by differing GAAP/IFRS treatment (S42).
- **Seasonality.** A snapshot ratio can mislead if the balance-sheet date is seasonally atypical; use averages across the period where possible (S37, S42).
- **Industry context is mandatory.** "Good" differs by sector — a retailer's thin margins with high turnover vs a software firm's high margins with low turnover. Compare within peer group and over time, never in isolation (S36).
- **Ratios don't explain causality.** They flag *what* changed, not *why*; pair with MD&A, segment data, and qualitative research (S36).
- **Predictive models decay.** Altman Z and Piotroski F were fit on historical samples; regimes, accounting standards, and market efficiency have changed. Treat as screens/risk flags, not certainties.

## Empirical evidence
**Robust (decades of support):**
- **Altman Z-score (1968)** — Altman built a multivariate discriminant model from financial ratios to predict corporate bankruptcy for publicly held manufacturers: Z = 1.2·X₁ + 1.4·X₂ + 3.3·X₃ + 0.6·X₄ + 1.0·X₅, where X₁ = Working capital/Total assets, X₂ = Retained earnings/Total assets, X₃ = EBIT/Total assets, X₄ = Market value of equity/Total liabilities, X₅ = Sales/Total assets (S41). The widely reproduced cutoff zones classify Z > 2.99 as "safe," 1.81–2.99 as a "grey" zone, and Z < 1.81 as indicating likely distress. Later out-of-sample tests (e.g., on JSE-listed firms, 2008–2010) report ~91% overall classification accuracy, though accuracy and optimal cutoffs vary by country/era (corroborated by multiple secondary reproductions). Strength: very strong, but model is calibrated to mid-20th-century US manufacturers and has variants (Z', Z'') for private/non-manufacturing firms.
- **Piotroski F-score (2000)** — Piotroski showed that a simple 9-signal accounting fundamental score, applied only to high book-to-market ("value") stocks, shifts the return distribution favorably: the mean return of a high-BM investor "can be increased by at least 7.5% annually" through selection of financially strong high-BM firms, and a long–short strategy (buy strong, short weak) "generates a 23% annual return between 1976 and 1996." Benefits were concentrated in small/medium firms, low-share-turnover names, and firms with no analyst following, consistent with the market *underreacting* to historical financial information (S40). Strength: robust in the original sample and widely replicated, but it is a historical backtest on US data and is not a forward guarantee.

**Emerging / contested:**
- Whether broad ratio-based "quality" screens beat the market *net of costs* in the current regime is debated; many anomalies (including value) have weakened post-publication (see `04-quant-and-factors`). Treat Piotroski-style results as evidence that *fundamental information is not fully priced in neglected stocks*, not as a free lunch.

## Conflicting views
- **"Higher is always better"?** Not universally. A very high current ratio can signal lazy, unproductive current assets (excess cash, slow collection); a very low debt-to-equity may indicate suboptimal capital structure (foregoing cheap leverage). Ratios must be read as trade-offs, not as monotonic goods.
- **EBIT vs EBITDA in coverage.** Coverage is often computed on EBITDA instead of EBIT to be more lenient; EBITDA-based coverage overstates cushion because it ignores depreciation/Amortization (S38). Which is "right" depends on capital intensity — a known practitioner disagreement.
- **Industry comparability.** Some argue cross-industry ratio comparison is meaningless and only within-peer medians matter; others use cross-industry ratios for top-down screening. Resolution: use cross-industry only for gross screening, peer-relative for conclusions (S36).
- **Static vs average denominators.** Balance-sheet items are point-in-time while income-statement items are flows; best practice uses *average* balances (S37). Many free screeners use period-end figures, creating small but real distortions — a silent source of cross-source disagreement.

## Common mistakes
1. **Single-ratio judgments.** Concluding "the company is healthy/unhealthy" from one ratio. Use the full set + trend + peers (S36).
2. **Comparing across industries or accounting regimes** without adjustment (S36, S42).
3. **Ignoring accounting-policy changes and one-offs** — a great margin may be a one-time gain; a bad ratio may be a restructuring charge (S42).
4. **Using period-end balances instead of averages** for turnover/returns, distorting efficiency and ROA/ROE (S37).
5. **Treating predictions as guarantees** — Altman Z and Piotroski F are historical models; survivorship-biased datasets and look-ahead in naive implementations inflate reported accuracy (see `15-pitfalls-and-antipatterns`).
6. **Window dressing** — managers can temporarily boost quarter-end ratios (e.g., paying down payables, accelerating collections), so snapshot liquidity can overstate ongoing health (S42).
7. **Confusing book equity with market value** in leverage — debt-to-equity using book equity behaves very differently from a market-value-based leverage measure, especially for distressed or high-growth firms.

## Further reading
- **[Tier 1]** CFA Institute, "Financial Analysis Techniques" (2026 CFA L1 FSA refresher) — categories, common-size, DuPont, limitations: https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/financial-analysis-techniques
- **[Tier 1]** CFA Institute, "Financial Ratio List" (Level II standard definitions) — exact formulas used above: https://www.cfainstitute.org/sites/default/files/-/media/documents/support/programs/cfa/cfa_program_level_ii_financial_ratio_list.pdf
- **[Tier 1]** Piotroski, J.D. (2000), "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers," *Journal of Accounting Research* 38, 1–41 (abstract/paper): https://www.anderson.ucla.edu/documents/areas/prg/asam/2019/F-Score.pdf
- **[Tier 1]** Altman, E.I. (1968), "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy," *Journal of Finance* 23(4):589–609: https://www.jstor.org/stable/2978933
- **[Tier 2]** Investopedia, "Interest Coverage Ratio" (updated Apr 2026) — coverage interpretation and EBITDA variant: https://www.investopedia.com/terms/i/interestcoverageratio.asp
- **[Tier 2]** AnalystPrep, "Activity, Liquidity, Solvency, Profitability, and Valuation Ratios" (CFA L1 notes): https://analystprep.com/cfa-level-1-exam/financial-reporting-and-analysis/activity-liquidity-solvency-profitability-valuation-ratios
- **[Tier 2]** Corporate Finance Institute, "Limitations of Ratio Analysis" (Feb 2020): https://corporatefinanceinstitute.com/resources/accounting/limitations-ratio-analysis
- **Data:** SEC EDGAR company filings (10-K/10-Q) and the EDGAR full-text/JSON APIs for pulling real line items: https://www.sec.gov/edgar/search/ and https://data.sec.gov/api/
