---
title: DuPont Analysis & ROE Decomposition
topic_id: 01-fundamental-analysis/dupont-analysis
tags: [fundamental-analysis, ROE, DuPont, profitability, efficiency, leverage, ratio-analysis]
last_updated: 2026-07-18
confidence: robust
sources: [S36, S37, S170, S171, S172, S173]
---

## TL;DR
- A single ROE number conflates *how much* a company returns with *how* it earns that return. DuPont analysis multiplies ROE out into profitability (margin), efficiency (asset turnover), and leverage (equity multiplier) so you can see which lever is driving performance.
- Two standard forms: the **3-way** `ROE = Net Profit Margin × Total Asset Turnover × Equity Multiplier`, and the **5-way** that further splits net margin into `Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Leverage`.
- Always use **average** balance-sheet values (beginning+ending ÷ 2) to align point-in-time assets/equity with period-flow income. Compare only within the same industry and trend.
- Leverage is a double-edged driver: it amplifies ROE on the upside **and** multiplies losses on the downside. A high-ROE company leaning on a 5×–6× equity multiplier is far riskier than one earning the same ROE from margin.

## Core explanation
**Plain language.** Return on Equity (ROE) answers "how much profit did the company earn per dollar of shareholder capital?" But two firms with identical 20% ROE can be completely different businesses — one earns it on thin margins and high sales volume, another on fat margins and a small asset base, a third by borrowing heavily. DuPont analysis (developed by the DuPont Corporation in the 1920s as an internal management tool) breaks the single ROE ratio into multiplicative components, each revealing a distinct strategic lever:

1. **Profitability** — how much profit per dollar of sales (net profit margin, and in the 5-way, the operating margin before tax and interest).
2. **Efficiency** — how much revenue each dollar of assets generates (total asset turnover).
3. **Leverage** — how much assets are financed by debt vs equity (the equity multiplier).

**Precise.** Start from the accounting identity `ROE = Net Income / Average Shareholders' Equity` and insert cancelling terms.

3-way decomposition:
```
ROE = (Net Income / Revenue)            × (Revenue / Avg Total Assets)        × (Avg Total Assets / Avg Shareholders' Equity)
    = Net Profit Margin (NPM)           × Total Asset Turnover (ATO)         × Equity Multiplier (EM)
```
An intermediate, 2-way view is `ROE = Return on Assets (ROA) × Equity Multiplier`, where `ROA = Net Income / Avg Total Assets`. Because `ROA = NPM × ATO`, the 3-way and 2-way are identical.

5-way decomposition (separates taxes and interest out of net margin):
```
ROE = (NI/EBT) × (EBT/EBIT) × (EBIT/Revenue) × (Revenue/Avg Total Assets) × (Avg Total Assets/Avg Equity)
    = Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Leverage
```
with:
- Tax Burden = NI / EBT = 1 − effective tax rate
- Interest Burden = EBT / EBIT
- EBIT Margin = EBIT / Revenue
- Asset Turnover = Revenue / Avg Total Assets
- Leverage (Equity Multiplier) = Avg Total Assets / Avg Shareholders' Equity

An algebraically equivalent "extended" form (useful for seeing leverage's downside) is:
`ROE = [(EBIT/Sales)(Sales/Assets) − (Interest Expense/Assets)] × (Assets/Equity) × (1 − t)`.
This exposes that higher leverage only raises ROE while `EBIT/Assets > Interest Expense/Assets`; when the cost of debt exceeds the return on assets, more leverage *lowers* ROE.

## Math / formulas

| Symbol | Definition (CFA canonical) | Source |
|---|---|---|
| Net Profit Margin | NI / Revenue | S37 |
| Total Asset Turnover | Revenue / Avg Total Assets | S37 |
| Equity Multiplier | Avg Total Assets / Avg Shareholders' Equity | S37 |
| ROA | NI / Avg Total Assets | S37 |
| ROE | NI / Avg Shareholders' Equity | S37 |
| Tax Burden | NI / EBT | S37 |
| Interest Burden | EBT / EBIT | S37 |
| EBIT Margin | EBIT / Revenue | S37 |

Identities (always hold by cancellation):
- `ROE = NPM × ATO × EM`
- `ROE = ROA × EM`
- `ROE = Tax Burden × Interest Burden × EBIT Margin × ATO × EM`

The **Sustainable Growth Rate** links ROE to valuation: `g = Retention Rate × ROE` (Retention = 1 − Dividend Payout). This feeds the Gordon Growth / DDM model, so *which* DuPont components drive ROE affects whether the implied growth is durable (S37).

## Worked example / code
**Data source:** the snippet below uses an *illustrative* company ("Illustra Corp") with line items stated explicitly so the decomposition is fully reproducible. For production use, pull real line items from a 10-K (EDGAR, see S152 in the registry) and use **average** balance-sheet values.

```python
# DuPont 3-way and 5-way decomposition (stdlib only, reproducible).
# Illustrative "Illustra Corp" FY figures ($ millions), averages over the year.
NI, EBT, EBIT, REV = 120.0, 150.0, 200.0, 1000.0
AVG_TA, AVG_EQUITY = 2500.0, 1000.0

# 3-way
npm = NI / REV                      # 0.120
ato = REV / AVG_TA                  # 0.400
em  = AVG_TA / AVG_EQUITY           # 2.500
roe_3 = npm * ato * em              # 0.120  (12%)

# 5-way
tax_burden = NI / EBT               # 0.800
int_burden = EBT / EBIT            # 0.750
ebit_margin = EBIT / REV           # 0.200
roe_5 = tax_burden * int_burden * ebit_margin * ato * em   # 0.120 (12%)

assert abs(roe_3 - roe_5) < 1e-12                       # 3-way == 5-way
assert abs(roe_3 - (NI / AVG_EQUITY)) < 1e-12          # == NI/avg equity
assert abs(roe_3 - (NI/AVG_TA) * em) < 1e-12           # == ROA * EM
```
Verified output: `ROE = 12.0%`; the three expressions (`ROE`, `3-way`, `5-way`, `ROA×EM`) tie out to 1e-12. As a cross-check, the AnalystPrep textbook example (NPM 17.54%, Revenue $285k, Avg TA $1.0m, Avg Equity $0.6m) reproduces `ROE ≈ 8.33%` exactly.

**Interpretation of the example:** Illustra earns 20% EBIT margin and turns assets 0.4× per year, leveraged 2.5×. A peer earning the same 12% ROE from a 20% margin but only 1.2× leverage is materially less financially fragile.

## Assumptions & limitations
- **Positive equity & positive operating profit.** The framework assumes `Avg Shareholders' Equity > 0` and (for clean interpretation of tax/interest burden) `EBIT > 0` and `EBT > 0`. With operating losses, tax/interest burdens can exceed 1.0 or go negative and mislead; with negative equity, the ratios are mathematically meaningless (S170).
- **Averaging matters.** Income is a period flow; the balance sheet is a point-in-time snapshot. Dividing annual NI by a single quarter-end equity balance mismatches flows and stocks. Use `(beginning + ending)/2` for TA and equity, and keep the income period and the balance-sheet averaging window consistent (don't mix TTM income with a single-quarter balance sheet) (S170).
- **Accrual, not cash.** ROE and its components derive from accrual net income, which can be inflated by one-off asset sales, litigation settlements, or aggressive accounting; DuPont does *not* assess quality of earnings (S170). Pair with the Quality-of-Earnings article (01-fundamental-analysis/quality-of-earnings).
- **Industry context required.** A 3% net margin is excellent for grocery retail but poor for software; the "right" DuPont profile is business-model-specific (S170).
- **Descriptive, not predictive.** The decomposition explains *why* ROE was what it was; it does not by itself forecast future ROE or returns.

## Empirical evidence
- **Framework validity is robust.** DuPont analysis is a standard, curriculum-level diagnostic (CFA Level I Financial Statement Analysis, "Financial Analysis Techniques," explicitly lists the 5-component decomposition as tax rate, interest burden, operating profitability, efficiency, and leverage — S36; exact sub-ratio definitions in S37). It is universally used for peer comparison, trend analysis, and management diagnosis (S170, S171, S172).
- **Leverage is asymmetric.** Multiple practitioner sources confirm that the equity multiplier amplifies *both* gains and losses: "If a company loses money in any year, the asset turnover or financial leverage multiplies this loss effect" (S171); "an equity multiplier of 5× means $5 of assets for every $1 of equity … if earnings decline, the same leverage that amplified returns will amplify losses" (S170). This is the core risk caveat, not a disputed claim.
- **Heterogeneous profitability structures.** Recent empirical work decomposing ROE across firms finds that similar ROE levels arise from very different operational-efficiency vs financial-leverage combinations, supporting the diagnostic value of the breakdown (Andriyanto et al., 2026 — noted as corroborating context, not a primary we opened; treat as emerging).
- **No claimed return premium.** We do **not** assert that any particular DuPont profile predicts stock returns; that would require factor-level out-of-sample evidence and is out of scope. Use the decomposition as a *diagnostic*, not a buy signal.

## Conflicting views
- **"Leverage" definition.** The CFA/standard DuPont uses the **equity multiplier** = Total Assets / Equity (S37). Some informal write-ups use Debt/Equity instead. These differ (equity multiplier = 1 + D/E for no preferred stock). Stick to the assets/equity multiplier to keep the identity exact.
- **2-way vs 3-way vs 5-way "right" form.** No conflict in math — they are nested identities. The 3-way is preferred for quick screening; the 5-way is preferred when comparing across tax jurisdictions, capital structures, or isolating operating vs financing effects (S170). Use the depth the question requires.
- **ROE vs "ROE for common equity."** CFA notes ROE uses total average shareholders' equity; if preferred dividends exist, Return on *Common* Equity uses `(NI − Preferred Dividends) / Avg Common Equity` (S37). Match the denominator to the claimholder you are analyzing.

## Common mistakes
1. **Comparing components across industries** (e.g., calling a retailer's 3% margin "bad" vs a software firm's 25%) — meaning is industry-relative (S170).
2. **Ignoring the risk behind a high equity multiplier** — 25% ROE driven by a 6× multiplier is far riskier than 25% from a 20% margin; check interest coverage and debt maturity alongside (S170).
3. **Inconsistent time periods** — annual NI ÷ quarter-end equity (S170).
4. **Mixing TTM income with a single-quarter balance sheet** — over/understates turnover and the multiplier depending on seasonality and trend (S170).
5. **Misreading ROE improvements from equity shrinkage** — buybacks, large dividends, or accumulated losses can shrink the equity denominator and *raise* ROE even as profitability falls. Always check *which* component moved (S170).
6. **Treating DuPont as a forecast** — it explains the past period; it is not a forward model and says nothing about sustainability without additional analysis (e.g., quality of earnings, competitive position).
7. **Over-weighting a single number** — examine all components together; a balanced view requires the full chain, not one ratio in isolation (S36).

## Further reading
- **[Tier 1]** CFA Institute, *Financial Analysis Techniques* (2026 L1 FSA refresher) — decomposition rationale & 5-component framing: https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/financial-analysis-techniques
- **[Tier 1]** CFA Institute, *Financial Ratio List* (L2 standard definitions) — exact formulas for ROE, ROA, tax/interest burden, EBIT margin, turnover, equity multiplier, sustainable growth: https://www.cfainstitute.org/sites/default/files/-/media/documents/support/programs/cfa/cfa_program_level_ii_financial_ratio_list.pdf
- **[Tier 2]** Ryan O'Connell, CFA, FRM, *DuPont Analysis Explained: 3-Factor & 5-Factor ROE Decomposition* — worked WMT/LVMH example, mistakes, limitations: https://ryanoconnellfinance.com/dupont-analysis
- **[Tier 2]** AnalystNotes, *Subject 6. The DuPont System* (CFA L1) — traditional & extended formulas: https://analystnotes.com/cfa-study-notes-demonstrate-the-application-of-dupont-analysis-of-return-on-equity-and-calculate-and-interpret-effects-of-changes-in-its-components.html
- **[Tier 2]** AnalystPrep, *DuPont Analysis of Return on Equity* — full 5-way derivation + textbook example: https://analystprep.com/cfa-level-1-exam/financial-reporting-and-analysis/dupont-analysis-of-return-on-equity
- **[Tier 2]** Investopedia, *DuPont Analysis*: https://www.investopedia.com/terms/d/dupontanalysis.asp
- **Related KB articles:** 01-fundamental-analysis/ratio-analysis.md (ratio families & DuPont identity), 01-fundamental-analysis/quality-of-earnings.md (why accrual NI can mislead), 02-valuation/dcf.md (ROE→sustainable growth feeds DDM).
