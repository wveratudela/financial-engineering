# Financial Engineering

A focused collection of financial engineering projects covering derivatives pricing, hedging, risk modelling, and volatility — built from first principles in Python.

Each project is self-contained and delivers a Jupyter notebook, a reusable Python module, and a README with methodology, findings, and honest limitations.

---

## Background & Motivation

My background is in numerical modelling, optimisation, and scientific computing (Python, C++, MATLAB). This repository focuses specifically on the mathematical and computational side of financial instruments — pricing, hedging, and modelling the behaviour of derivatives and risk.

The goal is not to survey the field. It is to go deep on a small number of problems, understand the theory from the ground up, and build tools that demonstrate both rigour and practical awareness.

---

## Repository Structure

```
financial-engineering/
│
├── README.md                        ← You are here
│
├── F1_monte_carlo_option_pricer/
│   ├── F1_notebook.ipynb
│   ├── F1_functions.py
│   └── README.md
│
├── F2_greeks_and_dynamic_hedging/   ← Planned
│   └── ...
│
├── F3_yield_curve_and_fixed_income/ ← Planned
│   └── ...
│
├── F4_volatility_surface/           ← Planned
│   └── ...
│
├── F5_copula_crash_dependence/      ← Planned
│   └── ...
│
└── utils/
    └── common.py                    ← Shared utilities
```

---

## Project Roadmap

| # | Project | Status | Key Concept |
|---|---------|--------|-------------|
| F1 | Monte Carlo Option Pricer | 🔄 In progress | GBM simulation, risk-neutral pricing, Black-Scholes benchmarking |
| F2 | Greeks & Dynamic Hedging | 📋 Planned | Delta/Gamma/Vega, hedging P&L simulation, hedging error analysis |
| F3 | Yield Curve & Fixed Income | 📋 Planned | Bootstrapping, bond pricing, duration, convexity |
| F4 | Volatility Surface Modelling | 📋 Planned | Implied vol, smile/skew, surface calibration |
| F5 | Copula-Based Crash Dependence | 📋 Planned | Tail correlation, default dependence, stress-tested joint distributions |

---

## Project Arc

The five projects form a deliberate progression — each one exposing a limitation of the last:

**F1** prices a European option assuming constant volatility and a single underlying. It works. But it immediately raises two questions: how do you hedge it, and what happens when volatility isn't constant?

**F2** answers the first question. A priced option is only useful if you can manage the risk it introduces. Delta hedging neutralises directional exposure — but only imperfectly, and the cost of that imperfection compounds over time.

**F3** introduces rates as a first-class variable. Option pricing discounts future payoffs — but at what rate? Bootstrapping a yield curve from real treasury data and pricing fixed income instruments grounds the discount factor in reality.

**F4** answers the constant volatility problem. Implied volatility is not flat — it forms a surface across strikes and maturities. Calibrating that surface is one of the core problems in derivatives risk management.

**F5** addresses the hardest problem: what happens in a crash, when correlations between instruments stop behaving as they do in normal markets? Copulas model the dependence structure in the tails, directly relevant to reinsurance, credit risk, and portfolio stress testing.

---

## Key Findings

*This section will be updated as projects are completed. Results are added only once verified — no placeholder metrics.*

### F1 — Monte Carlo Option Pricer *(in progress)*

*Findings to be documented on completion.*

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Jupyter Notebook | Research environment |
| NumPy & pandas | Numerical computing and data handling |
| SciPy | Statistical distributions, optimisation |
| matplotlib | Visualisation |
| arch | GARCH volatility modelling (F4) |
| cvxpy | Convex optimisation where needed |
| yfinance | Market data |

---

## Disclaimer

This repository is for educational and research purposes only. Nothing here constitutes financial advice. All models are tested on historical data, and past performance does not guarantee future results.