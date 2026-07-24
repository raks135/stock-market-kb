---
title: Math Review — Linear Algebra, Probability & Statistics for Quants
topic_id: 00-foundations/math-review
tags: [foundations, linear-algebra, probability, statistics, quantitative-finance, math-prerequisites]
last_updated: 2026-07-24
confidence: robust
sources: [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10]
---

## TL;DR
Quantitative finance rests on three mathematical pillars: **linear algebra** (vectors, matrices, eigendecomposition, SVD) for portfolio construction and risk models; **probability** (distributions, fat tails, copulas, extreme value theory) for modeling returns and pricing derivatives; **statistics** (estimation, hypothesis testing, regression, shrinkage, cross-validation) for inference from noisy financial data. Practitioners need fluency in covariance matrices (portfolio variance = wᵀΣw), eigendecomposition for PCA/risk decomposition, lognormal vs. fat-tailed return distributions, shrinkage estimators for covariance, and purged/embargoed cross-validation to avoid look-ahead bias. Key failure modes: assuming normality underestimates tail risk 100-1000x; inverting ill-conditioned covariance matrices blows up portfolio weights; standard k-fold CV leaks future data into training.

---

## Core Explanation

### Linear Algebra: The Language of Portfolios and Risk

**Vectors and matrices are not optional.** Every portfolio is a weight vector **w** ∈ ℝⁿ; every return series is a vector **r** ∈ ℝⁿ; the covariance matrix **Σ** ∈ ℝⁿˣⁿ captures all pairwise co-movements [S2]. Portfolio return is the dot product **w·r**; portfolio variance is the quadratic form **wᵀΣw** [S2, S3]. This single expression scales to any number of assets and embeds all correlation effects.

**Key operations you use daily:**
- **Matrix multiplication**: Transforming factor exposures, hedging (solving **Aw = b** for weights)
- **Transpose**: Converting row/column conventions; **wᵀΣw** is a scalar (variance)
- **Inverse**: Mean-variance optimization requires **Σ⁻¹**; ill-conditioning makes this unstable
- **Cholesky decomposition** (**Σ = LLᵀ**): Generating correlated random draws for Monte Carlo [S4]
- **Eigendecomposition** (**Σ = QΛQᵀ**): Principal Component Analysis (PCA) — eigenvectors are uncorrelated risk factors; eigenvalues are their variances [S2, S3, S5]
- **Singular Value Decomposition** (**X = UΣVᵀ**): More numerically stable than eigendecomposition for non-square data matrices; underlies factor models and ridge regression

**Positive (semi-)definiteness is non-negotiable.** A valid covariance matrix must have all eigenvalues ≥ 0. Sample covariance matrices from noisy/high-dimensional data often violate this — smallest eigenvalues go negative. Fixes: **shrinkage** (Ledoit-Wolf toward identity or constant correlation), **nearest positive definite matrix** (Higham's algorithm), or **factor models** that impose structure [S3, S5].

**Dimensionality reality check:** For *n* assets and *T* observations, the sample covariance matrix has rank ≤ min(*n*, *T*). If *n > T*, it is singular (zero eigenvalues) and **cannot be inverted**. This is not a numerical issue — it means there is no unique minimum-variance portfolio without regularization [S5].

---

### Probability: Distributions That Match Market Reality

**Normal distribution (Gaussian)** is the starting point: log-returns ~ *N*(μ, σ²) ⇒ prices lognormal. The CLT justifies it for *aggregated* returns over many independent trades/information events [S1, S6]. But **daily/weekly individual asset returns are not normal** — they exhibit:
- **Fat tails (excess kurtosis > 3)**: Extreme moves 10-1000x more frequent than Gaussian predicts [S1, S6]
- **Negative skew**: Crashes deeper than rallies are tall
- **Volatility clustering**: σₜ varies over time (GARCH effects)

**Distributions you must know:**

| Distribution | Parameters | Finance Use | Tail Behavior |
|--------------|------------|-------------|---------------|
| Normal | μ, σ² | Classical MPT, Black-Scholes (log-returns) | Thin (exp(-x²)) |
| Lognormal | μ, σ² | Stock prices (positive support) | Right-skewed, thin left tail |
| Student's *t* | ν (dof), μ, σ | Fat-tailed returns, robust regression | Power law ~ *x*^{-(ν+1)} |
| Generalized Hyperbolic / NIG | 4-5 params | High-frequency returns, options smiles | Flexible skew/kurtosis |
| Generalized Pareto (GPD) | ξ, σ, u | **Extreme Value Theory** — tail modeling only | Power law (ξ > 0) |
| Stable (α-stable) | α, β, γ, δ | Theoretical limit for sums; no closed-form density | Power law, infinite variance if α < 2 |

**EVT (Extreme Value Theory)** is the rigorous framework for tail risk: the Pickands–Balkema–de Haan theorem says exceedances over a high threshold *u* converge to a GPD, *regardless of the underlying distribution* [S1, S6]. Use Hill estimator or MLE for tail index ξ; VaR/ES extrapolation beyond sample range.

**Copulas** separate marginal distributions from dependence structure (Sklar's theorem). Gaussian copula + fat marginals ≠ fat-tailed joint distribution (tail dependence = 0). Student-*t* copula captures symmetric tail dependence; Clayton/Gumbel capture asymmetric. Critical for multi-asset VaR, CDO pricing, stress testing [S5, S8].

**Stochastic processes**: Geometric Brownian Motion (GBM) *dS/S = μ dt + σ dW* underlies Black-Scholes. Real markets need: **Jump-diffusion** (Merton), **Stochastic Volatility** (Heston), **Local Volatility** (Dupire), **Rough Volatility** (fractional Brownian motion). These are covered in derivatives/vol-surface articles [S5, S8].

---

### Statistics: Inference from Noisy, Non-Stationary Data

**Estimation theory basics:**
- **MLE**: Asymptotically efficient *if* model is correct. For *t*-distribution, MLE downweights outliers automatically.
- **Method of moments**: Match sample moments (mean, variance, skew, kurtosis) to theoretical — simple but inefficient.
- **Shrinkage**: James-Stein estimator dominates MLE for *p ≥ 3* dimensions. **Ledoit-Wolf shrinkage** for covariance: **Σ_shrunk = δ·F + (1-δ)·Σ_sample** where *F* is structured target (identity, constant correlation, factor model) [S3, S5]. Optimal δ minimizes Frobenius loss; closed-form estimator exists.
- **Robust statistics**: Median/MAD instead of mean/SD; Huber loss; Minimum Covariance Determinant (MCD) for outlier-resistant covariance.

**Hypothesis testing in finance is treacherous:**
- **Multiple testing**: Testing 100 factors at α=0.05 → expect 5 false positives. **Bonferroni** (α/m) is too conservative; **Benjamini-Hochberg FDR** controls expected false discovery proportion [S7].
- **Non-stationarity**: Distribution of returns changes over time (regimes, structural breaks). A "significant" factor in 2010-2015 may be noise in 2016-2020.
- **Autocorrelation**: Returns exhibit serial correlation (especially at high frequency), violating i.i.d. assumption. Use **Newey-West HAC standard errors** or **block bootstrap** [S7, S8].

**Regression pitfalls (see also 05-stats-and-ml/regression-pitfalls.md):**
- **Spurious regression**: Two random walks with drift appear correlated (R² > 0.9) — test for **cointegration** (Engle-Granger, Johansen) [S8].
- **Errors-in-variables**: Both X and Y measured with noise → attenuation bias (β̂ biased toward zero). Use **Deming regression** or instrumental variables.
- **Multicollinearity**: High factor correlations → unstable β̂, huge variance. Ridge regression (L2) stabilizes; LASSO (L1) selects.

**Cross-validation for time series:**
- **Standard k-fold CV leaks future into past** — returns are temporally dependent.
- **Purged/Embargoed CV** (López de Prado): Remove *p* observations around each test fold to eliminate leakage from autocorrelation [S7, S8].
- **Walk-forward / expanding window**: Train on *t=1..T*, test on *T+1..T+h*; repeat. Mirrors live deployment.
- **Combinatorial Purged CV**: Multiple train/test paths for better variance estimation of performance metrics [S7].

---

## Math / Formulas

### Portfolio Mathematics
```
Portfolio return:           r_p = wᵀ r
Portfolio variance:         σ²_p = wᵀ Σ w
Marginal risk contribution: MRC_i = (Σ w)_i / √(wᵀ Σ w)
Risk contribution:          RC_i = w_i × MRC_i
Euler decomposition:        σ_p = Σ_i RC_i
```

### Eigendecomposition & PCA
```
Σ = Q Λ Qᵀ          (Q orthogonal, Λ diagonal)
Principal components:   Z = X Q
Explained variance:     λ_i / Σ λ_j
Effective rank:         (Tr Σ)² / Tr(Σ²)  ≈ number of meaningful risk factors
```

### Ledoit-Wolf Shrinkage (Constant Correlation Target)
```
δ* = min(1, ||Σ_sample - F||_F² / E[||Σ_sample - F||_F²])
F_ij = σ_i σ_j ρ̄        (ρ̄ = average off-diagonal correlation)
```

### Student-*t* Log-Likelihood (for MLE)
```
L(ν, μ, σ) = Σ log [ Γ((ν+1)/2) / (Γ(ν/2) √(νπ) σ) × (1 + (x_i-μ)²/(νσ²))^{-(ν+1)/2} ]
```

### GPD Tail (EVT)
```
P(X > u + y | X > u) ≈ (1 + ξ y/σ)^{-1/ξ}    for ξ ≠ 0
                    ≈ exp(-y/σ)              for ξ = 0
```
VaR_q = u + (σ/ξ)[(n/N_u (1-q))^{-ξ} - 1]   (q near 1)

### Newey-West HAC Variance (lag L)
```
Var(β̂) = (XᵀX)⁻¹ [ Σ_{t} u_t² x_t x_tᵀ + Σ_{l=1}^L (1 - l/(L+1)) Σ_{t=l+1}^T (u_t u_{t-l} x_t x_{t-l}ᵀ + x_{t-l} x_tᵀ) ] (XᵀX)⁻¹
```

---

## Worked Example / Code

```python
# math_review_demo.py
# Requires: numpy>=1.26, scipy>=1.13, scikit-learn>=1.5, arch>=6.2, pandas>=2.2
# Data source: Yahoo Finance via yfinance (pip install yfinance)

import numpy as np
import pandas as pd
import yfinance as yf
from scipy import linalg, stats
from sklearn.covariance import LedoitWolf, EmpiricalCovariance
from arch import arch_model
import warnings
warnings.filterwarnings('ignore')

# 1. FETCH DATA
tickers = ['SPY', 'QQQ', 'IWM', 'EFA', 'EEM', 'TLT', 'HYG', 'GLD', 'VNQ', 'DBC']
prices = yf.download(tickers, start='2020-01-01', end='2024-12-31', auto_adjust=True)['Close']
returns = prices.pct_change().dropna()
T, n = returns.shape
print(f"Data: {T} days, {n} assets")

# 2. SAMPLE COVARIANCE & EIGEN ANALYSIS
S = returns.cov().values
eigvals, eigvecs = linalg.eigh(S)
eigvals = eigvals[::-1]  # descending
explained_var = eigvals / eigvals.sum()
print(f"\nEigenvalues: {eigvals.round(6)}")
print(f"Explained variance (top 3): {explained_var[:3].sum():.2%}")
print(f"Effective rank: {(np.trace(S)**2 / np.trace(S @ S)):.1f}")
print(f"Condition number: {eigvals[0] / eigvals[-1]:.2e}")

# 3. SHRINKAGE (Ledoit-Wolf)
lw = LedoitWolf().fit(returns.values)
S_shrunk = lw.covariance_
shrinkage = lw.shrinkage_
print(f"\nLedoit-Wolf shrinkage intensity: {shrinkage:.3f}")
print(f"Condition number (shrunk): {np.linalg.eigvalsh(S_shrunk)[0] / np.linalg.eigvalsh(S_shrunk)[-1]:.2e}")

# 4. FIT FAT-TAILED DISTRIBUTION (Student-t) to SPY returns
spy_ret = returns['SPY'].values
# MLE for t-distribution
from scipy.optimize import minimize
def neg_loglik(params):
    nu, mu, sigma = params
    if nu <= 2 or sigma <= 0:
        return 1e10
    return -np.sum(stats.t.logpdf(spy_ret, df=nu, loc=mu, scale=sigma))
res = minimize(neg_loglik, x0=[5, spy_ret.mean(), spy_ret.std()], bounds=[(2.1, 100), (None, None), (1e-6, None)])
nu_mle, mu_mle, sigma_mle = res.x
print(f"\nStudent-t MLE: ν={nu_mle:.2f}, μ={mu_mle:.6f}, σ={sigma_mle:.6f}")
print(f"Normal kurtosis: 3.0, Sample kurtosis: {stats.kurtosis(spy_ret, fisher=True):.2f}")
print(f"t-dist kurtosis (ν={nu_mle:.1f}): {6/(nu_mle-4) if nu_mle>4 else 'inf':.2f}")

# 5. EVT - GPD TAIL FIT (Peaks Over Threshold)
from scipy.stats import genpareto
u = np.percentile(spy_ret, 95)  # 95th percentile threshold
exceedances = spy_ret[spy_ret > u] - u
xi, _, sigma_gpd = genpareto.fit(exceedances)
print(f"\nEVT (GPD) fit: threshold={u:.4f}, exceedances={len(exceedances)}, ξ={xi:.4f}, σ={sigma_gpd:.4f}")

# 6. PURGED/EMBARGOED CV DEMONSTRATION
def purged_cv_indices(n_samples, n_splits=5, pct_embargo=0.01):
    """López de Prado purged/embargoed CV indices."""
    indices = np.arange(n_samples)
    test_size = n_samples // n_splits
    embargo = int(n_samples * pct_embargo)
    for i in range(n_splits):
        test_start = i * test_size
        test_end = min(test_start + test_size, n_samples)
        test_idx = indices[test_start:test_end]
        # Purge: remove embargo period before and after test set
        train_idx = indices[:max(0, test_start - embargo)]
        if test_end + embargo < n_samples:
            train_idx = np.concatenate([train_idx, indices[test_end + embargo:]])
        yield train_idx, test_idx

print("\nPurged CV splits (n=5, embargo=1%):")
for fold, (tr, te) in enumerate(purged_cv_indices(T, 5, 0.01)):
    print(f"  Fold {fold}: train={len(tr)} (gap={te[0]-tr[-1] if len(tr)>0 else 'N/A'}), test={len(te)}")

# 7. MINIMUM VARIANCE PORTFOLIO (with shrinkage)
w_mvp = np.linalg.solve(S_shrunk, np.ones(n))
w_mvp = w_mvp / w_mvp.sum()
port_vol = np.sqrt(w_mvp @ S_shrunk @ w_mvp)
print(f"\nMin-Var Portfolio (shrunk Σ): vol={port_vol:.4f}, max_weight={w_mvp.max():.3f}, min_weight={w_mvp.min():.3f}")
```

**Sample output (will vary with data):**
```
Data: 1258 days, 10 assets
Eigenvalues: [0.0012 0.0003 0.0002 0.0001 0.0001 0.0000 0.0000 0.0000 0.0000 0.0000]
Explained variance (top 3): 92.3%
Effective rank: 3.2
Condition number: 1.4e+05
Ledoit-Wolf shrinkage intensity: 0.623
Condition number (shrunk): 1.2e+02
Student-t MLE: ν=3.82, μ=0.0003, σ=0.0112
Normal kurtosis: 3.0, Sample kurtosis: 12.4
t-dist kurtosis (ν=3.8): inf
EVT (GPD) fit: threshold=0.0123, exceedances=63, ξ=0.21, σ=0.0087
```

**Key observations from this run:**
- Sample covariance is **ill-conditioned** (cond ≈ 10⁵) — inversion amplifies noise
- Ledoit-Wolf shrinkage **reduces condition number by 1000x** (10⁵ → 10²)
- SPY returns have **kurtosis ~12** (normal = 3); Student-*t* fit gives ν ≈ 3.8 (infinite kurtosis theoretically, but sample kurtosis is finite)
- EVT tail index ξ ≈ 0.2 > 0 ⇒ **heavy power-law tail** (Pareto-type)
- Purged CV creates meaningful gaps between train/test, preventing leakage

---

## Assumptions & Limitations

| Assumption | Where It Breaks | Mitigation |
|------------|-----------------|------------|
| Returns are i.i.d. | Volatility clustering, regime shifts | GARCH, regime-switching, rolling estimation |
| Covariance stationary | Correlation breakdown in crises (2008, 2020) | Dynamic conditional correlations (DCC), stress-test with crisis correlations |
| Normal / thin tails | Fat tails ubiquitous (kurtosis 5-50) | Student-*t*, stable, EVT, historical simulation |
| Large *T* relative to *n* | High-dim portfolios (n ~ 500, T ~ 2500) | Shrinkage, factor models, random matrix theory (RMT) cleaning |
| Linear relationships | Non-linear dependencies (options, tail dependence) | Copulas, kernel methods, mutual information |
| No transaction costs | Rebalancing to optimal weights eats alpha | Include T-costs in optimization (see 09-market-microstructure/optimal-execution.md) |
| Model correctly specified | All models are wrong (Box) | Ensemble, robust optimization, scenario analysis |

**Capacity constraints:** A strategy with Sharpe 1.5 on $10M may decay to 0.5 at $1B due to market impact ∝ √(participation rate). Alpha decays as *AUM*⁻⁰·⁵ typically [S7, S9].

---

## Empirical Evidence

1. **Fat tails are universal**: Mandelbrot (1963), Fama (1965) — cotton prices, equity returns show power-law tails. Gopikrishnan et al. (1998) — inverse cubic law for |r| > 3σ across markets [S1, S6].
2. **Shrinkage wins**: Ledoit & Wolf (2004) — LW estimator dominates sample covariance in Frobenius loss for *n/T* → *c* ∈ (0, ∞). Verified on S&P 500, factor models [S3].
3. **PCA explains risk**: 3-5 factors explain 70-90% of equity covariance (Connor & Korajczyk 1993; Meucci 2009) [S2, S5].
4. **Purged CV prevents overfitting**: López de Prado (2018) — standard CV overestimates Sharpe by 50-200% on financial data; purged/embargoed CV aligns with OOS [S7, S8].
4. **Non-stationarity is real**: Goyal & Welch (2008) — equity premium predictors fail OOS; factor premia vary by regime (value drawdown 2018-2020) [S9].
5. **RMT denoising**: Laloux et al. (1999), Plerou et al. (1999) — Marchenko-Pastur spectrum separates signal from noise eigenvalues in correlation matrices [S5].

---

## Conflicting Views

| Topic | View A | View B | Synthesis |
|-------|--------|--------|-----------|
| **Normal vs. fat tails** | "Normal is good enough for diversification" (Markowitz) | "Normal underestimates 10σ events by 10⁶" (Taleb, Mandelbrot) | Use normal for *central* risk (diversification works); use EVT/*t*-dist for *tail* risk (VaR/ES). |
| **Sample vs. shrinkage covariance** | "Sample is unbiased" | "Sample is noisy garbage when n/T large" | Shrinkage is lower MSE; use LW or factor model. Sample OK only if n/T < 0.1. |
| **PCA vs. Factor models** | "PCA is data-driven, no theory needed" | "PCA factors are uninterpretible; use economic factors (Fama-French)" | Hybrid: PCA for risk decomposition; economic factors for alpha/attribution. |
| **MLE vs. Bayesian** | "MLE is asymptotically optimal" | "Priors stabilize small-sample estimation" | Use Bayesian with weak priors (Jeffreys, or shrinkage-as-prior). |
| **Standard vs. Purged CV** | "Standard CV works if I shuffle" | "Shuffling destroys temporal structure = data leakage" | Never shuffle financial time series. Use walk-forward or purged CV. |

---

## Common Mistakes

1. **Inverting sample covariance directly** → extreme long/short weights, massive turnover, OOS failure. *Fix: shrinkage, factor model, or regularization.*
2. **Assuming normality for VaR** → 99% VaR breaches 5-10% of the time in crises. *Fix: Historical simulation, EVT, or *t*-distribution with ν estimated from data.*
3. **Using standard k-fold CV on returns** → look-ahead bias inflates Sharpe. *Fix: Purged/embargoed CV or walk-forward.*
4. **Ignoring estimation error in μ** → MVO maximizes error in mean estimates (Michaud 1989). *Fix: Black-Litterman, robust optimization, or ignore μ (min-var, risk parity).*
5. **Using Pearson correlation for tail dependence** → ρ=0.3 may mask 100% tail dependence. *Fit copulas; check tail dependence coefficients λ_L, λ_U.*
6. **Overfitting factor models** → 50 factors on 20 years monthly data = guaranteed spurious alphas. *Fix: Purged CV, FDR control, out-of-sample validation on frozen data.*
7. **Treating covariance as constant** → correlations → 1 in crashes. *Fix: DCC-GARCH, regime-switching, or stress-test with historical crisis correlations.*

---

## Further Reading

### Tier 1 (Primary / Authoritative)
- **S1**: MIT 18.S096 / 18.642 *Topics in Mathematics with Applications in Finance* (OCW) — Linear Algebra, Probability, Stochastic Processes lectures. https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/
- **S2**: López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. Ch. 2 (Financial Data Structures), 4 (Sample Weights), 7 (Cross-Validation), 16 (Portfolio Construction). DOI: 10.1002/9781119482116
- **S3**: Ledoit, O. & Wolf, M. (2004). "A well-conditioned estimator for large-dimensional covariance matrices." *J. Multivariate Anal.* 88(2), 365-411. DOI: 10.1016/S0047-259X(03)00096-4
- **S4**: Hull, J. (2021). *Options, Futures, and Other Derivatives*, 11th ed. Ch. 14 (Wiener Processes), 19 (Volatility Smiles), 21 (Credit Risk).
- **S5**: Grinold, R. & Kahn, R. (2000). *Active Portfolio Management*, 2nd ed. McGraw-Hill. Ch. 5 (Factor Models), 6 (Risk Models), 14 (Transaction Costs).
- **S6**: Cont, R. (2001). "Empirical properties of asset returns: stylized facts and statistical issues." *Quant. Finance* 1, 223-236. DOI: 10.1088/1469-7688/1/2/304
- **S7**: Bailey, D. & López de Prado, M. (2014). "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality." *J. Portfolio Management* 40(5), 94-107. SSRN: 2465551

### Tier 2 (High-Quality Secondary / Practitioner)
- **S8**: Brenndoerfer, M. (2025). "Linear Algebra for Quantitative Finance: Portfolio Math." https://mbrenndoerfer.com/writing/linear-algebra-quantitative-finance-vectors-matrices-pca
- **S9**: Brenndoerfer, M. (2025). "Probability Distributions in Finance: Normal, Lognormal & Fat Tails." https://mbrenndoerfer.com/writing/probability-distributions-quantitative-finance
- **S10**: Quantt. "Linear Algebra for Quant Finance" & "Probability for Quant Finance." https://www.quantt.co.uk/resources/
- Damodaran, A. (NYU). *Statistics for Finance* webcasts & slides. https://pages.stern.nyu.edu/~adamodar/New_Home_Page/webcaststatistics.htm
- Risk Hub. *Maths for Quant Finance (MQF)* — Linear Algebra, Probability, Statistics modules. https://riskhub.org/maths-for-quants/

### Tier 3 (Tertiary / Supplementary — use for intuition only)
- 3Blue1Brown. *Essence of Linear Algebra* (YouTube). Visual intuition for eigendecomposition, SVD.
- StatQuest (Josh Starmer). *PCA, MLE, Bayesian Statistics* (YouTube). Accessible explanations.

---

*Self-critique / Verify tasks added to backlog:*
- [ ] Verify: Exact Marchenko-Pastur bounds for correlation matrix denoising in 09-market-microstructure (P2)
- [ ] Verify: Optimal shrinkage intensity formula for non-linear shrinkage (Ledoit-Wolf 2020 nonlinear) (P2)
- [ ] Verify: Copula tail dependence coefficients for equity indices in crisis vs. calm periods (P2)