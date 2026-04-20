import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm



plt.style.use('default')
TEAL  = '#00ffcc'
AMBER = '#ffb300'
GREY  = '#444444'



def simulate_gbm(S0, r, sigma, T, n_steps, n_sims):

    '''
    Inputs: 
        S0      : Initial stock price
        r       : Risk-free rate (annual)
        sigma   : Volatility (annual)
        T       : Time to maturity (years)
        n_steps : Number of time steps
        n_sims  : Number of simulations

    Output:
        paths   : array of shape (n_steps+1, n_sims)
    '''

    dt = T / n_steps
    rng = np.random.default_rng()

    Z = rng.standard_normal(size=(n_steps, n_sims))
    increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z

    log_paths = np.concatenate(
        [np.zeros((1, n_sims)), np.cumsum(increments, axis=0)],
        axis=0
    )

    paths = S0 * np.exp(log_paths)

    return paths



def price_european(paths, K, r, T, option):

    '''
    Inputs: 
        paths   : Simulated GBM prices
        K       : Strike price
        r       : Risk-free rate (annual)
        T       : Time to maturity (years)
        option  : Option type, call or put

    Output:
        price   : scalar price
    '''

    ST = paths[ -1,:]

    discount = np.exp(-r * T)

    if option == 'call':
        payoffs = np.maximum(ST - K, 0.0)

    elif option == 'put':
        payoffs = np.maximum(K - ST, 0.0)

    else:
        raise ValueError(f"option must be 'call' or 'put', got '{option}'")

    price = discount * payoffs.mean()

    return price



def black_scholes(S0, K, r, sigma, T, option):

    '''
    Inputs: 
        S0      : Initial stock price
        K       : Strike price
        r       : Risk-free rate (annual)
        sigma   : Volatility (annual)
        T       : Time to maturity (years)
        option  : Option type, call or put

    Output:
        price   : scalar price
    '''

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option == 'call':
        price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        
    elif option == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

    else:
        raise ValueError(f"option must be 'call' or 'put', got '{option}'")

    return price



def convergence_analysis(S0, K, r, sigma, T, s_range):

    '''
    Inputs: 
        S0      : Initial stock price
        K       : Strike price
        r       : Risk-free rate (annual)
        sigma   : Volatility (annual)
        T       : Time to maturity (years)
        s_range : Simulation range

    Output:
        c_pairs : list of (N, price)
    '''

    n_steps = 252
    
    prices = []
    for n in s_range:
        paths = simulate_gbm(S0, r, sigma, T, n_steps, int(n))
        price = price_european(paths, K, r, T, 'call')
        prices.append(price)
    
    c_pairs = list(zip(s_range, prices))

    return c_pairs



def sensitivity_to_vol(S0, K, r, T, n_sims, v_range):

    '''
    Inputs: 
        S0      : Initial stock price
        K       : Strike price
        r       : Risk-free rate (annual)
        T       : Time to maturity (years)
        n_sims  : Number of simulations
        v_range : Volatility range

    Output:
        v_pairs : list of (sigma, price) pairs
    '''

    n_steps = 252
    
    prices = []
    for v in v_range:
        paths = simulate_gbm(S0, r, v, T, n_steps, n_sims)
        price = price_european(paths, K, r, T, 'call')
        prices.append(price)
    
    v_pairs = list(zip(v_range, prices))

    return v_pairs



def plot_paths(paths, n_disp):

    '''
    Inputs: 
        paths   : Simulated GBM paths
        n_disp  : Number of paths to display

    Output:
        figure  : Paths fan chart
    '''


    fig = plt.figure(figsize=(14,8))

    plt.plot(paths[:, 0], color=TEAL, alpha=0.4, label='Simulated paths')
    plt.plot(paths[:, 1:n_disp], color=TEAL, alpha=0.4)  # no label
    plt.plot(paths.mean(axis=1), color=AMBER, linestyle='--', label='Mean path')

    plt.title('Simulated GBM paths')
    plt.xlabel('Steps')
    plt.ylabel('Price')

    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.close(fig)
    return fig



def plot_convergence(results, bs_price):

    '''
    Inputs: 
        paths   : Simulated prices

    Output:
        figure  : Price convergence on N
    '''

    N, price = zip(*results)


    fig = plt.figure(figsize=(14,8))

    plt.semilogx(N, price, color=TEAL, label='MC Price')
    plt.axhline(bs_price, color=AMBER, linestyle='--', label='Black-Scholes')


    plt.title('Price convergence')
    plt.xlabel('Simulations')
    plt.ylabel('Price')

    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.close(fig)
    return fig



def plot_vol_sensitivity(results):

    '''
    Inputs: 
        paths   : Simulated prices

    Output:
        figure  : Price evolution on sigma
    '''

    sigma, price = zip(*results)
    
    fig = plt.figure(figsize=(14,8))

    plt.plot(sigma, price, color=TEAL)

    plt.title('Price sensitivity')
    plt.xlabel('Volatility')
    plt.ylabel('Price')

    plt.grid(True, alpha=0.3)

    plt.close(fig)
    return fig