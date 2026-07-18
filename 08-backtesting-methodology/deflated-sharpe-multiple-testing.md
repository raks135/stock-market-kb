---
title: Deflated Sharpe Ratio & Multiple-Testing Correction
topic_id: 08-backtesting-methodology/deflated-sharpe-multiple-testing
tags: [backtesting, sharpe-ratio, multiple-testing, selection-bias, deflated-sharpe, FDR, p-hacking, factor-zoo]
last_updated: 2026-07-18
confidence: robust
sources: [S80, S81, S82, S72, S83, S84, S85, S86]
---

## TL;DR
- A Sharpe ratio produced by searching over **N** candidate strategies is inflated by selection; the **Deflated Sharpe Ratio (DSR)** corrects it for both the number of trials and return non-normality (Bailey & López de Prado 2014).
- A single test at α=0.05 already gives a **>50% chance of at least one false positive after just 14 tests** (FWER = 1−(1−α)^m); multiplicity control is mandatory — Bonferroni/Holm for family-wise error rate (FWER), Benjamini–Hochberg for false-discovery rate (FDR).
- Whether "most" published return predictors are spurious is **contested**: Harvey–Liu–Zhu (2016) argue a |t|≈3.0 bar is needed after multiplicity; Chen (2024, Federal Reserve) bounds the false-discovery rate at 9–35% and argues ≥75% of findings are true. Treat discovery as probabilistic, not binary.

## Core explanation
The Sharpe ratio (Sharpe 1966, 1994) is the most-used risk-adjusted performance measure, but it is a **point estimate** with estimation error. Two pathologies inflate it:

1. **Multiple testing / selection bias.** Each test at significance α has a Type I error probability α. Running *m* independent tests, the probability of at least one false positive is the **family-wise error rate** FWER = 1−(1−α)^m. With α=0.05: 14 tests → 0.51, 100 tests → 0.994. Researchers also tend to report only "significant" results (file-drawer / publication bias, self-selection), so the displayed Sharpe comes from the *best* of many trials — exactly the one most likely to be a fluke.
2. **Backtest overfitting.** Optimizing parameters over many trials guarantees a profitable-looking strategy even on random data; the pattern that "worked" in-sample will not repeat (Bailey et al. 2014).

The **Probabilistic Sharpe Ratio (PSR)** reframes the Sharpe as a probability: P(true SR > benchmark SR\*), accounting for a finite, possibly non-normal track record (Bailey & López de Prado 2012). The **Deflated Sharpe Ratio (DSR)** is the PSR evaluated against a benchmark equal to the *expected maximum* Sharpe among N unskilled trials — i.e., it asks "is this strategy better than the best I'd expect by chance from N attempts?"

## Math / formulas

**Sharpe ratio** (per period, non-annualized):
$$\widehat{SR} = \frac{\bar r - r_f}{s_r}, \qquad SR_{ann} = \widehat{SR}\sqrt{p}$$
where $p$ = periods per year (12 monthly, 252 daily). Keep $\widehat{SR}$ and $T$ in the same frequency for PSR/DSR.

**Standard error of the Sharpe estimator** (Lo 2002; Mertens 2002):
$$SE(\widehat{SR}) = \sqrt{\frac{1 - \hat\gamma_3\,\widehat{SR} + \frac{\hat\gamma_4-1}{4}\widehat{SR}^2}{T}}$$
$\hat\gamma_3$ = skewness, $\hat\gamma_4$ = (Pearson) kurtosis of returns, $T$ = # observations. Under normality ($\gamma_3{=}0,\gamma_4{=}3$): $SE = \sqrt{(1 + \tfrac12\widehat{SR}^2)/T}$.

**Probabilistic Sharpe Ratio** (probability the true SR exceeds a benchmark $SR^*$):
$$PSR(SR^*) = \Phi\!\left(\frac{(\widehat{SR}-SR^*)\sqrt{T}}{\sqrt{1 - \hat\gamma_3\,\widehat{SR} + \frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right)$$
$\Phi$ = standard-normal CDF. (Some texts use $T-1$ or substitute $SR^*$ for $\widehat{SR}$ in the denominator; differences are second-order.)

**Expected maximum Sharpe under the null of no skill** (N independent trials):
$$SR_0 = \sqrt{V[\widehat{SR}_n]}\left[(1-\gamma)\,\Phi^{-1}\!\left(1-\tfrac1N\right) + \gamma\,\Phi^{-1}\!\left(1-\tfrac1{Ne}\right)\right]$$
$V[\widehat{SR}_n] = \big(1 - \hat\gamma_3\,\widehat{SR} + \frac{\hat\gamma_4-1}{4}\widehat{SR}^2\big)/T$ is the asymptotic variance; $\gamma\in[0,1]$ is the (prior) probability a tested strategy is genuinely skilled — **set γ=0 to be conservative**; $N$ = number of trials/strategies searched. For $N=1$, $SR_0=0$ (no selection).

**Deflated Sharpe Ratio:**
$$DSR = PSR(SR_0) = \Phi\!\left(\frac{(\widehat{SR}-SR_0)\sqrt{T}}{\sqrt{1 - \hat\gamma_3\,\widehat{SR} + \frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right)$$
$DSR \approx P(\text{strategy is not a false positive})$. As $N$ grows, $SR_0$ rises and DSR falls toward 0.

**Minimum Track Record Length (MinTRL):** the smallest $T$ such that $PSR(SR^*)\ge \text{confidence}$ (solve numerically; closed form in López de Prado 2014).

**Multiple-testing corrections:**
- **FWER = 1−(1−α)^m.** *Bonferroni:* reject if $p_i < \alpha/m$; adjusted $p_i^{adj}=\min(m\,p_i,1)$. Always valid, conservative. *Holm* step-down: thresholds $\alpha/(m-j+1)$ — uniformly more powerful, still controls FWER.
- **FDR = E[V/R]** (expected fraction of rejected hypotheses that are false). *Benjamini–Hochberg (1995):* order $p_{(1)}\le\dots\le p_{(m)}$; reject the largest $k$ with $p_{(k)}\le \frac{k}{m}q$; adjusted $p_{(k)}^{adj}=\min_{j\ge k}\min(\frac{m}{j}p_{(j)},1)$. Controls FDR ≤ q. *Benjamini–Yekutieli:* multiply threshold by $c(m)=\sum_{i=1}^m 1/i$ for arbitrary dependence (valid but more conservative).

**Factor-zoo significance bar (Harvey–Liu–Zhu 2016):** after accounting for the hundreds of factors tested, the customary $|t|>2.0$ (p<0.05) is far too lenient; the historical cutoff has risen to roughly **|t|≈3.0** (and higher for tests performed later, as the multiplicity bar keeps rising).

## Worked example / code
Pure standard-library Python (no third-party deps; verified on CPython 3.11+). Data source: **synthetic** illustrative returns (`random` module), not market data.

```python
import math, random

def phi(x):  # standard normal CDF via erf
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def phi_inv(p):  # inverse standard normal CDF (Acklam rational approximation)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p <= phigh:
        q = p - 0.5; r = q*q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    else:
        q = math.sqrt(-2 * math.log(1-p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)

def mean(x): return sum(x)/len(x)
def std(x, ddof=1):
    n=len(x); m=mean(x); return math.sqrt(sum((xi-m)**2 for xi in x)/(n-ddof))
def skew(x):
    n=len(x); m=mean(x); s=std(x,ddof=1)
    return sum((xi-m)**3 for xi in x)/n / s**3
def kurt_pearson(x):
    n=len(x); m=mean(x); s=std(x,ddof=1)
    return sum((xi-m)**4 for xi in x)/n / s**4
def sharpe(r, rf=0.0):
    ex=[xi-rf for xi in r]; return mean(ex)/std(ex,ddof=1)
def psr(sr_hat, T, sk, ku, sr_star=0.0):
    denom=math.sqrt(1 - sk*sr_hat + (ku-1)/4.0*sr_hat**2)
    return phi((sr_hat-sr_star)*math.sqrt(T)/denom)
def expected_max_sharpe(sr_hat, T, sk, ku, N, gamma=0.0):
    if N <= 1: return 0.0
    V=(1 - sk*sr_hat + (ku-1)/4.0*sr_hat**2)/T
    z1=phi_inv(1-1.0/N); z2=phi_inv(1-1.0/(N*math.e))
    return math.sqrt(V)*((1-gamma)*z1 + gamma*z2)
def dsr(sr_hat, T, sk, ku, N, gamma=0.0):
    return psr(sr_hat, T, sk, ku, expected_max_sharpe(sr_hat, T, sk, ku, N, gamma))

# Demo 1: PSR/DSR on a synthetic monthly series (seed 42, 120 obs)
rng=random.Random(42)
rets=[rng.gauss(0.01, 0.05) for _ in range(120)]
T=len(rets); sr=sharpe(rets); sk=skew(rets); ku=kurt_pearson(rets)
print(f"monthly SR={sr:.3f}, skew={sk:.3f}, kurt={ku:.3f}, T={T}")
print(f"PSR(0)={psr(sr,T,sk,ku,0):.3f}")
for N in [1,10,100,1000]:
    print(f"N={N:5d}  DSR={dsr(sr,T,sk,ku,N):.3f}")
# MinTRL: smallest T with PSR>=0.95 vs benchmark 0
lo,hi=1.0,1e6
for _ in range(200):
    mid=(lo+hi)/2
    if psr(sr,mid,sk,ku,0.0)<0.95: lo=mid
    else: hi=mid
print(f"MinTRL(95% skill vs 0)={lo:.0f} obs")

# Demo 2: multiple-testing simulation, all-null Gaussian (m=200, n=250)
m=200; rng=random.Random(0); pvals=[]
for _ in range(m):
    x=[rng.gauss(0,1) for _ in range(250)]
    xbar=mean(x); se=std(x,ddof=1)/math.sqrt(len(x)); z=xbar/se
    pvals.append(2*(1-phi(abs(z))))
alpha=0.05
naive=sum(1 for p in pvals if p<alpha)
bonf=sum(1 for p in pvals if p<alpha/m)
order=sorted(range(m), key=lambda i:pvals[i]); ps=[pvals[i] for i in order]
thr=[alpha*(k+1)/m for k in range(m)]
bh=sum(1 for k in range(m) if ps[k]<=thr[k])
print(f"m={m}: naive_sig={naive}, Bonferroni_sig={bonf}, BH_sig={bh}, FWER_naive={1-(1-alpha)**m:.3f}")
```

**Output (verified):**
```
monthly SR=0.287, skew=-0.155, kurt=3.160, T=120
PSR(0)=0.999
N=    1  DSR=0.999
N=   10  DSR=0.958
N=  100  DSR=0.753
N= 1000  DSR=0.468
MinTRL(95% skill vs 0)=36 obs
m=200: naive_sig=12, Bonferroni_sig=0, BH_sig=0, FWER_naive=1.000
```
Interpretation: the *same* track record looks essentially certain skill (PSR 0.999) when reported alone, but is only a coin-flip (DSR 0.47) once we learn it was the best of 1,000 attempts. Demo 2 shows 12 false positives out of 200 null tests at α=0.05, all eliminated by Bonferroni/BH. (In a single null draw BH may reject 0 — with real signals BH rejects more than Bonferroni while controlling FDR, not FWER.)

## Assumptions & limitations
- **DSR corrects statistical inflation only.** It does *not* fix non-stationarity, transaction costs, capacity, or look-ahead. A deflated Sharpe can still fail out-of-sample.
- **N must be the true number of trials**, including abandoned ones (file-drawer). Under-reporting N makes DSR optimistic. Correlated trials have a smaller effective $N$ (Bailey et al. 2015), so N should be an *effective* count.
- **Asymptotic formulas.** PSR/DSR use the large-sample distribution of $\widehat{SR}$; small $T$ or extreme kurtosis weaken them. The $SE$ term assumes IID observations — violated by autocorrelation/vol clustering.
- **γ=0** (no ex-ante skill) is conservative; if you believe some strategies are skilled, DSR rises — a subjective prior.
- **BH assumes independence / positive dependence.** Use Benjamini–Yekutieli for arbitrary dependence (more conservative). Bonferroni is valid under any dependence but loses power fast as $m$ grows.
- **t>3.0 is a rule of thumb**, not a law; the exact HLZ cutoff depends on how many tests were run historically (it drifts upward over time).

## Empirical evidence
- **DSR/PSR** are analytical results, validated by Monte Carlo in Bailey & López de Prado (2014): a Sharpe inflated by selection collapses toward 0 once $N$ and non-normality are entered.
- **Factor zoo (HLZ 2016):** at least **316** published factors predicting returns; the customary $|t|>2.0$ is too lenient after multiplicity, pushing the recommended cutoff to roughly **|t|≈3.0**.
- **Counter-evidence (Chen 2024, Federal Reserve):** bounding the FDR with summary statistics from eight studies (seven independent teams) implies **≥75%** of claimed cross-sectional findings are true (tightest bound 91%); HLZ's *own* figures imply an FDR of at most 35% (SMM estimate 9%). See Conflicting views.
- **Lo (2002)** establishes the sampling distribution of the Sharpe ratio; **Mertens (2002)** and **Bailey & López de Prado (2012)** give the non-normal SE and PSR.

## Conflicting views
- **"Most factors are false" (HLZ 2016):** after multiplicity, a huge share of published anomalies are statistical flukes; demand $|t|\approx 3.0$ and disclosure of all trials.
- **"Most findings are true" (Chen 2024):** an FDR bound using Benjamini–Hochberg logic shows ≥75% true; the apparent conflict is *interpretive* — HLZ equates "insignificant after their test" with "false," conflating significance with truth. Chen also notes HLZ's SMM implies only a 9% FDR.
- **Practical takeaway:** both sides agree multiplicity *matters*; they disagree on the *fraction* spurious. The defensible position is **probabilistic skepticism** — report N, deflate the statistic, and require out-of-sample/holdout confirmation rather than declaring factors "real" or "fake" from a single test.
- **DSR vs hold-out:** López de Prado argues hold-out sets are unreliable for heavily optimized backtests (PBO/CSCV preferred); others treat a clean hold-out as sufficient. Related: see the overfitting/look-ahead article.

## Common mistakes
- Reporting a Sharpe **without stating N** (the single most important omission — "a backtest without the number of trials is worthless").
- Mixing frequencies: annualizing $\widehat{SR}$ but feeding raw $T$ (or vice-versa) into PSR/DSR.
- Treating DSR as a **future-performance guarantee** — it only removes statistical inflation, not regime/non-stationarity/cost risk.
- Using Bonferroni on thousands of *correlated* factor tests → near-zero power (prefer BH/FDR, or BY for dependence).
- Equating "insignificant after correction" with "the factor is fake" (Chen's critique) — and the mirror error of equating "significant" with "profitable net of costs."
- **p-hacking:** peeking, retesting after seeing data, or stopping when $p<0.05$; running until significant inflates the false-positive rate to ~1 over many attempts.
- Forgetting that DSR's $SR_0$ uses an *effective* N; correlated/derived trials must not all be counted as independent.

## Further reading
**Tier 1 (primary):**
- Bailey, D.H. & López de Prado, M. (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality," *J. Portfolio Management* 40(5):94–107. [S80] https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- Harvey, C.R., Liu, Y. & Zhu, H. (2016), "…and the Cross-Section of Expected Returns," *Review of Financial Studies* 29(1):5–68. DOI 10.1093/rfs/hhv070. [S72] summary: https://foxholm.com/q/research/harvey-liu-zhu-cross-section
- Chen, A.Y. (2024), "Most claimed statistical findings in cross-sectional return predictability are likely true," Federal Reserve Board (May 2024). [S82] https://www.anderson.ucla.edu/sites/default/files/document/2024-05/5.24.24%20Paper%20Andrew%20Checn%20Fed%20Reserve%20Board.pdf
- Benjamini, Y. & Hochberg, Y. (1995), "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing," *JRSSB* 57(1):289–300. [S83]
- Lo, A.W. (2002), "The Statistics of Sharpe Ratios," *Financial Analysts Journal* 58(4):36–52. [S86]

**Tier 2 (practitioner):**
- QuantConnect, "Probabilistic Sharpe Ratio" (worked PSR + non-normality example). [S81] https://www.quantconnect.com/research/17112/probabilistic-sharpe-ratio
- Wikipedia, "Deflated Sharpe ratio" / "False discovery rate" (formula cross-check). [S85]

**Tier 3 (code reference, not sole source):**
- Brenndoerfer, M. (2026), "Multiple Comparisons: FWER, FDR, Bonferroni, Holm & Benjamini–Hochberg" (algorithm/code exposition). [S84] https://mbrenndoerfer.com/writing/multiple-comparisons-fwer-fdr-bonferroni-holm-benjamini-hochberg

**Related KB articles:** 05-stats-and-ml/overfitting-lookahead (PBO/CSCV, the factor-zoo cutoff, DSR context); 08-backtesting-methodology/transaction-costs-slippage-walkforward (cost/impact reality checks that DSR does not capture).
