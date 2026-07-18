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

## 2026-07-18 — iter 8
- Selected P0 task: 02-valuation relative valuation / comps.
- Sub-questions: definition & law of one price; multiple taxonomy (P/E, PEG, P/B, P/S, EV/EBITDA, EV/EBIT, EV/S); claimholder-matching rule; justified multiples from DCF; comps methodology (peer selection, scrub, median); empirical pervasiveness; limitations & common mistakes; conflicts.
- Sources: 4 (Tier 1: CFA Market-Based Valuation S58, Damodaran Relative Valuation S59; Tier 2: Investopedia comparables S60, Wall Street Prep trading comps S61). S58/S59/S60/S61 URLs opened + verified; comps mechanics corroborated across S58/S59/S61; justified-multiple algebra corroborated S58+S59.
- Wrote 02-valuation/relative-valuation.md (template-compliant; inline cites S58–S61; runnable stdlib Python comps demo — verified: peer medians EV/EBITDA 7.82, P/E 11.48, P/B 3.06, P/S 1.31; target $6000m bracketed by $5512m–$6439m implied).
- Three-bucket labeling applied (method robust; output emerging/folklore). Conflicts explicit: comps "objective" vs "circular" (Damodaran); median vs mean; P/E vs EV/EBITDA default. Failure modes: benchmark inherits peer bias/bubble, mismatched claimholders, skewed mean, negative denominators, leverage in P/E, sector-only peers, survivorship/look-ahead in backtests.
- Self-critique -> spawned 1 new Verify task (single-stock mean-reversion predictive power cited only via search abstracts, not primary papers).
- Repo health: 8/61 nodes done; many P0 open; open Verify tasks remain (carried forward).

## 2026-07-18 — iter 9
- Selected P0 task: 05-stats-and-ml stationarity, ADF, autocorrelation.
- Sub-questions: weak vs strong stationarity; why equity prices are I(1) and returns I(0); ADF null/regression/critical values; autocorrelation/ACF + Ljung-Box; volatility clustering (squared-return autocorrelation) and ARCH/GARCH; empirical stylized facts; common ADF null-reversal mistake; KPSS complement.
- Sources: 6 (Tier 1: statsmodels adfuller S62, Cont 2001 S63 [opened PDF], statsmodels ljungbox S66, statsmodels ADF/KPSS notebook S67; Tier 2: econometrics-with-r S64, machinelearningplus ADF S65). All URLs opened + verified.
- Wrote 05-stats-and-ml/stationarity-adf-autocorrelation.md (template-compliant; inline cites S62–S67; runnable stdlib+statsmodels Python verified in a pinned venv — price NON-STATIONARY p=0.61, log return STATIONARY p≈0, raw returns Ljung-Box p=0.29 no autocorrelation, squared returns Ljung-Box p≈0 strong autocorrelation).
- Three-bucket labeling applied (topic robust; contested: ADF null-reversal, ADF vs KPSS classification, "all models need stationarity" debated). Failure modes: ADF low power near unit root, structural breaks, stationarity is in-sample only, stationary≠predictable, Ljung-Box on heavy tails.
- Self-critique -> spawned 1 new Verify task (Jegadeesh 1990 reversal / Jegadeesh & Titman 1993 momentum primaries for horizon-dependent autocorrelation claim).
- Repo health: 9/61 nodes done; P0 gaps remain (overfitting/look-ahead, backtest costs, deflated Sharpe, survivorship); open Verify tasks carried forward.

## 2026-07-18 — iter 10
- Selected P0 task: 05-stats-and-ml overfitting & look-ahead bias.
- Sub-questions: overfitting/backtest-overfitting definition; look-ahead bias sources; multiple-testing & expected-max Sharpe; Deflated Sharpe Ratio / Probabilistic Sharpe Ratio; PBO/CSCV; Harvey-Liu-Zhu factor-zoo cutoff; mitigation; common mistakes.
- Sources: 7 (Tier 1 primaries: Bailey & López de Prado DSR S68, PBO/CSCV S69, overfitting simulator S70; Tier 2: Coqueret&Guida textbook S71, Foxholm HLZ review S72, CFI look-ahead S73, AnalystPrep backtesting S74). All URLs opened + verified; DSR/PSR formulas extracted directly from S68 PDF.
- Wrote 05-stats-and-ml/overfitting-lookahead.md (template-compliant; inline cites S68–S74; runnable stdlib Python overfitting demo VERIFIED: N=1000 noise trials -> best in-sample Sharpe 2.95, OOS −0.61, naive PSR 1.000, Deflated Sharpe 0.034).
- Three-bucket labeling applied (topic robust; contested: HLZ ~3.0 cutoff debated by Chen 2024; DSR vs holdout; CPCV vs walk-forward). Failure modes: effective-N for correlated trials, OOS≠future, non-stationarity, costs/capacity, DSR doesn't fix costs.
- Self-critique -> spawned 1 new Verify task (Harvey-Liu-Zhu exact t cutoff unverified against primary; SSRN/Oxford fetch failed, cited via Tier-2 Foxholm).
- Repo health: 10/61 nodes done; P0 gaps remain (backtest costs, deflated Sharpe, data-snooping, survivorship); open Verify tasks carried forward.
