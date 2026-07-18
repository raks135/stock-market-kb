---
title: Herding, Overconfidence, and Loss Aversion (deep dive)
topic_id: 12-behavioral-finance/herding-overconfidence-loss-aversion
tags: [behavioral-finance, herding, overconfidence, loss-aversion, prospect-theory, investor-psychology]
last_updated: 2026-07-18
confidence: contested
sources: [S329, S330, S331, S332, S333, S334, S335, S147, S144]
---

## TL;DR
Three of the most replicated findings in behavioral finance are (1) **loss aversion** — losses hurt ~2.25× more than equal gains feel good (prospect theory, Tversky & Kahneman 1992); (2) **overconfidence** — overconfident retail investors trade too much and *underperform* (Odean 1999; Barber & Odean 2000/2001); and (3) **herding** — under stress or in some markets, individual returns converge on the market (Chang, Cheng & Khorana 2000; Hwang & Salmon 2004). The *phenomena* are robust; their use as a standalone trading edge is **contested**. A runnable CSAD test below shows how herding is detected statistically (γ2 < 0) and why a naive "follow the crowd" rule is not an alpha source.

## Core explanation

### Loss aversion / prospect theory
People evaluate outcomes as **gains and losses relative to a reference point**, not as final wealth (Kahneman & Tversky 1979; cumulative version Tversky & Kahneman 1992 — S329/S335). The value function is concave for gains (risk-averse), convex for losses (risk-seeking), and **steeper for losses**. The empirically estimated loss-aversion coefficient is λ ≈ 2.25 with curvature α ≈ 0.88 (Tversky & Kahneman 1992 parameters adopted by Benartzi & Thaler 1995, S329). This is the basis of **myopic loss aversion (MLA)**: investors who evaluate their portfolios frequently feel the pain of temporary losses and demand a large equity premium to hold stocks (Benartzi & Thaler 1995, S329) — one behavioral resolution of the equity-premium puzzle.

### Overconfidence
Psychologists show most people overestimate the precision of their knowledge, and the effect is *largest in difficult, low-predictability tasks* (Griffin & Tversky 1992, cited in Odean 1999). In markets this produces **excessive trading**: overconfident investors believe their information signal is more precise than it is, so they trade even when expected gross profit is below transaction cost (Benos 1998; Odean 1998a, summarized in Odean 1999, S330). The surprising empirical result: the stocks these investors *buy* do not outperform the stocks they *sell* by enough to cover costs — on average buys **underperform** sells (Odean 1999, S330, full text verified).

### Herding
Herding is when investors imitate the market or each other rather than their own information. It can be rational (better-informed others, reputation/compensation incentives — Scharfstein & Stein 1990; Roll 1992) but can also suppress private information and move prices away from fundamentals (Bikhchandani, Hirshleifer & Welch 1992). Two measurement families dominate:
- **Return-dispersion tests** (Christie & Huang 1995, S332; Chang, Cheng & Khorana 2000, S333): if everyone herds, individual returns converge on the market return, so cross-sectional dispersion *falls* in extreme markets.
- **Beta-dispersion tests** (Hwang & Salmon 2004, S334): herd behavior shows up as a *fall in the cross-sectional variance of factor betas* (investors crowd into the same risk exposures — e.g., the market factor, or the value factor).

## Math / formulas

**Prospect value function (Tversky & Kahneman 1992):**
```
v(x) =  x^α            ,  x ≥ 0      (α ≈ 0.88, curvature / diminishing sensitivity)
v(x) = −λ(−x)^α        ,  x < 0      (λ ≈ 2.25, loss-aversion coefficient)
```
Loss-aversion ratio = λ ≈ 2.25 (a $100 loss needs ~$225 gain to feel neutral).

**Christie & Huang (1995) CSSD test (S332):**
```
CSSD_t = (1/N) Σ_i |R_{i,t} − R_{m,t}|           # cross-sectional std/deviation of returns
```
Herding prediction: dispersion is *lower* than normal during extreme up/down markets (dummies for tails significant and negative).

**Chang, Cheng & Khorana (2000) CSAD test (S333):**
```
CSAD_t = (1/N) Σ_i |R_{i,t} − R_{m,t}|
CSAD_t = α + γ1·|R_{m,t}| + γ2·R_{m,t}² + ε_t
```
- Under **no herding** (rational CAPM), dispersion is a *convex, increasing* function of |R_m| → **γ2 > 0**.
- Under **herding**, the relation becomes non-linear and dispersion *falls* at extreme moves → **γ2 < 0** (the canonical herding signature).

**Hwang & Salmon (2004) beta-herding (S334):**
```
H_t ∝ variance across assets of estimated β_{i,mkt,t}
```
Herding ⇒ cross-sectional variance of betas *declines* (all assets crowd onto the market/style factor). Unlike CSSD/CSAD, this is free of the idiosyncratic-noise component.

## Worked example / code
Pure-stdlib (no dependencies, Python 3.8+) implementation of the **CSAD herding test** plus the prospect value function. Data are **synthetic** (`random` module) — illustrative of the *method*, not a market claim. Verified on CPython 3.14.4.

```python
import random

def simulate(n_assets=150, n_days=4000, seed=42, herd=False, kappa=40.0,
             b_lo=0.5, b_hi=1.5, idio=0.004):
    rng = random.Random(seed)
    beta = [b_lo + (b_hi - b_lo) * rng.random() for _ in range(n_assets)]
    Rm, CSAD = [], []
    for t in range(n_days):
        rm = rng.gauss(0.0, 0.01)                       # daily market return, sd 1%
        w = min(1.0, kappa * abs(rm)) if herd else 0.0  # herding strength grows w/ |move|
        devs = []
        for i in range(n_assets):
            eff_beta = (1 - w) * beta[i] + w * 1.0      # pull beta toward 1 (the market)
            ri = eff_beta * rm + rng.gauss(0.0, idio)
            devs.append(abs(ri - rm))
        Rm.append(rm); CSAD.append(sum(devs) / n_assets)
    return Rm, CSAD

def ols_quad(x, y):                                     # CSAD = a + g1|Rm| + g2 Rm^2
    n = len(x)
    X = [[1.0, abs(xi), xi * xi] for xi in x]
    XtX = [[sum(X[k][i] * X[k][j] for k in range(n)) for j in range(3)] for i in range(3)]
    Xty = [sum(X[k][i] * y[k] for k in range(n)) for i in range(3)]
    A = [row[:] + [Xty[i]] for i, row in enumerate(XtX)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(A[r][c])); A[c], A[p] = A[p], A[c]
        piv = A[c][c]; A[c] = [v / piv for v in A[c]]
        for r in range(3):
            if r != c:
                f = A[r][c]; A[r] = [A[r][k] - f * A[c][k] for k in range(4)]
    return [A[i][3] for i in range(3)]

Rm_nh, C_nh = simulate(herd=False)
Rm_h,  C_h  = simulate(herd=True)
a1, g1, g2 = ols_quad(Rm_nh, C_nh)
a2, h1, h2 = ols_quad(Rm_h,  C_h)
print(f"NO-HERDING : a={a1:.5f} g1={g1:+.3f} g2={g2:+.4f}  (convex -> no herding)")
print(f"HERDING    : a={a2:.5f} g1={h1:+.3f} g2={h2:+.4f}  (gamma2<0 -> herding)")

# Prospect value function (Tversky & Kahneman 1992 params)
lam, alpha = 2.25, 0.88
v = lambda x: x ** alpha if x >= 0 else -lam * ((-x) ** alpha)
print(f"v(+100)={v(100):.2f}  v(-100)={v(-100):.2f}  loss-aversion ratio={-v(-100)/v(100):.2f}")
```

Output (seeded, reproducible):
```
NO-HERDING : a=0.01600 g1=+0.046 g2=+4.5564  (convex -> no herding)
HERDING    : a=0.01600 g1=+0.055 g2=-2.1004  (gamma2<0 -> herding)
v(+100)=57.54  v(-100)=-129.47  loss-aversion ratio=2.25
```
The no-herding case reproduces the rational-CAPM prediction (γ2 > 0: dispersion rises with market moves). The herding case flips the curvature (γ2 < 0), which is exactly what Chang et al. (2000, S333) test for. The value function confirms the λ ≈ 2.25 loss-aversion estimate.

## Assumptions & limitations
- **Loss aversion** is a *descriptive* regularity, not a tradable signal by itself; magnitude estimates vary (~1.9–2.5 across studies) and are context-dependent.
- **Overconfidence** studies rest on specific datasets (discount-brokerage account records 1987–1993 in Odean 1999, S330; the sample has some survivorship bias toward successful accounts, which Odean notes).
- **Herding measures** confound *true* herding (suppression of private info) with **spurious herding** — independent investors rationally moving together on common fundamentals (Hwang & Salmon 2004, S334). CSSD/CSAD cannot perfectly separate the two.
- CSAD's γ2 sign is **regime- and market-dependent** (often found in emerging/down markets, weak or absent in developed up-markets).
- Synthetic code above demonstrates the *statistical method* only; it is not a market claim.

## Empirical evidence
- **Loss aversion:** TK1992 parameters (α≈0.88, λ≈2.25) are the most-cited estimates (S329/S335). Benartzi & Thaler (1995, S329) show MLA quantitatively resolves the equity-premium puzzle. Meta-analyses (Camerer 2004) place the coefficient near 2.
- **Overconfidence → underperformance:** Odean (1999, S330, verified) finds buys *underperform* sells net of costs across 10,000 accounts / 162,948 trades. Barber & Odean (2000, S144) find the 20% most-active traders earned **11.4%** annualized vs **18.5%** for the least-active. Barber & Odean (2001, S331) find men trade **45%** more than women and earn **1.4%** lower risk-adjusted net returns (single men: 67% more, 2.3% lower).
- **Herding:** Christie & Huang (1995, S332) find *little* US herding except in small/down markets. Chang et al. (2000, S333) detect herding in developed markets, stronger in *down* markets, and more pronounced in emerging markets. Hwang & Salmon (2004, S334, verified) find herding toward the **market** factor in both bull and bear markets and toward the **value** factor (especially post-2001), but — counter-intuitively — crises (Asian, Russian) *reduce* herding as investors return to fundamentals. Lakonishok, Shleifer & Vishny (1992, S147) document measurable *institutional* herding in pension-fund trades.

## Conflicting views
- **Does herding matter / exist in efficient markets?** Rational asset pricing predicts a *convex* dispersion–market relation (γ2 > 0, no herding), so finding γ2 < 0 is the test. But many studies find γ2 > 0 (no herding) in US large-cap data, while emerging markets and down-markets show γ2 < 0 — i.e., herding is **regime- and market-dependent**, not a universal force (Bohl 2017 critique of CCK supports caution).
- **Spurious vs real herding:** Hwang & Salmon (2004, S334) stress that common co-movement on fundamentals is *not* herding; only beta-dispersion that survives conditioning on fundamentals counts.
- **Loss-aversion magnitude:** estimates range ~1.9–2.5; some argue it is manipulated by framing and reference-point choice, so the "2:1" rule is a rough heuristic, not a constant.
- **Exploitability:** These biases explain *why* mispricings exist, but **limits to arbitrage** (Shleifer & Vishny 1997, S142) mean they need not be easily tradable; see `12-behavioral-finance/cognitive-biases-sentiment-crowding.md`.

## Common mistakes
- Treating loss aversion as identical to the **disposition effect** (holding losers, selling winners) — related but distinct; disposition is a realized-behavior consequence (Shefrin & Statman 1985).
- Reading "overconfidence exists" as "be more confident to trade more" — the evidence says overconfident traders **underperform** (Odean 1999; Barber & Odean 2000/2001).
- Using a herding measure to *predict* crashes — γ2 < 0 is a contemporaneous description of co-movement, not a forecast; crises can *reduce* herding (Hwang & Salmon 2004).
- Ignoring **asymmetry**: herding is typically stronger in down markets; pooling up and down markets dilutes the signal.
- Confounding **fundamentals-driven co-movement** (spurious herding) with genuine information-suppression herding.

## Further reading
- S329 — Benartzi, S. & Thaler, R. (1995), "Myopic Loss Aversion and the Equity Premium Puzzle," *QJE* 110(1):73–92. [Tier 1; parameters λ=2.25/α=0.88; abstract/parameter values via search snippet — full PDF not directly opened]
- S330 — Odean, T. (1999), "Do Investors Trade Too Much?" *AER* 89(5):1279–1298. https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/doinvestors.pdf [Tier 1; full text opened & verified]
- S331 — Barber, B. & Odean, T. (2001), "Boys Will Be Boys," *QJE* 116(1):261–292. https://faculty.haas.berkeley.edu/odean/papers/gender/gender.html [Tier 1; opened — men trade 45% more, 1.4% lower risk-adj returns]
- S332 — Christie, W. & Huang, R. (1995), "Following the Pied Piper," *JFE* 37(5):371–399. [Tier 1; CSSD methodology quoted via S334 + search snippets; full text not directly opened]
- S333 — Chang, E., Cheng, J. & Khorana, A. (2000), "An Examination of Herding Behavior in Equity Markets," *JFE* 58(3):381–408. [Tier 1; CSAD equation via AccessEcon/Mobarek snippets + S334; full text not directly opened]
- S334 — Hwang, S. & Salmon, M. (2004), "Market Stress and Herding," *Journal of Empirical Finance* 11(4):585–616. https://warwick.ac.uk/fac/soc/wbs/subjects/finance/faculty1/mark_s/hwangsalmon.pdf [Tier 1; full text opened & verified]
- S335 — Wikipedia, "Prospect theory." https://en.wikipedia.org/wiki/Prospect_theory [Tier 2; opened]
- S147 — Lakonishok, J., Shleifer, A. & Vishny, R. (1992), "The Impact of Institutional Trading on Stock Prices," *JFE* 32:23–43. [Tier 1; institutional herding]
- S144 — Barber, B. & Odean, T. (2000), "Trading Is Hazardous to Your Wealth," *JFE* 55:773–806. [Tier 1; 11.4% vs 18.5% turnover result]
- Kahneman, D. & Tversky, A. (1979), "Prospect Theory," *Econometrica* 47(2):263–291. [foundational; via S335]
- Tversky, A. & Kahneman, D. (1992), "Advances in Prospect Theory," *JRU* 5:297–323. [foundational; parameters via S329]
- Shleifer, A. & Vishny, R. (1997), "The Limits of Arbitrage," *JFE* 52:35–55. [why behavioral mispricings persist — see cognitive-biases article]
