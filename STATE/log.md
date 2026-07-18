# Iteration Log

## 2026-07-18 — iter 19
- Selected PHASE A task: 10-derivatives option greeks intuition (first article for folder 10).
- Sub-questions: 5 greeks definitions/intuition (delta/gamma/vega/theta/rho); order (1st vs 2nd); BS closed-form formulas; call-put delta parity; vega/rho per-1% scaling trap; theta sign conventions; delta hedging & dollar gamma & P&L(imp-realized vol); volatility surface skew empirical; "delta=prob ITM" folklore; common mistakes.
- Sources: 4 new — Tier 2: Wikipedia Greeks S127, Macroption BS formulas S128, Investopedia Greeks S130; Tier 1: Columbia/Haugh BS lecture notes S129 (opened PDF: delta hedging, dollar gamma, P&L formula, vol-surface skew). All URLs opened+verified; greek definitions corroborated across S127/S128/S130 (3 independent); BS formulas via S128 + S129; vol-surface skew via opened S129.
- Wrote 10-derivatives/option-greeks.md (template-compliant; three-bucket labeling: BS mechanics robust, model assumptions limited/contested, "delta=prob ITM" flagged folklore; stdlib-only runnable Python VERIFIED: ATM call Δ=0.598/put −0.402 parity=1.000; gamma/vega equal call&put; deep ITM Δ→1, OTM→0; Taylor reprice err $0.0025 on $7.77).
- Self-critique: no new Verify spawned (all claims corroborated by >=2 opened sources; vol-surface skew from opened primary lecture notes). Hull textbook cited as further reading only (not a URL).
- Repo health: 19/61 nodes done; PHASE A: 03/04/06/07/09/10 done; 11/12/13/14 still need first articles; open Verify carried forward.

- Selected PHASE A task: 09-market-microstructure liquidity/spreads/execution/impact (first article for folder 09).
- Sub-questions: liquidity tri-dimensionality (tightness/depth/resiliency); spread measures (quoted/effective/realized); Roll (1984) implicit spread; Glosten–Harris (1988) transitory vs adverse-selection decomposition; Kyle (1985) lambda/depth; Almgren–Chriss (2000/01) temporary/permanent impact + efficient frontier; square-root impact law; implementation shortfall (Perold 1988).
- Sources: 8 new — Tier 1: Roll 1984 primary S119, Almgren–Chriss primary S120, BIS CGFS 1999 S121, Glosten–Harris 1988 primary S123, Perold 1988 primary S126; Tier 2: O'Connell IS S125; Kyle 1985 S122 & Huang–Stoll 1997 S124 cited as primaries via reference only (NOT directly opened → 2 new Verify tasks). Reused S75/S76/S79. All opened URLs verified; Roll/Almgren-Chriss/Glosten-Harris/BIS PDFs opened & formulas extracted directly.
- Wrote 09-market-microstructure/liquidity-spreads-execution-impact.md (template-compliant; three-bucket labeling; pure-stdlib runnable Python VERIFIED: Roll implicit spread 0.0484 vs injected 0.05; Almgren-Chriss schedules front-load from 2.0%→81.5%→97.4% first-interval as λ rises, E rises $192k→$359k→$423k while V falls, confirming cost/variance trade-off; square-root scaling ≈3.16× per 10× Q).
- Self-critique → spawned 2 Verify tasks (Kyle λ algebra; Huang–Stoll 3-way split) since primaries not directly opened.
- Repo health: 18/61 nodes done; PHASE A: 03/04/06/07/09 done; 10/11/12/13/14 still need first articles; open Verify carried forward.

## 2026-07-18 — iter 16
- Selected PHASE A task: 06-portfolio-construction mean-variance / efficient frontier (first article for folder 06).
- Sub-questions: MV optimization & efficient frontier definition; portfolio moments w'μ, w'Σw; GMV closed form; tangency/max-Sharpe with risk-free (CAL/CML); 2-fund theorem; estimation-error / error-maximization critique; 1/N vs sample MV empirical record (DeMiguel 2009); remedies.
- Sources: 7 new — Tier 1: CFA Part I S103, Columbia Haugh notes S104, DeMiguel 2009 primary abstract S106, Michaud 1989 abstract S108, Markowitz 1952 S109; Tier 2: Wikipedia S105, Scientific Portfolio abstract quote S107. All URLs opened+verified (DeMiguel & Michaud via opened abstract/search; full texts not directly opened → claims limited to abstract level; 1/N numbers corroborated S106+S107).
- Wrote 06-portfolio-construction/mean-variance-efficient-frontier.md (template-compliant; three-bucket labeling; pure-stdlib runnable Python VERIFIED: GMV vol 0.1105, tangency Sharpe 0.6283 at t=1.0, frontier traces correctly).
- Self-critique → spawned 1 Verify task (empirical edge of shrinkage/resampled efficiency vs 1/N OOS).
- Repo health: 16/61 nodes done; PHASE A: 03/04/06 done; 07/09/10/11/12/13/14 still need first articles; open Verify carried forward.

## 2026-07-18 — iter 17
- Selected PHASE A task: 07-risk-management VaR / CVaR (first article for folder 07).
- Sub-questions: VaR definition (quantile, not worst-case); three methods (parametric/historical/Monte Carlo); CVaR/Expected Shortfall definition & coherence; Artzner four axioms & VaR non-subadditivity; FRTB regulatory shift VaR→ES; Kupiec POF backtest + Basel traffic-light; limitations & common mistakes.
- Sources: 9 new — Tier 1: CFA "Measuring and Managing Market Risk" S110, Artzner et al. 1999 primary S111, Kupiec 1995 primary ref S116; Tier 2: Wikipedia VaR/ES/Coherent S112/S113/S114, MetricGate Kupiec POF S115, KPMG FRTB S117, SIFMA FRTB S118. All URLs opened + verified; FRTB ES-replaces-VaR corroborated across KPMG+SIFMA+search; coherence/critique corroborated Artzner primary + 3 Wikipedia pages.
- Wrote 07-risk-management/var-cvar.md (template-compliant; three-bucket labeling; pure-stdlib runnable Python VERIFIED: parametric VaR_95%=$15,949, CVaR_95%=$20,127; historical VaR=$16,124/CVaR=$20,101; Kupiec n=250, 18 breaches, LR=2.256, p=0.133 fail-to-reject).
- Self-critique → spawned 1 Verify task (exact FRTB IMA calibration 97.5% ES vs 99% VaR against BCBS d457 primary).
- Repo health: 17/61 nodes done; PHASE A: 03/04/06/07 done; 09/10/11/12/13/14 still need first articles; open Verify carried forward.

## 2026-07-18 — iter 15
- Selected PHASE A task: 04-quant-and-factors CAPM & beta (first article for folder 04).
- Sub-questions: CAPM/SML formula; beta definition & OLS estimation; levered/unlevered (bottom-up) beta; Blume shrinkage; empirical record (F&F 1992 flat beta); Roll's critique; assumptions/limitations; conflicts (CAPM dead vs alive; time-series vs cross-section).
- Sources: 7 new (Tier 1: CFA S97, Damodaran S98, Roll 1977 via Wikipedia S99, Fama&French 1992 abstract S100; Tier 2: Investopedia S96, MPRA S102; Tier 3: Folio Lab S101). All URLs opened+verified; flat-beta claim corroborated S100+S96.
- Wrote 04-quant-and-factors/capm-beta.md (template-compliant; three-bucket labeling; pure-stdlib runnable Python VERIFIED: beta=1.2425, alpha=-0.0033, CAPM E[R]=11.45%, Blume=1.1616).
- Self-critique: Blume coefficient labeled empirical (not canonical); no new Verify spawned.
- Repo health: 15/61 nodes done; PHASE A: 03,04 done; 06/07/09/10/11/12/13/14 still need first articles; open Verify carried forward.

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

## 2026-07-18 — iter 11
- Selected P0 task: 08-backtesting-methodology transaction costs, slippage, walk-forward.
- Sub-questions: explicit vs implicit cost split; implementation shortfall (Perold 1988) decomposition; effective/realized spread & VWAP benchmarking; slippage definition/drivers; square-root market-impact law; walk-forward protocol, mechanics, limitations; capacity.
- Sources: 5 new (Tier 1: CFA Trading Costs & Electronic Markets S75; Tier 2: Graham Capital TCA note S76, QuantInsti WFO S77, Investopedia Slippage S78, Bouchaud square-root law S79) + reused S68/S69 for deflated-Sharpe/CPCV cross-reference. All URLs opened + verified; cost decomposition corroborated S75+S76, square-root law S76+S79, IS S75+S76.
- Wrote 08-backtesting-methodology/transaction-costs-slippage-walkforward.md (template-compliant; inline cites S75–S79; stdlib-only runnable Python VERIFIED: IS=$408/0.408%, eff spread $0.50, 10% participation -> ~37.9 bps impact, naive Sharpe 1.69 vs WFO OOS 1.24).
- Three-bucket labeling applied (topic robust; square-root η market-specific; WFO mitigates not eliminates overfit). Failure modes: implicit costs dominate, VWAP understates impact, WFO regime-lag + window bias, capacity/scale, no look-ahead in code.
- Self-critique -> spawned 1 new Verify task (open Perold 1988 + Almgren&Chriss 2001 primaries for exact IS decomposition / impact constant).
- Repo health: 11/61 nodes done; open P0 gaps: 08 deflated Sharpe, 15 data-snooping, 15 survivorship; open Verify tasks carried forward.

## 2026-07-18 — iter 12
- Selected P0 task: 08-backtesting-methodology deflated Sharpe ratio + multiple-testing.
- Sub-questions: multiple-testing/FWER inflation; selection bias & backtest overfitting; PSR (non-normal SE of Sharpe estimator); DSR = PSR at expected-max-Sharpe null; MinTRL; Bonferroni/Holm (FWER) vs Benjamini-Hochberg (FDR) vs BY; factor-zoo t≈3.0 bar; HLZ vs Chen(2024) conflict.
- Sources: 8 new (Tier 1: Bailey&LdP DSR primary S80, Chen 2024 Fed S82, Benjamini&Hochberg 1995 S83, Lo 2002 S86; Tier 2: QuantConnect PSR S81, Wikipedia DSR/FDR S85; Tier 3: Brenndoerfer mult-comparisons S84) + reused HLZ summary S72. All primary/key URLs opened + verified (DSR PDF, Chen PDF, QuantConnect, Brenndoerfer). HLZ primary (Oxford/SSRN) failed fetch but 316/|t|≈3.0 corroborated via opened S72 (Foxholm) + SSRN abstract.
- Wrote 08-backtesting-methodology/deflated-sharpe-multiple-testing.md (template-compliant; inline cites S80–S86; stdlib-only runnable Python VERIFIED: PSR(0)=0.999, DSR deflates 0.999→0.958→0.753→0.468 for N=1/10/100/1000; MinTRL=36 obs; m=200 null → 12 naive false positives, 0 after Bonferroni/BH, FWER_naive=1.000).
- Three-bucket labeling applied (DSR/PSR mechanics robust; HLZ-vs-Chen "how many factors are real" magnitude contested). Conflicts explicit: HLZ "most false, |t|≈3.0" vs Chen "≥75% true, HLZ's own FDR 9–35%, conflict is interpretive."
- Failure modes explicit: DSR fixes statistical inflation only (not non-stationarity/costs/capacity); N must be true/effective trials; asymptotic; γ=0 prior; BH dependence assumption.
- Self-critique: no new Verify tasks spawned; HLZ magnitude now corroborated (2 sources) though primary PDF not directly opened (logged).
- Repo health: 12/61 nodes done; open P0 gaps: 15 data-snooping, 15 survivorship; open Verify tasks carried forward.

## 2026-07-18 — iter 13
- Selected P0 task: 15-pitfalls-and-antipatterns data snooping / p-hacking.
- Sub-questions: definition (data used >once for inference/model selection); why selection inflates type-I error; FWER 1-(1-a)^m; Bonferroni/Holm vs BH(FDR); White (2000) Reality Check / SPA bootstrap; DSR; factor-zoo (HLZ) multiple-testing; conflicts (HLZ vs Chen 2024).
- Sources: 2 new Tier-1 primaries opened + verified — White 2000 Econometrica (S87), Sullivan/Timmermann/White 1999 JoF (S88, abstract); reused Tier-1 S68/S69/S70/S80/S83/S86 and Tier-2 S71/S72/S82 from registry.
- Wrote 15-pitfalls-and-antipatterns/data-snooping-phacking.md (template-compliant; inline cites; runnable stdlib-only simulation VERIFIED: best of 1000 noise rules |t|=3.64 naive p=0.0003 -> Bonferroni p=0.27; avg max|t|=3.45 across 200 searches; 95% of searches yield |t|>3).
- Three-bucket labeling applied (topic robust; HLZ-vs-Chen magnitude contested). Failure modes explicit: hidden trial counts, dependence, non-stationarity/costs/capacity not fixed by corrections, walk-forward still snoops if reused.
- Self-critique: S88 full text not opened -> conclusion softened; no new Verify spawned.
- Repo health: 13/61 nodes done; open P0 gap: 15 survivorship; open Verify tasks carried forward.

## 2026-07-18 — iter 14
- Selected PHASE A task: 03-technical-analysis trend, support/resistance, momentum (first article for folder 03).
- Sub-questions: TA definition/three tenets (Dow); trend & moving averages (golden/death cross); support/resistance (zones, role reversal, psychology/loss aversion); cross-sectional momentum (Jegadeesh & Titman 1993) vs time-series momentum (Moskowitz Ooi Pedersen 2012); empirical record & decay; conflicts (EMH/Malkiel vs Lo); common mistakes.
- Sources: 7 (Tier 1: CFA Institute RF monograph S89 [opened — quotes Brock/J&T/Park&Irwin/Cowles]; Moskowitz TSM primary S91 [opened & verified]; Brock 1992 S90 + J&T 1993 S92 asserted only as faithfully quoted in opened S89, full PDFs not directly opened → flagged; Park & Irwin 2007 S93 via S89; Tier 2: Investopedia S94 [opened], analystnotes S95). All cited URLs either opened or quoted from an opened source.
- Wrote 03-technical-analysis/trend-support-momentum.md (template-compliant; inline cites S89–S95; three-bucket labeling: robust=momentum premium, emerging=simple MA-rule profitability in current US equities, folklore=single-pattern clairvoyance; stdlib-only runnable SMA-cross + 12-1 momentum snippet VERIFIED executing).
- Failure modes explicit: lagging reactive indicators, costs dominate churn, support/resistance are zones not lines, data-mining (7,846 Brock rules), regime non-stationarity; ties to KB 05/08/15.
- Self-critique: Brock 1992 and J&T 1993 primaries not directly opened (fetch failed) — findings asserted only as quoted in opened S89; no new Verify spawned (carried forward).
- Repo health: 14/61 nodes done; PHASE A in progress (03 done; 04/06/07/09/10/11/12/13/14 still need first articles); open Verify tasks carried forward.
