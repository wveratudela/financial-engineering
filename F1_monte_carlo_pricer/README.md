# F1 — Monte Carlo Option Pricer

Price European call/put options by simulating thousands of Geometric Brownian Motion paths, then benchmark the result against the Black–Scholes closed-form solution.

---

## Project Structure

```
F1_monte_carlo_pricer/
├── F1_functions.py       # All reusable functions
├── F1_notebook.ipynb     # Loads parameters, runs analysis, displays results
└── README.md             # Project structure, methodology, findings
```

---

## Methodology

### Geometric Brownian Motion
Stock prices are simulated under the **risk-neutral measure**, replacing the real-world drift μ with the risk-free rate r. This is justified by the no-arbitrage argument: a perfectly delta-hedged option portfolio is riskless and must therefore earn exactly r. The drift of the underlying becomes irrelevant to pricing.

Each path is constructed via the log-normal discretisation:

$$S_{t+\Delta t} = S_t \cdot \exp\!\left[\left(r - \tfrac{1}{2}\sigma^2\right)\Delta t + \sigma\sqrt{\Delta t}\cdot Z\right], \quad Z \sim \mathcal{N}(0,1)$$

The $-\frac{1}{2}\sigma^2$ term is the **Itô correction** — it adjusts for the convexity of the exponential so that $\mathbb{E}[S_t] = S_0 e^{rt}$ holds exactly under the risk-neutral measure.

### Monte Carlo Pricing
For each simulated terminal price $S_T$, the option payoff is computed and discounted:

$$C_0 = e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \max(S_T^{(i)} - K,\ 0)$$

By the Law of Large Numbers, this estimator converges to the true option price as $N \to \infty$. The MC standard error decays at rate $1/\sqrt{N}$ — halving the error requires quadrupling the number of simulations.

### Black–Scholes Benchmark
The closed-form BS price serves as the ground truth:

$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$

$$d_1 = \frac{\ln(S_0/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

Put prices are derived via put-call parity. Both MC and BS share the same risk-neutral assumptions, so MC must converge to BS as $N \to \infty$.

---

## Results & Analysis

### GBM Fan Chart
Simulated paths fan out from $S_0 = 100$ in a characteristic cone shape, widening with time. The mean path drifts upward at the risk-free rate, consistent with the risk-neutral construction. The spread of terminal prices $S_T$ is the source of option value.

### MC vs BS Comparison (1,000 simulations)
| | MC Price | BS Price |
|---|---|---|
| Call | ~10.47 | 10.45 |
| Put | ~5.61 | 5.57 |

At 1,000 simulations, MC already prices within a few cents of BS — well within acceptable error for most applications.

### Convergence Analysis
MC prices are volatile at low simulation counts (100–1,000), with errors exceeding $0.50. By $10^4$ simulations the price stabilises close to the BS benchmark, and by $10^5$ it is essentially indistinguishable. The log-scale x-axis makes the $1/\sqrt{N}$ convergence rate visually interpretable — each order of magnitude of additional simulations yields a proportional reduction in error.

### Vol Sensitivity (Vega Sweep)
Option price increases monotonically with volatility across the range σ = 0.01 to 0.50. This reflects the asymmetric payoff structure of options: higher vol widens the distribution of $S_T$, increasing the probability and magnitude of large positive payoffs, while the downside remains floored at zero. The curve is approximately linear through the mid-vol range (0.10–0.35) and shows increasing MC noise above σ = 0.40 due to higher payoff variance at large vol.

---

## Conclusions

- MC option pricing converges reliably to the BS closed form, validating the risk-neutral GBM framework
- The $1/\sqrt{N}$ convergence rate makes MC computationally expensive for high precision — 100× more paths are needed to achieve 10× more accuracy
- Vega (price sensitivity to vol) is strictly positive for calls and puts — consistent with BS theory
- At moderate simulation counts (10,000+), MC is a practical and flexible pricing engine, particularly for path-dependent or exotic options where BS has no closed form

---

## Limitations & Next Steps

**Limitations**
- GBM assumes constant volatility — real markets exhibit volatility clustering and skew (addressed by GARCH or stochastic vol models)
- The model assumes no dividends, frictionless markets, and continuous trading — all simplifications
- MC noise at high vol degrades the vol sensitivity curve; smoothing requires significantly more simulations

**Next Steps**
- **GARCH integration**: Replace the flat σ assumption in `simulate_gbm()` with a GARCH(1,1) forecast for time-varying volatility
- **Antithetic variates**: Use paired $(Z, -Z)$ draws to reduce MC variance without increasing simulation count
- **Exotic options**: Extend `price_european()` to price Asian options (payoff depends on path average) or barrier options — cases where BS has no closed form and MC is the only practical approach
- **Greeks via MC**: Estimate delta, gamma, and vega numerically by bumping parameters and re-pricing

---

## Dependencies

```bash
pip install numpy scipy matplotlib
```

| Library | Usage |
|---|---|
| `numpy` | GBM path simulation, array operations |
| `scipy.stats` | Normal CDF for Black–Scholes (`norm.cdf`) |
| `matplotlib` | Fan chart, convergence plot, vol sensitivity curve |