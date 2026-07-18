---
title: Mean-Reversion & Statistical-Arbitrage Strategies
topic_id: 14-strategy-catalog/mean-reversion-stat-arb
tags: [strategy-catalog, mean-reversion, statistical-arbitrage, stat-arb, pairs-trading, factor-neutral, market-neutral, Ornstein-Uhlenbeck, variance-ratio]
last_updated: 2026-07-18
confidence: contested
sources: [S367, S368, S369, S370, S371, S372]
---

## TL;DR
Mean-reversion strategies bet that temporary dislocations — in single-stock residuals, spreads, or short-horizon returns — revert to an equilibrium, and statistical arbitrage ("stat-arb") scales this into a diversified, factor-neutral book of many small contrarian bets. The phenomenon is empirically robust at short horizons (Jegadeesh 1990 ~2%/mo reversal; Lo–MacKinlay 1988 variance-ratio rejects the random walk at the weekly horizon), but the *net-of-cost, live* edge has decayed (Avellaneda–Lee 2010 PCA Sharpe 1.44 over 1997–2007 vs 0.9 in 2003–2007) and is regime- and crowding-dependent (Khandani–Lo 2007 quant meltdown). Treat mean reversion of *residuals/spreads* as real; mean reversion of *raw prices* is generally absent.

## Core explanation
**Plain language.** Many prices don't wander randomly forever — when a stock temporarily drifts too far above or below its fair relationship with a peer, a sector ETF, or its own recent average, it tends to snap back. Mean-reversion traders systematically bet *against* extremes: buy the laggard, sell the leader, and profit as they converge. "Statistical arbitrage" is the institutional form of this idea — instead of one pair, a quant fund holds hundreds of small, market-neutral, factor-neutral contrarian positions at once, so the book is roughly beta-zero and earns a low-volatility "convergence" return from diversification across many independent reversion bets.

**Precise.** Mean reversion is the property that a process reverts to a long-run level μ rather than following a random walk. In equities it appears in three distinct, non-overlapping forms:
1. **Cross-sectional short-horizon reversal** — last month's (or week's) losers outperform winners (Jegadeesh 1990; Lehmann 1990).
2. **Relative-value / pairs** — two cointegrated securities diverge and reconverge (covered in `05-stats-and-ml/cointegration-pairs-trading.md`).
3. **Model-driven stat-arb** — regress each stock's return on systematic factors (PCA eigenvectors or sector ETFs); the *idiosyncratic residual* is modeled as a mean-reverting process, and contrarian signals are generated on the residual (Avellaneda & Lee 2010). This is "generalized pairs trading."

The crucial distinction: **raw prices are ~I(1) random walks (no mean reversion), but estimated residuals and spreads can be I(0) and mean-reverting.** Confusing the two is the most common error.

## Math / formulas

**Ornstein–Uhlenbeck (OU) process** — the canonical mean-reverting model for a residual Xₜ:
$$ dX_t = \kappa(\mu - X_t)\,dt + \sigma\,dW_t $$
- κ = mean-reversion speed (higher = faster), μ = long-run mean, σ = volatility.
- **Half-life** (expected time for a deviation to shrink by 50%): $\tau_{1/2} = \ln(2)/\kappa$.
- Discrete AR(1) fit $X_{t+1} = a + b X_t + \varepsilon_t$ gives $b = e^{-\kappa\Delta t}$, so $\hat\kappa = -\ln(\hat b)/\Delta t$.

**s-score (Avellaneda–Lee 2010)** — standardized distance of the residual from equilibrium:
$$ s = \frac{X_t - m_{eq}}{\sigma_{eq}}, \qquad m_{eq} = \frac{a}{1-b},\quad \sigma_{eq} = \sigma\sqrt{\frac{1-b^2}{2b}} $$
Trade rule: go long when $s < -s_{entry}$, short when $s > +s_{entry}$, exit near $s \approx 0$. Fast reversion requires κ large enough that mean-reversion time is ≲ 1.5 months.

**Variance-ratio test (Lo & MacKinlay 1988)** — tests the random-walk null $V(k)=1$:
$$ V\!R(k) = \frac{\widehat{\mathrm{Var}}(k\text{-period return})}{k\cdot\widehat{\mathrm{Var}}(1\text{-period return})} ,\qquad Z(k) = \frac{VR(k)-1}{\sqrt{\phi(k)}} $$
Under homoscedasticity $\phi(k) = \frac{2(2k-1)(k-1)}{3kT}$. **VR < 1 ⇒ negative return autocorrelation ⇒ mean reversion; VR ≈ 1 ⇒ random walk.**

**Factor decomposition (stat-arb engine)** — Avellaneda & Lee decompose returns:
$$ \frac{dP_t}{P_t} = \alpha\,dt + \sum_{j=1}^{n}\beta_j F_t^{(j)} + dX_t $$
where $F^{(j)}$ are risk factors (PCA or sector ETFs) and $X_t$ is the mean-reverting idiosyncratic residual. The book is constructed to be **market-neutral** (zero β) by netting long/short single-stock positions against the factor shorts.

**Formal definition of statistical arbitrage (Hogan–Jarrow–Teo–Warachka 2004)** — a *self-financing, zero-cost* trading strategy whose cumulative discounted payoff $V(t)$ satisfies $V(0)=0$, $\lim_{t\to\infty}\mathbb{E}[V(t)]>0$ (positive expected profit), $\lim_{t\to\infty}P(V(t)<0)=0$ (vanishing probability of loss), and bounded variance growth $\lim_{t\to\infty}\mathrm{Var}[V(t)]/t = 0$. HJTW note this definition is *independent of any equilibrium model* and its existence is incompatible with market efficiency — so it "circumvents the joint-hypothesis dilemma" of traditional efficiency tests.

## Worked example / code
Stdlib-only (Python 3.14.4, no external libraries), seeded for reproducibility. **Data source: synthetic** (Box–Muller OU vs random walk) — it demonstrates the *statistics and mechanics*, not a market claim. Verified output is printed beneath the code.

```python
# Mean-reversion / stat-arb mechanics — stdlib only, CPython 3.14.4
import random, math

def std_normal():
    u1, u2 = random.random(), random.random()
    return math.sqrt(-2*math.log(u1))*math.cos(2*math.pi*u2)

def simulate_ou(n, kappa, mu, sigma, dt, seed=42):
    random.seed(seed); x = mu; path=[x]
    for _ in range(n):
        x += kappa*(mu-x)*dt + sigma*math.sqrt(dt)*std_normal(); path.append(x)
    return path

def simulate_rw(n, sigma, seed=7):
    random.seed(seed); x=100.0; path=[x]
    for _ in range(n): x += sigma*std_normal(); path.append(x)
    return path

def log_returns(p): return [math.log(p[i]/p[i-1]) for i in range(1,len(p))]

def variance_ratio(r, k):
    T=len(r); mu=sum(r)/T
    var1=sum((x-mu)**2 for x in r)/(T-1)
    kr=[sum(r[i:i+k]) for i in range(0,T-k+1)]
    m=k*(T-k+1)*(1-k/T)
    vark=sum((x-k*mu)**2 for x in kr)/m
    vr=vark/var1; phi=2*(2*k-1)*(k-1)/(3*k*T)
    return vr,(vr-1)/math.sqrt(phi)

def estimate_ou(xs, dt):
    n=len(xs)-1; Xt=xs[:-1]; Xp=xs[1:]
    mx=sum(Xt)/n; my=sum(Xp)/n
    sxx=sum((x-mx)**2 for x in Xt)
    sxy=sum((x-mx)*(y-my) for x,y in zip(Xt,Xp))
    b=sxy/sxx; kap=-math.log(b)/dt
    return kap, math.log(2)/kap

def s_score_backtest(path, mu, sigma, entry=1.5, exit_z=0.5):
    pnl=0.0; pos=0.0; tp=0.0; trades=0; wins=0
    for t in range(1,len(path)):
        s=(path[t]-mu)/sigma; target=max(-1.0,min(1.0,-s))
        if pos==0.0 and abs(s)>=entry: pos=target; tp=0.0
        elif pos!=0.0 and abs(s)<=exit_z:
            step=pos*(path[t]-path[t-1]); tp+=step; pnl+=step
            if tp>0: wins+=1
            trades+=1; pos=0.0
        else:
            step=pos*(path[t]-path[t-1]); tp+=step; pnl+=step
    return pnl, trades, (wins/trades if trades else 0.0)

N=5000; DT=1.0; KAPPA=0.1
ou=simulate_ou(N,kappa=KAPPA,mu=100.0,sigma=1.0,dt=DT,seed=42)
rw=simulate_rw(N,sigma=0.01,seed=7)
for k in (5,20):
    vo,zo=variance_ratio(log_returns(ou),k); vr,zr=variance_ratio(log_returns(rw),k)
    print(f"[VR k={k}] OU VR={vo:.3f} Z={zo:.2f} (expect <1) | RW VR={vr:.3f} Z={zr:.2f} (~1)")
kap,hl=estimate_ou(ou,DT)
print(f"[OU fit] kappa_est={kap:.3f} (true {KAPPA}) | half_life={hl:.2f} (true {math.log(2)/KAPPA:.2f})")
ou0=simulate_ou(N,kappa=KAPPA,mu=0.0,sigma=1.0,dt=DT,seed=99)
pnl,tr,hr=s_score_backtest(ou0,mu=0.0,sigma=1.0)
print(f"[s-score P&L] cum_pnl={pnl:.2f} | trades={tr} | win_rate={hr:.2f}")
```

**Verified output (CPython 3.14.4):**
```
[VR k=5]  OU VR=0.800 Z=-6.46 (expect <1) | RW VR=0.958 Z=-1.36 (~1)
[VR k=20] OU VR=0.409 Z=-8.41 (expect <1) | RW VR=1.006 Z=0.09  (~1)
[OU fit] kappa_est=0.112 (true 0.100) | half_life=6.16 (true 6.93)
[s-score P&L] cum_pnl=623.59 | trades=318 | win_rate=1.00
```
The OU (mean-reverting) series rejects the random walk via VR<1 with strongly negative Z, while the random walk cannot be rejected. The AR(1) fit recovers κ≈0.11 and a ~6-period half-life. The contrarian s-score book is profitable on the synthetic OU *because the process is constructed to revert* — with real data, costs, estimation error, and non-stationarity shrink this to a contested live edge (see Empirical evidence).

## Assumptions & limitations
- **The reversion is estimated, not known.** κ, μ, σ are fit from a trailing window; if the true process is not stationary (regime change, cointegration breakdown), the s-score is garbage and signals invert.
- **Costs dominate when half-life is long.** A reversion that takes 6–12 months to play out is eaten by financing, borrow, and spread costs; Avellaneda–Lee require κ large enough for ≲1.5-month mean-reversion times.
- **Estimation look-ahead.** Betas/vols must be computed only from data available *at the trade date*; using the full sample (as the demo's in-sample params do) is look-ahead and inflates the edge (see `15-pitfalls/look-ahead` and `08-backtesting/transaction-costs`).
- **Shorting & capacity.** Stat-arb is long/short and market-neutral; it needs a short book, borrow, and capacity that degrades as AUM grows (Khandani–Lo 2007).
- **Crowding / common-factor risk.** Many quant books use similar factor models, so "idiosyncratic" residuals share a hidden common component; a forced unwind by one fund propagates to all (Aug 2007).
- **Non-stationarity.** The edge has visibly decayed with competition, decimalization, and lower volatility (Avellaneda–Lee 2010).

## Empirical evidence
- **Short-horizon reversal is robust.** Jegadeesh (1990) documents ~2% per month from a contrarian strategy on prior-month returns over 1934–1987; Lehmann (1990) finds analogous weekly winner/loser reversal. Corroborated across independent summaries (Springer, NY Fed staff report 513, Jegadeesh 1992).
- **Variance-ratio rejects the random walk at short horizons.** Lo & MacKinlay (1988) show weekly U.S. stock returns are incompatible with the random walk — i.e., negative short-horizon autocorrelation consistent with mean reversion (their abstract states the rejection explicitly; the test statistic and homoscedastic formula are implemented/verified above).
- **Stat-arb works but has decayed.** Avellaneda & Lee (2010, *Quantitative Finance*, full text opened) build PCA- and ETF-based market-neutral strategies on 60-day residual estimation (universe capped >$1B at trade date to avoid survivorship bias). After transaction costs: **PCA Sharpe 1.44 (1997–2007), falling to 0.9 in 2003–2007; ETF-based Sharpe 1.1 (1997–2007); ETF strategies with volume information 1.51 (2003–2007).** Performance degrades after ~2002–2003 and is tied to the market/liquidity cycle.
- **Crowding caused a real crisis.** Khandani & Lo (2007, *JOIM*, full text opened) document that during the week of Aug 6, 2007, quantitative market-neutral/stat-arb funds lost −5% to −30% while the S&P moved little; they attribute it to the forced, rapid unwind of one or more large market-neutral books, with "25-standard-deviation moves, several days in a row" (Goldman CFO). The losses reversed partially on Aug 10, consistent with an unwind rather than a fundamental breakdown — but they show the sector had become a *common-factor* risk.

## Conflicting views
- **Efficient-markets camp (Fama & French, EMH):** persistent mean reversion in *liquid large-cap* prices is not reliable; apparent reversals are often small-cap/illiquid or data-mined, and disappear after costs (ties to `15-pitfalls/data-snooping` and `04-quant/cross-sectional` decay).
- **Practitioner/quant camp:** short-horizon reversal and *residual* mean reversion are real and economically significant, especially when made market-neutral and diversified (Avellaneda–Lee; the whole stat-arb industry pre-2007).
- **The decay debate:** is stat-arb "dead" or just "more competitive"? Avellaneda–Lee show the Sharpe fell from ~1.44 to ~0.9 in five years *before* the 2007 crisis, and Khandani–Lo list competition, decimalization, declining retail flow, and lower volatility as structural drags. Most practitioners now treat the *unconcentrated* version as a low-Sharpe, capacity-constrained, regime-sensitive source of return rather than a free lunch.
- **August 2007: structural fragility vs. one-off event.** Some see it as proof stat-arb is inherently fragile to crowding; others as a liquidity shock that the strategy survived (partial rebound). The consensus is that *crowding*, not the alpha, was the vulnerability.

## Common mistakes
- **Reverting prices vs. reverting residuals.** Fitting an OU to a raw stock price (an I(1) random walk) and expecting reversion is a category error; mean reversion lives in residuals/spreads (properly stationary series).
- **Ignoring the half-life vs. holding-period mismatch.** A 6-month half-life strategy forced to close in 2 weeks is just noise exposure.
- **In-sample parameter estimation = look-ahead.** Estimating μ, σ, β on the full history (or the future) inflates the backtest; use only trailing data at each trade date.
- **Forgetting costs and shorts.** A gross "reversion" edge of a few bps is often negative net of spread, borrow, and financing.
- **Treating the synthetic demo as tradable.** The OU backtest above is *constructed* to revert; real residuals are noisier, non-stationary, and cost-sensitive. It teaches mechanics, not expectancy.
- **Overfitting entry/exit thresholds** to a backtest (see `15-pitfalls/overfitting`, `08-backtesting/deflated-sharpe`).

## Further reading
- **[S367 | Tier 1]** Avellaneda, M. & Lee, J.-H. (2010), "Statistical arbitrage in the US equities market," *Quantitative Finance* 10(7):761–782. https://traders.berkeley.edu/papers/Statistical%20arbitrage%20in%20the%20US%20equities%20market.pdf — primary; Sharpe numbers, OU/s-score methodology, decay, survivorship check.
- **[S368 | Tier 1]** Khandani, A. & Lo, A. (2007), "What Happened to the Quants in August 2007?" *Journal of Investment Management* 5(4):5–54. https://w4.stern.nyu.edu/finance/docs/pdfs/Seminars/083w-lo.pdf — primary; quant meltdown, unwind hypothesis, crowding.
- **[S369 | Tier 1]** Lo, A. & MacKinlay, C. (1988), "Stock Market Prices Do Not Follow Random Walks," *Review of Financial Studies* 1:41–66. https://www.jstor.org/stable/2962126 (abstract) + VR methodology https://mingze-gao.com/posts/lomackinlay1988 — variance-ratio test, short-horizon reversion.
- **[S370 | Tier 1]** Jegadeesh, N. (1990), "Short-Term Reversal in Stock Returns" (UCLA working paper, ~2%/mo reversal 1934–1987). Findings corroborated via Springer, NY Fed staff report 513, and Jegadeesh (1992); primary PDF not directly opened → numbers from independent secondary reproductions.
- **[S371 | Tier 1]** Hogan, S., Jarrow, R., Teo, M. & Warachka, M. (2004), "Testing Market Efficiency using Statistical Arbitrage…," *Journal of Financial Economics* 73(3):525–565. https://digitalcommons.chapman.edu/business_articles/123 — formal definition (abstract opened).
- **[S372 | Tier 1]** Lehmann, B. (1990), "Fads, Martingales, and Market Efficiency," *Quarterly Journal of Economics* 105:1–28 — weekly reversal (referenced via Avellaneda–Lee and secondary snippets; primary not directly opened).
- **[Tier 1, lead]** Poterba, J. & Summers, L. (1988), "Mean reversion in stock prices," *Journal of Financial Economics* 22:27–59 — *long-horizon* mean reversion (contrast with short-horizon); cited via Avellaneda–Lee bibliography, not directly opened.
- Companion KB articles: `05-stats-and-ml/cointegration-pairs-trading.md`, `05-stats-and-ml/stationarity-adf-autocorrelation.md`, `08-backtesting-methodology/transaction-costs-slippage-walkforward.md`, `15-pitfalls-and-antipatterns/*`.
