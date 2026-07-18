---
title: Data Sources, Libraries & Reproducibility
topic_id: 13-data-and-tooling/data-vendors-apis-libraries-reproducibility
tags: [data, vendors, APIs, libraries, reproducibility, yfinance, alphavantage, FRED, EDGAR, pandas, vectorbt, backtrader, zipline, pyportfolioopt, point-in-time, survivorship]
last_updated: 2026-07-18
confidence: robust
sources: [S149, S150, S151, S152, S153, S154, S155, S156, S157, S158, S62, S67, S74]
---

## TL;DR
- For **research-grade equity/fundamental data**, the free, authoritative sources are **SEC EDGAR** (filings, XBRL financials, free) and **FRED** (macro/time-series, free, with vintage tracking via ALFRED). For price series, **Alpha Vantage** and **yfinance** are free but limited, delayed, and (for yfinance) explicitly personal-use-only under Yahoo's terms.
- For **serious survivorship-free backtests**, CRSP/Compustat delivered through **WRDS** (paid) is the de-facto standard. Free price feeds silently exclude delisted names and use *current* index constituents, embedding look-ahead and survivorship bias that overstate returns by roughly **0.6%–4%+ per year**.
- **Reproducibility** is non-negotiable: pin library versions, set random seeds, version your raw data, and use point-in-time fundamentals. The library cookbook below (pandas/numpy/statsmodels core; vectorbt for speed; backtrader/zipline-reloaded for event-driven realism; PyPortfolioOpt for optimization) is runnable with the pinned deps shown.

## Core explanation
Every analysis in this KB rests on data and code. This article maps *where the data comes from*, *what libraries manipulate it*, and *how to make a result reproducible* so someone else (or future-you) can re-run it and get the same number.

**Three buckets of data source:**
1. **Free & authoritative (regulator / central bank).** SEC EDGAR (corporate filings, free public access to millions of documents, full-text search over 20+ years, plus RESTful EDGAR APIs for submission history and XBRL financial statements) [S152]; FRED (St. Louis Fed economic data via API v1/v2, with ALFRED providing historical *vintages* — i.e., the value as it was published on a given date, before revisions) [S151].
2. **Free but constrained (vendor/aggregator).** Alpha Vantage (free API key; 9 categories — core time series, indices, options, "Alpha Intelligence", fundamentals, FX, crypto, commodities, economic indicators; 20+ years of history; intraday is a premium endpoint; split/dividend adjustment on by default) [S150]; yfinance (open-source Python wrapper that *scrapes Yahoo's publicly available APIs*; Apache-2.0 licensed; **not affiliated, endorsed, or vetted by Yahoo**, intended for research/education, and Yahoo's terms limit use to personal use) [S149].
3. **Paid / institutional.** Bloomberg, Refinitiv/Eikon, FactSet, and CRSP/Compustat via WRDS. These are the only practical sources of **point-in-time, delisting-inclusive** US equity data needed to avoid the biases below.

**Library stack** (all verified against their official docs):
- **Core data wrangling:** pandas + NumPy + SciPy + statsmodels (ADF, Ljung–Box, regressions — see 05-stats-and-ml articles S62–S67).
- **Backtesting — vectorized:** **vectorbt** operates on pandas/NumPy objects accelerated by Numba and Rust, claiming thousands of strategy variants tested "in seconds" [S153]. Open-source core with advanced features behind a paid PRO tier.
- **Backtesting — event-driven:** **backtrader** is built around a `Cerebro` engine, a `Strategy` class, data feeds, and `cerebro.run()` / `cerebro.plot()` [S154]. **zipline-reloaded** is the community-maintained successor to Quantopian's engine; it is event-driven, integrates with pandas, supports `pipeline`-style research, requires Python ≥3.8, and its 3.0 release moved to pandas ≥2.0 [S155].
- **Portfolio optimization:** **PyPortfolioOpt** (MIT, v1.5.4) implements efficient-frontier methods, Black–Litterman, shrinkage estimators, and Hierarchical Risk Parity [S156].

## Math / formulas
**Total return from an adjusted close** (splits & dividends already baked in):
$$r_t = \frac{P^{\text{adj}}_t}{P^{\text{adj}}_{t-1}} - 1$$
Most free feeds (Alpha Vantage `adjusted=true`, yfinance `auto_adjust=True`) return this series directly.

**Annualized Sharpe** (used throughout the KB):
$$S = \frac{\bar r - r_f}{\sigma_r}\sqrt{252}$$

**Survivorship / look-ahead contamination (intuition).** Let the *true* universe at time $t$ be $U_t$ (including firms that later delist). A naive backtest using the *current* constituent list $U_T$ with $T \gg t$ computes
$$\hat\mu = \frac{1}{|U_T|}\sum_{i\in U_T} \mu_i$$
but the investable reality was $\mu^* = \frac{1}{|U_t|}\sum_{i\in U_t}\mu_i$ with $U_t \supset U_T$ on the downside. Because the excluded (delisted/bankrupt) names have $\mu_i \ll 0$, $\hat\mu > \mu^*$ — the backtest *overstates* the mean and *understates* drawdown. Independent sources place this gap at **~0.6%–4%+ per annum** (see Empirical evidence).

**Data fingerprinting (reproducibility).** Hash the raw input so a result can be tied to an exact dataset:
$$h = \text{SHA256}\big(\text{hash\_pandas\_object}(D)\big)$$
If two runs produce the same $h$ and the same seed, they are byte-for-byte reproducible.

## Worked example / code
Data source for the example: **Yahoo Finance via yfinance** (free; personal-use terms). Pin versions in your environment.

```text
# requirements.txt  — freeze exact versions in YOUR env with:  pip freeze > requirements.txt
pandas>=2.0            # zipline-reloaded 3.0 requires pandas>=2.0 [S155]
numpy>=1.24
yfinance>=0.2.40       # verify latest on PyPI; Apache-2.0, not Yahoo-affiliated [S149]
statsmodels>=0.14      # ADF / Ljung-Box (S62-S67)
scipy>=1.10
# Install backtesting/optimization per their official docs:
#   vectorbt            # vectorized, Numba/Rust  [S153]
#   backtrader          # event-driven Cerebro   [S154]
#   zipline-reloaded    # conda-forge; pandas>=2.0 [S155]
#   pyportfolioopt==1.5.4  # MIT                  [S156]
```

```python
import yfinance as yf
import pandas as pd

TICKERS = ["AAPL", "MSFT", "SPY"]
START, END = "2018-01-01", "2022-12-31"

def load_prices(tickers, start, end) -> pd.DataFrame:
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
    close = raw["Close"] if isinstance(raw["Close"], pd.DataFrame) else raw[["Close"]]
    return close.dropna(how="any")

prices = load_prices(TICKERS, START, END)          # source: Yahoo Finance via yfinance
rets = prices.pct_change().dropna()
ann_sharpe = (rets.mean() / rets.std()) * 252 ** 0.5
print(ann_sharpe.round(3))
```

**Reproducibility harness** (pure stdlib — verified to run deterministically; replace the synthetic draws with your real loader):

```python
import hashlib, random, math, statistics

def set_seed(seed=42):
    random.seed(seed)

def arr_hash(vals):
    b = b"".join(bytes(repr(v), "utf-8") for v in vals)
    return hashlib.sha256(b).hexdigest()[:16]

def gen(seed):                     # synthetic Box-Muller returns; NOT market data
    set_seed(seed)
    out = []
    for _ in range(252):
        u1, u2 = random.random(), random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        out.append(0.0005 + 0.01 * z)
    return out

a, b, c = gen(42), gen(42), gen(7)
print("deterministic (same seed):", arr_hash(a) == arr_hash(b))   # True
print("differs (other seed)    :", arr_hash(a) != arr_hash(c))   # True
```

## Assumptions & limitations
- **Free price feeds are not point-in-time and are not delisting-inclusive.** yfinance/Alpha Vantage return *currently listed* series; a backtest that selects "all S&P 500 stocks" using today's list is contaminated by look-ahead (the constituents changed over time) and survivorship (dead names are missing). Remedy: CRSP/Compustat (WRDS) with delisting returns and historical index membership.
- **yfinance is a scraper.** It depends on Yahoo's undocumented endpoints and breaks when Yahoo changes them; it is explicitly personal-use-only under Yahoo's terms of service — not for commercial products [S149].
- **Adjusted series hide corporate actions** only to the extent the vendor handles them; verify split/dividend adjustment before trusting multi-year returns.
- **Macro data is revised.** A 2020 "GDP" print differs from the 2024 revision. For regime/nowcasting work use **ALFRED vintages** [S151], not the latest FRED value.
- **Library version drift is real.** zipline-reloaded 3.0's jump to pandas ≥2.0 is a breaking change [S155]; PyPortfolioOpt needs a C++ toolchain and cvxpy/cvxopt [S156]. Unpinned environments silently diverge.

## Empirical evidence
- **Survivorship bias magnitude is well documented and material.** Dimensional (2021) finds that for actively managed US equity mutual funds (1991–2020), survivorship bias overstates the median fund alpha by **0.60% per year (≈60 bps)** — roughly half the size of the survivorship-free median alpha [S158]. Luxalgo summarizes practitioner estimates that excluding defunct stocks overstates annual returns by **1%–4%** and can understate drawdown by ~14% [S157]. Two independent opened sources corroborate a *material* (sub-1% to several-%-per-year) inflation — treat any free-data equity backtest as an *upper bound* on real performance.
- **Look-ahead benchmark bias** (using end-of-period index constituents instead of point-in-time membership) is a distinct but related contamination; academic work on CRSP 1926–2006 estimates it can reach **up to ~8% per annum** for an S&P 500 benchmark [background, see Further reading — primary not directly opened in this iteration].
- **FRED/ALFRED** is the standard free macro source and explicitly supports vintage/real-time tracking, which is why revision-aware studies prefer it [S151].

## Conflicting views
- **"Free data is good enough."** True for *learning and signal exploration*; false for *performance claims*, where missing delistings and current-constituent selection inflate results (see above). Practitioners split: retail researchers use yfinance/Alpha Vantage; institutional researchers pay for CRSP/Compustat.
- **Vectorized vs event-driven backtesting.** vectorbt wins on speed and parameter sweeps [S153]; backtrader/zipline-reloaded win on realistic, path-dependent event handling and live-trading parity [S154][S155]. The "right" tool depends on whether you need *throughput* (research) or *fidelity* (production).
- **Open-source optimization vs black-box.** PyPortfolioOpt is transparent and MIT-licensed [S156]; commercial optimizers add support and data but obscure methodology. For a KB built on showing the math, open source is preferred.

## Common mistakes
1. **Not pinning versions** — `pandas` 1.x vs 2.x breaks zipline and many indicators; freeze with `pip freeze`.
2. **Using current index constituents** as the historical universe → look-ahead bias (ties to 15-pitfalls look-ahead article S74).
3. **Dropping delisted firms** → survivorship bias inflates returns (above).
4. **Trusting "adjusted close" blindly** without checking split/dividend handling across the vendor.
5. **Using the latest FRED value for past regimes** instead of ALFRED vintages → revision look-ahead.
6. **Relying on a single vendor without cross-check** (e.g., yfinance vs Alpha Vantage vs EDGAR XBRL) — gaps and errors are common.
7. **Violating Yahoo's terms** by building a commercial product on yfinance [S149].

## Further reading
- **Tier 1 (official / regulator):**
  - SEC EDGAR & EDGAR APIs — https://www.sec.gov/edgar/searchedgar/companysearch [S152]
  - FRED API (St. Louis Fed), incl. ALFRED vintages — https://fred.stlouisfed.org/docs/api/fred/ [S151]
  - Alpha Vantage API docs — https://www.alphavantage.co/documentation/ [S150]
  - yfinance (GitHub, Apache-2.0) — https://github.com/ranaroussi/yfinance [S149]
  - vectorbt docs — https://vectorbt.dev [S153]; backtrader docs — https://www.backtrader.com/docu/ [S154]; zipline-reloaded — https://zipline.ml4trading.io [S155]; PyPortfolioOpt — https://pyportfolioopt.readthedocs.io/en/latest/ [S156]
- **Tier 2 (practitioner):**
  - Dimensional, "Why Worry About Survivorship Bias?" — https://www.dimensional.com/us-en/insights/why-worry-about-survivorship-bias [S158]
  - Luxalgo, "Survivorship Bias in Backtesting Explained" — https://www.luxalgo.com/blog/survivorship-bias-in-backtesting-explained [S157]
  - Investopedia, "Survivorship Bias" — https://www.investopedia.com/terms/s/survivorshipbias.asp
- **Classic academic (further verification):** Elton, Gruber & Blake (1996), "Survivorship Bias and Mutual Fund Performance" (Journal of Business) — early estimate of ~1.4% annual overstatement; C.A. Cowell et al., "Look-Ahead Benchmark Bias" (arXiv 0810.1922) — up to ~8%/yr for S&P 500 benchmarks (primary PDF not opened this iteration → Verify before asserting the exact figure).
- **KB cross-links:** 15-pitfalls-and-antipatterns/data-snooping-phacking.md (multiple-testing), 05-stats-and-ml/overfitting-lookahead.md (look-ahead), 08-backtesting-methodology/* (costs, walk-forward, deflated Sharpe).
