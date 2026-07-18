---
title: Fama–French Factor Models (3-Factor, 5-Factor, and Extensions)
topic_id: 04-quant-and-factors/fama-french-factors
tags: [factors, fama-french, size, value, profitability, investment, asset-pricing, smart-beta, momentum]
last_updated: 2026-07-18
confidence: contested
sources: [S205, S206, S207, S209, S210, S211, S212, S100, S164, S165, S72]
---

## TL;DR
- The Fama–French 3-factor model (1993) adds **size (SMB)** and **value (HML)** to the market factor; the 5-factor model (2015) further adds **profitability (RMW)** and **investment (CMA)**.
- Over the classic sample (Jul 1963–Dec 2013) the average monthly premiums were: market ~0.50%, SMB ~0.29%, HML ~0.37%, RMW ~0.25%, CMA ~0.33% (Fama–French 2015, Table 4). Annualized arithmetically that is roughly 6–7% market, 3–5% for each style factor.
- **Robust:** the model structure and historical description. **Contested:** whether these premiums persist forward — the size and value premiums have decayed badly since the 1980s/2007, while profitability (RMW) has held up best. Treat factor premiums as empirical regularities, not guaranteed forward returns.

## Core explanation
The Capital Asset Pricing Model (CAPM) explains expected returns with a single factor — market beta. Eugene Fama and Kenneth French showed (1992, 1993) that two **characteristic** portfolios — small-minus-big (SMB) and high-minus-low book-to-market (HML) — capture large chunks of average-return variation that CAPM's beta misses. Their three-factor model therefore augments CAPM with size and value.

In 2015 they added two more factors motivated by the dividend-discount identity: **operating profitability** (RMW, robust minus weak) and **investment** (CMA, conservative minus aggressive). A key result in their paper: once profitability and investment are included, the original value factor HML becomes largely **redundant** for describing average returns in their sample (Fama–French 2015, abstract).

Crucially, these are **empirical factor models**, not derived from a formal equilibrium the way CAPM is. They describe *what has been rewarded*; they do not by themselves prove *why*. Fama and French interpret the factors as proxies for state-variable risk (in the spirit of Merton's ICAPM); behavioral critics read the same premiums as compensation for underexploited mispricing. That interpretive conflict is unresolved.

### The factors (construction)
All factors are long-short, value-weighted portfolios formed by sorting US stocks (NYSE/AMEX/NASDAQ) on June market equity (ME) and accounting variables measured with a lag. Breakpoints use NYSE percentiles (median for size; 30th/70th for the characteristic). The 2×3 ("2&3") construction (Fama–French 2015, Table 3; Kenneth French Data Library):

- **Rm−Rf**: value-weighted market return minus the 1-month T-bill rate.
- **SMB** = ⅓·[SMB(B/M) + SMB(OP) + SMB(INV)], where e.g. SMB(B/M) = ⅓(Small Value + Small Neutral + Small Growth) − ⅓(Big Value + Big Neutral + Big Growth).
- **HML** = ½(Small Value + Big Value) − ½(Small Growth + Big Growth).
- **RMW** = ½(Small Robust + Big Robust) − ½(Small Weak + Big Weak), where OP = (revenues − COGS − SG&A − interest expense) / book equity.
- **CMA** = ½(Small Conservative + Big Conservative) − ½(Small Aggressive + Big Aggressive), where Inv = growth rate of total assets.

### Extensions (Momentum / Carhart)
Mark Carhart (1997) added a **momentum** factor — prior 12-month (skipping the most recent month) winner-minus-loser return, often called UMD or PR1YR — to form the widely used **4-factor** model (Rm−Rf, SMB, HML, MOM). Momentum is the most robust cross-sectional premium in the literature (see KB 03 / 14) but is conspicuously absent from the Fama–French factor set because it does not arise cleanly from their dividend-discount motivation.

## Math / formulas
The time-series regression for asset/portfolio *i*:

3-factor:
R_it − Rf_t = α_i + β_i (Rm_t − Rf_t) + s_i·SMB_t + h_i·HML_t + ε_it

5-factor:
R_it − Rf_t = α_i + β_i (Rm_t − Rf_t) + s_i·SMB_t + h_i·HML_t + r_i·RMW_t + c_i·CMA_t + ε_it

- β, s, h, r, c = factor loadings (sensitivities).
- **α_i** = intercept = average return *not* explained by the factors. In performance attribution, α ≈ skill; in asset pricing, a zero α for a broad set ofSorted portfolios supports the model.

The factors themselves are themselves returns (long-short portfolios), so the same model describes the factor premiums' own average returns (with loading 1 on themselves).

### Average historical premiums (Fama–French 2015, Table 4, 2&3 factors, Jul 1963–Dec 2013, 606 months)
| Factor | Mean monthly % | Std dev % | t-stat |
|---|---|---|---|
| Rm−Rf | 0.50 | 4.49 | 2.74 |
| SMB | 0.29 | 3.07 | 2.31 |
| HML | 0.37 | 2.88 | 3.20 |
| RMW | 0.25 | 2.14 | 2.92 |
| CMA | 0.33 | 2.01 | 4.07 |

All five are statistically distinguishable from zero at conventional levels in this sample, but the t-stats are modest (2–4), i.e. the premiums are real but noisy.

## Worked example / code
A reproducible, stdlib-only illustration: annualize the Table-4 monthly premiums and use the 5-factor equation to estimate the expected excess return of a hypothetical **value-and-quality-tilted** portfolio given its loadings. (Data: Fama–French 2015 Table 4 monthly means; annualization uses (1+m)^12−1.)

```python
# Fama-French 5-factor: historical premiums and a forward expected-return calc.
# Sources: monthly means from Fama-French (2015) Table 4 (2&3 factors, 1963-2013).
# Pure stdlib; deterministic.
factors = {
    "Rm-Rf": 0.50,   # % per month
    "SMB":   0.29,
    "HML":   0.37,
    "RMW":   0.25,
    "CMA":   0.33,
}

def annualize_pct(monthly_pct):
    return (1.0 + monthly_pct/100.0)**12 - 1.0

print("Historical annualized premiums (arithmetic-to-geometric, 1963-2013):")
ann = {k: annualize_pct(v) for k, v in factors.items()}
for k, a in ann.items():
    print(f"  {k:6s}: {factors[k]:.2f}%/mo -> {a*100:.2f}%/yr")

# Hypothetical portfolio loadings (betas) to the 5 factors.
loadings = {"Rm-Rf": 1.0, "SMB": 0.3, "HML": 0.5, "RMW": 0.2, "CMA": 0.1}
exp_excess_annual = sum(loadings[k] * ann[k] for k in factors)
rf_annual = 0.02  # assume 2% risk-free
exp_total_annual = exp_excess_annual + rf_annual
print(f"\nIllustrative portfolio expected excess return: {exp_excess_annual*100:.2f}%/yr")
print(f"Expected total return (rf=2%):            {exp_total_annual*100:.2f}%/yr")
```

Output (verified, stdlib-only):
```
Historical annualized premiums (arithmetic-to-geometric, 1963-2013):
  Rm-Rf: 0.50%/mo -> 6.17%/yr
  SMB:   0.29%/mo -> 3.54%/yr
  HML:   0.37%/mo -> 4.53%/yr
  RMW:   0.25%/mo -> 3.04%/yr
  CMA:   0.33%/mo -> 4.03%/yr

Illustrative portfolio expected excess return: 10.51%/yr
Expected total return (rf=2%):            12.51%/yr
```

**Caveat:** plugging historical loadings × historical premiums gives a *historical analog*, not a forecast. Estimating the loadings (the `s, h, r, c` coefficients) on real data requires the actual factor return series (Kenneth French Data Library CSVs) and a regression routine (statsmodels / numpy). The code above isolates the arithmetic so the magnitude is transparent and reproducible.

## Assumptions & limitations
- **Stationarity / non-stationarity:** the premiums are estimated over a specific 50-year window dominated by the US. Out-of-sample they are not stable — see Empirical Evidence.
- **Survivorship & look-ahead in replication:** naive factor backtests that sort on characteristics using *current* accounting data (not point-in-time) and ignore delisted firms overstate premiums (see KB 13/15).
- **Construction sensitivity:** the exact premium depends on sort breakpoints, weighting (value- vs equal-weight), and whether extremes (2×3) or NYSE medians (2×2) are used. Fama–French (2015) show means are similar across variants but not identical.
- **ICAPM interpretation is not testable in isolation:** like CAPM, the multi-factor model is a *description*; Roll's critique (unobservable true market portfolio) carries over, and a zero α does not prove the factors are "risk" (see KB 04/capm-beta).
- **Data revisions:** Akey et al. (2026, *Review of Finance*) find Fama–French factor returns differ materially depending on *when* the underlying CRSP data were pulled — a reminder that even "official" factor series are revision-sensitive.

## Empirical evidence
- **Three-factor model (1993):** size and value explain most of the cross-section that CAPM beta misses; controlling for size, the beta–return relation largely disappears (Fama–French 1992; Wikipedia/S210). The 3-factor model explains ~90% of diversified-portfolio return *variation* in-sample (Investopedia/S211), vs ~70% for CAPM.
- **Long-run cumulative records (CFA Institute, 2022 / S165):**
  - **SMB (size):** performed extremely well *to ~1982* (≈600% cumulative), then reversed (large beat small 1982–2000), rebounded modestly, and has stagnated for ~10–15 years. Clifford Asness ("There Is No Size Effect") argues the size premium is largely an artifact.
  - **HML (value):** historic run 1926–2007 with >4000% cumulative long-short return, then **lost about half its value after 2007** as growth outperformed. Arnott et al. argue much of the recent shortfall is a *definitional* artifact (book value ignores intangibles) plus a valuation plunge, not proof value is dead.
  - **RMW (profitability/quality):** the **single factor that has held up across all cycles since 1963** — going long profitable, short unprofitable firms has been consistently positive.
  - **CMA (investment):** worked for ~40 years, dissipated since ~2004; aggressive-investment firms have only modestly lagged since 2013.
- **Redundancy result:** Fama–French (2015) find that adding RMW and CMA makes HML's own average return largely *absorbed* by its exposures to the other four factors (especially RMW and CMA). This is a sample-specific, striking result they themselves flag as possibly period-dependent.
- **Momentum (Carhart 1997 / S209):** adding a 12-month momentum factor materially improves fit and is the most robust cross-sectional premium; it is the basis of the 4-factor performance model used widely in mutual-fund attribution.
- **Factor zoo:** Harvey, Liu & Zhu (2016 / S72) catalog ~316 "factors" in the published literature and argue the publication bar (|t| ≈ 2) is far too lax; a multiple-testing-adjusted cutoff of ~|t| ≈ 3 is more appropriate. Most published factors do not survive.
- **Challenge from q-theory (Hou, Mo, Xue & Zhang 2019, "Which Factors?" / S212):** the q-factor model (market, size, investment, profitability/ROE, expected growth) largely *subsumes* the Fama–French factors in spanning tests, and the FF factors fail to explain the q-factor premiums — i.e. the FF set may not be the most parsimonious description of average returns.

## Conflicting views
- **Risk vs mispricing:** Fama–French frame factors as state-variable risk proxies; behavioral finance (Shleifer, Baker–Wurgler) frames them as limits-to-arbitrage-exploitable mispricing. Both fit the same return patterns; the debate is about *cause*, which return data alone cannot settle.
- **Is HML dead or redundant?** Fama–French (2015) say redundant *within their 5-factor sample*; practitioners (and Arnott) argue HML still carries independent information and its post-2007 pain is a valuation/intangibles artifact, not a structural death.
- **Does the size premium exist?** Asness ("no size effect") vs. Alquist–Israel–Moskowitz ("Fact, Fiction, and the Size Effect," 2018) who show controlling for *quality* resurrects a linear, more uniform size premium. Contested.
- **Forward validity:** the 3/5-factor models are excellent *descriptive* tools but weak *predictive* ones. Damodaran treats Fama–French as useful for understanding *realized* returns, not for forward-looking cost-of-capital estimates (see KB 02/04).

## Common mistakes
- **Anchoring on historical premiums as forecasts.** The 4–5%/yr style premiums are in-sample averages; live, net-of-cost implementation has been poor for size/value since the 1980s/2007.
- **Treating α as pure skill without checking factor coverage.** A fund "beating the market" may simply load on HML/RMW; the 3/5-factor model is the right attribution baseline (Carhart 4-factor for momentum-aware funds).
- **Using HML as a clean "value" signal.** HML is not neutral to profitability/investment (Fama–French 2015 note it mixes B/M, OP, and Inv premiums) and ignores intangibles — a definitional blind spot in the post-2007 era.
- **Ignoring transaction costs and capacity.** Long-short factor portfolios turn over and can be capacity-constrained; the *gross* premiums above are before costs (see KB 08).
- **Data snooping in factor construction.** Choosing breakpoints, weighting, and the factor set to maximize historical fit is exactly the multiple-testing trap documented by Harvey–Liu–Zhu and Bailey–López de Prado (see KB 05/08/15).
- **Survivorship/look-ahead bias.** Sorting on *as-reported-later* accounting data or excluding delisted firms inflates every premium in this article.

## Further reading
- **Primary (Tier 1):**
  - Fama, E.F. & French, K.R. (1993), "Common Risk Factors in the Returns on Stocks and Bonds," *Journal of Financial Economics* 33:3–56 — the 3-factor model. [Kenneth French Data Library factor details: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html]
  - Fama, E.F. & French, K.R. (2015), "A Five-Factor Asset Pricing Model," *Journal of Financial Economics* 116:1–22 — primary PDF (Table 4 averages reproduced above): https://tevgeniou.github.io/EquityRiskFactors/bibliography/FiveFactor.pdf
  - Kenneth R. French Data Library, "Description of Fama/French 5 Factors (2x3)" (authoritative construction + live data): http://mba.tuck.dartmouth.edu/pages/faculty/Ken.french/Data_Library/f-f_5_factors_2x3.html
  - Carhart, M. (1997), "On Persistence in Mutual Fund Performance," *Journal of Finance* 52:57–82 (momentum/4-factor): https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1997.tb03808.x
  - Hou, Mo, Xue & Zhang (2019), "Which Factors?" *Review of Finance* 23(1) (q-factor challenge): https://theinvestmentcapm.com/uploads/1/2/2/6/122679606/houmoxuezhang2019rf.pdf
- **Reused Tier-1 in this KB:** Fama & French (1992) cross-section [S100]; Fama & French (2005) value premium [S164]; CFA Institute (Horstmeyer, Liu, Wilkins) 2022 "Five-Factor Model Revisited" [S165]; Harvey, Liu & Zhu (2016) factor zoo [S72].
- **Secondary (Tier 2):**
  - Wikipedia, "Fama–French three-factor model": https://en.wikipedia.org/wiki/Fama%E2%80%93French_three-factor_model
  - Investopedia, "Fama French Three Factor Model": https://www.investopedia.com/terms/f/famaandfrenchthreefactormodel.asp
- **Related KB articles:** 04-quant-and-factors/capm-beta (Roll's critique, beta flatness); 05-stats-and-ml/overfitting-lookahead & 08-backtesting-methodology/deflated-sharpe-multiple-testing (factor-zoo multiple testing); 13-data-and-tooling (point-in-time/survivorship-free data); 14-strategy-catalog/value-quality-strategies (live factor-strategy evidence); 15-pitfalls-and-antipatterns (survivorship, regime change).
