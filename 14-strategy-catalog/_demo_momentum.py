"""
Demo: mechanism of time-series momentum (TSM).
ILLUSTRATIVE ONLY -- synthetic AR(1) returns, NOT a market claim.
Holds the noise path fixed across autocorrelation values so the ONLY thing
that changes is rho (return autocorrelation). Shows TSM P&L rises with the
autocorrelation it exploits, and is flat-to-negative when rho=0 (volatility
drag from being always fully exposed with a random sign).
Run: .venv/bin/python _demo_momentum.py   (numpy 2.5.1)
"""
import numpy as np

rng = np.random.default_rng(42)
T = 360                                 # 30y of monthly observations
target_vol = 0.10 / np.sqrt(12)         # monthly vol target ~2.89% (10% annualized)
base = rng.normal(0.0, 0.04, T)         # SAME noise for every rho -> isolates autocorrelation

def make_ar1(rho):
    x = np.zeros(T)
    for t in range(1, T):
        x[t] = rho * x[t - 1] + base[t]
    return x

def tsm_returns(rets, lookback=12):
    out = np.zeros(len(rets))
    for t in range(lookback, len(rets)):
        signal = np.sign(np.sum(rets[t - lookback:t]))      # trailing lookback cumulative
        vol = np.std(rets[t - lookback:t], ddof=1)
        vol = vol if vol > 1e-9 else 1e-9
        pos = signal * (target_vol / vol)                   # vol-scaled
        out[t] = pos * rets[t]
    return out

print(f"{'rho':>5} | {'TSM cum P&L':>12} | {'ann. Sharpe':>12}")
for rho in [0.0, 0.10, 0.20, 0.30]:
    pnl = tsm_returns(make_ar1(rho))
    cum = (np.prod(1.0 + pnl) - 1.0) * 100.0
    shr = np.mean(pnl) / np.std(pnl, ddof=1) * np.sqrt(12)
    print(f"{rho:5.2f} | {cum:11.1f}% | {shr:12.2f}")
print("Read: TSM profit rises with the return autocorrelation it harvests;")
print("at rho=0 it is flat-to-negative (volatility drag), not a market edge.")
