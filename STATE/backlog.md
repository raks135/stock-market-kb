# Backlog — Stock Market Analysis KB

Priorities: P0 = foundations & traps, P1 = depth, P2 = catalog & niches. Each item = one article. The loop must clear ALL items (and all folders 00-15) before declaring complete.

## P0 (foundations & traps — do first)
- [x] 00-foundations: market structure, instruments, order types, participants, mechanics  (DONE: market-structure.md)
- [x] 00-foundations: what is a stock / share / equity claim
- [x] 00-foundations: exchanges, ATS/dark pools, Reg NMS basics (DONE: exchanges-ats-regnms.md)
- [x] 01-fundamental-analysis: income statement / balance sheet / cash flow reading  (DONE: financial-statements.md)
- [x] 01-fundamental-analysis: ratio analysis (DONE: ratio-analysis.md)
- [x] 01-fundamental-analysis: quality of earnings & red flags  (DONE: quality-of-earnings.md)
- [x] 02-valuation: DCF (FCFF/FCFE) (DONE: dcf.md)
- [x] 02-valuation: relative valuation / comps (DONE: relative-valuation.md)
- [x] 05-stats-and-ml: stationarity, ADF, autocorrelation (DONE: stationarity-adf-autocorrelation.md)
- [x] 05-stats-and-ml: overfitting & look-ahead bias (DONE: overfitting-lookahead.md)
- [x] 08-backtesting-methodology: transaction costs, slippage, walk-forward (DONE)
- [x] 08-backtesting-methodology: deflated Sharpe ratio, multiple-testing (DONE)
- [ ] 15-pitfalls-and-antipatterns: data snooping / p-hacking
- [ ] 15-pitfalls-and-antipatterns: survivorship bias

## P1 (fundamentals depth + quant + portfolio + risk)
- [ ] 03-technical-analysis: trend, support/resistance, momentum
- [ ] 03-technical-analysis: indicators (RSI, MACD) — evidence grade
- [ ] 03-technical-analysis: chart patterns & volume (evidence grade)
- [ ] 04-quant-and-factors: CAPM & beta
- [ ] 04-quant-and-factors: Fama–French 3/5 factors (empirical record)
- [ ] 04-quant-and-factors: momentum & value premiums — robust or fading?
- [ ] 04-quant-and-factors: low-vol / quality / carry factors
- [ ] 04-quant-and-factors: APT & multi-factor models
- [ ] 06-portfolio-construction: mean-variance / efficient frontier
- [ ] 06-portfolio-construction: risk parity & Kelly sizing
- [ ] 06-portfolio-construction: Black–Litterman
- [ ] 07-risk-management: VaR / CVaR
- [ ] 07-risk-management: drawdown & position sizing / stops
- [ ] 07-risk-management: stress testing & scenario analysis
- [ ] 10-derivatives: option greeks intuition (delta/gamma/vega/theta/rho)
- [ ] 11-macro-and-regimes: rates, business cycles, sector rotation
- [ ] 12-behavioral-finance: cognitive biases, sentiment, crowding
- [ ] 13-data-and-tooling: data vendors/APIs, libraries (pinned), reproducibility

## P2 (catalog & niches — must also be covered)
- [ ] 02-valuation: residual income / EVA & sum-of-parts valuation
- [ ] 03-technical-analysis: candlesticks (evidence grade)
- [ ] 04-quant-and-factors: factor timing & factor crowding
- [ ] 05-stats-and-ml: cointegration & pairs trading basics
- [ ] 05-stats-and-ml: feature engineering & ML pitfalls in finance
- [ ] 06-portfolio-construction: factor portfolios & smart beta
- [ ] 09-market-microstructure: liquidity, spreads, execution, market impact
- [ ] 09-market-microstructure: maker-taker, payment for order flow, HFT
- [ ] 10-derivatives: volatility surface, skew, hedging basics
- [ ] 10-derivatives: option strategies (covered call, protective put, spreads) — evidence/use cases
- [ ] 11-macro-and-regimes: regime detection methods
- [ ] 11-macro-and-regimes: inflation, yields & equity valuation
- [ ] 12-behavioral-finance: herding, overconfidence, loss aversion (prospect theory)
- [ ] 12-behavioral-finance: limits to arbitrage
- [ ] 13-data-and-tooling: data hygiene & survivorship-free datasets
- [ ] 13-data-and-tooling: backtesting libraries cookbook (vectorbt/backtrader/zipline-reloaded)
- [ ] 14-strategy-catalog: value & quality factor strategies (evidence + failure modes)
- [ ] 14-strategy-catalog: momentum & trend-following strategies (evidence + failure modes)
- [ ] 14-strategy-catalog: mean-reversion / stat-arb strategies (evidence + failure modes)
- [ ] 14-strategy-catalog: carry & volatility strategies (evidence + failure modes)
- [ ] 15-pitfalls-and-antipatterns: overfitting / curve fitting
- [ ] 15-pitfalls-and-antipatterns: regime change & non-stationarity
- [ ] 15-pitfalls-and-antipatterns: look-ahead bias (deep dive)
- [ ] 15-pitfalls-and-antipatterns: transaction-cost neglect

## Verify tasks (insufficient evidence — promote to Tier 1/2 before claiming; do NOT assert)
- [ ] VERIFY: maker-taker rebate net effect on retail execution quality.
- [ ] VERIFY: HFT net contribution to liquidity vs. fragility (peer-reviewed summary).
- [ ] VERIFY: Altman Z-score cutoff zones (confirm against Altman 1968 primary; note Z'/Z'' variants).
- [ ] VERIFY: Piotroski F-score 23% long–short return — gross vs net of costs; out-of-sample after 1996.
- [ ] VERIFY: revenue-recognition fraud as largest fraud category — confirm vs COSO/AAA primary.
- [ ] VERIFY: Beneish (1999) M-Score canonical TATA coefficient — confirm in FAJ primary.
- [ ] VERIFY (DCF): cross-sectional evidence DCF predicts future prices better than multiples OOS.
- [ ] VERIFY (relative valuation): single-stock OOS validity of "cheap = outperform" (open Campbell & Shiller 1998 / Weigand & Irons 2007).
- [ ] VERIFY: Jegadeesh (1990) short-horizon reversal & Jegadeesh & Titman (1993) momentum — open primaries.
- [ ] VERIFY: Perold (1988) implementation shortfall decomposition & Almgren & Chriss (2001) square-root impact — open primaries.

COMPLETION: all above (P0+P1+P2) done + no open Verify tasks → KB COMPLETE.
