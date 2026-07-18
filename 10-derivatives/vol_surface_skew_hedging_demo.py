"""
Verification script for:
 10-derivatives/volatility-surface-skew-hedging.md

Pure standard library (math, random) -- NO external dependencies.
Reproduce:  python3 _verify_vol_surface.py

Two demonstrations:
  A) A toy implied-volatility SURFACE with equity-style put skew + term
     structure, and the skew / risk-reversal metrics computed from it.
  B) A discrete-time delta-hedged SHORT STRADDLE, where the (risk-neutral)
     P&L of a gamma-scalping book is driven by (sigma_imp^2 - sigma_real^2).
"""
import math
import random

# ----------------------------------------------------------------------
# Black-Scholes primitives (stdlib only)
# ----------------------------------------------------------------------
def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bs_price(S, K, T, r, sigma, kind="call"):
    if T <= 0 or sigma <= 0:
        if kind == "call":
            return max(S - K, 0.0)
        return max(K - S, 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if kind == "call":
        return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    return K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)

def bs_delta(S, K, T, r, sigma, kind="call"):
    if T <= 0:
        if kind == "call":
            return 1.0 if S > K else 0.0
        return 0.0 if S > K else -1.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    if kind == "call":
        return norm_cdf(d1)
    return norm_cdf(d1) - 1.0

def bs_gamma(S, K, T, r, sigma):
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return math.exp(-0.5 * d1 ** 2) / (S * sigma * math.sqrt(2.0 * math.pi * T))

def implied_vol(S, K, T, r, market_price, kind="call", lo=1e-4, hi=5.0, tol=1e-7):
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        p = bs_price(S, K, T, r, mid, kind)
        if p > market_price:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)

# ----------------------------------------------------------------------
# A) Toy implied-volatility SURFACE
#    iv(strike, maturity) = atm_term(T) + smile*((K/S)-1)^2 + skew*((S/K)-1)
#    skew > 0 raises LOW-strike (OTM put) vol  -> equity "put skew"
# ----------------------------------------------------------------------
S0 = 100.0
r = 0.02

def atm_term(T):
    # term structure: shorter maturities a touch richer, longer flatter
    return 0.18 + 0.04 * math.exp(-T / 1.0)  # 0.22 near, 0.18 far

def iv_surface(K, T):
    smile = 0.30          # curvature (U-shape)
    skew = 1.20           # asymmetry (put skew)
    return atm_term(T) + smile * ((K / S0) - 1.0) ** 2 + skew * ((S0 / K) - 1.0)

print("=== A) Volatility surface & skew metrics (S0=%.0f) ===" % S0)
# Build an IV chain for a 30-day (T=30/252) option at a few strikes
T30 = 30.0 / 252.0
strikes = [88, 92, 95, 100, 105, 108, 112]
chain = [(K, iv_surface(K, T30)) for K in strikes]
print("Strike  IV(30d)")
for K, iv in chain:
    print("  %3d   %.4f" % (K, iv))

# 25-delta approximations (illustrative, not solved): use OTM put @95 and OTM call @105
iv_25p = iv_surface(95, T30)
iv_atm = iv_surface(100, T30)
iv_25c = iv_surface(105, T30)
put_skew = iv_25p - iv_atm
risk_rev = iv_25c - iv_25p
print("\n25-delta put IV  = %.4f" % iv_25p)
print("ATM IV           = %.4f" % iv_atm)
print("25-delta call IV = %.4f" % iv_25c)
print("Put skew  (25d put - ATM)     = %.4f" % put_skew)
print("Risk reversal (25d call - put) = %.4f" % risk_rev)
assert put_skew > 0, "expected positive put skew"
assert risk_rev < 0, "expected negative risk reversal (equity put skew)"

# Term-structure of ATM vol
print("\nATM term structure:")
for T in [1/12, 3/12, 6/12, 1.0, 2.0]:
    print("  T=%.2f yr  atm_iv=%.4f" % (T, atm_term(T)))

# Round-trip IV recovery check: price a call, solve IV back, compare
K_atm = S0
sigma_true = atm_term(T30)
c_price = bs_price(S0, K_atm, T30, r, sigma_true, "call")
iv_back = implied_vol(S0, K_atm, T30, r, c_price, "call")
print("\nRound-trip IV check: true=%.6f  recovered=%.6f  err=%.2e"
      % (sigma_true, iv_back, abs(sigma_true - iv_back)))
assert abs(sigma_true - iv_back) < 1e-4

# ----------------------------------------------------------------------
# B) Discrete-time delta-hedged SHORT STRADDLE
# ----------------------------------------------------------------------
print("\n=== B) Delta-hedged short straddle (discrete, w/ txn costs) ===")

def simulate(sigma_imp, sigma_real, cost_rate, seed=42, days=252, T=1.0):
    random.seed(seed)
    K = S0
    dt = T / days
    # write straddle at t0 using IMPLIED vol
    C0 = bs_price(S0, K, T, r, sigma_imp, "call")
    P0 = bs_price(S0, K, T, r, sigma_imp, "put")
    premium = C0 + P0
    # dynamic share position H (start delta-neutral for ATM straddle)
    delta_opt = bs_delta(S0, K, T, r, sigma_imp, "call") + \
                bs_delta(S0, K, T, r, sigma_imp, "put")   # ~0 for ATM
    H = -delta_opt
    cash = premium - H * S0            # receive premium, buy/short shares
    cash -= abs(H) * S0 * cost_rate    # initial hedge cost
    S = S0
    for step in range(1, days):
        # GBM step under REALIZED vol
        z = random.gauss(0.0, 1.0)
        S = S * math.exp((r - 0.5 * sigma_real ** 2) * dt + sigma_real * math.sqrt(dt) * z)
        Tleft = T - step * dt
        dC = bs_delta(S, K, Tleft, r, sigma_imp, "call")
        dP = bs_delta(S, K, Tleft, r, sigma_imp, "put")
        d_opt = dC + dP
        H_new = -d_opt
        trade = H_new - H
        cash -= trade * S
        cash -= abs(trade) * S * cost_rate
        H = H_new
    # maturity: close option (pay the straddle payoff) and close shares
    payoff = abs(S - K)                 # short straddle payoff
    cash -= payoff
    cash += H * S
    cash -= abs(H) * S * cost_rate
    return cash

for sigma_real, label in [(0.20, "realized == implied"),
                          (0.30, "realized HIGHER (short vol loses)"),
                          (0.10, "realized LOWER (short vol wins)")]:
    pl = simulate(sigma_imp=0.20, sigma_real=sigma_real, cost_rate=0.0005)
    print("  sigma_real=%.2f  (%s): P&L = %.4f" % (sigma_real, label, pl))

print("\nAll assertions passed.")
