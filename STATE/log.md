# Iteration Log

## 2026-07-15 — iter 1 (kickoff + first loop)
- Initialized repo: tree 00–15, STATE/{backlog,progress,sources}, README, CHANGELOG.
- Selected P0 task: 00-foundations market structure.
- Sub-questions: bid-ask/spread, order types, primary vs secondary, market makers/participants, microstructure/HFT.
- Sources: 12 gathered (Tier 1: SEC 2014, FINRA, Investor.gov, NYSE paper, O'Hara 2015; Tier 2: Investopedia, Optiver, Schwab, CFA-prep). Confirmed each by fetching summary.
- Wrote 00-foundations/market-structure.md (template-compliant, inline cites, conflict + caveat sections).
- Self-critique → backlog: maker-taker & HFT effects flagged as contested/Verify.
- Committed. Repo health: 1/61 nodes done; many P0 open.

## 2026-07-18 — iter 2
- Selected P0 task: 00-foundations what is a stock / share / equity claim.
- Sub-questions: definition/residual claim; common vs preferred; shareholder rights (voting, dividends, limited liability); capital-structure/liquidation priority; share counts (authorized/issued/outstanding/treasury) + market cap vs book value; how ownership is recorded (street name / beneficial / DTC nominee / DRS).
- Sources: 7 (Tier 1: Investor.gov Stocks FAQ, Shareholder Voting, Holding Your Securities; Tier 2: Investopedia Common Stock & Market Cap, CFI common vs preferred, BDC share counts). All URLs opened + verified. Every major claim corroborated by >=2 independent sources.
- Wrote 00-foundations/equity-claim.md (template-compliant; inline cites S13–S19; TL;DR, core, formulas, runnable code verified, assumptions/limits, evidence, conflicts, mistakes, further reading).
- No new Verify tasks; no self-critique gaps beyond noting dual-class voting nuance flagged in Assumptions.
- Repo health: 2/61 nodes done; many P0 open.

## 2026-07-18 — iter 3
- Selected P0 task: 00-foundations exchanges / ATS / dark pools / Reg NMS basics.
- Sub-questions: lit exchanges vs ATS vs dark pools; Reg ATS/Reg NMS origins; Reg NMS four rules (610 access, 611 order protection/NBBO, 612 sub-penny, market-data 604/605/606); protected quotes/trade-throughs/ISO; dark-pool trade reporting (FINRA TRF); fragmentation & volume; 2024 amendments; 2026 rescission proposal.
- Sources: 10 (Tier 1: SEC Reg ATS page S20, FINRA dark-pool S21, CRS R43739 S22, SEC NMS FAQ S23, SEC Atkins S25, + prior S1 HFT; Tier 2: Investopedia S24, Sidley S26, Nasdaq S27, Davis Polk S28). All URLs opened + verified.
- Wrote 00-foundations/exchanges-ats-regnms.md (template-compliant; inline cites S1/S20–S28; runnable stdlib Python for NBBO + trade-through check, verified executing).
- Three-bucket labeling applied; conflicts explicit (Rule 611 benefit vs fragmentation critique; dark-pool efficiency vs transparency; 2026 rescission contested/proposal-only). Failure modes: NBBO size limits, dark pools benchmark lit prices, Reg NMS evolving.
- No new Verify tasks spawned (existing maker-taker/HFT Verify items from iter 1 remain open and still flagged).

## 2026-07-18 — iter 4
- Selected P0 task: 01-fundamental-analysis income statement / balance sheet / cash flow reading.
- Sub-questions: the four statements; accounting equation; income-statement waterfall; current/non-current split; how the three link (NI->RE, CFS->cash); where to get real data (10-K Item 8/EDGAR); GAAP vs IFRS CFS classification; non-GAAP caveats; common misreads.
- Sources: 7 (Tier 1: SEC Beginners' Guide S29, SEC 10-K bulletin PDF S30, Investor.gov 10-K S31, CFA cash-flow reading S32; Tier 2: CFI S33, Investopedia S34, Pearson GAAP/IFRS S35). All URLs opened + verified.
- Wrote 01-fundamental-analysis/financial-statements.md (template-compliant; inline cites S29–S35; stdlib-only runnable 3-statement model verified to tie out: BS balances, NI->RE and CFS->cash links hold).
- Three-bucket labeling applied (topic robust; contested areas flagged: GAAP vs IFRS classification, non-GAAP weighting). Failure modes: accrual NI != cash, estimates/judgments, book != market value, audits=reasonable assurance not guarantee.
- Self-critique -> spawned 1 new Verify task (academic accrual/cash-flow-prediction evidence) since I did not open primary papers; not asserted.
- Repo health: 4/61 nodes done; many P0 open.

## 2026-07-18 — iter 5
- Selected P0 task: 01-fundamental-analysis ratio analysis (liquidity, solvency, profitability, efficiency).
- Sub-questions: 4 ratio families + canonical formulas; DuPont ROE decomposition (3- & 5-way); efficiency/activity ratios (turnover, DOH/DSO, CCC); empirical use for distress (Altman Z) and return prediction (Piotroski F); limitations & common mistakes.
- Sources: 7 (Tier 1: CFA Financial Analysis Techniques S36, CFA Ratio List S37, Piotroski 2000 S40, Altman 1968 S41; Tier 2: Investopedia interest coverage S38, AnalystPrep categories S39, CFI limitations S42). All URLs opened + verified; Altman Z weights/cutoffs corroborated across secondary reproductions (flagged as Verify).
- Wrote 01-fundamental-analysis/ratio-analysis.md (template-compliant; inline cites S36–S42; runnable stdlib Python computing all ratios verified — ROE ties to DuPont identity to 1e-9).
- Three-bucket labeling applied (topic robust; contested: EBIT vs EBITDA coverage, "higher always better", static vs average denominators). Failure modes: historical data, accounting-policy/inflation/seasonality distortions, predictive-model decay, survivorship/look-ahead in naive backtests.
- Self-critique -> spawned 2 new Verify tasks (Altman cutoff zones from primary; Piotroski net-of-cost/out-of-sample robustness).
- Repo health: 5/61 nodes done; many P0 open.

## 2026-07-18 — iter 6
- Selected P0 task: 01-fundamental-analysis quality of earnings & red flags.
- Sub-questions: definition (cash vs accruals); CFO/NI quality screen; Sloan (1996) accrual anomaly (persistence + returns); Beneish M-Score 8 variables/coefficients/threshold; red-flag categories (revenue recognition, capitalization, reserves, CFO management); empirical validation + decay; conflicts.
- Sources: 7 (Tier 1: Sloan 1996 primary S43, CFA Institute QofE blog S44, reused SEC S29/S30/S31 as S48; Tier 2: Investopedia Beneish S45, MarketXLS S46, Soleadea CFA L1 red flags S47, Quantpedia accrual-anomaly S49). All URLs opened + verified. Sloan primary opened (resolves earlier accrual Verify); Beneish coefficients cross-checked S45 vs S46 (minor TATA 4.679 vs 4.697 discrepancy noted).
- Wrote 01-fundamental-analysis/quality-of-earnings.md (template-compliant; inline cites S43–S49; runnable stdlib Python for accruals ratio, CFO/NI, and full Beneish M-Score — verified executing: M≈−2.08 gray zone).
- Three-bucket labeling applied (framework robust; trading-edge of accrual strategy contested/decayed post-2002 per S49; M-Score a forensic flag not proof). Failure modes: accruals≠fraud, single-metric decisions, look-ahead via restatements, survivorship in backtests, taxes/costs, non-stationarity.
- Self-critique -> resolved Sloan accrual Verify (primary opened); spawned 2 new Verify tasks (COSO fraud-category primary; Beneish TATA coefficient canonical value).
- Repo health: 6/61 nodes done; many P0 open.

## 2026-07-18 — iter 7
- Selected P0 task: 02-valuation DCF (FCFF/FCFE intuition + mechanics).
- Sub-questions: DCF definition/intrinsic value; FCFF vs FCFE + build formulas; WACC + CAPM cost of equity; two-stage model; terminal value (Gordon growth + exit multiple) and the "terminal value dominates" problem; practical limitations & common mistakes (cash-flow/discount-rate mismatch).
- Sources: 8 (Tier 1: CFA Free Cash Flow Valuation S50, Damodaran NYU DCF problems S51, Damodaran blog "Terminal Value ate my DCF" S56; Tier 2: Investopedia TV S52, Wall Street Prep TV S53, Investopedia WACC S54, CFI FCFF vs FCFE S55, Macabacus TV S57). All URLs opened + verified.
- Wrote 02-valuation/dcf.md (template-compliant; inline cites S50–S57; runnable stdlib Python two-stage DCF — verified executing: WACC≈7.78%, PV of terminal value ≈81.5% of firm value, equity value Gordon≈$748m / $37.39 sh, exit-9x≈$493m / $24.66 sh, implied g from exit TV≈0.66%; plus WACC×g sensitivity grid).
- Three-bucket labeling applied (method robust; inputs emerging/folklore). Conflicts explicit: perpetuity vs exit multiple (academics vs practitioners); high-TV% is/isn't a flaw (Damodaran: not a flaw); relative valuation "assumption-free" myth. Failure modes: g<WACC, g≤GDP, going-concern only, NI/EBITDA≠cash, single-point false precision, survivorship in any "DCF beats market" backtest.
- Self-critique — spawned 2 new Verify tasks (DCF vs multiples predictive evidence; independent confirmation of 75% TV figure).
- Repo health: 7/61 nodes done; many P0 open; open Verify tasks remain (carried forward).
