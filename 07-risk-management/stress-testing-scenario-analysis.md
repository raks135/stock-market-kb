---
title: Stress Testing & Scenario Analysis
topic_id: 07-risk-management/stress-testing-scenario-analysis
tags: [risk-management, stress-testing, scenario-analysis, reverse-stress, sensitivity, CCAR, tail-risk]
last_updated: 2026-07-18
confidence: robust
sources: [S290, S291, S292, S293, S294, S295, S110]
---

## TL;DR
- Stress testing answers the question normal risk models leave open: *what happens when markets break?* It evaluates a portfolio under extreme, unlikely-but-plausible scenarios that fall outside the statistical frame of VaR/ES (S294, S295).
- Three scenario families are used in practice: **stylized** (predefined factor shocks, e.g. the Derivatives Policy Group's seven), **historical** (replay real past crises), and **hypothetical** (events that never happened) (S294, S295).
- **Reverse stress testing** — start from a failure outcome and work backward to the scenario that causes it — is now a regulatory expectation (PRA, SAMA) and consistently surfaces vulnerabilities forward tests miss (S293, S295).
- A stress loss is an *order-of-magnitude estimate, not a probability*. Its biggest failure modes are one-factor-at-a-time shocks (missing correlation spikes), static assumptions, model risk, and filing results without acting (S292, S295).

## Core explanation
Plain language: a stress test takes your portfolio and subjects it to a violent but plausible market event — a 2008-style crash, a 300bp emergency rate hike, a combined sovereign-default-and-liquidity-freeze — then computes how much you lose. VaR and Expected Shortfall summarize losses *within a modeled distribution*; stress tests deliberately step outside that distribution to probe the tails where the model's assumptions (normality, stable correlations, liquid markets) are most likely to fail (S294, S295).

Precise framing (CFA curriculum): risk measures split into **sensitivity measures** (beta, duration, convexity, option Greeks — the ∂V/∂factor response to a *small* move) and **scenario measures** (joint, large moves across several factors). Stress testing is the scenario-measure branch. Unlike sensitivity/VaR, scenario measures do **not** convey a likelihood of occurrence — they quantify impact conditional on the scenario happening (S294).

Key distinctions:
- **Sensitivity analysis** — one risk factor moved a small amount; isolates a single exposure.
- **Scenario analysis** — several factors move together, coherently (a narrative: recession + falling rates + widening credit + falling real estate).
- **Stress testing** — scenario analysis pushed to *extreme* negative outcomes (S292, S294). The BIS taxonomy explicitly includes sensitivity, scenario (including enterprise-wide), and reverse stress under "stress testing" (S292).

## Math / formulas
A factor-based stress loss for a portfolio of positions is:

```
P&L(scenario) = Σ_i  w_i · ( β_i^eq·Δequity + β_i^rate·(−Δy) + β_i^credit·(−Δs) + β_i^re·Δre )
```

where `w_i` = position value, `β` = sensitivity to each risk factor, `Δy` = yield change (prices rise when yields fall, hence the minus), `Δs` = credit-spread change (prices fall when spreads widen), all in consistent units (percent or basis points).

- **Sensitivity** is the linear/local limit: for a bond, `ΔP/P ≈ −D · Δy` (duration); for an option, the Greeks. Stress tests use the *full* (often non-linear) repricing, not just the first derivative.
- **Factor push**: push each factor to its most adverse plausible value, one at a time, and sum. Simple but misses cross-factor interaction (S295).
- **Maximum-loss optimization**: search the bounded region of factor moves for the worst portfolio outcome — accounts for interactions but is computationally heavy and bound-sensitive (S295).
- **Reverse stress**: solve for the scenario `Δf*` such that `P&L(Δf*) = −L_target` (the loss that breaks the firm). Often solved one factor at a time holding others at stress levels (S293, S295).

The BIS principles require stresses to be "sufficiently severe" to be meaningful and to capture material risks (Principle 4, S292).

## Worked example / code
A deterministic, pure-stdlib stress engine. The portfolio is **hypothetical** ($1,000m multi-asset book). Equity-shock magnitudes for the historical scenarios are taken from Ryan O'Connell's event-window table (S295: GFC 2007–09 S&P 500 −56.8%; COVID Feb–Mar 2020 −33.9%, 23 trading days). Companion rate/credit/real-estate shocks are **illustrative** for the engine demonstration and are clearly labeled as such; the Federal Reserve's 2025 supervisory severely-adverse scenario publishes real macro shocks (unemployment +5.9pp to 10%, house prices ≈ −33%, commercial real estate ≈ −30% — S291) and is discussed in the prose.

Data source: hypothetical portfolio + factor shocks from S291/S295. Pinned runtime: CPython 3.14.4 (no third-party libraries; fully reproducible).

```python
"""
Stress testing & scenario analysis — illustrative factor-based engine (pure stdlib).
Equity shocks sourced: S295 (GFC -56.8%, COVID -33.9%). Companion rate/credit/RE
shocks are ILLUSTRATIVE for the engine demo. Real Fed 2025 macro shocks: S291.
"""
PORTFOLIO = {
    "Global equities":    {"value": 550.0, "eq_beta": 1.00, "rate_dur": 0.0, "spread_dur": 0.0, "re_beta": 0.0},
    "IG corporate bonds": {"value": 250.0, "eq_beta": 0.25, "rate_dur": 6.0, "spread_dur": 7.0, "re_beta": 0.0},
    "REIT":               {"value": 100.0, "eq_beta": 0.80, "rate_dur": 3.0, "spread_dur": 3.0, "re_beta": 1.00},
    "Sovereign bonds":    {"value": 100.0, "eq_beta": 0.05, "rate_dur": 6.0, "spread_dur": 1.0, "re_beta": 0.0},
}

def position_pnl(pos, s):
    pnl  = pos["value"] * pos["eq_beta"]    * (s["equity_pct"] / 100.0)
    pnl += pos["value"] * pos["rate_dur"]   * (-s["rates_bps"] / 10000.0)   # prices ~ -D*dy
    pnl += pos["value"] * pos["spread_dur"] * (-s["credit_bps"] / 10000.0)  # spreads widen -> loss
    pnl += pos["value"] * pos["re_beta"]    * (s["re_pct"] / 100.0)
    return pnl

def portfolio_pnl(shock):
    return sum(position_pnl(p, shock) for p in PORTFOLIO.values())

# Historical equity numbers from S295; companion shocks illustrative.
SCENARIOS = {
    "GFC 2007-09 (equity -56.8%, S295)":      {"equity_pct": -56.8, "rates_bps": -200, "credit_bps": 600, "re_pct": -30.0},
    "COVID 2020 (equity -33.9%, S295)":       {"equity_pct": -33.9, "rates_bps": -150, "credit_bps": 350, "re_pct": -20.0},
}

if __name__ == "__main__":
    total = sum(p["value"] for p in PORTFOLIO.values())
    for name, shk in SCENARIOS.items():
        loss = portfolio_pnl(shk)
        print(f"{name:38s} P&L = ${loss:7.1f}m  ({loss/total*100:5.1f}% of ${total:.0f}m)")
    worst = min(portfolio_pnl(s) for s in SCENARIOS.values())
    limit = 0.25 * total                       # policy max drawdown = 25%
    print(f"Worst loss ${abs(worst):.1f}m vs limit ${limit:.1f}m -> "
          f"{'WITHIN LIMIT' if abs(worst) <= limit else 'BREACH'}")

    # --- Reverse stress: equity shock that produces a $250m (=-25%) loss,
    #     holding rates/credit/RE at GFC stress levels ---
    base = {"equity_pct": 0.0, "rates_bps": -200, "credit_bps": 600, "re_pct": -30.0}
    target = -250.0
    fixed   = sum(position_pnl(p, base) for p in PORTFOLIO.values())   # equity move = 0
    eq_exp  = sum(p["value"] * p["eq_beta"] for p in PORTFOLIO.values())
    x = (target - fixed) / eq_exp * 100.0
    print(f"Reverse stress: equity shock of {x:.1f}% (rates/credit/RE at GFC levels) -> ${target:.0f}m loss")
```

Expected output (verified on CPython 3.14.4):
```
GFC 2007-09 (equity -56.8%, S295)      P&L = $ -507.2m  ( -50.7% of $1000m)
COVID 2020 (equity -33.9%, S295)       P&L = $ -295.7m  ( -29.6% of $1000m)
Worst loss $507.2m vs limit $250.0m -> BREACH
Reverse stress: equity shock of -19.9% (rates/credit/RE at GFC levels) -> $250m loss
```
Interpretation: the book would breach its 25% drawdown limit in both historical crises, and — the reverse-stress insight — even a *moderate* ~−20% equity drop, once credit/rates/real-estate are already stressed, is enough to hit the limit. That is the kind of hidden vulnerability forward tests surface.

## Assumptions & limitations
- **Not a probability.** A stress loss has no attached likelihood; it answers "if X happens, we lose Y," never "X will happen with probability p" (S294). Mistaking it for a forecast is the most common misuse.
- **Scenario selection is judgment, not science.** Which events? How severe? There is no unique answer; different plausible scenarios give wildly different losses (S292, S295).
- **One-factor-at-a-time understates risk.** Stylized/DPG shocks and factor-push tests move factors singly; real crises move everything *together* with correlations spiking toward 1 (the LTCM 1998 lesson — S295).
- **Static portfolio assumption.** Tests usually freeze the book; in reality managers hedge, rebalance, or panic-sell, and margin calls create feedback loops (S295).
- **Model risk.** Pricing models (Black–Scholes, duration, multifactor) are calibrated to normal conditions and can be unreliable exactly when accuracy matters most (S292, S295).
- **Liquidity/funding gaps.** Even "liquid" assets can freeze (AAA private-label RMBS in 2008; the Fed explicitly warns markets' liquidity can change abruptly — S291 footnote 13). Pure price-shock stresses omit funding and fire-sale dynamics.
- **Backward-looking bias.** Historical scenarios assume the next crisis resembles the last; hypothetical scenarios try to fix this but are hard to design credibly (S295).

## Empirical evidence
- **Regulatory adoption is near-universal for large banks.** The Federal Reserve runs annual supervisory stress tests (CCAR/DFAST, now the stress capital buffer) on firms with ≥ $100bn assets, using a minimum of two scenarios (baseline + severely adverse), and the largest U.S. banking organizations have *more than doubled* aggregate common equity since 2009 in part due to this regime (S290).
- **Concrete supervisory severity (Fed 2025):** the severely-adverse scenario specifies unemployment rising 5.9pp to a 10% peak, ~33% house-price decline, ~30% commercial-real-estate decline, widening corporate spreads and a global market shock / counterparty-default component for trading firms (S291).
- **Historical scenarios are used because tail events have higher real probability than models imply**, and they capture the full complexity (correlation spikes, liquidity freezes, contagion) that theoretical models understate (S295). Representative event-window S&P 500 losses: Black Monday Oct 1987 −20.5% (1 day), LTCM/Russia 1998 −19.3%, GFC 2007–09 −56.8%, Euro-sovereign 2011 −19.4%, COVID 2020 −33.9% in 23 trading days (S295).
- The evidence base is largely **qualitative/regulatory** rather than a tradable "edge"; stress testing's value is resilience diagnosis and capital/sizing discipline, not return prediction.

## Conflicting views
- **"Essential complement to VaR" vs "false precision."** Practitioners (S295) and the BIS (S292) frame stress tests as indispensable because VaR/ES fail in tails; critics warn a single deterministic path can create false confidence and is gameable by banks optimizing to the published scenario.
- **Severity calibration.** How bad is "severe enough"? Too mild → useless; too extreme → ignored as unrealistic. The BIS mandates "sufficiently severe" but leaves calibration to judgment (S292).
- **Supervisory vs internal use.** Some argue supervisory stress tests are procyclical and mechanically distort capital; others credit them with materially hardening the banking system post-2009 (S290, S292).
- **Reverse stress as box-ticking vs strategic tool.** Regulators require it (PRA/SAMA, S293); skeptics say the backward construction is often contrived. The KB treats it as genuinely useful when taken seriously (S295).

## Common mistakes
1. **Treating the stress number as a probability or forecast.** It is conditional impact only (S294).
2. **Factor-push / DPG-style one-at-a-time shocks** that miss the correlation breakdown characteristic of real crises (S295).
3. **Filing the report without action** — the documented governance failure is running tests and not connecting them to limits/hedges (S292, S295).
4. **Assuming the portfolio is static** through the crisis; ignoring margin spirals and behavioral responses (S295).
5. **Only historical scenarios** — the next crisis will differ in detail (S295).
6. **Trusting normal-condition pricing models at extremes** (model risk) (S292).
7. **Omitting liquidity, funding, and contagion channels** — pure mark-to-market price shocks understate true stress (S291, S295).

## Further reading
- Federal Reserve, "Stress Tests" (CCAR/DFAST, stress capital buffer) — https://www.federalreserve.gov/supervisionreg/stress-tests-capital-planning.htm (S290, Tier 1)
- Federal Reserve, "2025 Stress Test Scenarios" (real macro shock magnitudes) — https://www.federalreserve.gov/publications/2025-stress-test-scenarios.htm (S291, Tier 1)
- Basel Committee on Banking Supervision, "Stress testing principles" (Oct 2018, d450) — https://www.bis.org/bcbs/publ/d450.pdf (S292, Tier 1)
- SAMA Rulebook, "Reverse Stress Testing" (5.4) — https://rulebook.sama.gov.sa/en/54-reverse-stress-testing (S293, Tier 1)
- AnalystPrep, "Use of Sensitivity and Scenario Risk Measures" (CFA L2, Reading 41) — https://analystprep.com/study-notes/cfa-level-2/describe-the-use-of-sensitivity-risk-measures-and-scenario-risk-measures (S294, Tier 2 / CFA curriculum)
- Ryan O'Connell, CFA FRM, "Stress Testing & Scenario Analysis" — https://ryanoconnellfinance.com/stress-testing-scenario-analysis (S295, Tier 2)
- Complements: `07-risk-management/var-cvar.md` (VaR/ES) and `07-risk-management/drawdown-position-sizing-stops.md` (drawdown limits) in this KB.
