"""
optimizer.py
============
Project F2 — Portfolio Optimizer (with Constraints)
Reusable functions and PortfolioOptimizer class implementing Markowitz MPT
with cvxpy-based quadratic programming.
"""

import numpy as np
import pandas as pd
import cvxpy as cp
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.optimize import minimize


# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────

def fetch_returns(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Pull adjusted close prices via yfinance and compute daily log returns.

    Parameters
    ----------
    tickers : list of ticker strings, e.g. ['SPY', 'GLD', 'BTC-USD']
    start   : start date string 'YYYY-MM-DD'
    end     : end date string   'YYYY-MM-DD'

    Returns
    -------
    pd.DataFrame of daily log returns, shape (T, N), columns = tickers
    """
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)["Close"]
    if isinstance(raw, pd.Series):          # single ticker edge case
        raw = raw.to_frame(tickers[0])
    raw = raw[tickers]                       # preserve requested order
    log_returns = np.log(raw / raw.shift(1)).dropna()
    return log_returns


def compute_stats(returns: pd.DataFrame, trading_days: int = 252) -> dict:
    """
    Compute annualised mean vector μ and covariance matrix Σ.

    Parameters
    ----------
    returns      : daily log-return DataFrame
    trading_days : annualisation factor (default 252)

    Returns
    -------
    dict with keys:
        'mu'    : np.ndarray, shape (N,)  — annualised expected returns
        'sigma' : np.ndarray, shape (N,N) — annualised covariance matrix
        'tickers': list of str
    """
    mu    = returns.mean().values * trading_days
    sigma = returns.cov().values  * trading_days
    return {"mu": mu, "sigma": sigma, "tickers": list(returns.columns)}


# ─────────────────────────────────────────────
# Optimizer
# ─────────────────────────────────────────────

class PortfolioOptimizer:
    """
    Markowitz mean-variance optimizer with position-size constraints.

    Parameters
    ----------
    mu        : annualised expected return vector, shape (N,)
    sigma     : annualised covariance matrix, shape (N,N)
    tickers   : list of asset names (length N)
    """

    def __init__(self, mu: np.ndarray, sigma: np.ndarray, tickers: list[str]):
        self.mu      = np.array(mu, dtype=float)
        self.sigma   = np.array(sigma, dtype=float)
        self.tickers = tickers
        self.n       = len(mu)

    # ── internal solver ──────────────────────────────────────────────────────

    def _solve_min_variance(
        self,
        max_weight: float = 1.0,
        target_return: float | None = None,
    ) -> np.ndarray | None:
        """
        Solve QP:  min w'Σw  s.t. 1'w=1, 0≤w≤max_weight, [w'μ≥target]
        Returns weight vector or None if infeasible.
        """
        w = cp.Variable(self.n)
        risk = cp.quad_form(w, self.sigma)
        constraints = [
            cp.sum(w) == 1,
            w >= 0,
            w <= max_weight,
        ]
        if target_return is not None:
            constraints.append(self.mu @ w >= target_return)

        prob = cp.Problem(cp.Minimize(risk), constraints)
        prob.solve(solver=cp.OSQP, warm_starting=True)

        if prob.status not in ("optimal", "optimal_inaccurate"):
            return None
        return w.value

    # ── public API ────────────────────────────────────────────────────────────

    def min_variance(self, max_weight: float = 1.0) -> dict:
        """
        Compute the global minimum-variance portfolio.

        Returns
        -------
        dict: weights, expected_return, volatility, sharpe (rf=0)
        """
        w = self._solve_min_variance(max_weight=max_weight)
        if w is None:
            raise RuntimeError("min_variance: QP infeasible")
        return self._portfolio_stats(w, label="Min-Variance")

    def max_sharpe(self, rf: float = 0.05, max_weight: float = 1.0) -> dict:
        """
        Compute the maximum-Sharpe portfolio via sequential minimisation
        of the negative Sharpe ratio (scipy.optimize.minimize SLSQP).

        Parameters
        ----------
        rf         : risk-free rate (annualised)
        max_weight : upper bound per asset

        Returns
        -------
        dict: weights, expected_return, volatility, sharpe
        """
        def neg_sharpe(w):
            ret  = self.mu @ w
            vol  = np.sqrt(w @ self.sigma @ w)
            return -(ret - rf) / (vol + 1e-12)

        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        bounds      = [(0, max_weight)] * self.n
        w0          = np.full(self.n, 1 / self.n)

        res = minimize(neg_sharpe, w0, method="SLSQP",
                       bounds=bounds, constraints=constraints,
                       options={"ftol": 1e-12, "maxiter": 1000})
        if not res.success:
            raise RuntimeError(f"max_sharpe: optimiser failed — {res.message}")
        return self._portfolio_stats(res.x, label="Max-Sharpe", rf=rf)

    def efficient_frontier(
        self,
        n_points: int = 60,
        max_weight: float = 1.0,
    ) -> pd.DataFrame:
        """
        Sweep target returns and solve min-variance at each point to
        trace the efficient frontier.

        Returns
        -------
        pd.DataFrame with columns: expected_return, volatility, sharpe, weights
        """
        # Feasible return range: between min-var return and max achievable
        mv_w   = self._solve_min_variance(max_weight=max_weight)
        mu_min = float(self.mu @ mv_w)
        mu_max = float(np.max(self.mu))
        targets = np.linspace(mu_min, mu_max * 0.99, n_points)

        rows = []
        for t in targets:
            w = self._solve_min_variance(max_weight=max_weight, target_return=t)
            if w is None:
                continue
            vol  = float(np.sqrt(w @ self.sigma @ w))
            ret  = float(self.mu @ w)
            rows.append({
                "expected_return": ret,
                "volatility":      vol,
                "sharpe":          ret / (vol + 1e-12),
                "weights":         w,
            })
        return pd.DataFrame(rows)

    def random_portfolios(self, n: int = 5000) -> pd.DataFrame:
        """
        Monte Carlo scatter — sample random weight vectors.

        Returns
        -------
        pd.DataFrame with columns: expected_return, volatility, sharpe
        """
        results = []
        for _ in range(n):
            w = np.random.dirichlet(np.ones(self.n))
            ret = float(self.mu @ w)
            vol = float(np.sqrt(w @ self.sigma @ w))
            results.append({"expected_return": ret, "volatility": vol,
                            "sharpe": ret / (vol + 1e-12)})
        return pd.DataFrame(results)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _portfolio_stats(self, w: np.ndarray, label: str = "", rf: float = 0.0) -> dict:
        ret  = float(self.mu @ w)
        vol  = float(np.sqrt(w @ self.sigma @ w))
        shrp = (ret - rf) / (vol + 1e-12)
        return {
            "label":           label,
            "weights":         dict(zip(self.tickers, w)),
            "expected_return": ret,
            "volatility":      vol,
            "sharpe":          shrp,
        }


# ─────────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────────

DARK_BG   = "#0d1117"
PANEL_BG  = "#161b22"
TEAL      = "#00d4aa"
AMBER     = "#f0a500"
RED       = "#ff4d6d"
GREY      = "#8b949e"
WHITE     = "#e6edf3"

_STYLE = {
    "figure.facecolor": DARK_BG,
    "axes.facecolor":   PANEL_BG,
    "axes.edgecolor":   GREY,
    "axes.labelcolor":  WHITE,
    "axes.titlecolor":  WHITE,
    "xtick.color":      GREY,
    "ytick.color":      GREY,
    "grid.color":       "#21262d",
    "text.color":       WHITE,
    "font.family":      "monospace",
}


def plot_frontier(
    frontier:   pd.DataFrame,
    max_sharpe: dict,
    min_vol:    dict,
    random_portfolios: pd.DataFrame | None = None,
    rf: float = 0.05,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Efficient frontier chart with Monte Carlo scatter background.

    Parameters
    ----------
    frontier           : output of optimizer.efficient_frontier()
    max_sharpe         : output of optimizer.max_sharpe()
    min_vol            : output of optimizer.min_variance()
    random_portfolios  : output of optimizer.random_portfolios() (optional)
    rf                 : risk-free rate used for Sharpe colouring
    save_path          : if given, save figure to this path
    """
    with plt.rc_context(_STYLE):
        fig, ax = plt.subplots(figsize=(11, 7))

        # — Monte Carlo scatter
        if random_portfolios is not None:
            sc = ax.scatter(
                random_portfolios["volatility"],
                random_portfolios["expected_return"],
                c=random_portfolios["sharpe"],
                cmap="plasma", alpha=0.25, s=6, zorder=1,
            )
            cbar = fig.colorbar(sc, ax=ax, pad=0.01)
            cbar.set_label("Sharpe Ratio", color=WHITE, fontsize=9)
            cbar.ax.yaxis.set_tick_params(color=GREY)
            plt.setp(cbar.ax.yaxis.get_ticklabels(), color=GREY, fontsize=8)

        # — Efficient frontier line
        ax.plot(
            frontier["volatility"],
            frontier["expected_return"],
            color=TEAL, lw=2.5, zorder=3, label="Efficient Frontier",
        )

        # — Capital Market Line
        mv_vol  = min_vol["volatility"]
        ms_ret  = max_sharpe["expected_return"]
        ms_vol  = max_sharpe["volatility"]
        cml_x   = np.linspace(0, ms_vol * 1.6, 100)
        slope   = (ms_ret - rf) / ms_vol
        cml_y   = rf + slope * cml_x
        ax.plot(cml_x, cml_y, color=AMBER, lw=1.2, ls="--",
                alpha=0.7, zorder=2, label="Capital Market Line")

        # — Special portfolios
        ax.scatter(ms_vol, ms_ret, color=AMBER, s=140, zorder=5,
                   marker="*", label=f"Max Sharpe  ({max_sharpe['sharpe']:.2f})")
        ax.scatter(mv_vol, min_vol["expected_return"], color=RED, s=90,
                   zorder=5, marker="D", label=f"Min Variance")

        # — Annotations
        ax.annotate(
            f"  Max Sharpe\n  Ret={ms_ret:.1%}  Vol={ms_vol:.1%}",
            (ms_vol, ms_ret), color=AMBER, fontsize=8,
            xytext=(ms_vol + 0.01, ms_ret + 0.005),
        )
        ax.annotate(
            f"  Min Var\n  Ret={min_vol['expected_return']:.1%}  Vol={mv_vol:.1%}",
            (mv_vol, min_vol["expected_return"]), color=RED, fontsize=8,
            xytext=(mv_vol + 0.01, min_vol["expected_return"] - 0.025),
        )

        ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
        ax.set_xlabel("Annualised Volatility (σ)", fontsize=10)
        ax.set_ylabel("Annualised Expected Return (μ)", fontsize=10)
        ax.set_title("Efficient Frontier — Markowitz MPT", fontsize=13, pad=14)
        ax.legend(fontsize=8, framealpha=0.3, loc="upper left")
        ax.grid(True, alpha=0.4)

        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        return fig


def plot_weights(
    portfolios: list[dict],
    save_path: str | None = None,
) -> plt.Figure:
    """
    Grouped bar chart of weight allocations for multiple portfolios.

    Parameters
    ----------
    portfolios : list of dicts with 'label' and 'weights' keys
    save_path  : if given, save figure to this path
    """
    tickers = list(portfolios[0]["weights"].keys())
    n_tickers  = len(tickers)
    n_ports    = len(portfolios)
    x          = np.arange(n_tickers)
    width      = 0.8 / n_ports
    colours    = [TEAL, AMBER, RED, "#a78bfa", "#34d399"]

    with plt.rc_context(_STYLE):
        fig, ax = plt.subplots(figsize=(10, 5))

        for i, port in enumerate(portfolios):
            vals = [port["weights"].get(t, 0) for t in tickers]
            offset = (i - (n_ports - 1) / 2) * width
            bars = ax.bar(x + offset, vals, width=width * 0.9,
                          label=port["label"], color=colours[i % len(colours)],
                          alpha=0.85, zorder=3)
            for bar, v in zip(bars, vals):
                if v > 0.02:
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.005, f"{v:.0%}",
                            ha="center", va="bottom", fontsize=7, color=WHITE)

        ax.set_xticks(x)
        ax.set_xticklabels(tickers, fontsize=9)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
        ax.set_ylabel("Portfolio Weight", fontsize=10)
        ax.set_title("Portfolio Allocations — Optimal Portfolios", fontsize=13, pad=12)
        ax.legend(fontsize=9, framealpha=0.3)
        ax.grid(axis="y", alpha=0.35)
        ax.set_ylim(0, 1)

        plt.tight_layout()
        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
        return fig