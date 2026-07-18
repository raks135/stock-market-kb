"""Reproducibility demo for KB article 14-strategy-catalog/carry-volatility-strategies.md.
Pure stdlib (no external packages). CPython 3.14.4.
Run: python3 carry_volatility_demo.py
Verified output:
CARRY  mean(mo)=0.0073  Sharpe(ann)=1.04  skew=-2.74  worst_mo=-0.120  maxDD=0.184  pct_pos=0.76
VRP    mean(mo)=0.0087  Sharpe(ann)=1.01  skew=-4.59  worst_mo=-0.135  pct_pos=0.96
"""
import random, math, statistics

# ---- Part A: cross-sectional carry (long high-carry, short low-carry) ----
random.seed(42)
N = 12                       # assets per leg
CARRY = 0.005               # monthly carry per side (high=+c, low=-c)
SIGMA = 0.035               # monthly idiosyncratic vol
RISKOFF_P = 0.04            # probability of a risk-off month
CRASH_HI = -0.09            # extra shock to HIGH-carry assets in risk-off
FLIGHT_LO = 0.015           # extra (positive) shock to LOW-carry assets in risk-off

def sim_carry(months=600):
    out = []
    for _ in range(months):
        hi = [CARRY + random.gauss(0, SIGMA) for _ in range(N)]
        lo = [-CARRY + random.gauss(0, SIGMA) for _ in range(N)]
        if random.random() < RISKOFF_P:
            hi = [x + CRASH_HI for x in hi]
            lo = [x + FLIGHT_LO for x in lo]
        out.append(sum(hi) / N - sum(lo) / N)
    return out

pnl = sim_carry()
mean = statistics.mean(pnl); sd = statistics.pstdev(pnl)
sharpe = mean / sd * math.sqrt(12)
m3 = statistics.mean([(x - mean) ** 3 for x in pnl])
m2 = statistics.mean([(x - mean) ** 2 for x in pnl])
skew = m3 / (math.sqrt(m2) ** 3) if m2 > 0 else 0
cum = 0.0; peak = 0.0; maxdd = 0.0
for x in pnl:
    cum += x; peak = max(peak, cum); maxdd = max(maxdd, peak - cum)
worst = min(pnl)
print("CARRY  mean(mo)=%.4f  Sharpe(ann)=%.2f  skew=%.2f  worst_mo=%.3f  maxDD=%.3f  pct_pos=%.2f"
      % (mean, sharpe, skew, worst, maxdd, sum(1 for x in pnl if x > 0) / len(pnl)))

# ---- Part B: short variance swap (= volatility risk premium) ----
random.seed(7)
K = 0.045                   # implied variance received (~21% vol)^2
RV_NORMAL = 0.03            # realized variance paid (~17% vol)
SPIKE_P = 0.035
SPIKE_RV = 0.18             # vol spike -> ~42% vol realized
vrp = []
for _ in range(600):
    rv = SPIKE_RV if random.random() < SPIKE_P else RV_NORMAL
    vrp.append(K - rv)      # receive variance swap rate K, pay realized variance
mean2 = statistics.mean(vrp); sd2 = statistics.pstdev(vrp)
sharpe2 = mean2 / sd2 * math.sqrt(12)
m3b = statistics.mean([(x - mean2) ** 3 for x in vrp])
m2b = statistics.mean([(x - mean2) ** 2 for x in vrp])
skew2 = m3b / (math.sqrt(m2b) ** 3) if m2b > 0 else 0
worst2 = min(vrp)
print("VRP    mean(mo)=%.4f  Sharpe(ann)=%.2f  skew=%.2f  worst_mo=%.3f  pct_pos=%.2f"
      % (mean2, sharpe2, skew2, worst2, sum(1 for x in vrp if x > 0) / len(vrp)))
