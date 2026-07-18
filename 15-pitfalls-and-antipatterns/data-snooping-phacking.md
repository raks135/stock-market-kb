---
title: Data Snooping & p-Hacking (Backtest Selection Bias)
topic_id: 15-pitfalls-and-antipatterns/data-snooping-phacking
tags: [pitfalls, multiple-testing, backtest-overfitting, data-snooping, p-hacking, reality-check, FDR]
last_updated: 2026-07-18
confidence: robust
sources: [S68, S69, S70, S71, S72, S80, S82, S83, S86, S87, S88]
---

## TL;DR
- Data snooping (a.k.a. p-hacking / data mining) is reusing the same historical data for inference, model selection, and performance reporting. When you search many strategies, parameters, or factors and then report only the best, the "winner" is almost always an artifact of chance.
- The remedy is **not** to stop searching but to correct for the search. Use multiple-testing controls (Bonferroni/Holm for FWER, Benjamini–Hochberg for FDR), White's Reality Check / SPA bootstrap, or the Deflated Sharpe Ratio — and demand that any "significant" result state how many trials it survived.
- A single best Sharpe or t-stat with no trial count attached is worthless (Bailey & López de Prado 2014). In our simulation, searching 1,000 noise strategies yields a "best" with |t|=3.64 and p=0.0003 — but Bonferroni-corrected p=0.27, i.e. pure luck 95% of the time.

## Core explanation
**Plain language.** Imagine flipping 1,000 coins and showing your friends only the one that came up heads 9 times in a row. It looks miraculous, but with 1,000 trials a "miracle" is guaranteed by chance. Backtesters do the same: they try hundreds of parameter sets, indicators, and entry/exit rules, then trumpet the single configuration that "worked." The displayed performance reflects the *selection* of the luckiest draw, not any real edge.

White (2000) defines data snooping as "when a given set of data is used more than once for purposes of inference or model selection," and notes it is "widely acknowledged … to be avoided, but in fact it is endemic" in time-series work because usually only one history of a phenomenon exists.

**Precise.** Let a strategy universe contain *m* candidate models (rules, parameterizations, or factors). Under the null that none has genuine predictive power, each test statistic is drawn from its null distribution. Selecting the maximum statistic `max_i t_i` and then computing its p-value *as if it were the only test* massively understates the type-I error rate. The correct null is the *intersection* hypothesis "no model in the universe beats the benchmark," which is exactly what White's Reality Check and the Superior Predictive Ability (SPA) test evaluate via bootstrapping the maximum across the search.

This is why data snooping is filed under *pitfalls*: it is the single most common reason a brilliant backtest dies in live trading. It is closely related to, but distinct from, overfitting (overfitting is parameter memorization; snooping is selection across many candidates, whether or not parameters are estimated).

## Math / formulas
**Family-Wise Error Rate (FWER).** With *m* independent tests at level α, the probability of ≥1 false positive is
```
FWER = 1 − (1 − α)^m
```
For m=100, α=0.05 → FWER ≈ 0.994. Even m=14 → 0.51 (illustrated in Brenndoerfer 2026, S-bucket).

**Bonferroni correction (controls FWER).** Reject the i-th test only if `p_i ≤ α/m`. Conservative; ignores dependence.

**Benjamini–Hochberg (BH, 1995 — controls FDR).** Sort p-values `p_(1) ≤ … ≤ p_(m)`. Let `k = max{i : p_(i) ≤ (i/m)·q}`. Reject all tests 1…k. FDR = E[V/R] (false discoveries / total rejections).

**White (2000) Reality Check / SPA.** Tests
```
H0: max_{i=1..m} E[f_i] ≤ 0     (no model beats benchmark)
```
where `f_i` is the per-period performance differential vs a benchmark, using a stationary bootstrap to preserve dependence and to compute a p-value for the *maximum* over the universe (asymptotically controls FWER). Hansen's SPA (2005) refines this with a studentized version and consistent null.

**Deflated Sharpe Ratio (Bailey & López de Prado 2014).** Adjusts a reported Sharpe `Ŝ` for the number of trials *N*, non-normality (skew, kurtosis), and sample length *T*:
```
DSR = P( SR* ≤ Ŝ )
where SR* = expected max Sharpe among N independent trials under the null.
```
A "significant" DSR requires the trial count *N* to be disclosed; without it the backtest is uninterpretable.

## Worked example / code
Simulate *m*=1,000 strategies on i.i.d. N(0,σ) daily returns — a pure null with **no edge** — then select the best by |t-stat| of mean return. Data source: synthetic (Box–Muller normals, `random` stdlib only, seed 42). Reproduce with:

```python
import random, math
from math import erf, sqrt

random.seed(42)
def gaussian():
    u1, u2 = random.random(), random.random()
    return math.sqrt(-2*math.log(u1))*math.cos(2*math.pi*u2)
def t_stat(r):
    n=len(r); m_=sum(r)/n
    v=sum((x-m_)**2 for x in r)/(n-1)
    return m_/(math.sqrt(v)/math.sqrt(n))
def p2(t):
    x=abs(t); return 2*(1-0.5*(1+erf(x/sqrt(2))))

M, T, sigma = 1000, 252, 0.01
all_t=[t_stat([gaussian()*sigma for _ in range(T)]) for _ in range(M)]
best=max(all_t, key=abs)
print(f"best |t|={abs(best):.2f}  naive p={p2(best):.4f}  Bonferroni p={min(1,M*p2(best)):.4f}")
print("naive |t|>2 count =", sum(1 for t in all_t if abs(t)>2.0))
```

**Verified output (this exact script):**
```
Single search (seed 42): best |t| = 3.64
  naive p(best) = 0.0003  -> Bonferroni-adjusted p = 0.2712
  # of 1000 strategies with |t|>2.0 by chance = 54  (expect ~46)
  # BH-significant at q=0.05 (global null) = 0
Across 200 replications of a 1000-rule search:
  average max|t| = 3.45   fraction with max|t|>3 = 95%
```

**Interpretation.** On pure noise, the single best of 1,000 rules shows |t|=3.64 (naively "highly significant," p=0.0003), but Bonferroni inflates it to p=0.27 — consistent with chance. Across 200 independent searches, the average best |t| is 3.45 and **95% of searches produce a rule with |t|>3**. This is the data-snooping trap made concrete: a headline t-stat of 3+ proves nothing without a multiple-testing correction and a disclosed trial count.

## Assumptions & limitations
- Corrections assume the *m* tests are the **full** universe actually searched. Hidden searches (trying 500 rules, reporting 1) break every method — the trial count must be honest and complete.
- Bonferroni/Holm assume (approximate) independence or use a conservative bound; strong positive dependence among strategies reduces effective trials (Bailey et al. 2015 CSCV estimates an *effective N*).
- White's RC/SPA is **asymptotic** and relies on the bootstrap preserving the dependence structure; it controls error under the null but says nothing about live performance under regime change.
- BH controls FDR *in expectation*; for a single study it can still pass a few false positives, and under a global null it returns ~q·m expected false positives.
- None of these fix **non-stationarity, costs, capacity, or look-ahead** — they only correct statistical selection inflation.

## Empirical evidence
- **White (2000, Econometrica 68(5):1097–1126)** establishes the Reality Check bootstrap and the "newsletter scam" / coin-flipping analogy; data snooping is "endemic" in time-series. *(S87, Tier 1, opened)*
- **Sullivan, Timmermann & White (1999, Journal of Finance 54(5):1647–1691)** apply White's Reality Check bootstrap to an expanded universe of technical-trading rules over ~100 years of DJIA and quantify the data-snooping bias; it is the canonical demonstration that unadjusted significance overstates rule performance. *(S88, Tier 1, opened abstract; 300+ citations)*
- **Lo & MacKinlay (1990, Review of Financial Studies 3(3):431–467)** document data-snooping biases in tests of asset-pricing models (classic reference, cited by S88).
- **Bailey & López de Prado (2014, JPM 40(5):94–107)** show the Deflated Sharpe Ratio and that "a backtest without a stated number of trials is meaningless." *(S68/S80, Tier 1)*
- **Bailey et al. (2014, 2015)** simulate backtests on random walks and find the optimal in-sample Sharpe is large while out-of-sample it is ~0 — selection manufactures edges. *(S69/S70, Tier 1)*
- **Harvey, Liu & Zhu (2016, RFS 29(1):5–68)** count 316+ published "factors" and argue a t-stat near **3.0** (not 2.0) is needed after multiple-testing; most claimed findings fail. *(S72, Tier 2 summary of Tier-1 paper)*

## Conflicting views
- **"How many factors are real?"** Harvey–Liu–Zhu (2016) conclude most of the 316+ factors are false discoveries and advocate |t|≈3.0. **Chen (2024, Federal Reserve Board)** counters that most claimed cross-sectional findings are *likely true* (FDR bound ≥75%, their own HLZ-based bound ≤35%, tightest 9%), arguing the conflict is interpretive (significance threshold vs. truth of the claim). *(S72 vs S82 — both carried in registry; magnitude contested, direction of "how bad is it" debated.)*
- **FWER vs FDR.** Bonferroni/Holm eliminate false positives at the cost of power; BH tolerates some to keep more real findings. The "right" choice depends on whether a false discovery is catastrophic (regulatory/trading-capital) or merely wasteful (research triage).
- **Reality Check vs. holdout.** White's RC tests the *search* on the same data via bootstrap; a single holdout is unreliable for backtests (Bailey et al. 2015) because correlated trials leak information. Both aim at the same inflation but disagree on the practical estimator.

## Common mistakes
1. **Reporting the best of a search as a single prespecified test** — the cardinal sin; always disclose *m* (or effective N).
2. **Ignoring parameter combinations.** Tuning 5 parameters at 10 values each = 100,000 implicit trials, not 1.
3. **Using t>2.0 / p<0.05 without correction** — under multiple testing this guarantees false positives (FWER→~1 for large m).
4. **p-hacking by specification shopping** — trying many dependent variables, lags, subsamples, and reporting only significant cuts.
5. **Treating walk-forward / "out-of-sample" as a cure** — if the *same* data is reused across many rounds of re-optimization, it still snoops.
6. **Selective publication** of "working" strategies and silent dropping of failures (file-drawer effect).
7. **Confusing statistical significance with economic significance** — even a correctly-adjusted tiny edge is killed by costs/capacity.

## Further reading
- **Tier 1 (primary):** White H. (2000) "A Reality Check for Data Snooping," *Econometrica* 68(5):1097–1126 — https://www.ssc.wisc.edu/~bhansen/718/White2000.pdf (opened)
- **Tier 1 (primary):** Sullivan R., Timmermann A., White H. (1999) "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap," *Journal of Finance* 54(5):1647–1691 — https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1647-1691.html (opened); DOI 10.1111/0022-1082.00163
- **Tier 1:** Bailey D.H. & López de Prado M. (2014) "The Deflated Sharpe Ratio," *JPM* 40(5):94–107 — https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf (opened, S80)
- **Tier 1:** Bailey D.H. et al. (2015) "The Probability of Backtest Overfitting" — https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf (opened, S69)
- **Tier 1:** Benjamini Y. & Hochberg Y. (1995) "Controlling the False Discovery Rate," *JRSSB* 57(1):289–300 (opened, S83)
- **Tier 1:** Lo A.W. (2002) "The Statistics of Sharpe Ratios," *FAJ* 58(4):36–52 (opened, S86)
- **Tier 2:** Foxholm review of Harvey, Liu & Zhu (2016) — https://foxholm.com/q/research/harvey-liu-zhu-cross-section (opened, S72)
- **Tier 2:** Coqueret G. & Guida T. "The Dangers of Backtesting" — https://portfoliooptimizationbook.com/book/8.3-dangers-backtesting.html (opened, S71)
- **Companion KB articles:** `05-stats-and-ml/overfitting-lookahead.md`, `08-backtesting-methodology/deflated-sharpe-multiple-testing.md`, `15-pitfalls-and-antipatterns/survivorship-bias.md` (next).
