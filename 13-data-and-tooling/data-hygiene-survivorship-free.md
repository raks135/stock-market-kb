---
title: Data Hygiene & Survivorship-Free Datasets
topic_id: 13-data-and-tooling/data-hygiene-survivorship-free
tags: [data-hygiene, survivorship-bias, point-in-time, corporate-actions, delisting-returns, back-adjustment, data-quality]
last_updated: 2026-07-18
confidence: robust
sources: [S350, S351, S352, S353, S354, S355, S157, S158, S160, S152, S151]
---

## TL;DR
- Survivorship bias (using only currently-listed names) inflates backtested returns by roughly **1–4%/yr** and hides the left tail: vendor/academic studies report a survivorship-free US equity series at ~7.4%/yr vs ~9.0% biased, Sharpe inflation up to ~0.5, and drawdown underestimation of ~14 percentage points [S157].
- The fixes are mechanical and non-negotiable: build the universe **point-in-time** (include delisted/dead names and their delisting returns), **back-adjust** prices for splits/dividends/spin-offs, and source **as-of-date** fundamentals (not restated "as-reported" data).
- A diversifying 500-name index dilutes the *average* effect; the damage is worst in concentrated/selection strategies and in single-name risk, where a survivors-only dataset can understate the share of names losing >50% by **5–7x** (demonstrated below).

## Core explanation
**Data hygiene** is the discipline of making a historical dataset faithfully represent what an investor could have known and held at each past date. It sits upstream of every backtest: no amount of clever strategy logic survives a contaminated input. The two dominant contamination channels in equity research are **survivorship bias** and **look-ahead / revision bias**, plus a cluster of **corporate-action and quality defects** (wrong adjustments, stale prices, phantom precision, timezone/FX mismatches).

**Survivorship bias** occurs when the dataset silently drops securities that disappeared — bankruptcies, liquidations, mergers, delistings, acquisitions. Because disappearing firms are disproportionately the *losers*, excluding them trims the left tail of the return distribution: mean returns rise, volatility and drawdowns fall, and any selection rule that "would have picked winners" is tested only against other winners [S157]. A current-only database (e.g., a ticker list scraped "today") is inherently survivorship-biased because it contains only names that survived to today.

**Look-ahead / revision bias** occurs when a field's *current* value is used as if it were known on the simulation date. This hits fundamentals hardest: a 2026 restatement of 2018 earnings, or a 2026 index-membership change, leaks future information into a 2018 signal. The remedy is **point-in-time (PIT)** data — the value exactly as it stood on each historical date [S354][S355].

**Corporate-action bias** occurs when prices are not adjusted for splits, dividends, spin-offs, and mergers, so a 2-for-1 split looks like a −50% crash and dividend payments look like losses [S351].

## Math / formulas

**Survivorship bias (intuition).** Let the true return distribution at time *t* over the full investable set be the mixture of survivors and delisted names. A biased sample uses only the survivor subset *S_t*:
$$ \bar r^{\text{biased}}_t = \frac{1}{|S_t|}\sum_{i\in S_t} r_{i,t} \;>\; \bar r^{\text{true}}_t = \frac{1}{N_t}\sum_{i=1}^{N_t} r_{i,t} $$
because the excluded delisted returns $r_{i,t}$ are systematically negative (bankruptcy, forced delisting). The inequality is a statement about omitted negative mass, not noise.

**Delisting return (CRSP).** The return realized at the moment a security leaves the listing, comparing the post-delisting value (price on another venue, cash/distribution paid, or zero if declared worthless) to the last trading-date price [S350][S351]:
$$ \text{DLRET} = \frac{P_{\text{after delist}} - P_{\text{last trade}}}{P_{\text{last trade}}}, \qquad \text{DLRETX} = \text{same without dividends} $$
CRSP stores `DLSTCD` (delisting *code* — why it left: merger, bankruptcy, liquidation, etc.) and `DLRET`/`DLRETX` (with/without dividends). When post-delisting information is insufficient, the return is reported missing and the researcher must impute (commonly using the distributions/merger consideration or treating as a total loss) — the choice materially changes results [S350][S352].

**Back-adjustment (CRSP convention).** All data are made comparable to a base (anchor) date via a cumulative adjustment factor $C(t)$:
$$ A(t) = \frac{P(t)}{C(t)} \quad\text{(prices/dividends)},\qquad A(t)=P(t)\cdot C(t)\quad\text{(shares/volume)} $$
where $C(t)=1$ at the anchor and accumulates split/dividend factors [S351]. The total (dividend-inclusive) return between $t-1$ and $t$ using adjusted prices is:
$$ R_t = \frac{\text{adjprc}_t + \text{divamt}_t /(\text{cumfacpr}\cdot\text{facpr})}{\text{adjprc}_{t-1}} - 1 $$
This recovers the true economic return across a split/dividend instead of the spurious −47.6% a naive $(55-105)/105$ would show (worked example below) [S351].

**Point-in-time signal (definition).** A signal $s_t$ is point-in-time correct iff it uses only information $\mathcal{I}_{\le t}$ available on or before *t*:
$$ s_t = f\big(\mathcal{I}_{\le t}\big), \quad \mathcal{I}_{\le t} \text{ excludes restatements, future membership, future revisions} $$
EDGAR preserves each filing *as originally submitted* and tracks amendments separately, so PIT fundamentals can be reconstructed from 10-K/10-Q as-filed [S152]; FRED's **ALFRED** preserves macro vintages so a 2008 GDP print is the 2008 estimate, not today's revision [S151].

## Worked example / code
Pure-stdlib Python (CPython 3.14.4), deterministic via `seed(42)`. It simulates 500 stocks over 240 months; 40% delist at a random month with a mostly-negative delisting return. Two universes are compared: a **survivorship-free** portfolio (holds every name, realizes delisting losses) vs a **survivorship-biased** portfolio (a "current-only" database that only ever shows the 301 never-delisted names).

```python
import random, math

random.seed(42)
N, T, mu, sigma = 500, 240, 0.008, 0.06
stocks = []                       # (delist_month, delist_return); > T means never delists
for i in range(N):
    if random.random() < 0.4:
        dmonth = random.randint(1, T - 1)
        dret = random.uniform(-0.8, -0.3) if random.random() < 0.5 else random.uniform(-0.3, 0.1)
    else:
        dmonth, dret = T + 1, 0.0
    stocks.append((dmonth, dret))

def max_drawdown(series):
    peak, mdd = series[0], 0.0
    for v in series:
        peak = max(peak, v); mdd = min(mdd, (v - peak) / peak)
    return mdd

v_free = v_bias = 1.0
free_series, bias_series = [1.0], [1.0]
for t in range(T):
    free_univ = [i for i in range(N) if stocks[i][0] > t]      # still alive at start of month t
    fr = [stocks[i][1] if stocks[i][0] == t + 1 else random.gauss(mu, sigma) for i in free_univ]
    v_free *= (1 + sum(fr) / len(fr)); free_series.append(v_free)

    bias_univ = [i for i in range(N) if stocks[i][0] > T]      # only names visible in a current-only DB
    br = [random.gauss(mu, sigma) for _ in bias_univ]
    v_bias *= (1 + sum(br) / len(br)); bias_series.append(v_bias)

cagr = lambda v, m: (v ** (12.0 / m)) - 1.0
print(f"FREE CAGR={cagr(v_free,T)*100:.2f}%  MaxDD={max_drawdown(free_series)*100:.2f}%")
print(f"BIAS CAGR={cagr(v_bias,T)*100:.2f}%  MaxDD={max_drawdown(bias_series)*100:.2f}%")

# Risk channel: catastrophic single-name outcomes hidden by survivors-only data
def terminal(i, rng):
    dm, dret = stocks[i]; w = 1.0; m = T if dm > T else dm
    for t in range(m):
        w *= (1 + (dret if (dm <= T and t == dm - 1) else rng.gauss(mu, sigma)))
    return w
rng = random.Random(7)
surv = [terminal(i, rng) for i in range(N) if stocks[i][0] > T]
alln = [terminal(i, rng) for i in range(N)]
cat = lambda xs: sum(1 for w in xs if w < 0.5) / len(xs)
print(f"Share losing >50%: survivors-only={cat(surv)*100:.1f}%  all-inclusive={cat(alln)*100:.1f}%")

# CRSP-style back-adjustment across a 2:1 split + $1 dividend
raw = {0: 100.0, 1: 105.0, 2: 55.0}; C = {0: 1.0, 1: 1.0, 2: 0.5}   # split halves raw price at t=2
adj = {t: raw[t] / C[t] for t in raw}
tot = (adj[2] + 1.0) / adj[1] - 1.0
print("Adjusted prices:", adj, " Total return t1->t2:", round(tot*100, 2), "%")
```
**Verified output (CPython 3.14.4, seed 42):**
```
FREE CAGR=9.19%  MaxDD=-0.29%
BIAS CAGR=10.17% MaxDD=-0.36%
Share losing >50%: survivors-only=1.0%  all-inclusive=6.6%
Adjusted prices: {0: 100.0, 1: 105.0, 2: 110.0}  Total return t1->t2: 5.71%
```
Interpretation: the biased (survivors-only) portfolio shows a **~1.0 pp/yr higher CAGR** — squarely inside the 1–4%/yr range reported in the literature [S157][S158] — while the share of names that lost more than half their value is **~6.6x understated** (6.6% vs 1.0%). In a 500-name equal-weight index the *average* drawdown is diluted to near-zero (law of large numbers), which is exactly why the 14pp drawdown-understatement figure from hedge-fund-database studies [S157] is a *concentrated-strategy* effect, not an index effect — a point often missed when people dismiss survivorship bias as "small." The back-adjustment block shows adjusted prices 100→105→110 (comparable) and a true **+5.71%** total return versus the **−47.6%** a naive raw-price calculation would falsely report.

## Assumptions & limitations
- **The simulation is synthetic** (seeded RNG, Gaussian monthly returns, stylized delisting). It demonstrates *direction and mechanism*, not a market magnitude; the cited 1–4%/yr, 0.6%/yr, 0.5 Sharpe, and 14pp figures come from the opened vendor/academic sources, not from this toy.
- **Delisting returns are often missing** in practice. CRSP reports them when post-delisting price/distribution info exists; otherwise the researcher imputes, and the imputation rule is a modeling choice that shifts results [S350][S352]. Treating a missing delisting return as 0 (total loss) vs. ignoring the name gives different answers.
- **Point-in-time fundamentals are expensive.** Free sources (Yahoo/finviz scrapes) are typically *restated/as-reported*, i.e., look-ahead contaminated; PIT data (Compustat Point-in-Time, FactSet, S&P Capital IQ) sits behind paid licenses [S152][S354][S355].
- **Adjustment factors can be wrong or late** (corporate actions reported with lag, spin-offs mis-coded), and **phantom precision** (CRSP notes 4-byte floats rendered $138.46 as 138.46001) can create spurious "signals" in naive pipelines [S350].
- **Even PIT data has a vintage**: the *filing date* (when info became public) not the fiscal period end is the tradable event; using fiscal-period-end prices with as-filed values is itself a mild look-ahead.

## Empirical evidence
- **Return inflation, 1–4%/yr.** Excluding defunct stocks overstates annual returns by ~1–4% across studies; a widely cited CRSP-based figure is **7.4% survivorship-free vs 9.0% biased (1926–2001)**, a 1.6 pp gap [S157]. Dimensional reports a **0.60%/yr** overstatement in a representative test [S158]. LuxAlgo summarizes practitioner estimates of 4–6%/yr in aggressive cases [S157]. (Robust direction; magnitude depends on universe, period, and selection rule.)
- **Risk metrics understated.** Brown, Goetzmann, Ibbotson & Ross find survivorship can inflate Sharpe ratios by up to ~0.5; Andrikogiannopoulou & Papakonstantinou find ~14 percentage-point drawdown *under*-estimation in hedge-fund databases; Bianchi & Koutmos find ~2.1%/yr mutual-fund overstatement concentrated in 2008 [S157]. (These are concentrated-strategy/manager-database effects, not index effects — see limitations.)
- **Look-ahead bias is large too.** Cowell et al. (arXiv:0810.1922) estimate look-ahead contamination in naive market simulations on the order of ~8%/yr [S160] — *flagged Verify*: the exact figure is cited via abstract/snippet-level access, not a fully opened primary; promote to Tier 1 only after opening the PDF.
- **Corporate-action adjustment is non-trivial.** CRSP's own methodology documents the split/dividend adjustment math and the delisting-return construction in detail, confirming these are first-class data-engineering steps, not optional [S350][S351].

## Conflicting views
- **"Survivorship bias is small, so who cares."** True *only* for broadly diversified buy-and-hold indices, where the omitted left tail is diluted. For **selection/stock-picking/concentrated** strategies — the entire point of most quant research — the bias is first-order and can flip a losing strategy to "profitable" in backtest (the LuxAlgo-cited QIM case: projected 20% vs realized 8% once bias was corrected) [S157].
- **"Free data (Yahoo etc.) is fine for research."** Acceptable for *illustration* and liquid large-caps, but these feeds are survivorship-biased (only currently listed) and restated (look-ahead in fundamentals), so they are unsuitable for performance claims or selection strategies [S152][S354].
- **"Just drop missing delisting returns."** Dropping them *is* the bias; the correct move is to include the name with an imputed/observed delisting return, or at minimum bounds the sensitivity to the imputation rule [S350][S352].
- **Magnitude disagreement** (0.6% vs 4–6%/yr) is reconciled by realizing it is a function of universe breadth, selection intensity, and period — there is no single number; report the *range* and your own corrected-vs-biased comparison.

## Common mistakes
- Building the backtest universe from a **current index membership or ticker list** (e.g., "all S&P 500 names today" applied to 1990) — this is pure survivorship bias; reconstruct membership **point-in-time** from index historical-constituents files [S157].
- Using **restated "as-reported"** fundamentals instead of **point-in-time** filings — injects future revisions into past signals [S152][S354][S355].
- Trading on **raw (unadjusted) prices**, so splits/dividends appear as crashes and the strategy "learns" the wrong thing [S351].
- **Dropping delisted names or their missing returns** rather than modeling the delisting loss [S350][S352].
- Treating **price-return** indices (no dividends) as total return, overstating the gap to a dividend-reinvesting strategy [S351].
- Ignoring **data revisions**: re-running a "finished" backtest a year later on a revised dataset and trusting the change as signal rather than as revision noise (a 2025 working paper finds CRSP rewrote ~9.6% of monthly returns in a 2025 tape transition — *Verify*: full text not opened, cite as a lead only).
- **Over-aggressive tick/cleaning filters** that delete informative outliers (e.g., real price dislocations) as "errors" — QuantPedia warns this can strip exactly the trades that matter [S353].
- Forgetting **timezones, FX, and corporate-action timing** when mixing cross-listed or multi-currency instruments.

## Further reading
- **S350** CRSP, *US Stock & Indexes Databases* (flat-file layout; `DLSTCD`, `DLRET`/`DLRETX`, distributions `FACPR`/`FACSHR`, missing-value convention, double-precision note) — https://www.crsp.org/wp-content/uploads/2023/10/crsp_us_stock.pdf (Tier 1, opened)
- **S351** UMich/CRSP, *CRSP Calculations* (adjustment formulas $A(t)=P(t)/C(t)$, total-return formula, delisting-return definition) — https://leiq.bus.umich.edu/docs/crsp_calculations_splits.pdf (Tier 1, opened)
- **S352** WRDS, *CRSP Useful Variables* (how delisting returns are calculated, missing-delisting handling, market-cap computation) — https://wrds-www.wharton.upenn.edu/pages/grid-items/crsp-useful-variables (Tier 1, opened)
- **S157** LuxAlgo, *Survivorship Bias in Backtesting Explained* (CRSP 7.4% vs 9.0%, Sharpe 0.5, drawdown 14pp, QIM 8% vs 20%) — https://www.luxalgo.com/blog/survivorship-bias-in-backtesting-explained (Tier 2, opened)
- **S158** Dimensional, survivorship-bias note (0.60%/yr overstatement) — see registry (Tier 2, opened)
- **S152** SEC EDGAR (as-filed filings + amendments = point-in-time fundamentals) — https://www.sec.gov/edgar (Tier 1, opened)
- **S151** FRED / ALFRED (macro vintages for point-in-time) — https://fred.stlouisfed.org/docs/api/fred/ (Tier 1, opened)
- **S160** Cowell, G. et al., "Look-ahead bias in market simulations," arXiv:0810.1922 — https://arxiv.org/abs/0810.1922 (Tier 1 preprint; **Verify**: exact ~8%/yr figure unconfirmed against full text)
- **S353** QuantPedia, *Working with High-Frequency Tick Data – Cleaning the Data* — https://quantpedia.com/working-with-high-frequency-tick-data-cleaning-the-data (Tier 2, opened)
- **S354** FactSet, *Fundamentals Point-in-Time* — https://www.factset.com/marketplace/catalog/product/factset-fundamentals-point-in-time (Tier 2, opened)
- **S355** S&P Global, *Fundamental Data* (point-in-time, "preserve the historical record as it existed on each date") — https://www.spglobal.com/market-intelligence/en/solutions/products/fundamental-data (Tier 2, opened)
- López de Prado, M. (2018), *Advances in Financial Machine Learning* — Ch. 13 (backtest overfitting) and data-leakage chapters; quote on leakage sourced via S157. Foundational on PIT/leakage discipline.
- Cross-links: `13-data-and-tooling/data-vendors-apis-libraries-reproducibility.md` (vendor landscape), `05-stats-and-ml/overfitting-lookahead.md`, `15-pitfalls-and-antipatterns/data-snooping-phacking.md`, and the forthcoming `15-pitfalls-and-antipatterns/survivorship-bias.md`.
