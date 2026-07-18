"""Mean-variance efficient frontier demo (pure stdlib, no numpy/scipy needed).
Reproduces: global minimum-variance (GMV) portfolio, tangency (max-Sharpe)
portfolio, and the efficient frontier via the 2-fund theorem.

Run: python3 _mv_demo.py   (Python 3.8+; no third-party deps)
Data source for the illustration: illustrative annualized expected returns and
covariance, NOT real market data. Replace `mu`/`Sigma` with point-in-time
estimates from your own dataset.
"""
import math


def mat_inv(M):
    """Gauss-Jordan inverse of a square matrix (list of lists)."""
    n = len(M)
    A = [M[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[piv][col]) < 1e-12:
            raise ValueError("matrix is singular / not invertible")
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0.0:
                f = A[r][col]
                A[r] = [A[r][k] - f * A[col][k] for k in range(2 * n)]
    return [row[n:] for row in A]


def mat_vec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))


# ---- Illustrative inputs (annualized; NOT real market data) ----
mu = [0.10, 0.12, 0.08]            # expected returns of 3 assets
Sigma = [                            # covariance matrix (must be pos-def)
    [0.0400, 0.0060, 0.0050],
    [0.0060, 0.0300, 0.0040],
    [0.0050, 0.0040, 0.0200],
]
rf = 0.03
n = len(mu)
ones = [1.0] * n

Sinv = mat_inv(Sigma)

# Global minimum-variance portfolio: w_gmv = S^-1 1 / (1' S^-1 1)
num = mat_vec(Sinv, ones)
den = dot(ones, num)
w_gmv = [x / den for x in num]

# Tangency portfolio: w ∝ S^-1 (mu - rf*1), then normalized to sum to 1
excess = [mu[i] - rf * ones[i] for i in range(n)]
w_tan_raw = mat_vec(Sinv, excess)
s = sum(w_tan_raw)
w_tan = [x / s for x in w_tan_raw]


def port_return(w):
    return dot(w, mu)


def port_vol(w):
    return math.sqrt(dot(w, mat_vec(Sigma, w)))


print("GMV      weights:", [round(x, 4) for x in w_gmv], "sum =", round(sum(w_gmv), 6))
print("  ret = %.4f  vol = %.4f" % (port_return(w_gmv), port_vol(w_gmv)))
print("Tangency weights:", [round(x, 4) for x in w_tan], "sum =", round(sum(w_tan), 6))
print("  ret = %.4f  vol = %.4f  Sharpe = %.4f" %
      (port_return(w_tan), port_vol(w_tan),
       (port_return(w_tan) - rf) / port_vol(w_tan)))
print()
print("Efficient frontier (upper branch = t >= 0): w = GMV + t*(TAN - GMV)")
for t in [-0.5, 0.0, 0.5, 1.0, 1.5, 2.0]:
    w = [w_gmv[i] + t * (w_tan[i] - w_gmv[i]) for i in range(n)]
    r = port_return(w)
    v = port_vol(w)
    print("t=%+4.1f  w=%s  ret=%.4f  vol=%.4f  Sharpe=%.4f" %
          (t, [round(x, 3) for x in w], r, v, (r - rf) / v))
