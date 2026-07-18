# Backlog — Stock Market Analysis KB

Priorities: P0 = foundations & traps, then fan out. Each item = one article.

## P0 (do first)
- [x] 00-foundations: market structure, instruments, order types, participants, mechanics  (DONE: market-structure.md)
- [x] 00-foundations: what is a stock / share / equity claim
- [x] 00-foundations: exchanges, ATS/dark pools, Reg NMS basics (DONE: 00-foundations/exchanges-ats-regnms.md)
- [x] 01-fundamental-analysis: income statement / balance sheet / cash flow reading  (DONE: 01-fundamental-analysis/financial-statements.md)
- [x] 01-fundamental-analysis: ratio analysis (liquidity, solvency, profitability, efficiency) (DONE: 01-fundamental-analysis/ratio-analysis.md)
- [x] 01-fundamental-analysis: quality of earnings & red flags  (DONE: 01-fundamental-analysis/quality-of-earnings.md)
- [x] 02-valuation: DCF (FCFF/FCFE) intuition + mechanics (DONE: 02-valuation/dcf.md)
- [ ] 02-valuation: relative valuation / comps
- [ ] 05-stats-and-ml: stationarity, ADF, autocorrelation
- [ ] 05-stats-and-ml: overfitting & look-ahead bias
- [ ] 08-backtesting-methodology: transaction costs, slippage, walk-forward
- [ ] 08-backtesting-methodology: deflated Sharpe ratio, multiple-testing
- [ ] 15-pitfalls-and-antipatterns: data snooping / p-hacking
- [ ] 15-pitfalls-and-antipatterns: survivorship bias

## P1 (fundamentals depth + quant)
- [ ] 03-technical-analysis: trend, support/resistance, momentum
- [ ] 03-technical-analysis: indicators (RSI, MACD) — evidence grade
- [ ] 04-quant-and-factors: CAPM & beta
- [ ] 04-quant-and-factors: Fama–French 3/5 factors (empirical record)
- [ ] 04-quant-and-factors: momentum & value premiums — robust or fading?
- [ ] 04-quant-and-factors: low-vol / quality factors
- [ ] 06-portfolio-construction: mean-variance / efficient frontier
- [ ] 06-portfolio-construction: risk parity & Kelly sizing
- [ ] 06-portfolio-construction: Black–Litterman
- [ ] 07-risk-management: VaR / CVaR
- [ ] 07-risk-management: drawdown & position sizing
- [ ] 10-derivatives: option greeks intuition
- [ ] 11-macro-and-regimes: rates, cycles, sector rotation
- [ ] 12-behavioral-finance: cognitive biases, crowding
- [ ] 13-data-and-tooling: data vendors/APIs, libraries (pinned)

## P2 (catalog & niches)
- [ ] 09-market-microstructure: liquidity, spreads, execution, market impact
- [ ] 14-strategy-catalog: strategies WITH evidence, assumptions, failure modes
- [ ] 14-strategy-catalog: factor portfolios (replication notes)
- [ ] 11-macro-and-regimes: regime detection methods

## Verify tasks (insufficient evidence — promote to Tier 1/2 before claiming)
- [ ] VERIFY: maker-taker rebate net effect on retail execution quality (conflicting: some studies say improves liquidity, some say harms price discovery) — need Tier 1 source.
- [ ] VERIFY: HFT net contribution to liquidity vs. fragility — SEC 2014 lit review Part II is a start; need a peer-reviewed summary.
- [x] VERIFY: academic evidence that accruals predict future cash flows / earnings persistence (Dechow 1994, Sloan 1996) — Sloan (1996) primary opened + cited (S43) in quality-of-earnings.md; Dechow 1994 not opened (folklore-grade, not asserted).
- [ ] VERIFY: Altman Z-score cutoff zones (Z>2.99 safe, 1.81–2.99 grey, Z<1.81 distress) — cited from secondary reproductions; confirm directly against Altman (1968) primary text and note private/non-manufacturing variants (Z', Z'').
- [ ] VERIFY: Piotroski F-score 23% long–short annual return (1976–1996) — confirm whether gross or net of transaction costs, and out-of-sample robustness after the 1996 sample end; cite a peer-reviewed replication.
- [ ] VERIFY: revenue-recognition manipulation is the single largest category of financial-statement fraud — qualitative claim made in quality-of-earnings.md but only sourced via CFA/practitioner (Tier 2); confirm against a primary Tier-1 study (e.g., COSO/AAA "Fraudulent Financial Reporting" 1987–1997/1998–2007) before asserting magnitudes.
- [ ] VERIFY: Beneish (1999) M-Score canonical TATA coefficient — quality-of-earnings.md notes 4.679 (most-cited) vs 4.697 (MarketXLS S46); confirm the exact value in the FAJ primary.
- [ ] VERIFY (DCF): cross-sectional empirical evidence that DCF intrinsic values predict future market prices better than multiples out-of-sample — most claims are anecdotal; seek a peer-reviewed test before asserting predictive power.
- [ ] VERIFY (DCF): the "75% terminal value" figure for a specific forecast length — WSP/Macabacus quote ~75% (5-yr) and ~50% (10-yr); confirm against an independent practitioner/academic source (illustrative, not a law).
