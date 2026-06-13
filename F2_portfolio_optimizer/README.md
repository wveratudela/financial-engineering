# F2 Portfolio Optimizer (with Constraints)

Markowitz Mean-Variance Optimization implemented from first principles using
`cvxpy` (QP solver) and `scipy` (max-Sharpe). Full efficient frontier sweep,
Monte Carlo scatter, and constrained weight allocation.

---

## File Structure

```
project2_portfolio_optimizer/
├── optimizer.py      ← all reusable functions and PortfolioOptimizer class
├── notebook.ipynb    ← data pull, optimization runs, frontier & weight plots
└── README.md         ← this file
```

---

## Theory

### Expected Returns & Covariance

Daily log returns are computed as $r_t = \ln(P_t / P_{t-1})$.

Annualised statistics (252 trading days):

$$\mu = 252 \cdot \frac{1}{T}\sum_{t=1}^T r_t, \qquad \Sigma = 252 \cdot \text{Cov}(R)$$

### Min-Variance QP

The global minimum-variance portfolio solves:

$$\min_w \; w^\top \Sigma w \quad \text{s.t.} \quad \mathbf{1}^\top w = 1,\; w_i \geq 0,\; w_i \leq w_{\max}$$

Implemented with `cvxpy` (OSQP backend). A `target_return` constraint
$w^\top \mu \geq \mu^*$ is added when sweeping the efficient frontier.

### Max-Sharpe Portfolio

$$\max_w \; S = \frac{w^\top \mu - r_f}{\sqrt{w^\top \Sigma w}}$$

Solved by minimising $-S$ via `scipy.optimize.minimize` (SLSQP) with the same
bounds and equality constraint. SLSQP handles non-convex objectives and is
well-suited for this smooth, bounded problem.

### Efficient Frontier

Return range $[\mu_{\min\text{-var}},\; 0.99 \cdot \mu_{\max}]$ is swept in
`n_points` steps. At each target return a constrained QP is solved; infeasible
points (return target exceeds the constrained maximum) are dropped.

### Monte Carlo Scatter

Random weight vectors are drawn from a symmetric Dirichlet distribution
($\alpha = \mathbf{1}$), which gives uniform coverage of the simplex. Each
portfolio's (vol, return, Sharpe) is plotted as background to the frontier.

---

## optimizer.py — API Reference

### Data Functions

| Function | Returns |
|---|---|
| `fetch_returns(tickers, start, end)` | `pd.DataFrame` of daily log returns |
| `compute_stats(returns, trading_days=252)` | `dict` with `mu`, `sigma`, `tickers` |

### `PortfolioOptimizer(mu, sigma, tickers)`

| Method | Description |
|---|---|
| `.min_variance(max_weight)` | Global min-vol portfolio |
| `.max_sharpe(rf, max_weight)` | Max risk-adjusted return portfolio |
| `.efficient_frontier(n_points, max_weight)` | DataFrame of frontier points |
| `.random_portfolios(n)` | Monte Carlo DataFrame |

All portfolio methods return a dict:
```python
{
    "label":           str,
    "weights":         dict[ticker -> float],
    "expected_return": float,   # annualised
    "volatility":      float,   # annualised
    "sharpe":          float,
}
```

### Plot Functions

| Function | Output |
|---|---|
| `plot_frontier(frontier, max_sharpe, min_vol, random_portfolios, rf)` | Frontier + CML + scatter |
| `plot_weights(portfolios)` | Grouped bar chart of allocations |

---

## Notebook Flow

1. **Pull data** — `fetch_returns()` downloads via yfinance, computes log returns
2. **Compute μ, Σ** — `compute_stats()` annualises; correlation matrix printed
3. **Run optimizer** — min-var, max-Sharpe, frontier sweep, Monte Carlo scatter
4. **Plot frontier** — efficient frontier line, CML, Monte Carlo background, annotated special portfolios
5. **Plot weights** — grouped bars for min-var vs max-Sharpe
6. **Summary table** — return / vol / Sharpe / weights for both portfolios

---

## Configuration

Edit the top of the notebook to adjust the universe and constraints:

```python
TICKERS = ['SPY', 'QQQ', 'GLD', 'TLT', 'BTC-USD']
START   = '2020-01-01'
END     = '2024-12-31'
RF      = 0.05   # risk-free rate (annualised)
WMAX    = 0.40   # max weight per asset
```

Tightening `WMAX` (e.g. to 0.25) forces broader diversification and compresses
the frontier toward the centre. Setting `WMAX = 1.0` removes the upper bound.

---

## Dependencies

```
yfinance>=0.2
cvxpy>=1.4
scipy>=1.11
numpy>=1.25
pandas>=2.0
matplotlib>=3.8
```

Install: `pip install yfinance cvxpy scipy numpy pandas matplotlib`

---

## Key Findings (on SPY / QQQ / GLD / TLT / BTC-USD, 2020–2024)

- **Min-Variance** concentrates in TLT (bonds) and GLD (gold) — assets with
  negative or near-zero correlation to equities dominate when the objective is
  pure risk reduction.
- **Max-Sharpe** tilts into SPY / QQQ and takes the maximum allowed BTC
  allocation — higher expected return assets win once Sharpe is the criterion.
- The `WMAX = 0.40` constraint meaningfully diversifies both portfolios vs the
  unconstrained solution; removing it causes Max-Sharpe to corner-load into BTC.
- Correlation between SPY/QQQ is high (~0.9), so the optimizer rarely holds both
  at significant weights simultaneously.
- The Capital Market Line slope (Sharpe of the tangency portfolio) is sensitive
  to the assumed risk-free rate; higher `RF` pulls the CML steeper and shifts
  the tangency point leftward on the frontier.