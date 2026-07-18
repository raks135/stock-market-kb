# Backlog — Stock Market Analysis KB

COMPLETION GOAL: EVERY folder 00-15 must contain real knowledge-base articles (not just .gitkeep).
Two phases:
  PHASE A (breadth): one core, high-value article in EVERY currently-empty folder (03,04,06,07,09,10,11,12,13,14,15) FIRST — so all 16 folders have content.
  PHASE B (depth): fill remaining P0/P1/P2 subtopics listed below.

## PHASE A — cover every empty folder (do these next, in order)
- [x] 03-technical-analysis: trend, support/resistance, momentum  (first article for 03) — DONE 2026-07-18 (trend-support-momentum.md; confidence: contested)
- [x] 04-quant-and-factors: CAPM & beta  (first article for 04) — DONE 2026-07-18 (capm-beta.md; confidence: contested)
- [x] 06-portfolio-construction: mean-variance / efficient frontier  (first article for 06) — DONE 2026-07-18 (mean-variance-efficient-frontier.md; confidence: robust)
- [x] 07-risk-management: VaR / CVaR  (first article for 07) — DONE 2026-07-18 (var-cvar.md; confidence: robust)
- [x] 09-market-microstructure: liquidity, spreads, execution, market impact  (first article for 09) — DONE 2026-07-18 (liquidity-spreads-execution-impact.md; confidence: robust)
- [x] 10-derivatives: option greeks intuition (delta/gamma/vega/theta/rho)  (first article for 10) — DONE 2026-07-18 (option-greeks.md; confidence: robust)
- [x] 11-macro-and-regimes: rates, business cycles, sector rotation  (first article for 11) — DONE 2026-07-18 (rates-business-cycles-sector-rotation.md; confidence: robust)
- [x] 12-behavioral-finance: cognitive biases, sentiment, crowding  (first article for 12) — DONE 2026-07-18 (cognitive-biases-sentiment-crowding.md; confidence: robust)
- [x] 13-data-and-tooling: data vendors/APIs, libraries (pinned), reproducibility  (first article for 13) — DONE 2026-07-18 (data-vendors-apis-libraries-reproducibility.md; confidence: robust)
- [ ] 14-strategy-catalog: value & quality factor strategies (evidence + failure modes)  (first article for 14)
- [x] 15-pitfalls-and-antipatterns: data snooping / p-hacking  (first article for 15) — DONE earlier (data-snooping-phacking.md); marked complete this iteration

## PHASE B — depth (after every folder has >=1 article)
- [x] 00-foundations: market structure (DONE)
- [x] 00-foundations: equity claim (DONE)
- [x] 00-foundations: exchanges/ATS/Reg NMS (DONE)
- [x] 01-fundamental-analysis: financial statements (DONE)
- [x] 01-fundamental-analysis: ratio analysis (DONE)
- [x] 01-fundamental-analysis: quality of earnings (DONE)
- [x] 02-valuation: DCF (DONE)
- [x] 02-valuation: relative valuation (DONE)
- [x] 05-stats-and-ml: stationarity/ADF (DONE)
- [x] 05-stats-and-ml: overfitting/look-ahead (DONE)
- [x] 08-backtesting-methodology: transaction costs/slippage/walk-forward (DONE)
- [x] 08-backtesting-methodology: deflated Sharpe/multiple-testing (DONE)
- [ ] 01-fundamental-analysis: DuPont analysis & ROE decomposition
- [ ] 02-valuation: residual income / EVA & sum-of-parts
- [ ] 03-technical-analysis: indicators (RSI, MACD) — evidence grade
- [ ] 03-technical-analysis: chart patterns & volume (evidence grade)
- [ ] 03-technical-analysis: candlesticks (evidence grade)
- [ ] 04-quant-and-factors: Fama–French 3/5 factors (empirical record)
- [ ] 04-quant-and-factors: momentum & value premiums — robust or fading?
- [ ] 04-quant-and-factors: low-vol / quality / carry factors
- [ ] 04-quant-and-factors: APT & multi-factor models
- [ ] 04-quant-and-factors: factor timing & factor crowding
- [ ] 05-stats-and-ml: cointegration & pairs trading basics
- [ ] 05-stats-and-ml: feature engineering & ML pitfalls in finance
- [ ] 06-portfolio-construction: risk parity & Kelly sizing
- [ ] 06-portfolio-construction: Black–Litterman
- [ ] 06-portfolio-construction: factor portfolios & smart beta
- [ ] 07-risk-management: drawdown & position sizing / stops
- [ ] 07-risk-management: stress testing & scenario analysis
- [ ] 09-market-microstructure: maker-taker, payment for order flow, HFT
- [ ] 10-derivatives: volatility surface, skew, hedging basics
- [ ] 10-derivatives: option strategies (covered call, protective put, spreads)
- [ ] 11-macro-and-regimes: regime detection methods
- [ ] 11-macro-and-regimes: inflation, yields & equity valuation
- [ ] 12-behavioral-finance: herding, overconfidence, loss aversion (prospect theory)
- [ ] 12-behavioral-finance: limits to arbitrage
- [ ] 13-data-and-tooling: data hygiene & survivorship-free datasets
- [ ] 13-data-and-tooling: backtesting libraries cookbook (vectorbt/backtrader/zipline-reloaded)
- [ ] 14-strategy-catalog: momentum & trend-following strategies
- [ ] 14-strategy-catalog: mean-reversion / stat-arb strategies
- [ ] 14-strategy-catalog: carry & volatility strategies
- [ ] 15-pitfalls-and-antipatterns: overfitting / curve fitting
- [ ] 15-pitfalls-and-antipatterns: regime change & non-stationarity
- [ ] 15-pitfalls-and-antipatterns: look-ahead bias (deep dive)
- [ ] 15-pitfalls-and-antipatterns: transaction-cost neglect
- [ ] 15-pitfalls-and-antipatterns: survivorship bias

## Verify tasks (promote to Tier 1/2 before claiming; do NOT assert)
- [ ] VERIFY: exact FRTB IMA calibration — 97.5% Expected Shortfall replacing 99% 10-day VaR — against BCBS d457 primary (KPMG/SIFMA confirm ES-replaces-VaR; exact confidence levels rest on secondary summaries only).
- [ ] VERIFY: HFT net contribution to liquidity vs. fragility.
- [ ] VERIFY: Altman Z-score cutoff zones (Altman 1968 primary; Z'/Z'' variants).
- [ ] VERIFY: Piotroski F-score 23% long–short — gross vs net of costs; OOS after 1996.
- [ ] VERIFY: revenue-recognition fraud as largest fraud category (COSO/AAA primary).
- [ ] VERIFY: Beneish (1999) M-Score canonical TATA coefficient (FAJ primary).
- [ ] VERIFY (DCF): OOS evidence DCF predicts prices better than multiples.
- [ ] VERIFY (relative valuation): single-stock OOS validity (Campbell & Shiller 1998 / Weigand & Irons 2007).
- [ ] VERIFY: Jegadeesh (1990) reversal & Jegadeesh & Titman (1993) momentum primaries.
- [ ] VERIFY: Perold (1988) IS decomposition & Almgren & Chriss (2001) square-root impact primaries.
- [ ] VERIFY: Kyle (1985) exact λ / market-depth algebra and linear pricing rule p = p* + λ·y (primary PDF not directly opened; cited via S120/S121 — only qualitative depth=1/λ asserted).
- [ ] VERIFY: Huang & Stoll (1997) exact three-way spread split (order processing / inventory / adverse selection) coefficients — primary not directly opened; two-component S123 opened corroborates the decomposition concept only.
- [ ] VERIFY: Cowell et al. (arXiv 0810.1922) "look-ahead benchmark bias up to ~8%/yr for S&P500" exact figure — cited via search snippet only this iteration (PDF not opened); cross-check against CRSP 1926-2006 study before asserting magnitude.

COMPLETION: all 16 folders (00-15) have >=1 article AND all Phase A/B items done AND no open Verify tasks → KB COMPLETE.
- Simulation is synthetic noise (Box–Muller, stdlib, seed 42) — deliberately null; demonstrates the *selection* effect, not a market claim. Numbers are reproducible as written.
- S88 (Sullivan/Timmermann/White 1999) only abstract opened; conclusion softened to "quantify the bias / canonical demonstration" rather than asserting "profitability disappears" (full text not opened → do NOT assert stronger).
- Carried forward open Verify tasks from prior iters remain; no new Verify spawned (White 2000 + STW 1999 primaries now opened, resolving the earlier Jegadeesh/White "data-snooping" gap at the conceptual level).

COMPLETION: all above (P0+P1+P2) done + no open Verify tasks → KB COMPLETE.
