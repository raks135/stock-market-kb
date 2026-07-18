"""
Illustrative (SYNTHETIC) construction demo for a combined Value + Quality
long-short strategy.

IMPORTANT: This is NOT a market backtest. Returns are simulated from a known
factor structure (each stock's monthly return loads on a latent value score
and a latent quality score plus noise) so the code reliably demonstrates the
*mechanics* of building value/quality scores, z-scoring, and forming an
equal-weight long-short portfolio. Real implementation requires point-in-time
fundamentals and delisting-inclusive returns (see KB 13-data-and-tooling and
15-pitfalls-and-antipatterns).

Stdlib only. Pinned: Python 3.14 (no third-party deps).
"""
import random, math, statistics

random.seed(42)
N = 200   # number of stocks
T = 120   # months

# Latent true (ex-ante) value and quality scores ~ N(0,1)
value_true = [random.gauss(0, 1) for _ in range(N)]
qual_true  = [random.gauss(0, 1) for _ in range(N)]

# Simulated monthly returns: r = base + 0.004*value + 0.003*quality + noise
ret = [[0.0] * T for _ in range(N)]
for i in range(N):
    vz, qz = value_true[i], qual_true[i]
    for t in range(T):
        ret[i][t] = 0.004 + 0.004 * vz + 0.003 * qz + random.gauss(0, 0.04)


def zscores(xs):
    m = statistics.mean(xs)
    sd = statistics.pstdev(xs) or 1.0
    return [(x - m) / sd for x in xs]


def annualized_sharpe(series):
    m = statistics.mean(series)
    sd = statistics.pstdev(series) or 1e-9
    return m / sd * math.sqrt(12)


def long_short_returns(score, ret, top_frac=0.20):
    order = sorted(range(N), key=lambda i: score[i], reverse=True)
    k = int(N * top_frac)
    longs, shorts = order[:k], order[-k:]
    out = []
    for t in range(T):
        long_ret = statistics.mean(ret[i][t] for i in longs)
        short_ret = statistics.mean(ret[i][t] for i in shorts)
        out.append(long_ret - short_ret)
    return out


def cumulative(series):
    c = 1.0
    for r in series:
        c *= (1 + r)
    return c


# Ex-ante scores an investor would actually observe (value = B/M z, quality = GP/A z)
v_scores = zscores(value_true)
q_scores = zscores(qual_true)
composite = [(v + q) / 2 for v, q in zip(v_scores, q_scores)]

ls_v = long_short_returns(v_scores, ret)
ls_q = long_short_returns(q_scores, ret)
ls_c = long_short_returns(composite, ret)

print("Annualized Sharpe (equal-weight long-short, synthetic):")
print(f"  Value only   : {annualized_sharpe(ls_v):.3f}")
print(f"  Quality only  : {annualized_sharpe(ls_q):.3f}")
print(f"  Value+Quality: {annualized_sharpe(ls_c):.3f}")
print("Growth of $1 over 120 months (synthetic):")
print(f"  Value only   : {cumulative(ls_v):.3f}")
print(f"  Quality only  : {cumulative(ls_q):.3f}")
print(f"  Value+Quality: {cumulative(ls_c):.3f}")
print(f"Top-decile composite stocks (first 5 ids): {sorted(range(N), key=lambda i: composite[i], reverse=True)[:5]}")
