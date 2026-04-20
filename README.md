# Financial Engineering Projects

A collection of financial engineering projects covering derivatives pricing, portfolio optimization, risk simulation, and volatility forecasting using Python.

---

## Overview

This repository is designed as a hands-on learning portfolio for quantitative finance, financial engineering, and risk modeling.

Each project combines:

- A Jupyter notebook for experimentation, visualization, and explanation
- A Python module for reusable functions and classes
- Financial theory and mathematical intuition
- Charts, simulations, and performance evaluation

The goal is to build projects that are both educational and professional enough to showcase to recruiters, hiring managers, and quantitative teams.

---

## Projects

### 1. Monte Carlo Option Pricer

Simulates European option prices using Geometric Brownian Motion and compares the results against Black-Scholes.

Topics covered:

- Geometric Brownian Motion
- Monte Carlo simulation
- Risk-neutral pricing
- Discounted payoff estimation
- Volatility sensitivity
- Price convergence

---

### 2. Portfolio Optimizer

Builds constrained portfolios using mean-variance optimization and identifies efficient allocations.

Topics covered:

- Portfolio returns and volatility
- Covariance matrices
- Efficient frontier
- Sharpe ratio maximization
- Convex optimization with constraints
- Position sizing and allocation rules

---

### 3. Market Crash Simulator

Models extreme market scenarios using correlated returns, fat tails, and stress testing techniques.

Topics covered:

- Correlation risk
- Student t-distributions
- Scenario analysis
- Stress testing
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR)

---

### 4. Volatility Forecasting

Forecasts future market volatility using statistical and machine learning methods.

Topics covered:

- Rolling volatility models
- GARCH
- Time series features
- Machine learning regressions
- Forecast evaluation
- Volatility clustering

---

## Repository Structure

```text
financial-engineering-projects/
├── README.md
├── requirements.txt
├── data/
├── notebooks/
│   ├── monte_carlo_option_pricer.ipynb
│   ├── portfolio_optimizer.ipynb
│   ├── market_crash_simulator.ipynb
│   └── volatility_forecasting.ipynb
├── src/
│   ├── options/
│   ├── portfolio/
│   ├── risk/
│   └── volatility/
├── tests/
├── reports/
└── figures/
```

---

## Tech Stack

Main libraries expected to be used across the repo:

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- scikit-learn
- statsmodels
- arch
- cvxpy
- yfinance
- Jupyter

---

## Goals

This repo is meant to demonstrate:

- Quantitative reasoning
- Financial intuition
- Statistical modeling
- Optimization techniques
- Risk analysis
- Clean Python structure
- Reusable code design

---

## Future Improvements

Potential upgrades include:

- American option pricing
- Regime-switching volatility models
- Copulas for crash dependence
- Transaction cost modeling
- Rolling backtests
- Bayesian optimization
- LSTM volatility forecasting
- Interactive dashboards

---

## Disclaimer

These projects are for educational and research purposes only. They are not financial advice and should not be used for live trading without further validation, testing, and risk controls.

