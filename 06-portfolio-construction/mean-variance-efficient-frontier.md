---
title: Mean–Variance Optimization & the Efficient Frontier
topic_id: 06-portfolio-construction/mean-variance-efficient-frontier
tags: [portfolio-construction, markowitz, efficient-frontier, mean-variance, estimation-error, diversification, capm]
last_updated: 2026-07-18
confidence: robust
sources: [S103, S104, S105, S106, S107, S108, S109]
---

## TL;DR
- Mean–variance (Markowitz 1952) chooses portfolios by two numbers only: expected return (reward) and variance (risk). The best risky-only portfolios lie on the **efficient frontier** — the upper edge of the minimum-variance set [S103, S104, S105].
- With a risk-free asset, the efficient set becomes a straight **capital allocation line (CAL)**; its tangency point with the risky frontier is the unique **tangency (max-Sharpe) portfolio**, and every investor holds a mix of it and cash (one-fund separation) [S104].
- **The catch (robust, not folklore):** sample mean–variance is exquisitely sensitive to input estimates. DeMiguel, Garlappi & Uppal (2009) show that across 7 datasets and 14 models, none consistently beats the naive **1/N** rule out-of-sample, and you'd need ~3,000 months (25 assets) or ~6,000 months (50 assets) of history before MV reliably wins [S106, S107]. Plug-and-play MV is a myth.
- Practitioners respond with shrinkage/robust estimators, resampling, weight constraints, and Bayesian views (e.g., Black–Litterman — see the KB's separate article) [S108, S104].

## Core explanation
Mean–variance analysis (Markowitz 1952) is the founding framework of modern portfolio theory [S109]. An investor facing a set of risky assets evaluates any portfolio by just two moments of its return distribution:
- **Expected return** `E[R_p] = wᵀμ` — the reward.
- **Variance** `Var(R_p) = wᵀΣw` — the risk, where `w` is the weight vector, `μ` the expected-return vector, and `Σ` the covariance matrix.

The core behavioral assumption is **mean–variance preference**: for a given level of risk an investor wants the highest expected return, and for a given expected return the lowest risk [S103]. Plotting every feasible risky portfolio in (risk, return) space yields an **opportunity set** (a blob). Its left boundary is the **minimum-variance frontier**. The segment of that boundary whose expected return exceeds the **global minimum-variance (GMV) portfolio** is the **efficient frontier** — "efficient" meaning no other portfolio offers more return at the same risk or less risk at the same return [S103, S104, S105].

Adding a **risk-free asset** (return `r_f`) changes the geometry. Portfolios of the risk-free asset plus any risky portfolio lie on a straight line from `(0, r_f)` through that risky portfolio — the **capital allocation line (CAL)**. The CAL that is *tangent* to the risky efficient frontier dominates all others; the tangency point is the **tangency portfolio** (the portfolio of risky assets that maximizes the Sharpe ratio). By the **two-fund / one-fund separation theorem**, every investor's optimal portfolio is a combination of the risk-free asset and this single tangency portfolio [S104, S103].

## Math / formulas
**Portfolio moments** (fully invested: `wᵀ1 = 1`) [S104]:
```
E[R_p] = wᵀ μ
Var(R_p) = wᵀ Σ w
```

**No risk-free asset — minimum-variance frontier.** Solve the quadratic program
```
min_w ½ wᵀΣw   subject to   wᵀμ = p ,  wᵀ1 = 1
```
The **global minimum-variance portfolio** has closed form [S104]:
```
w_gmv = Σ⁻¹1 / (1ᵀΣ⁻¹1)
```
Its expected return is `A/C` and its variance `1/C`, where `C = 1ᵀΣ⁻¹1`.

**With a risk-free asset — tangency portfolio.** The unnormalized tangency weights are proportional to `Σ⁻¹(μ − r_f·1)`, then normalized to sum to 1 [S104]:
```
w_tan ∝ Σ⁻¹(μ − r_f 1)
```
The CAL (and, under CAPM, the **capital market line**) is the line through `(0, r_f)` with slope equal to the tangency portfolio's Sharpe ratio; the efficient frontier is therefore a straight line, not a hyperbola, once `r_f` is available [S104, S105].

**Two-fund theorem.** Any two efficient portfolios (e.g., GMV and tangency) span the *entire* efficient frontier: every efficient portfolio is a linear combination of them. This is the basis of the worked example below (combine GMV and tangency by a scalar `t`) [S104, S103].

**Closed form of the risky frontier.** Define `A = 1ᵀΣ⁻¹μ`, `B = μᵀΣ⁻¹μ`, `C = 1ᵀΣ⁻¹1`, `D = BC − A²`. Then for a target return `p`, the minimum variance is [S104]:
```
σ²_min(p) = (C·p² − 2A·p + B) / D
```
which describes the hyperbola (the "Markowitz bullet") in (σ, μ) space [S105].

## Worked example / code
Pure-stdlib demo (no numpy/scipy) computing the GMV portfolio, the tangency portfolio, and the efficient frontier by combining them. Saved as `_mv_demo.py` in this folder; output below is the actual run.

```python
# _mv_demo.py — Mean–variance efficient frontier (pure stdlib)
import math

def mat_inv(M):
    n = len(M)
    A = [M[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[piv][col]) < 1e-12:
            raise ValueError("matrix singular")
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0.0:
                f = A[r][col]
                A[r] = [A[r][k] - f * A[col][k] for k in range(2 * n)]
    return [row[n:] for row in A]

def mat_vec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]

def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))

# Illustrative annualized inputs (NOT real market data)
mu = [0.10, 0.12, 0.08]
Sigma = [[0.0400, 0.0060, 0.0050],
         [0.0060, 0.0300, 0.0040],
         [0.0050, 0.0040, 0.0200]]
rf = 0.03
n = len(mu); ones = [1.0] * n
Sinv = mat_inv(Sigma)

num = mat_vec(Sinv, ones); den = dot(ones, num)
w_gmv = [x / den for x in num]
excess = [mu[i] - rf * ones[i] for i in range(n)]
w_tan_raw = mat_vec(Sinv, excess); s = sum(w_tan_raw)
w_tan = [x / s for x in w_tan_raw]

ret = lambda w: dot(w, mu)
vol = lambda w: math.sqrt(dot(w, mat_vec(Sigma, w)))

print("GMV      w =", [round(x,4) for x in w_gmv], "ret =", round(ret(w_gmv),4), "vol =", round(vol(w_gmv),4))
print("Tangency w =", [round(x,4) for x in w_tan], "ret =", round(ret(w_tan),4),
      "vol =", round(vol(w_tan),4), "Sharpe =", round((ret(w_tan)-rf)/vol(w_tan),4))
print("Frontier (w = GMV + t*(TAN-GMV)), efficient for t>=0:")
for t in [0.0, 0.5, 1.0, 1.5, 2.0]:
    w = [w_gmv[i] + t*(w_tan[i]-w_gmv[i]) for i in range(n)]
    print(f" t={t:+.1f}  w={[round(x,3) for x in w]}  ret={ret(w):.4f}  vol={vol(w):.4f}  Sharpe={(ret(w)-rf)/vol(w):.4f}")
```

**Actual output (Python 3.14, stdlib only):**
```
GMV      w = [0.1977, 0.3009, 0.5014] ret = 0.096  vol = 0.1105
Tangency w = [0.214, 0.4707, 0.3153] ret = 0.1031 vol = 0.1164 Sharpe = 0.6283
Frontier (w = GMV + t*(TAN-GMV)), efficient for t>=0:
 t=+0.0  w=[0.198, 0.301, 0.501]  ret=0.0960  vol=0.1105  Sharpe=0.5970
 t=+0.5  w=[0.206, 0.386, 0.408]  ret=0.0995  vol=0.1120  Sharpe=0.6208
 t=+1.0  w=[0.214, 0.471, 0.315]  ret=0.1031  vol=0.1164  Sharpe=0.6283
 t=+1.5  w=[0.222, 0.556, 0.222]  ret=0.1067  vol=0.1232  Sharpe=0.6222
 t=+2.0  w=[0.23, 0.64, 0.129]  ret=0.1102  vol=0.1323  Sharpe=0.6066
```
The demo confirms the theory: GMV has the lowest volatility (0.1105); the tangency portfolio is the **max-Sharpe** point (Sharpe peaks at t=1.0, 0.6283); and moving beyond tangency (borrowing, t>1) lowers Sharpe — exactly the geometry of the efficient frontier + CAL. **Data source:** illustrative only; replace `mu`/`Sigma` with your own point-in-time estimates (see Assumptions about estimation error).

## Assumptions & limitations
- **MV preferences or normality.** Mean–variance optimality requires either quadratic utility or jointly normal returns. Real returns have fat tails and skew; investors who care about higher moments may reject MV portfolios [S103].
- **Inputs are estimated, with error.** `μ` and `Σ` are estimated from history. The covariance `Σ` is estimable with moderate accuracy; the mean vector `μ` is notoriously noisy, and the optimizer is *most* sensitive to the noisiest input [S104].
- **Error maximization (the "enigma").** Michaud (1989) famously called MV an *error-maximizer*: it tends to overweight assets with extreme or erroneously estimated inputs, producing extreme, unstable, and highly concentrated weights that swing wildly for tiny input changes [S108, S104]. (Confirmed qualitatively — Michaud 1989 abstract opened via search; full text not directly opened.)
- **Single-period, static.** Ignores multi-period effects, taxes, transaction costs, liquidity, and constraints (long-only, min/max weights).
- **Non-stationarity.** `μ` and `Σ` drift; an in-sample-optimal portfolio is not the out-of-sample-optimal one (ties to KB 05-stats-and-ml and 15-pitfalls).

## Empirical evidence
- **Estimation-error critique is robust** and long-standing [S108, S104].
- **1/N vs sample MV (DeMiguel, Garlappi & Uppal, RFS 2009).** Across seven empirical datasets and 14 allocation models (including several designed to curb estimation error), **none** consistently beat the naive **equal-weight (1/N)** portfolio on Sharpe ratio, certainty-equivalent return, or turnover. Calibrated to the US equity market, the estimation window needed for sample MV to *outperform* 1/N is roughly **3,000 months (~250 years) for 25 assets** and **6,000 months (~500 years) for 50 assets** — i.e., "still many miles to go" before MV's promised gains materialize out-of-sample [S106, S107]. This is one of the most-cited results in empirical asset allocation and has been replicated across studies.
- **Nuance / conflict.** The 1/N dominance is strongest for *sample* MV with noisy mean estimates. Later work shows MV can win with superior estimators (Bayesian shrinkage, resampling) or in some asset classes (e.g., currency markets, Ackermann, Pohl & Schmedders 2016) — so the result condemns naive estimation more than the MV *framework* itself.

## Conflicting views
- **Theory vs practice.** MV is the rigorous workhorse behind the CAPM and portfolio theory [S104], yet *sample* MV routinely loses to 1/N out-of-sample [S106]. The tension is real but mostly about *estimation*, not the optimization logic.
- **"Is MV dead?"** No — the math of diversification is correct. The practical debate is how to feed it: (a) shrink the mean toward the cross-sectional average (Jorion 1986) and/or constrain weights; (b) use robust/shrunk covariance estimators (Ledoit–Wolf 2004); (c) resample the frontier (Michaud 1998); (d) impose long-only and min/max bounds; (e) inject investor views via Black–Litterman (separate KB article). The empirical edge of each remedy over 1/N is an open, data-dependent question — see Verify task below.
- **Normality assumption.** Defenders note MV needs only MV preferences, not strict normality; critics note real distributions violate both, so higher-moment and tail-risk considerations matter.

## Common mistakes
- Treating the **in-sample** efficient frontier as a forward-looking promise.
- Ignoring **estimation error**: feeding raw historical means into the optimizer and trusting the resulting corner/extreme weights.
- Forgetting **constraints** (no shorting, min weights) → optimizer parks everything in one asset.
- Assuming **normality**; ignoring skew, fat tails, and tail risk.
- Neglecting **transaction costs / rebalancing churn** — high-turnover MV portfolios bleed alpha (see KB 08-backtesting-methodology).
- Re-estimating on a moving window without testing out-of-sample (see KB 05-stats-and-ml and 15-pitfalls-and-antipatterns).
- Using a point estimate of `Σ` without a robustness/shrinkage check.

## Further reading
- **[Tier 1]** CFA Institute, *Portfolio Risk and Return: Part I* (2026 refresher reading) — efficient frontier, GMV, two-fund separation, CAL. https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-risk-return-part-1
- **[Tier 1]** Haugh, M. (Columbia), *Mean-Variance Optimization and the CAPM* lecture notes — full derivations, GMV/tangency closed forms, 1- & 2-fund theorems. https://www.columbia.edu/~mh2078/FoundationsFE/MeanVariance-CAPM.pdf
- **[Tier 1]** DeMiguel, V., Garlappi, L. & Uppal, R. (2009), "Optimal Versus Naive Diversification," *Review of Financial Studies* 22(5):1915–1953 — the 1/N benchmark result. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1376199 (abstract); https://academic.oup.com/rfs/article-abstract/22/5/1915/1592901
- **[Tier 1]** Michaud, R. (1989), "The Markowitz Optimization Enigma: Is 'Optimized' Optimal?" — error-maximization critique. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2387669
- **[Tier 1]** Markowitz, H. (1952), "Portfolio Selection," *Journal of Finance* 7(1):77–91 — the founding paper (cited by S104/S105).
- **[Tier 2]** Wikipedia, "Efficient frontier" — accessible geometry (hyperbola / Markowitz bullet, tangency, CML). https://en.wikipedia.org/wiki/Efficient_frontier
- **[Tier 2]** Scientific Portfolio, abstract of DeMiguel et al. 2009 (verbatim abstract quoted). https://scientificportfolio.com/external-research-anthology/victor-demiguel-lorenzo-garlappi-raman-uppal-2009/optimal-versus-naive-diversification-how-inefficient-is-the-1-n-portfolio-strategy
- **Next in KB:** 06-portfolio-construction/black-litterman (Bayesian views), 06-portfolio-construction/risk-parity-kelly (robust weighting), 08-backtesting-methodology (costs, walk-forward), 05-stats-and-ml (stationarity, overfitting), 15-pitfalls-and-antipatterns (data snooping, survivorship).
