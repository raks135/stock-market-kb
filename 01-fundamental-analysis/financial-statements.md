---
title: Reading the Three Financial Statements (Income, Balance Sheet, Cash Flow)
topic_id: 01-fundamental-analysis/financial-statements
tags: [fundamental-analysis, financial-statements, income-statement, balance-sheet, cash-flow, accrual-accounting, 10-K]
last_updated: 2026-07-18
confidence: robust
sources: [S29, S30, S31, S32, S33, S34, S35]
---

## TL;DR
- The three core statements are the **income statement** (profitability over a period), the **balance sheet** (financial position at a point in time), and the **cash flow statement** (cash movements over a period). A fourth, the statement of shareholders' equity, bridges them.
- They are **linked**: net income flows into retained earnings on the balance sheet, and the cash flow statement's ending cash must equal the cash on the balance sheet. Always check those two links.
- Net income is **not** cash. Accrual accounting means earnings and cash diverge; read the cash flow statement to see why.
- Source the real filings from a company's **10-K, Item 8** (audited) on SEC EDGAR; treat any "non-GAAP" number as supplementary, not a substitute.

## Core explanation
Public companies file three (really four) primary financial statements. They describe the same business from three angles and, by construction, must agree with one another.

**Income statement** (a.k.a. statement of operations / P&L; "period" view). It walks from revenue down to net income like a staircase: revenue at the top, then deductions for costs and expenses, with net income at the "bottom line." It is prepared on an **accrual** basis — revenue is recognized when earned and expenses when incurred, regardless of when cash changes hands [S29, S33].

**Balance sheet** (a.k.a. statement of financial position; "point-in-time" snapshot). It lists what the company owns (assets), what it owes (liabilities), and the owners' residual claim (shareholders' equity), obeying the accounting equation `Assets = Liabilities + Shareholders' Equity` [S29]. Assets are split into current (expected to convert to cash within a year) and non-current; liabilities similarly into current and long-term [S29].

**Cash flow statement** ("period" view). It reconciles the period's change in the cash balance, grouping cash movements into **operating**, **investing**, and **financing** activities. It "undoes" accrual accounting to show pure cash movement, typically starting from net income and adjusting for non-cash items (e.g., depreciation) and changes in working capital [S33, S32].

**Statement of shareholders' equity** (the fourth statement). Shows how equity accounts changed — most importantly, how net income (less dividends) moved into **retained earnings** [S29, S30].

### How they connect
- **Net income → retained earnings**: `RE_end = RE_beg + Net Income − Dividends`. Net income from the income statement increases equity on the balance sheet [S29, S34].
- **Net income → cash flow statement**: under the indirect method, the cash flow statement *starts* at net income and adjusts to cash from operations [S32, S33].
- **Cash flow statement → balance sheet**: the ending cash on the cash flow statement must equal the cash account on the balance sheet [S33].

## Math / formulas
Accounting equation:
```
Assets = Liabilities + Shareholders' Equity
```
Income-statement waterfall (multi-step form):
```
Net Revenue      = Gross Revenue − Returns/Allowances
Gross Profit     = Net Revenue − COGS
Operating Income = Gross Profit − Operating Expenses − Depreciation & Amortization   (≈ EBIT)
Pretax Income    = Operating Income + Non-operating items (e.g., − Interest Expense)
Net Income       = Pretax Income − Income Tax
```
Earnings per share:
```
EPS = Net Income / Weighted-Average Diluted Shares
```
The SEC frames EPS as "how much money shareholders would receive for each share if the company distributed all of its net income for the period" (companies almost never do) [S29].

Cash-flow / equity links:
```
Ending Cash          = Beginning Cash + CFO + CFI + CFF
RE_end               = RE_beg + Net Income − Dividends
```

## Worked example / code
A fully self-consistent, illustrative 3-statement model (stdlib-only, so it runs anywhere). It proves the two linkage identities and that the balance sheet balances. Numbers are synthetic but tie out exactly. In practice analysts build this in pandas (e.g., `pandas==2.2.2`); the logic is identical.

```python
#!/usr/bin/env python3
# Run: python3 financial_statements_demo.py   (Python 3.10+, no external deps)
revenue, cogs, opex, depreciation = 1000.0, 400.0, 300.0, 50.0
interest_exp, tax_rate, shares, dividends = 25.0, 0.21, 100.0, 50.0
gross_profit  = revenue - cogs                       # 600
operating_inc = gross_profit - opex - depreciation   # EBIT = 250
pretax        = operating_inc - interest_exp         # 225
net_income    = pretax * (1 - tax_rate)              # 177.75
eps           = net_income / shares                  # 1.7775

beg = dict(cash=100.0, ar=200.0, inv=150.0, ppe=550.0, ap=120.0, debt=280.0, cs=0.0, re=600.0)
d_ar, d_inv, d_ap, capex = 120.0, 30.0, 50.0, 100.0

cfo = net_income + depreciation - d_ar - d_inv + d_ap   # 127.75 (indirect method)
cfi = -capex                                            # -100
cff = -dividends                                        # -50
net_change_cash = cfo + cfi + cff                       # -22.25

end = dict(
    cash = beg["cash"] + net_change_cash,
    ar   = beg["ar"] + d_ar,
    inv  = beg["inv"] + d_inv,
    ppe  = beg["ppe"] + capex - depreciation,
    ap   = beg["ap"] + d_ap,
    debt = beg["debt"], cs = beg["cs"],
    re   = beg["re"] + net_income - dividends,          # 727.75
)
assets = end["cash"] + end["ar"] + end["inv"] + end["ppe"]
le     = end["ap"] + end["debt"] + end["cs"] + end["re"]

assert abs(assets - le) < 1e-9, "Balance sheet must balance"
assert abs(end["cash"] - (beg["cash"] + net_change_cash)) < 1e-9
assert abs(end["re"]   - (beg["re"] + net_income - dividends)) < 1e-9
print(f"NI={net_income:.2f} EPS={eps:.4f} | CFO/CFI/CFF={cfo:.2f}/{cfi:.2f}/{cff:.2f} | BS balances={abs(assets-le)<1e-9}")
```
**Data source for real numbers:** pull audited statements from the company's **Form 10-K, Item 8** via SEC EDGAR — either the full-text search (https://www.sec.gov/edgar/searchedgar/companysearch) or the structured XBRL endpoint `https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json` (pad CIK to 10 digits; SEC requires a descriptive User-Agent header). The 10-K's Item 7 (MD&A) and the footnote disclosures explain the judgments behind the numbers [S30, S31].

## Assumptions & limitations
- **Accrual basis:** revenue/expenses are booked when earned/incurred, not when cash moves. Net income and cash flow therefore diverge by design; a profitable company can still run out of cash [S29, S32].
- **Estimates & judgments:** depreciation lives, inventory method (LIFO/FIFO), allowance for doubtful accounts, warranty/reserve accruals, and revenue-recognition timing are all management estimates that materially affect the numbers. The footnotes disclose them [S30].
- **Historical, not forward-looking:** statements report the past period; they say nothing guaranteed about the future.
- **Book value ≠ market value:** the balance sheet carries assets at historical cost (mostly), so equity book value is not the company's market value.
- **Audited ≠ guaranteed:** the auditor gives "reasonable assurance" (an unqualified opinion that statements present fairly per GAAP); audits detect material misstatement, not fraud-proof perfection. A "qualified" or "disclaimer" opinion is a red flag [S30].
- **Non-GAAP measures:** companies may show "adjusted" earnings that do **not** conform to GAAP; they must reconcile to the nearest GAAP figure, but weighting them is the investor's call [S30].

## Empirical evidence
- The three-statement framework is not a hypothesis but a **regulatory requirement**: U.S. public companies must present GAAP-basis audited financial statements, and the Sarbanes-Oxley Act requires the CEO and CFO to certify the 10-K's accuracy and the SEC to review each company's filings at least every three years [S30].
- The *reason* a separate cash flow statement exists is empirical: under accrual accounting, net income and cash flow measure different things, and both are needed to assess liquidity, solvency, and financial flexibility — which is why CFA curriculum treats the cash flow statement as integral to valuation (payments to investors are made in cash) [S32].
- Specific academic claims about, e.g., accruals predicting future cash flows or earnings persistence, are **not** asserted here because they were not independently re-verified for this article; see "Verify" tasks below.

## Conflicting views
- **GAAP vs IFRS classification of interest/dividends in the cash flow statement.** Under U.S. GAAP, interest paid/received and dividends received are operating, dividends paid are financing. Under IFRS, classification is more flexible: interest paid may be operating or financing, and interest/dividends received may be operating or investing, applied consistently [S32, S35]. This means cross-standard comparisons need care.
- **Non-GAAP "adjusted" earnings.** Permitted and often useful, but critics note they can flatter results; the SEC requires reconciliation and investors should treat them as supplementary [S30].
- **Single-step vs multi-step income statement.** Both are acceptable formats; the multi-step "staircase" (used above) separates operating from non-operating and highlights gross/operating profit, which many analysts prefer [S33].

## Common mistakes
- **Treating net income as cash.** A company can show profits and still face a cash crunch; always read CFO [S29, S32].
- **Ignoring the statement of shareholders' equity** and thus missing buybacks, option exercises, and the dividends that lower retained earnings.
- **Trusting "adjusted" non-GAAP numbers uncritically** without the GAAP reconciliation [S30].
- **Comparing across companies/fiscal years without normalizing** accounting policies (LIFO vs FIFO, capitalization thresholds) or fiscal year-ends.
- **Skipping the footnotes and MD&A**, where the real estimates, commitments, and off-balance-sheet items live [S30, S31].
- **Confusing book value with intrinsic value**; the balance sheet is a historical-cost snapshot, not a valuation.
- **Reading one period in isolation.** Trend (multiple periods) and peer comparison matter more than a single snapshot.

## Further reading
- [S29] SEC, *Beginners' Guide to Financial Statements* (Office of Investor Education) — https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide (Tier 1)
- [S30] SEC Investor.gov, *Investor Bulletin: How to Read a 10-K* (Sep 2011) — https://www.sec.gov/files/reada10k.pdf (Tier 1)
- [S31] Investor.gov, *How to Read a 10-K* — https://www.investor.gov/introduction-investing/getting-started/researching-investments/how-read-10-k (Tier 1)
- [S32] CFA Institute, *Analyzing Statements of Cash Flows I* (2026 CFA L1 FSA) — https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/analyzing-statements-of-cash-flows-i (Tier 1)
- [S33] Corporate Finance Institute, *The 3 Financial Statements* — https://corporatefinanceinstitute.com/resources/accounting/three-financial-statements (Tier 2)
- [S34] Investopedia, *How Financial Statements Connect* — https://www.investopedia.com/ask/answers/031815/how-are-three-major-financial-statements-related-each-other.asp (Tier 2)
- [S35] Pearson, *GAAP vs. IFRS: Statement of Cash Flows* — https://www.pearson.com/channels/financial-accounting/learn/brian/ch-15-gaap-vs-ifrs/gaap-vs-ifrs-statement-of-cash-flows (Tier 2)

### Verify tasks spawned
- [ ] VERIFY: academic evidence that accruals predict future cash flows / earnings persistence (Dechow 1994, Sloan 1996) — need to open and cite the primary paper before asserting.
