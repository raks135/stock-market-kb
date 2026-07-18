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
| Risk parity / Kelly | 06-portfolio-construction/... | todo | — |
| Black–Litterman | 06-portfolio-construction/... | todo | — |
| VaR / CVaR | 07-risk-management/var-cvar.md | done | robust |
| Drawdown / sizing | 07-risk-management/... | todo | — |
| Backtest: costs/slippage/walk-forward | 08-backtesting-methodology/transaction-costs-slippage-walkforward.md | done | robust |
| Deflated Sharpe / multiple-testing | 08-backtesting-methodology/deflated-sharpe-multiple-testing.md | done | robust |
| Microstructure: liquidity, spreads, execution, impact | 09-market-microstructure/liquidity-spreads-execution-impact.md | done | robust |
|| Options greeks (delta/gamma/vega/theta/rho, BS formulas, hedging) | 10-derivatives/option-greeks.md | done | robust |
| Macro / regimes: rates, business cycle, sector rotation, regime detection | 11-macro-and-regimes/rates-business-cycles-sector-rotation.md | done | robust |
| Behavioral: biases, sentiment, crowding | 12-behavioral-finance/cognitive-biases-sentiment-crowding.md | done | robust |
| Data & tooling (vendors, libraries, reproducibility) | 13-data-and-tooling/data-vendors-apis-libraries-reproducibility.md | done | robust |
| Data & tooling (hygiene / survivorship-free datasets) | 13-data-and-tooling/... | todo | — |
| Value & quality factor strategies (evidence + failure modes) | 14-strategy-catalog/value-quality-strategies.md | done | robust |
| Data snooping & p-hacking | 15-pitfalls-and-antipatterns/data-snooping-phacking.md | done | robust |
| Survivorship bias | 15-pitfalls-and-antipatterns/... | todo | — |

## Health check
- Coverage: 35/61 nodes done.
- PHASE A breadth: ALL folders 00–15 now have >=1 first article. Breadth complete.
- Next up: 06 risk-parity/Kelly/Black–Litterman/smart-beta; 07 drawdown/position-sizing/stress; 09 maker-taker/HFT; 10 vol-surface/option-strategies; 11 regime-detection/inflation; 12 herding/limits-to-arbitrage; 13 hygiene/backtesting-cookbook; 14 momentum/mean-reversion/carry-vol; 15 overfitting/regime/look-ahead/txn-cost/survivorship.
- P0 gaps: 15 survivorship still open (Phase A/B). All other P0 (00,01,02,05,07,08) sourced.
- DONE when every folder 00-15 has >=1 article AND all Phase A/B items done AND no open Verify tasks.
