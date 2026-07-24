# Backlog — Stock Market Analysis Knowledge Base

## Priority Legend
- **P0** — Foundational / must-have for every folder
- **P1** — Core methodology / widely used in practice
- **P2** — Niche / advanced / SMC-ICT / vendor cookbooks / failure-mode depth

---

## 00-foundations
- [x] 00-foundations/math-review.md — Linear algebra / probability / stats refresher for quants (P0) — DONE
- [ ] 00-foundations/python-env.md — Reproducible env, venv, requirements.lock, reproducibility (P0)
- [ ] 00-foundations/ethics-regulatory.md — SEC/FINRA rules, insider trading, Reg BI, MiFID II overview (P1)
- [x] 00-foundations/market-structure.md — Market structure, order types, participants (P0) — DONE
- [x] 00-foundations/equity-claim.md — What is a stock, equity claim, capital structure (P0) — DONE
- [x] 00-foundations/exchanges-ats-regnms.md — Exchanges, ATS, dark pools, Reg NMS (P1) — DONE

## 01-fundamental-analysis
- [ ] 01-fundamental-analysis/financial-statements.md — Reading 10-K/10-Q, BS/IS/CF, MD&A, footnotes (P0)
- [ ] 01-fundamental-analysis/ratio-analysis.md — Profitability, liquidity, leverage, efficiency, DuPont (P0)
- [ ] 01-fundamental-analysis/earnings-quality.md — Accruals, cash conversion, red flags, Beneish M-score (P1)
- [ ] 01-fundamental-analysis/guidance-revisions.md — Guidance, estimate revisions, post-earnings drift (P1)
- [ ] 01-fundamental-analysis/industry-analysis.md — Porter, lifecycle, comps, KPIs by sector (P1)
- [ ] 01-fundamental-analysis/forensic-accounting.md — Aggressive accounting, revenue recognition, off-BS (P2)
- [ ] 01-fundamental-analysis/management-quality.md — Capital allocation, insider ownership, governance (P2)
- [ ] 01-fundamental-analysis/esg-fundamentals.md — ESG integration, SASB/TCFD, data quality caveats (P2)

## 02-valuation
- [ ] 02-valuation/dcf-fundamentals.md — FCFF/FCFE, WACC, terminal value, sensitivity (P0)
- [ ] 02-valuation/relative-valuation.md — Multiples (P/E, EV/EBITDA, P/B), comps, harmonic mean (P0)
- [ ] 02-valuation/ddm-residual-income.md — DDM variants, residual income, EVA (P1)
- [ ] 02-valuation/sum-of-parts.md — SOTP, conglomerate discount, holdco structures (P1)
- [ ] 02-valuation/valuation-pitfalls.md — Terminal value traps, circularity, terminal growth > GDP (P1)
- [ ] 02-valuation/real-options.md — Real options, growth options, abandonment (P2)
- [ ] 02-valuation/startup-valuation.md — VC method, scorecard, Berkus, cap tables (P2)
- [ ] 02-valuation/esg-adjustments.md — ESG premium/discount, climate transition risk (P2)

## 03-technical-analysis
- [ ] 03-technical-analysis/chart-types.md — OHLC, candlesticks, Heikin-Ashi, Renko, Kagi (P0)
- [ ] 03-technical-analysis/trend-structure.md — Dow theory, HH/HL/LH/LL, trend lines, channels (P0)
- [ ] 03-technical-analysis/support-resistance.md — Horizontal S/R, psychological levels, pivot points (P0)
- [ ] 03-technical-analysis/moving-averages.md — SMA/EMA/WMA, ribbons, crossovers, MACD (P0)
- [ ] 03-technical-analysis/momentum-oscillators.md — RSI, Stoch, CCI, Williams %R, divergences (P0)
- [ ] 03-technical-analysis/volume-analysis.md — OBV, VWAP, VPVR, accumulation/distribution (P1)
- [ ] 03-technical-analysis/volatility-indicators.md — ATR, Bollinger, Keltner, Donchian, standard error (P1)
- [ ] 03-technical-analysis/market-breadth.md — Advance-decline, McClellan, new highs/lows, TRIN (P1)
- [ ] 03-technical-analysis/intermarket.md — Intermarket ratios, yield curve, copper/gold, USD index (P2)
- [ ] 03-technical-analysis/elliott-wave.md — EW basics, fractals, rules, criticisms (P2)
- [ ] 03-technical-analysis/harmonic-patterns.md — Gartley, Butterfly, Bat, Crab, AB=CD (P2)
- [ ] 03-technical-analysis/smc-market-structure.md — **SMC/ICT Market Structure: swing highs/lows, BOS, CHoCH, market structure shifts (MSS)** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/smc-liquidity.md — **SMC/ICT Liquidity: buy-side/sell-side liquidity, liquidity pools, inducement, stop hunts, ICT liquidity voids, displacement** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/smc-order-blocks.md — **SMC/ICT Order Blocks: bullish/bearish OB, breaker blocks, rejection blocks, mitigation, ICT premium/discount arrays** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/smc-fvg.md — **SMC/ICT Fair Value Gaps: FVG, IFVG, balanced price range, ICT consequent encroachment** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/smc-entries.md — **SMC/ICT Entry Strategies: OB entries, FVG entries, liquidity sweep + OB/FVG confluence, session-based entries London/NY kill zones, ICT silver bullet, ICT turtle soup** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/smc-exits.md — **SMC/ICT Exit Strategies: opposing liquidity targets, partial TP 1:1/1:2/1:3, trail behind structure, time-based exits session close, ICT optimal trade entry OTE** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/smc-risk.md — **SMC/ICT Risk Management: ATR/vol position sizing, max daily DD, correlation limits, R-multiple journaling, ICT min 1:2 R:R** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/smc-mtf.md — **SMC/ICT Multi-Timeframe: HTF bias + LTF entry, 4H/1H/15M alignment, fractal structure, ICT weekly/daily/4H bias** (P2 - SMC/ICT)
- [ ] 03-technical-analysis/ict-specific.md — **ICT Specific: Judas swing, MMM buy/sell models, weekly/daily profile, Asian range, London open, NY open, PD arrays, algorithm matrix, IPDA** (P2 - SMC/ICT)

## 04-quant-and-factors
- [ ] 04-quant-and-factors/factor-zoo.md — Value, momentum, quality, low vol, size, investment, profitability (P0)
- [ ] 04-quant-and-factors/factor-construction.md — Long/short, rank vs z-score, sector neutralization, turnover control (P0)
- [ ] 04-quant-and-factors/factor-timing.md — Factor timing: business cycle, valuation spread, momentum crashes (P1)
- [ ] 04-quant-and-factors/multi-factor-models.md — Combining factors, PCA, risk models, Barra-style (P1)
- [ ] 04-quant-and-factors/alpha-decay.md — Alpha half-life, information coefficient decay, capacity (P1)
- [ ] 04-quant-and-factors/alternative-data.md — Alt data types, licensing, survivorship, feature engineering (P2)
- [ ] 04-quant-and-factors/ml-factor-discovery.md — ML for alpha: trees, NN, feature selection, purged CV (P2)
- [ ] 04-quant-and-factors/transaction-cost-models.md — Linear, square-root, Almgren-Chriss, market impact (P1)
- [ ] 04-quant-and-factors/signal-to-portfolio.md — Optimization, risk budgeting, turnover constraints (P1)

## 05-stats-and-ml
- [ ] 05-stats-and-ml/timeseries-basics.md — Stationarity, unit roots, cointegration, ARIMA, GARCH (P0)
- [ ] 05-stats-and-ml/regression-pitfalls.md — Spurious regression, heteroskedasticity, serial correlation, Newey-West (P0)
- [ ] 05-stats-and-ml/cross-validation.md — Purged/embargoed CV, walk-forward, CPCV, combinatorial CV (P1)
- [ ] 05-stats-and-ml/feature-engineering.md — Lags, rolling stats, interactions, target encoding, leakage guards (P1)
- [ ] 05-stats-and-ml/model-selection.md — Regularization, ensembles, stacking, calibration, model cards (P1)
- [ ] 05-stats-and-ml/probabilistic-forecasting.md — Quantile regression, conformal prediction, prediction intervals (P2)
- [ ] 05-stats-and-ml/causal-inference.md — Diff-in-diff, IV, synthetic control, causal ML in finance (P2)
- [ ] 05-stats-and-ml/deep-learning.md — LSTM/Transformer for returns, attention, positional encoding (P2)

## 06-portfolio-construction
- [x] 06-portfolio-construction/mean-variance-efficient-frontier.md — MVO, efficient frontier, constraints (P0) — DONE
- [x] 06-portfolio-construction/black-litterman.md — BL model, views, confidence, equilibrium (P1) — DONE
- [x] 06-portfolio-construction/factor-portfolios-smart-beta.md — Factor portfolios, smart beta, implementation (P1) — DONE
- [x] 06-portfolio-construction/risk-parity-kelly-sizing.md — Risk parity, Kelly, half-Kelly, fractional Kelly (P1) — DONE
- [ ] 06-portfolio-construction/hrp-hca.md — Hierarchical risk parity, hierarchical clustering (P1)
- [ ] 06-portfolio-construction/max-diversification.md — Max diversification, minimum correlation (P1)
- [ ] 06-portfolio-construction/dynamic-allocation.md — Regime-switching, volatility targeting, CPPI, TIPP (P1)
- [ ] 06-portfolio-construction/tax-aware.md — Tax-loss harvesting, asset location, transition management (P2)
- [ ] 06-portfolio-construction/esg-constraints.md — Exclusionary screens, tilt, impact, transition risk (P2)

## 07-risk-management
- [x] 07-risk-management/var-cvar.md — VaR, CVaR, historical/parametric/Monte Carlo (P0) — DONE
- [x] 07-risk-management/drawdown-position-sizing-stops.md — Max DD, position sizing, stop types (P0) — DONE
- [x] 07-risk-management/stress-testing-scenario-analysis.md — Historical, hypothetical, factor stress, climate (P1) — DONE
- [ ] 07-risk-management/tail-risk-hedging.md — Put spreads, VIX calls, tail risk funds, cost of carry (P1)
- [ ] 07-risk-management/liquidity-risk.md — Funding liquidity, market liquidity, redemption gates (P1)
- [ ] 07-risk-management/counterparty-operational.md — CCPs, bilateral, op risk, cyber, model risk (P2)
- [ ] 07-risk-management/risk-budgeting.md — Risk budgets, marginal/component risk, factor risk attribution (P1)

## 08-backtesting-methodology
- [x] 08-backtesting-methodology/deflated-sharpe-multiple-testing.md — Deflated Sharpe, multiple testing correction (P0) — DONE
- [x] 08-backtesting-methodology/transaction-costs-slippage-walkforward.md — TCA, slippage models, walk-forward (P0) — DONE
- [ ] 08-backtesting-methodology/backtest-framework.md — Vectorized vs event-driven, data structures, reproducibility (P0)
- [ ] 08-backtesting-methodology/look-ahead-survivorship.md — Look-ahead bias, survivorship, delisting bias, corporate actions (P0)
- [ ] 08-backtesting-methodology/out-of-sample-validation.md — IS/OOS, PBO, probability of backtest overfitting (P0)
- [ ] 08-backtesting-methodology/simulation-methods.md — Monte Carlo, bootstrap, block bootstrap, synthetic paths (P1)
- [ ] 08-backtesting-methodology/performance-attribution.md — Brinson, factor attribution, timing vs selection (P1)
- [ ] 08-backtesting-methodology/live-trading-transition.md — Paper trading, shadow book, latency, fill simulation (P2)

## 09-market-microstructure
- [x] 09-market-microstructure/liquidity-spreads-execution-impact.md — Spreads, impact models, execution (P0) — DONE
- [x] 09-market-microstructure/maker-taker-pfof-hft.md — Maker-taker, PFOF, HFT economics (P1) — DONE
- [ ] 09-market-microstructure/order-book-dynamics.md — LOB dynamics, queue position, order flow toxicity (P1)
- [ ] 09-market-microstructure/optimal-execution.md — Almgren-Chriss, TWAP/VWAP/POV, implementation shortfall (P1)
- [ ] 09-market-microstructure/high-frequency.md — Market making, adverse selection, latency, colocation (P2)
- [ ] 09-market-microstructure/dark-pool-dynamics.md — Dark pool segmentation, midpoint matching, block trading (P2)
- [ ] 09-market-microstructure/reg-nms-deep-dive.md — Reg NMS deep dive, rule 605/606 analysis, SIP latency (P2)
- [ ] 09-market-microstructure/microstructure-invariance.md — Invariance laws, volume-synchronized time, Kyle's lambda (P2)

## 10-derivatives
- [x] 10-derivatives/option-greeks.md — Greeks, second-order, greek management (P0) — DONE
- [x] 10-derivatives/option-strategies.md — Option strategies (P1) — DONE
- [x] 10-derivatives/volatility-surface-skew-hedging.md — Vol surface, skew, hedging (P1) — DONE
- [ ] 10-derivatives/exotic-options.md — Exotic options & structured products (P2)
- [ ] 10-derivatives/variance-swaps.md — Variance swaps & volatility trading (P2)
- [ ] 10-derivatives/ir-derivatives.md — Interest rate derivatives (swaps, swaptions) (P2)
- [ ] 10-derivatives/credit-derivatives.md — Credit derivatives (CDS, indices) (P2)
- [ ] 10-derivatives/commodity-fx-derivatives.md — Commodity & FX derivatives (P2)

## 11-macro-and-regimes
- [x] 11-macro-and-regimes/inflation-yields-equity-valuation.md — Inflation, yields & equity valuation (P0) — DONE
- [x] 11-macro-and-regimes/rates-business-cycles-sector-rotation.md — Rates, business cycles & sector rotation (P1) — DONE
- [x] 11-macro-and-regimes/regime-detection-methods.md — Regime detection methods (P1) — DONE
- [ ] 11-macro-and-regimes/fiscal-policy-debt.md — Fiscal policy & debt dynamics (P1)
- [ ] 11-macro-and-regimes/currency-regimes-carry.md — Currency regimes & carry (P1)
- [ ] 11-macro-and-regimes/commodity-cycles.md — Commodity cycles & inflation hedging (P2)
- [ ] 11-macro-and-regimes/central-bank-frameworks.md — Central bank policy frameworks (P2)
- [ ] 11-macro-and-regimes/global-liquidity.md — Global liquidity & cross-asset (P2)

## 12-behavioral-finance
- [x] 12-behavioral-finance/cognitive-biases-sentiment-crowding.md — Cognitive biases, sentiment & crowding (P0) — DONE
- [x] 12-behavioral-finance/herding-overconfidence-loss-aversion.md — Herding, overconfidence, loss aversion (P0) — DONE
- [x] 12-behavioral-finance/limits-to-arbitrage.md — Limits to arbitrage (P1) — DONE
- [ ] 12-behavioral-finance/behavioral-factors.md — Behavioral factor models (P1)
- [ ] 12-behavioral-finance/anomalies-behavioral.md — Market anomalies & behavioral explanations (P1)
- [ ] 12-behavioral-finance/investor-flows-sentiment.md — Investor flows & sentiment indicators (P1)
- [ ] 12-behavioral-finance/neurofinance.md — Neurofinance & decision making (P2)
- [ ] 12-behavioral-finance/culture-microstructure.md — Culture & market microstructure (P2)

## 13-data-and-tooling
- [x] 13-data-and-tooling/data-hygiene-survivorship-free.md — Data hygiene & survivorship-free data (P0) — DONE
- [x] 13-data-and-tooling/backtesting-libraries-cookbook.md — Backtesting libraries cookbook (P1) — DONE
- [x] 13-data-and-tooling/data-vendors-apis-libraries-reproducibility.md — Data vendors, APIs, libraries, reproducibility (P1) — DONE
- [ ] 13-data-and-tooling/data-storage-versioning.md — Data storage & versioning (Delta Lake, Parquet) (P1)
- [ ] 13-data-and-tooling/feature-stores.md — Feature stores for finance (P2)
- [ ] 13-data-and-tooling/cloud-compute.md — Cloud compute for quant (Ray, Dask, Spark) (P2)
- [ ] 13-data-and-tooling/ci-cd-research.md — CI/CD for research pipelines (P2)
- [ ] 13-data-and-tooling/visualization-reporting.md — Visualization & reporting (Streamlit, Dash) (P2)

## 14-strategy-catalog
- [x] 14-strategy-catalog/value-quality-strategies.md — Value & quality strategies (P0) — DONE
- [x] 14-strategy-catalog/momentum-trend-following-strategies.md — Momentum & trend following (P1) — DONE
- [x] 14-strategy-catalog/mean-reversion-stat-arb.md — Mean reversion & stat arb (P1) — DONE
- [x] 14-strategy-catalog/carry-volatility-strategies.md — Carry & volatility strategies (P1) — DONE
- [x] 14-strategy-catalog/inner-circle-trader-ict.md — **Inner Circle Trader (ICT) Core Concepts** (P2 - SMC/ICT) — DONE
- [x] 14-strategy-catalog/ict-futures-commodities.md — **ICT Futures & Commodities** (P2 - SMC/ICT) — DONE
- [ ] 14-strategy-catalog/multi-strategy.md — Multi-strategy / ensemble (P1)
- [ ] 14-strategy-catalog/event-driven.md — Event-driven & special situations (P2)
- [ ] 14-strategy-catalog/global-macro.md — Global macro discretionary (P2)
- [ ] 14-strategy-catalog/hft-market-making.md — HFT / market making (P2)
- [ ] 14-strategy-catalog/options-vol-arb.md — Options volatility arbitrage (P2)
- [ ] 14-strategy-catalog/crypto-defi.md — Crypto/DeFi strategies (if in scope) (P2)

## 15-pitfalls-and-antipatterns
- [x] 15-pitfalls-and-antipatterns/data-snooping-phacking.md — Data snooping & p-hacking (P0) — DONE
- [x] 15-pitfalls-and-antipatterns/look-ahead-bias.md — Look-ahead bias (P0) — DONE
- [x] 15-pitfalls-and-antipatterns/overfitting-curve-fitting.md — Overfitting & curve fitting (P0) — DONE
- [x] 15-pitfalls-and-antipatterns/regime-change-non-stationarity.md — Regime change & non-stationarity (P1) — DONE
- [x] 15-pitfalls-and-antipatterns/transaction-cost-neglect.md — Transaction cost neglect (P0) — DONE
- [ ] 15-pitfalls-and-antipatterns/survivorship-delisting.md — Survivorship & delisting bias (P0)
- [ ] 15-pitfalls-and-antipatterns/selection-bias.md — Selection bias & cherry-picking (P0)
- [ ] 15-pitfalls-and-antipatterns/benchmark-misspec.md — Benchmark mis-specification (P1)
- [ ] 15-pitfalls-and-antipatterns/leverage-path-dependency.md — Leverage & path dependency (P1)
- [ ] 15-pitfalls-and-antipatterns/operational-execution.md — Operational & execution failures (P2)
- [ ] 15-pitfalls-and-antipatterns/model-risk.md — Model risk & validation failures (P2)
- [ ] 15-pitfalls-and-antipatterns/behavioral-traps-live.md — Behavioral traps in live trading (P2)

---

## Verification Tasks (append when a claim needs corroboration)
- [ ] Verify: SMC/ICT concept "Judas Swing" — is it documented in primary ICT sources or only secondary? (P2)
- [ ] Verify: Maker-taker net liquidity effect — SEC 2014 lit review vs post-2010 flash event analyses (P1)
- [ ] Verify: Reg NMS Rule 611 rescission proposal status — comments due Aug 17 2026, not yet adopted (P1)