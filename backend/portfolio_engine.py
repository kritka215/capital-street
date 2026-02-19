import numpy as np

np.random.seed(42)

# ==============================
# ASSET UNIVERSE
# ==============================
ASSETS = {
    "Equity":       {"mu": 0.12, "sigma": 0.18, "tax": 0.10},
    "Debt":         {"mu": 0.06, "sigma": 0.06, "tax": 0.30},
    "Gold":         {"mu": 0.09, "sigma": 0.12, "tax": 0.20},
    "Silver":       {"mu": 0.11, "sigma": 0.25, "tax": 0.20},
    "Oil":          {"mu": 0.10, "sigma": 0.22, "tax": 0.20},
    "Cash":         {"mu": 0.03, "sigma": 0.01, "tax": 0.30}
}

ASSET_NAMES = ["Equity", "Debt", "Gold", "Silver", "Oil", "Cash"]
N_ASSETS = len(ASSET_NAMES)

# ==============================
# CORRELATION & COVARIANCE
# ==============================
CORR = np.array([
    [1.0, 0.2, 0.6, 0.3, 0.5, 0.0],
    [0.2, 1.0, 0.1, 0.1, 0.0, 0.1],
    [0.6, 0.1, 1.0, 0.25, 0.2, 0.0],
    [0.3, 0.1, 0.25, 1.0, 0.3, 0.0],
    [0.5, 0.0, 0.2, 0.3, 1.0, 0.0],
    [0.0, 0.1, 0.0, 0.0, 0.0, 1.0]
])

SIGMA = np.array([ASSETS[a]["sigma"] for a in ASSET_NAMES])
COV = np.outer(SIGMA, SIGMA) * CORR

# ==============================
# TAX ADJUSTED RETURNS
# ==============================
def tax_adjusted_mu(tax_slab):
    mu = []
    for a in ASSET_NAMES:
        eff_tax = min(ASSETS[a]["tax"], tax_slab)
        mu.append(ASSETS[a]["mu"] * (1 - eff_tax))
    return np.array(mu)

# ==============================
# INVESTOR SCORE ENGINE
# ==============================
def compute_scores(inv):
    risk_capacity = (
        0.4 * (inv["time_horizon"] / 25) +
        0.3 * inv["savings_rate"] +
        0.3 * (1 - inv["liability_ratio"])
    )

    loss_tolerance = inv["max_drawdown"] / 0.5
    liquidity_pressure = (
        0.5 * inv["required_withdrawal"] +
        0.5 * (1 - inv["emergency_fund"])
    )

    return {
        "risk_capacity": np.clip(risk_capacity, 0, 1),
        "loss_tolerance": np.clip(loss_tolerance, 0, 1),
        "liquidity_pressure": np.clip(liquidity_pressure, 0, 1)
    }

# ==============================
# ALLOCATION ENGINE
# ==============================
def lifecycle_base(scores):
    growth_bias = scores["risk_capacity"] * scores["loss_tolerance"]
    liquidity_bias = scores["liquidity_pressure"]

    base = np.array([
        0.20 + 0.40 * growth_bias,
        0.35 - 0.20 * growth_bias + 0.30 * liquidity_bias,
        0.10 + 0.15 * growth_bias,
        0.07,
        0.03 + 0.12 * growth_bias,
        0.25 + 0.20 * liquidity_bias - 0.15 * growth_bias
    ])

    base = np.clip(base, 0.05, None)
    return base / base.sum()

def generate_weights(scores):
    base = lifecycle_base(scores)
    risk_tilt = scores["risk_capacity"] * scores["loss_tolerance"]

    tilt = np.array([
        0.10 * risk_tilt,
       -0.10 * risk_tilt,
        0.05 * risk_tilt,
        0.02,
        0.08 * risk_tilt,
       -0.05 * risk_tilt
    ])

    weights = np.clip(base + tilt, 0.05, None)
    return weights / weights.sum()

# ==============================
# MONTE CARLO & RISK
# ==============================
def max_drawdown(series):
    cumulative = np.cumprod(1 + series)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def compute_cvar(returns, alpha=0.05):
    # Calculate the average of the worst alpha% of returns
    sorted_returns = np.sort(returns)
    cutoff = int(alpha * len(sorted_returns))
    expected_shortfall = np.mean(sorted_returns[:cutoff])
    # Return absolute value representing "Loss Magnitude" (Standard Finance Convention)
    return abs(expected_shortfall)

def simulate_portfolio(weights, mu, cov, years=10, sims=3000):
    yearly = np.random.multivariate_normal(mu, cov, (sims, years))
    port_returns = yearly @ weights
    terminal_wealth = np.prod(1 + port_returns, axis=1)
    return port_returns, terminal_wealth

def evaluate_portfolio(weights, mu):
    paths, terminal = simulate_portfolio(weights, mu, COV)

    # Compute CVaR on the distribution of annual returns
    all_annual_returns = paths.flatten()
    cvar_5 = compute_cvar(all_annual_returns)

    return {
        "expected_return": float(np.dot(weights, mu)),
        "cvar_5": float(cvar_5),             # Annual Loss Magnitude
        "terminal_wealth": float(np.mean(terminal)),
        "avg_max_drawdown": float(np.mean([max_drawdown(p) for p in paths]))
    }

# ==============================
# EFFICIENT FRONTIER
# ==============================
# ==============================
# EFFICIENT FRONTIER OPTIMIZATION
# ==============================
def efficient_frontier_cvar(mu, n=2000):
    frontier_points = []
    frontier_weights = []

    for _ in range(n):
        w = np.random.dirichlet(np.ones(N_ASSETS))
        # Use fewer simulations per point for the frontier to maintain speed
        paths, _ = simulate_portfolio(w, mu, COV, sims=500)
        
        frontier_points.append([
            compute_cvar(paths.flatten()),     # CVaR (Risk)
            np.dot(w, mu)                      # Return
        ])
        frontier_weights.append(w)

    return np.array(frontier_points), np.array(frontier_weights)

def get_efficient_recommendation(target_risk, frontier_points, frontier_weights):
    # Filter portfolios that are close to the target risk
    # We look for the one with the highest return near that risk level
    # Or simply find the one that minimizes distance to the risk target while being on the frontier
    
    # 1. Broadly find portfolios within a small risk bound
    risk_diff = np.abs(frontier_points[:, 0] - target_risk)
    
    # 2. Find the index of the portfolio closest to the target CVaR
    # (To be even better, we could find the max return for all portfolios where risk <= target_risk)
    best_idx = np.argmin(risk_diff)
    
    return frontier_weights[best_idx]

# ==============================
# PUBLIC API
# ==============================
def recommended_portfolio(investor_profile):
    scores = compute_scores(investor_profile)
    weights = generate_weights(scores)
    
    mu = tax_adjusted_mu(investor_profile.get("tax_slab", 0.30))
    results = evaluate_portfolio(weights, mu)
    
    # We still generate the frontier for the chart, but don't use it for the weights
    # Reduced N for fast initialization transition
    frontier_points, _ = efficient_frontier_cvar(mu, n=200)

    return {
        "allocation": dict(zip(ASSET_NAMES, weights)),
        "weights": weights,
        "mu": mu,
        "results": results,
        "frontier": frontier_points
    }
