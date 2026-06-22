# Financial Engineering

Derivatives pricing, hedging, and risk modelling.
Mathematical finance from first principles.

**github.com/wveratudela/financial-engineering** · *Dr. Walter Vera-Tudela*

---

## Overview

Five projects covering the mathematical foundations of derivatives pricing and risk management: from option pricing via simulation through Greeks and dynamic hedging, yield curve construction, volatility surface modelling, and tail dependence via copulas. Each project is built from first principles and benchmarked against analytical solutions where they exist.

This work runs parallel to the empirical research in the **Q repo** and the control-theoretic methods in the **M repo**. The derivatives layer connects to both: volatility modelling feeds into regime detection, and hedging cost analysis informs rebalancing design.

---

## Repository Structure
```
financial-engineering/
│
├── README.md                              ← You are here
│
├── F1_monte_carlo_option_pricer/
│   ├── F1_notebook.ipynb
│   ├── F1_functions.py
│   └── README.md
│
├── F2_greeks_dynamic_hedging/
│   ├── F2_notebook.ipynb
│   ├── F2_functions.py
│   └── README.md
│
├── F3_yield_curve_fixed_income/
│   ├── F3_notebook.ipynb
│   ├── F3_functions.py
│   └── README.md
│
├── F4_volatility_surface/
│   ├── F4_notebook.ipynb
│   ├── F4_functions.py
│   └── README.md
│
├── F5_copula_tail_dependence/
│   ├── F5_notebook.ipynb
│   ├── F5_functions.py
│   └── README.md
│
└── utils/
    └── common.py                          ← Shared utilities (data fetching, pricing helpers)
```

---

## Project Roadmap

| # | Project | Status | Key Concept |
|---|---------|--------|-------------|
| F1 | Monte Carlo Option Pricer | 🔄 In Progress | GBM simulation, risk-neutral pricing, Black-Scholes benchmark |
| F2 | Greeks & Dynamic Hedging | 📋 Planned | Delta/Gamma/Vega sensitivities, hedging cost, P&L simulation |
| F3 | Yield Curve & Fixed Income | 📋 Planned | Curve bootstrapping, bond pricing, duration, convexity |
| F4 | Volatility Surface Modelling | 📋 Planned | Implied vol extraction, smile/skew, surface calibration |
| F5 | Copula-Based Crash Dependence | 📋 Planned | Tail correlation, Gaussian/t/Clayton copulas, stress scenarios |

---

## Projects

### F1 — Monte Carlo Option Pricer *(in progress)*
`Python · numpy · scipy`

European option pricing via Geometric Brownian Motion simulation, benchmarked against the Black-Scholes closed-form solution. Covers risk-neutral pricing, convergence analysis as a function of simulation count, and volatility sensitivity.

**Research questions:** How many paths are needed for pricing accuracy within 1bp? How does simulation error scale with moneyness and time to expiry? What does constant-volatility GBM miss that the later projects (F4) address?

*This project establishes the simulation infrastructure and constant-vol baseline that F2–F4 extend and stress-test.*

---

### F2 — Greeks & Dynamic Hedging *(planned)*
`Python · numpy · matplotlib`

Analytical and numerical computation of Delta, Gamma, Vega, Theta, and Rho. P&L simulation of a dynamically delta-hedged options position across a range of rehedging frequencies.

**Research questions:** How does hedging error accumulate over time? What is the actual cost of maintaining a delta-neutral book under discrete rehedging? How does Gamma exposure drive P&L between rehedge points?

*Connects derivative sensitivities to practical risk management — the translation from model to desk.*

---

### F3 — Yield Curve & Fixed Income *(planned)*
`Python · numpy · scipy`

Bootstrapping a par yield curve from real US Treasury data, pricing zero-coupon and coupon bonds, computing duration and convexity, and pricing interest rate swaps.

**Research questions:** How sensitive is bond pricing to curve shape assumptions? What does the 2022 rate shock look like through a duration/convexity lens? How does TLT's Q4 behaviour (60% of tail loss in 2022) decompose in fixed income terms?

*Grounds the discount factor in real market data and introduces rates as a first-class variable — the foundation for credit derivatives in F5.*

---

### F4 — Volatility Surface Modelling *(planned)*
`Python · numpy · scipy · matplotlib`

Implied volatility extraction from option chain data across strikes and maturities. Smile and skew analysis. Surface interpolation and basic calibration.

**Research questions:** What does the volatility surface look like around earnings announcements vs quiet markets? How does the surface shift before and after the COVID crash? How much pricing error does constant-vol GBM (F1) introduce on OTM puts?

*Breaks the central assumption of F1 and directly motivates the jump-diffusion and stochastic vol extensions that underlie modern options desks.*

---

### F5 — Copula-Based Crash Dependence *(planned)*
`Python · scipy · numpy`

Tail correlation modelling using Gaussian, Student-t, and Clayton copulas. Analysis of pairwise and portfolio-level tail dependence during stress scenarios (2020 COVID, 2022 rates, 2008 financial crisis).

**Research questions:** Which asset pairs exhibit tail dependence that their unconditional correlations hide? Does the diversification observed in Q3 survive in the tail? How does the copula structure shift between crisis and non-crisis regimes?

*Assets that appear uncorrelated in normal markets crash together — this project makes that dependence explicit and connects directly to the stress testing findings in Q4.*

---

## Research Positioning

> *"The Q repo tests what works empirically. This repo asks why — and what the mathematics predicts when markets break."*

F1–F3 build the pricing and rates foundations. F4 connects to the volatility regime work in Q4 and M. F5 closes the loop on tail risk by modelling the dependence structure that MC VaR (Q4) cannot capture.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core language |
| numpy & scipy | Numerical methods, optimisation, statistical distributions |
| matplotlib | Visualisation, surface plots |
| pandas | Data handling for real market inputs |

All projects built from first principles. No black-box pricing libraries — the goal is to understand the machinery, not call a function.

---

## Related Repositories

| Repo | Focus |
|---|---|
| [Q — Quant Research](https://github.com/wveratudela/quant-research) | Signal generation, portfolio optimisation, tail risk, ML signals |

---

*Dr. Walter Vera-Tudela · [github.com/wveratudela](https://github.com/wveratudela)*

---

## Disclaimer

This repository is for educational and research purposes only. Nothing here constitutes financial advice. All models are tested on historical data, and past performance does not guarantee future results.
