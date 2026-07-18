# Progress Map — Stock Market Analysis KB

Coverage status per taxonomy node. Status: todo / drafting / sourced / done. Confidence: robust | emerging | contested.

| Topic | Path | Status | Confidence |
|---|---|---|---|
| Market structure, instruments, order types, participants, mechanics | 00-foundations/market-structure.md | done | robust |
| Equity claim (what a share is) | 00-foundations/equity-claim.md | done | robust |
| Exchanges / ATS / Reg NMS | 00-foundations/exchanges-ats-regnms.md | done | robust |
| Financial statements | 01-fundamental-analysis/financial-statements.md | done | robust |
| Ratio analysis | 01-fundamental-analysis/ratio-analysis.md | done | robust |
| Quality of earnings | 01-fundamental-analysis/quality-of-earnings.md | done | robust |
| DuPont analysis & ROE decomposition | 01-fundamental-analysis/dupont-analysis.md | done | robust |
| DCF (FCFF/FCFE, WACC, terminal value) | 02-valuation/dcf.md | done | robust |
| Relative valuation / comps | 02-valuation/relative-valuation.md | done | robust |
| Residual income / EVA / SOTP | 02-valuation/residual-income-eva-sotp.md | done | robust |
| Technical: trend/momentum | 03-technical-analysis/trend-support-momentum.md | done | contested |
|| Technical: indicators (RSI, MACD, evidence grade) | 03-technical-analysis/indicators-rsi-macd.md | done | contested |
||| Technical: chart patterns & volume (evidence grade) | 03-technical-analysis/chart-patterns-volume.md | done | contested |
||| Technical: candlesticks (evidence grade) | 03-technical-analysis/candlesticks.md | done | contested |
| CAPM & beta (SML, estimation, Blume, Roll's critique) | 04-quant-and-factors/capm-beta.md | done | contested |
|| Fama–French 3/5 factors (construction, empirical record, extensions) | 04-quant-and-factors/fama-french-factors.md | done | contested |
|| Momentum & value premiums (robust vs fading, crash risk, diversification) | 04-quant-and-factors/momentum-value-premiums.md | done | contested |
||| Low-vol / quality / carry factors (BAB, QMJ, Carry) | 04-quant-and-factors/low-vol-quality-carry-factors.md | done | contested |
|||| APT & multi-factor models (Ross 1976, factor structure, macro/fundamental/statistical, vs CAPM) | 04-quant-and-factors/apt-multi-factor-models.md | done | contested |
|||| Factor timing & factor crowding | 04-quant-and-factors/factor-timing-crowding.md | done | contested |
|| Stats: stationarity, ADF, autocorrelation | 05-stats-and-ml/stationarity-adf-autocorrelation.md | done | robust |
|| Stats: cointegration, Engle-Granger/Johansen, pairs trading | 05-stats-and-ml/cointegration-pairs-trading.md | done | contested |
|| Feature engineering & ML pitfalls in finance | 05-stats-and-ml/feature-engineering-ml-pitfalls.md | done | contested |
| Stats: overfitting/look-ahead | 05-stats-and-ml/overfitting-lookahead.md | done | robust |
| Mean-variance / efficient frontier | 06-portfolio-construction/mean-variance-efficient-frontier.md | done | robust |
| Risk parity / Kelly sizing | 06-portfolio-construction/risk-parity-kelly-sizing.md | done | robust |
| Black–Litterman (reverse optimization + Bayesian views blend) | 06-portfolio-construction/black-litterman.md | done | robust |
| Factor portfolios & smart beta (construction, long–short vs ETF gap, capacity/costs) | 06-portfolio-construction/factor-portfolios-smart-beta.md | done | contested |
| VaR / CVaR | 07-risk-management/var-cvar.md | done | robust |
|| Drawdown / position sizing / stops | 07-risk-management/drawdown-position-sizing-stops.md | done | contested |
| Stress testing & scenario analysis | 07-risk-management/stress-testing-scenario-analysis.md | done | robust |
| Backtest: costs/slippage/walk-forward | 08-backtesting-methodology/transaction-costs-slippage-walkforward.md | done | robust |
| Deflated Sharpe / multiple-testing | 08-backtesting-methodology/deflated-sharpe-multiple-testing.md | done | robust |
| Microstructure: liquidity, spreads, execution, impact | 09-market-microstructure/liquidity-spreads-execution-impact.md | done | robust |
| Maker-taker, PFOF, HFT (pricing, routing, speed, contested net effect) | 09-market-microstructure/maker-taker-pfof-hft.md | done | contested |
||| Options greeks (delta/gamma/vega/theta, BS formulas, hedging) | 10-derivatives/option-greeks.md | done | robust |
||| Vol surface, skew, delta/gamma hedging, P&L decomposition | 10-derivatives/volatility-surface-skew-hedging.md | done | robust |
|| Option strategies (covered call, protective put, bull/bear spreads, collar, straddle, calendar) | 10-derivatives/option-strategies.md | done | robust |
|| Macro / regimes: rates, business cycle, sector rotation, regime detection | 11-macro-and-regimes/rates-business-cycles-sector-rotation.md | done | robust |
|| Regime detection methods (Markov-switching/HMM, structural breaks, heuristics) | 11-macro-and-regimes/regime-detection-methods.md | done | contested |
| Inflation, yields & equity valuation (discount-rate/equity-duration channels, Fed-model critique, inflation-illusion) | 11-macro-and-regimes/inflation-yields-equity-valuation.md | done | contested |
| Behavioral: biases, sentiment, crowding | 12-behavioral-finance/cognitive-biases-sentiment-crowding.md | done | robust |
| Herding, overconfidence, loss aversion (prospect theory deep dive) | 12-behavioral-finance/herding-overconfidence-loss-aversion.md | done | contested |
| Limits to arbitrage (Shleifer–Vishny; noise-trader risk; agency/performance capital; empirical exhibits) | 12-behavioral-finance/limits-to-arbitrage.md | done | contested |
| Data & tooling (vendors, libraries, reproducibility) | 13-data-and-tooling/data-vendors-apis-libraries-reproducibility.md | done | robust |
| Data & tooling (hygiene / survivorship-free datasets) | 13-data-and-tooling/data-hygiene-survivorship-free.md | done | robust |
| Data & tooling (backtesting libraries cookbook) | 13-data-and-tooling/backtesting-libraries-cookbook.md | done | robust |
|| Value & quality factor strategies (evidence + failure modes) | 14-strategy-catalog/value-quality-strategies.md | done | robust |
||| Momentum & trend-following strategies (cross-sectional + TSM; evidence, costs, crashes) | 14-strategy-catalog/momentum-trend-following-strategies.md | done | contested |
|||| Mean-reversion & statistical-arbitrage strategies (OU/s-score, variance-ratio, Avellaneda–Lee, Aug-2007) | 14-strategy-catalog/mean-reversion-stat-arb.md | done | contested |
|| Carry & volatility (short-tail-risk) strategies (cross-asset carry + VRP, evidence, failure modes) | 14-strategy-catalog/carry-volatility-strategies.md | done | contested |
|| Data snooping & p-hacking | 15-pitfalls-and-antipatterns/data-snooping-phacking.md | done | robust |
|| Overfitting & curve fitting (bias-variance, selection bias, DSR/PBO/MCS) | 15-pitfalls-and-antipatterns/overfitting-curve-fitting.md | done | robust |
|| Survivorship bias | 15-pitfalls-and-antipatterns/... | todo | — |

## Health check
- Coverage: 53/61 nodes done (overfitting-curve-fitting added; folder 15 now has 2 articles).
- PHASE A breadth: ALL folders 00–15 now have >=1 first article. Breadth complete.
- Next up (Phase B depth): 15 regime/look-ahead/txn-cost/survivorship (4 items).
- Open Phase B items: 15 (4) = 4 remaining. Open Verify tasks carried forward (not asserted).
- DONE when every folder 00-15 has >=1 article AND all Phase A/B items done AND no open Verify tasks.
