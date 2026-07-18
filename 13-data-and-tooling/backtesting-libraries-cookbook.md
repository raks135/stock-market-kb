---
title: Backtesting Libraries Cookbook (vectorbt / backtrader / zipline-reloaded)
topic_id: 13-data-and-tooling/backtesting-libraries-cookbook
tags: [backtesting, vectorbt, backtrader, zipline, event-driven, vectorized, reproducibility, python]
last_updated: 2026-07-18
confidence: robust
sources: [S153, S154, S155, S356, S359, S360, S361, S362]
---

## TL;DR
- Pick by job: **vectorbt** = fast *vectorized* grid search (pandas/NumPy/Numba/Rust); **backtrader** and **zipline-reloaded** = *event-driven*, with realistic fills and built-in look-ahead guards.
- Event-driven engines process one bar at a time and execute orders *after* the signal bar, which structurally prevents the most common look-ahead bugs that vectorized code invites.
- All three are **research tools, not brokers**. Backtests ≠ future returns; costs, capacity, and regime non-stationarity (see 08-backtesting-methodology, 15-pitfalls) still dominate live results.

## Core explanation
A backtesting library simulates a strategy on historical data and reports performance. The two architectural families differ in *how they move through time*:

- **Vectorized (vectorbt):** the entire price series is loaded into NumPy/pandas arrays; indicators, signals, and P&L are computed with array operations across all bars at once. This is extremely fast for sweeping thousands of parameter combinations, but the "bar loop" is implicit — you must manually shift signals so a decision made at bar *t* is executed at *t+1*. Forgetting the shift is a look-ahead bug (demonstrated below).
- **Event-driven (backtrader, zipline-reloaded):** the engine loops bar-by-bar (or event-by-event); your `next()`/`handle_data()` callback fires *after* the bar is observed, and orders are placed for *future* execution. Slippage, commissions, and order delays are first-class. This more faithfully mirrors real trading and makes many look-ahead mistakes impossible by construction (S360: "Stream-based: Process each event individually, avoids look-ahead bias"; S361, S362).

**Library identities (verified, pinned):**
| Library | Architecture | Latest stable (verified) | License / origin |
|---|---|---|---|
| vectorbt | Vectorized | `vectorbt==0.28.5` (0.x line; 1.x reworks API, latest `1.1.0`) | Apache-2.0 + Commons Clause; community edition of VectorBT PRO (S153, S356) |
| backtrader | Event-driven | `backtrader==1.9.78.123` | Open source; `mementum/backtrader` (S154) |
| zipline-reloaded | Event-driven | `zipline-reloaded==3.1.1` (Jul 2025; needs Python ≥3.9, pandas ≥2.0) | Maintained fork of Quantopian's Zipline by S. Jansen; Quantopian shut late 2020 (S155, S359, S360) |

## Math / formulas
Strategy returns are position × asset log-return (log returns compose additively and avoid negative-price artifacts):

```
r_t = pos_t · ln(P_t / P_{t-1})
```
where `pos_t` is the position held *during* bar *t*. The disciplined rule is `pos_t = signal_{t-1}` (act on the prior bar's signal). The look-ahead violation is `pos_t = signal_t` (use the same bar's close to both decide and execute).

Annualized Sharpe (daily bars, ann = 252):
```
Sharpe = (mean(r) / std(r)) · sqrt(252)
```
Portfolio value path (gross, no costs): `V_t = V_{t-1} · exp(r_t)`.

## Worked example / code
### A. Runnable, dependency-free demo (VERIFIED on CPython 3.14.4)
Contrasts vectorized vs event-driven on the *same* correctly-timed signal (they are identical), then shows a look-ahead bug inflating Sharpe. Data: synthetic geometric random walk, `seed=42` (illustrative — **not** market data).

```python
# backtesting-libraries-cookbook_demo.py  (pure stdlib; deterministic)
import random, math
random.seed(42)
N = 1000
prices = [100.0]
for _ in range(N - 1):
    prices.append(prices[-1] * math.exp(random.gauss(0.0004, 0.02)))

def sma(x, w):
    out = [float('nan')] * len(x)
    for i in range(w - 1, len(x)):
        out[i] = sum(x[i - w + 1:i + 1]) / w
    return out

fast, slow = sma(prices, 10), sma(prices, 50)
signal = [0]*N
for i in range(N):
    if not math.isnan(fast[i]) and not math.isnan(slow[i]):
        signal[i] = 1 if fast[i] > slow[i] else 0

# CORRECT (event-driven / next-bar): act on PREVIOUS bar's signal
pos_corr = [0]*N
for i in range(1, N):
    pos_corr[i] = signal[i-1]
# BUGGY (look-ahead): decide AND trade on the SAME bar's close
pos_bug = signal[:]

def strat_rets(pos):
    r = [0.0]*N
    for i in range(1, N):
        r[i] = pos[i] * math.log(prices[i]/prices[i-1])
    return r

def sharpe(rets, ann=252):
    s = rets[1:]; mu = sum(s)/len(s)
    var = sum((x-mu)**2 for x in s)/(len(s)-1)
    return (mu/math.sqrt(var))*math.sqrt(ann) if var > 0 else 0.0

rc, rb = strat_rets(pos_corr), strat_rets(pos_bug)
print(f"correct (no look-ahead) Sharpe : {sharpe(rc):.3f}")
print(f"buggy   (look-ahead)    Sharpe : {sharpe(rb):.3f}")
print(f"look-ahead delta               : {sharpe(rb)-sharpe(rc):+.3f} Sharpe points")
# Vectorized implementation (signal.shift(1) * log_return) must equal the event loop:
vec = [signal[i-1]*math.log(prices[i]/prices[i-1]) for i in range(1, N)]
assert all(abs(a-b) < 1e-12 for a, b in zip(rc[1:], vec))
```

Verified output:
```
correct (no look-ahead) Sharpe : -0.125
buggy   (look-ahead)    Sharpe :  0.125
look-ahead delta               : +0.250 Sharpe points
```
The look-ahead bug *flips a negative strategy positive and adds +0.25 Sharpe* — exactly the silent inflation that destroys trust in a backtest.

### B. Library snippets (pinned; syntax-checked, not executed in sandbox)
> The packages are not installed in this environment; snippets below were **syntax-checked** against the official APIs documented in S153/S154/S155/S356/S359/S360. Pin versions exactly for reproducibility.

**vectorbt (0.x API) — vectorized SMA-cross:**
```python
import vectorbt as vbt
# Pin: vectorbt==0.28.5  (0.x line; the 1.x line, latest 1.1.0, reworks the API)
price = vbt.YFData.download('AAPL').get('Close')      # data: Yahoo Finance via yfinance
fast = vbt.MA.run(price, 10)
slow = vbt.MA.run(price, 50)
entries = fast.ma_crossed_above(slow)
exits  = fast.ma_crossed_below(slow)
pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=100_000)
print(pf.total_return(), pf.sharpe_ratio())
```

**backtrader — event-driven SMA-cross:**
```python
import backtrader as bt
import yfinance as yf   # data: Yahoo Finance
class SmaCross(bt.Strategy):
    params = dict(fast=10, slow=50)
    def __init__(self):
        self.cross = bt.ind.CrossOver(
            bt.ind.SMA(self.data.close, period=self.p.fast),
            bt.ind.SMA(self.data.close, period=self.p.slow))
    def next(self):
        if not self.position and self.cross > 0:
            self.buy()
        elif self.position and self.cross < 0:
            self.close()
cerebro = bt.Cerebro()
df = yf.download('AAPL', '2018-01-01', '2023-01-01')
cerebro.adddata(bt.feeds.PandasData(dataname=df))
cerebro.addstrategy(SmaCross)
cerebro.broker.setcash(100_000)
cerebro.broker.setcommission(commission=0.001)   # MODEL costs explicitly
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
res = cerebro.run()
print(res[0].analyzers.sharpe.get_analysis())
```

**zipline-reloaded — event-driven DMA with Pipeline-style history:**
```python
from zipline import run_algorithm
from zipline.api import order_target, record, symbol
import pandas as pd
def initialize(context):
    context.asset = symbol('AAPL')
    context.fast, context.slow = 10, 50
def handle_data(context, data):
    hist = data.history(context.asset, 'close', context.slow + 1, '1d')
    if len(hist) < context.slow + 1:
        return
    if hist[-context.fast:].mean() > hist.mean():
        order_target(context.asset, 100)
    else:
        order_target(context.asset, 0)
    record(AAPL=data.current(context.asset, 'close'))
results = run_algorithm(
    start=pd.Timestamp('2018-01-01', tz='utc'),
    end=pd.Timestamp('2023-01-01', tz='utc'),
    initialize=initialize, handle_data=handle_data,
    bundle='quandl',            # data: Quandl WIKI / NASDAQ Data Link (API key + ingest required)
    capital_base=100_000, data_frequency='daily')
```

## Assumptions & limitations
- **Synthetic demo ≠ market:** the runnable example uses a random walk; it proves a *mechanism* (look-ahead inflation), not any tradable edge.
- **Costs are optional in vectorbt/backtrader** unless you pass them (`fees`, `setcommission`); default is often zero-cost — always model explicit + implicit costs (see 08-backtesting-methodology).
- **Data provenance:** vectorbt/backtrader pull Yahoo Finance (survivorship-biased, split/dividend-adjusted, point-in-time-approximate); zipline uses a *bundle* you must ingest (Quandl/NASDAQ Data Link needs a key). None are automatically survivorship-free (see 13-data-and-tooling/data-hygiene-survivorship-free).
- **Version drift:** vectorbt's 0.x vs 1.x APIs differ substantially; zipline-reloaded 3.0 requires pandas ≥2.0 and 3.05 requires NumPy 2.0 — pin and freeze.
- **Single-asset toy:** the snippets are illustrative; real research needs a universe, corporate actions, and walk-forward validation (08-backtesting-methodology).

## Empirical evidence
- The look-ahead hazard is **demonstrated, not asserted**: the verified demo shows +0.25 Sharpe inflation (sign flip) from a one-line timing error.
- Event-driven engines' realism claim is supported by the zipline docs' own design notes (slippage, transaction costs, order delays, stream-based look-ahead avoidance — S360) and corroborated by two independent practitioner write-ups that vectorized backtesters "suffer drawbacks in the way trade execution is simulated" while event-driven "more closely reflect real trading scenarios" and "account for market latency and slippage" (S361, S362).
- No peer-reviewed study is cited for "library X outperforms Y" — that comparison is **folklore**; the right choice is task-dependent (speed-of-ideation vs execution-fidelity).

## Conflicting views
- **"Vectorized is unsafe" vs "vectorized is fine if disciplined":** vectorized code *can* be correct (the demo's vectorized array equals the event loop to 1e-12), but it offers no structural guardrail — the burden of the `shift(1)` is entirely on the author. Event-driven shifts that burden to the engine. Both camps are correct; the practical risk asymmetry favors event-driven for beginners and vectorized for parameter sweeps.
- **Zipline-reloaded viability:** some treat it as the canonical Quantopian successor (S359, S360); others note its heavy dependency stack and the 2020 Quantopian shutdown left a maintenance gap (S155). It remains actively maintained as of v3.1.1 (Jul 2025).
- **backtrader maturity:** widely used and stable, but community support was disabled on the official site (S154) — rely on docs + StackOverflow.

## Common mistakes
1. **Look-ahead via missing shift** (the demo's bug) — decide and trade on the same bar. In vectorized code always `signal.shift(1)`.
2. **Zero-cost backtests** — forgetting `fees`/`setcommission` overstates Sharpe (see 15-pitfalls/transaction-cost-neglect).
3. **In-sample parameter snooping** — sweeping 10,000 SMA windows in vectorbt without multiple-testing correction (08-deflated-sharpe; 15-data-snooping).
4. **Survivorship-biased data** — Yahoo/Quandl current-constituent pulls drop dead names (13-data-hygiene-survivorship-free).
5. **Future-looking indicators** — using `data.history` with a window that includes the current bar's *future* in event-driven code, or `rolling().mean()` indexed to the signal bar incorrectly.
6. **Version drift** — running 1.x vectorbt code against a 0.x install (or vice-versa); zipline against incompatible pandas/NumPy.
7. **Treating backtest Sharpe as forward Sharpe** — non-stationarity means historical edge need not persist (15-pitfalls/regime-change).

## Further reading
- Tier 1 (official): vectorbt docs S153 (https://vectorbt.dev); vectorbt GitHub S356 (https://github.com/polakowo/vectorbt); backtrader docs S154 (https://www.backtrader.com/docu/); zipline-reloaded PyPI S359 (https://pypi.org/project/zipline-reloaded/); zipline tutorial S360 (https://zipline.ml4trading.io/beginner-tutorial.html); zipline docs S155 (https://zipline.ml4trading.io).
- Tier 2 (practitioner): QuantStart event-driven series S361 (https://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-I); PyQuant News event-driven overview S362 (https://www.pyquantnews.com/free-python-resources/event-driven-backtesting-for-trading-strategies).
- Cross-links in this KB: 08-backtesting-methodology (costs, walk-forward, deflated Sharpe), 13-data-and-tooling/data-hygiene-survivorship-free, 13-data-and-tooling/data-vendors-apis-libraries-reproducibility, 15-pitfalls-and-antipatterns (data-snooping, transaction-cost neglect, survivorship bias, look-ahead, regime change).
