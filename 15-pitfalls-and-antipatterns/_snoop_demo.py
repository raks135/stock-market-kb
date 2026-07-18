import random, math
from math import erf, sqrt

random.seed(42)

def gaussian():
    u1 = random.random(); u2 = random.random()
    return math.sqrt(-2*math.log(u1))*math.cos(2*math.pi*u2)

def t_stat(returns):
    n = len(returns)
    mean = sum(returns)/n
    var = sum((r-mean)**2 for r in returns)/(n-1)
    return mean/(math.sqrt(var)/math.sqrt(n))

def two_sided_p(t):
    # t with T-1 df ~ normal for large T; use normal CDF via erf
    x = abs(t)
    return 2*(1-0.5*(1+erf(x/sqrt(2))))

# Simulate M strategies on i.i.d. N(0, sigma) daily returns (NULL: no true edge)
M = 1000
T = 252
sigma = 0.01
all_t = []
for _ in range(M):
    rets = [gaussian()*sigma for _ in range(T)]
    all_t.append(t_stat(rets))

best_t = max(all_t, key=abs)
best_abs = abs(best_t)
naive_p = two_sided_p(best_t)
bonf_p = min(1.0, M*naive_p)

# How many of the M strategy t-stats exceed 2.0 (naive "significant") just by chance?
naive_sig = sum(1 for t in all_t if abs(t) > 2.0)
# Benjamini-Hochberg at q=0.05 (global null => expected ~ q*M false positives)
sorted_p = sorted(two_sided_p(t) for t in all_t)
m = len(sorted_p)
bh_sig = sum(1 for i,p in enumerate(sorted_p) if p <= (i+1)/m*0.05)

# Distribution of max |t| across 200 independent replications of the whole search
max_abs_list = []
for _ in range(200):
    mx = 0.0
    for _ in range(M):
        rets = [gaussian()*sigma for _ in range(T)]
        a = abs(t_stat(rets))
        if a > mx: mx = a
    max_abs_list.append(mx)
avg_max = sum(max_abs_list)/len(max_abs_list)
frac_gt3 = sum(1 for x in max_abs_list if x > 3.0)/len(max_abs_list)

print(f"Single search (seed 42): best |t| = {best_abs:.2f}")
print(f"  naive p(best) = {naive_p:.4f}  -> Bonferroni-adjusted p = {bonf_p:.4f}")
print(f"  # of {M} strategies with |t|>2.0 by chance = {naive_sig}  (expect ~{0.0455*M:.0f})")
print(f"  # BH-significant at q=0.05 (global null) = {bh_sig}")
print(f"Across 200 replications of a {M}-rule search:")
print(f"  average max|t| = {avg_max:.2f}   fraction with max|t|>3 = {frac_gt3*100:.0f}%")
