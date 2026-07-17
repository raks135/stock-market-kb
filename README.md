# Stock Market Analysis — Knowledge Base

> **Disclaimer:** This is educational knowledge curation, **not** personalized financial advice. Nothing here is a recommendation to buy or sell any security. Backtests are not predictions of future returns. Do your own research.

A version-controlled, source-cited knowledge base covering the full landscape of stock-market analysis:
fundamental, technical, quantitative, risk, portfolio, microstructure, and the **traps** that make most of it fail.

Every non-obvious claim cites ≥2 independent, credible sources (see `STATE/sources.md`).
Three-bucket labeling is used throughout: **robust** · **emerging/unproven** · **folklore/marketing**.

## How to navigate
Each folder is a topic area. Start with `00-foundations` and `15-pitfalls-and-antipatterns`.

| # | Area |
|---|---|
| 00 | Foundations (markets, instruments, order types, participants) |
| 01 | Fundamental analysis |
| 02 | Valuation (DCF, comps, residual income) |
| 03 | Technical analysis |
| 04 | Quant & factors (CAPM, Fama–French, momentum, quality, low-vol) |
| 05 | Stats & ML (stationarity, cointegration, overfitting, look-ahead) |
| 06 | Portfolio construction (MPT, risk parity, Kelly, Black–Litterman) |
| 07 | Risk management (VaR/CVaR, drawdown, sizing) |
| 08 | Backtesting methodology (costs, slippage, walk-forward, deflated Sharpe) |
| 09 | Market microstructure (liquidity, spreads, execution, impact) |
| 10 | Derivatives (greeks, vol surface, hedging) |
| 11 | Macro & regimes |
| 12 | Behavioral finance |
| 13 | Data & tooling (vendors, APIs, libraries, reproducibility) |
| 14 | Strategy catalog (evidence + failure modes) |
| 15 | Pitfalls & antipatterns (the bulletproofing chapter) |

## Article template
Every file follows `STATE`/… the template in the spec: TL;DR, core, math, worked code, assumptions, empirical evidence, conflicting views, common mistakes, further reading.

## Agent state
`STATE/` holds the backlog, progress map, source registry, and per-iteration log.
