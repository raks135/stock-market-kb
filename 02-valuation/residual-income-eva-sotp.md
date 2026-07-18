---
title: Residual Income Valuation, EVA, and Sum-of-the-Parts (SOTP)
topic_id: 02-valuation/residual-income-eva-sotp
tags: [valuation, residual-income, abnormal-earnings, EVA, economic-value-added, MVA, sum-of-the-parts, conglomerate-discount, clean-surplus, Ohlson]
last_updated: 2026-07-18
confidence: robust
sources: [S174, S175, S176, S177, S178, S179, S180, S181, S182, S183]
---

## TL;DR
- Residual income (RI, a.k.a. abnormal earnings) values equity as **current book value + the present value of future residual income**; it explicitly charges the cost of equity that GAAP net income ignores. It is mathematically equivalent to the dividend-discount model under the clean-surplus relation (Ohlson 1995).
- Economic Value Added (EVA) is the firm-level commercial implementation of the same idea: `EVA = NOPAT − WACC × Invested Capital = (ROIC − WACC) × Invested Capital`.
- Sum-of-the-Parts (SOTP) values a multi-segment/conglomerate by valuing each division on its own merits and summing — the basis for the well-documented **conglomerate discount** (diversified firms often trade 13–15% below their SOTP value).
- Empirical work (Penman & Sougiannis 1998) finds **lower valuation errors** from accrual/RI techniques than from DCF or dividend discounting over finite horizons — but RI inherits all the accounting-dependence and terminal-value problems of any model.

## Core explanation

### Residual income (equity lens)
A company can report positive net income yet still destroy shareholder value if it earns **less than its cost of equity**. Net income charges the cost of *debt* (interest) but not the cost of *equity*. Residual income fixes that by subtracting an **equity charge**:

> Residual income = Net income − (cost of equity × beginning book value of equity)

Equivalently, in per-share / ROE form:

> RI_t = (ROE_t − r) × B_{t−1}

So RI is positive only when the firm's ROE exceeds the required return on equity. The intrinsic value of equity is then **today's book value plus the discounted stream of future RI** — current accounting already "pays" for the book, and RI captures the value added (or destroyed) on top.

### EVA (firm lens)
EVA is the same economic-profit concept applied at the *firm* level using operating (not equity) numbers:

> EVA = NOPAT − (WACC × Invested Capital) = (ROIC − WACC) × Invested Capital

Where RI is equity-focused (uses net income and the cost of equity), EVA is capital-structure-neutral (uses NOPAT and WACC). Both measure "profit after a full charge for *all* capital." Market Value Added (MVA) is the market's verdict: `MVA = Market Value of Equity + Debt − Invested Capital`, and in theory MVA ≈ present value of *future* EVA.

### Sum-of-the-parts (SOTP)
For a diversified holding company, conglomerate, or multi-division firm whose segments have different growth, risk, and capital-intensity profiles, a single consolidated multiple can misprice the whole. SOTP values each segment independently (DCF, RI, or the method best suited to that segment) and aggregates:

> Enterprise Value ≈ Σ (segment values) − net debt + non-operating asset adjustments
> Equity Value = EV − net debt (+/− other claims)

The gap between SOTP and the traded market cap is the **conglomerate discount** when negative (the usual case), or a **conglomerate premium** in rare cases (e.g., Berkshire Hathaway, which has historically traded above its SOTP).

## Math / formulas

**Clean-surplus relation** (required for RI ⇔ DDM equivalence):
```
B_t = B_{t-1} + NI_t − D_t
```
Book value only changes through earnings and dividends (no direct equity charges bypassing the income statement). Under clean surplus, the RI model and the dividend-discount model yield identical values (Ohlson 1995).

**General RI valuation (per share):**
```
V0 = B0 + Σ_{t=1}^{∞} RI_t / (1+r)^t
   = B0 + Σ_{t=1}^{∞} (E_t − r·B_{t-1}) / (1+r)^t
   = B0 + Σ_{t=1}^{∞} (ROE_t − r)·B_{t-1} / (1+r)^t
```

**Multistage with continuing value at horizon T:**
```
V0 = B0 + Σ_{t=1}^{T} RI_t/(1+r)^t + (P_T − B_T)/(1+r)^T
```
where `(P_T − B_T)` is the continuing (terminal) value expressed as the PV of post-horizon RI.

**Single-stage constant-growth RI (Gordon form):** if RI grows at a constant rate `g < r`,
```
V0 = B0 + RI_1 / (r − g)
```
and the **justified price-to-book** is
```
Justified P/B = V0 / B0 = 1 + PV(RI) / B0
```
so a firm earns a P/B above 1 precisely when ROE > r (i.e., it generates positive RI).

**Ohlson persistence (intuition):** residual income is not a random walk; empirically it decays toward zero (high ROE attracts competition). A common specification is `RI_{t+1} = ω·RI_t + ν_t` with persistence `0 ≤ ω < 1+r`. Higher `ω` ⇒ more value sits in the continuing-value term and a higher justified P/B — which is why "quality"/moat firms command premium multiples.

**EVA / MVA:**
```
EVA   = NOPAT − WACC·Invested Capital
MVA   = MV Equity + MV Debt − Invested Capital  ≈  PV(future EVA)
```

**SOTP:**
```
Equity Value ≈ Σ_i Value(Segment_i) − Net Debt + Non-op adjustments
```

## Worked example / code
Pure standard-library Python (no external dependencies). Figures are **synthetic and illustrative** — they demonstrate the arithmetic, not a market claim.

```python
# Residual income & EVA valuation — synthetic illustrative figures (no market data).
# Python 3.11+, standard library only.

# ---- 1) Single-stage constant-growth RI valuation ----
B0  = 20.0     # current book value per share ($)
roe = 0.15     # persistent ROE
r   = 0.12     # cost of equity
g   = 0.04     # book-value growth rate (payout keeps B growing at g, with g < r)

ri1 = (roe - r) * B0          # first-period residual income
cv  = ri1 / (r - g)          # continuing value of all future RI (Gordon form)
V0  = B0 + cv                # intrinsic value per share
justified_pb = V0 / B0
print(f"[RI single-stage] RI_1={ri1:.4f}  PV(RI)={cv:.4f}  V0={V0:.4f}  Justified P/B={justified_pb:.4f}")

# ---- 2) Multistage RI: 5y of ROE=15% (no payout), then ROE reverts to r (RI->0) ----
B = 20.0
r_hi = 0.12
roe_hi = 0.15
pv_ri = 0.0
for t in range(1, 6):
    ri = (roe_hi - r_hi) * B
    pv_ri += ri / (1 + r_hi) ** t
    B *= (1 + roe_hi)        # no dividends -> book grows at ROE
V0_ms = 20.0 + pv_ri
print(f"[RI multistage]  PV(RI)={pv_ri:.4f}  V0={V0_ms:.4f}")

# ---- 3) EVA on a project ----
nopat = 8_000_000.0          # $8m after-tax operating profit
invested_capital = 50_000_000.0
wacc = 0.08
eva = nopat - wacc * invested_capital
roic = nopat / invested_capital
print(f"[EVA] NOPAT=${nopat/1e6:.1f}m  IC=${invested_capital/1e6:.0f}m  WACC={wacc:.0%}  "
      f"ROIC={roic:.1%}  EVA=${eva/1e6:.1f}m  spread={roic-wacc:.1%}")

# ---- 4) SOTP skeleton ----
segments = {"Cloud": 1_200e6, "Industrial": 800e6, "Retail": 400e6}
net_debt = 300e6
sotp_ev = sum(segments.values())            # sum of segment enterprise values
sotp_equity = sotp_ev - net_debt
print(f"[SOTP] Segment EV sum=${sotp_ev/1e6:.0f}m  Net debt=${net_debt/1e6:.0f}m  "
      f"Equity value=${sotp_equity/1e6:.0f}m")
```

**Expected output (verified):**
```
[RI single-stage] RI_1=0.6000  PV(RI)=7.5000  V0=27.5000  Justified P/B=1.3750
[RI multistage]  PV(RI)=2.8260  V0=22.8260
[EVA] NOPAT=$8.0m  IC=$50m  WACC=8%  ROIC=16.0%  EVA=$4.0m  spread=8.0%
[SOTP] Segment EV sum=$2400m  Net debt=$300m  Equity value=$2100m
```
The single-stage example shows a justified P/B of 1.375 precisely because ROE (15%) > r (12%); the multistage example shows how value accrues mostly in the near-term RI when ROE reverts to the cost of equity; the EVA line shows $4m of true economic profit; the SOTP line aggregates three segments net of debt.

## Assumptions & limitations
- **Clean-surplus relation must hold** for RI ⇔ DDM equivalence. Real-world items (certain OCI entries, treasury-stock-method effects, direct equity charges) can violate it; practitioners apply adjustments.
- **Forecasts of book value, ROE, and the cost of equity** drive the answer. Garbage in, garbage out; RI is no more "objective" than DCF.
- **Terminal/continuing-value problem persists.** Like DCF, most of the value often sits in the continuing-value term; the `g < r` constraint bites (if RI is assumed to grow faster than the cost of equity forever, value explodes).
- **Accounting-dependence.** RI and EVA are only as good as the book values and earnings feeding them — they inherit all the quality-of-earnings and accrual risks covered in `01-fundamental-analysis/quality-of-earnings.md` (e.g., aggressive capitalization inflates book value and understates RI).
- **EVA adjustments.** Stern Stewart's commercial EVA applies ~100+ accounting adjustments (e.g., capitalizing R&D, adding back deferred tax, strategic-investment timing) to approximate economic book value and NOPAT. Ignoring them can make EVA misleading; applying them is labor-intensive.
- **SOTP double-counting / mismatch risk.** Segment values must use consistent claimholder treatment (EV vs equity), and corporate overhead, cross-segment guarantees, and net debt must be handled once. A single bad segment multiple propagates.
- **Non-stationarity & regime dependence.** Cost of equity, ROE, and segment multiples shift with the cycle; a SOTP/RI number is a point estimate, not a forecast.

## Empirical evidence
- **Penman & Sougiannis (1998), *Contemporary Accounting Research* 15(3):343–83** (primary, opened): comparing dividend-discount, DCF, and accrual/earnings (residual-income) approaches applied over finite horizons against ex-ante market prices, they find *"valuation errors are lower using accrual earnings techniques rather than cash flow and dividend discounting techniques."* Because the RI model anchors on current book value, truncation error at the forecast horizon is smaller than for DCF/DDM, which depend heavily on a distant terminal value. Multiple secondary reviews corroborate that RIM "outperforms" DCF and DDM on accuracy.
- **EVA ↔ MVA link:** a large body of applied work (Stewart 1991; subsequent empirical studies) finds a positive association between EVA and MVA for wealth-creating firms, weaker for firms with persistently negative EVA — i.e., the market eventually prices economic profit, but with noise and lag.
- **Conglomerate discount:** the SOTP-vs-market gap is a robust, repeatedly-documented stylized fact. Investopedia's reference synthesis puts the **sum-of-parts value above the conglomerate's market cap by roughly 13–15%** on average (single Tier-2 source for the exact magnitude — treat as indicative, see Verify note). The *existence* of a discount is independently corroborated by Wikipedia, Andersen, and practitioner M&A literature.

## Conflicting views
- **"RI is just DCF in disguise."** Technically true under clean surplus (Ohlson 1995) — they are algebraically equivalent. The *practical* disagreement is about which formulation is more robust to finite-horizon forecasting; Penman & Sougiannis argue accrual/RI wins on that operational ground, while DCF proponents note RI's heavy dependence on forecasted book values and accounting quality.
- **Is EVA worth the adjustment burden?** Proponents (Stern Stewart) argue the ~100+ adjustments make it the truest performance metric and align management with shareholders. Critics note the adjustments are arbitrary in places, the metric is backward-looking, and simple ROIC−WACC spreads capture most of the signal at far lower cost.
- **Conglomerate discount magnitude & cause.** The ~13–15% figure is a commonly cited average but varies widely by era, sector, and governance; some argue the "discount" is partly an artifact of using inappropriate pure-play comparables in the SOTP, not genuine value destruction. Berkshire-type premiums show the discount is not universal.

## Common mistakes
- **Forgetting the equity charge.** Treating positive net income as value creation; RI/EVA exist precisely to subtract the full cost of capital.
- **Assuming RI grows forever faster than r.** The `g < r` constraint is mandatory; otherwise continuing value diverges.
- **Mixing EV and equity in SOTP.** Valuing a segment on an equity multiple then forgetting to subtract net debt (or double-counting it) is the classic error.
- **Using unadjusted book value for RI/EVA** when accounting quality is poor — aggressive accruals inflate B0 and understate true RI (ties to `01-fundamental-analysis/quality-of-earnings.md`).
- **Reading SOTP as a price target.** SOTP is a *range* built on assumptions; the discount can persist for years and is not an arbitrageable "free money" signal (taxes, control premia, and break-up frictions apply).
- **Backtesting a "buy below SOTP" screen without point-in-time, delisting-inclusive data** — survivorship and look-ahead bias will inflate any apparent edge (see `13-data-and-tooling/...` and `15-pitfalls-and-antipatterns/...`).

## Further reading
- **(Tier 1)** CFA Institute, *Residual Income Valuation* (2026 L2 Equity Valuation refresher) — formulas, single/multistage, EVA/MVA, strengths/weaknesses. https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/residual-income-valuation
- **(Tier 1, primary)** Penman, S.H. & Sougiannis, T. (1998), "A Comparison of Dividend, Cash Flow, and Earnings Approaches to Equity Valuation," *Contemporary Accounting Research* 15(3):343–83. https://doi.org/10.1111/j.1911-3846.1998.tb00564.x
- **(Tier 1, primary)** Ohlson, J.A. (1995), "Earnings, Book Values, and Dividends in Equity Valuation," *Journal of Accounting Research* 11:661–87 — the clean-surplus / linear-information-dynamics foundation of the RI model.
- **(Tier 2)** Investopedia, "Economic Value Added (EVA)." https://www.investopedia.com/terms/e/eva.asp
- **(Tier 2)** Investopedia, "Conglomerate Discount." https://www.investopedia.com/terms/c/conglomeratediscount.asp
- **(Tier 2)** Wikipedia, "Sum-of-the-parts analysis." https://en.wikipedia.org/wiki/Sum-of-the-parts_analysis
- **(Tier 2)** Wall Street Prep, "Economic Value Added (EVA)." https://www.wallstreetprep.com/knowledge/economic-value-added-eva
- **(Tier 2)** Andersen, "Sum-of-the-Parts: The Key to Valuing Conglomerates Accurately." https://eg.andersen.com/sum-of-the-parts-valuation
- **(Tier 2)** AnalystPrep, "Residual Income Model" (CFA L2). https://analystprep.com/study-notes/cfa-level-2/residual-income-model
- **(Tier 2)** AnalystNotes, "The Residual Income Valuation Model" (CFA L2). https://analystnotes.com/cfa-study-notes-the-residual-income-valuation-model.html
- Companion KB articles: `02-valuation/dcf.md`, `02-valuation/relative-valuation.md`, `01-fundamental-analysis/quality-of-earnings.md`, `01-fundamental-analysis/dupont-analysis.md` (ROE decomposition feeds RI).
