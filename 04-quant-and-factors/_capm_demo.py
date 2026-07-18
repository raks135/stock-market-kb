import math

def rng(seed=42):
    state = seed
    while True:
        state = (state * 1103515245 + 12345) % 2147483647
        yield state / 2147483647.0

def normal(gen):
    u1 = next(gen)
    u2 = next(gen)
    return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

n = 120
gen = rng(42)
mkt_ex = [0.008 + 0.04 * normal(gen) for _ in range(n)]
asset_ex = [1.2 * m + 0.02 * normal(gen) for m in mkt_ex]

def mean(xs):
    return sum(xs) / len(xs)

def var(xs):
    mx = mean(xs)
    return sum((x - mx) ** 2 for x in xs) / (len(xs) - 1)

def cov(xs, ys):
    mx = mean(xs)
    my = mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)

beta = cov(asset_ex, mkt_ex) / var(mkt_ex)
m_a = mean(asset_ex)
m_m = mean(mkt_ex)
alpha = m_a - beta * m_m
Rf = 0.04 / 12
ERP = 0.06
E_R = Rf * 12 + beta * ERP
beta_blume = (2.0 / 3.0) * beta + (1.0 / 3.0)

print("n =", n)
print("mean mkt ex  = %.6f" % m_m)
print("mean asset ex= %.6f" % m_a)
print("beta (OLS)   = %.4f" % beta)
print("alpha        = %.6f" % alpha)
print("CAPM annual E[R] = %.4f" % E_R)
print("Blume beta        = %.4f" % beta_blume)
