import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import brentq
from data import load_data
# volatility function of the heston model


def heston_call_price(S0, K, T, r, v0, kappa, theta, sigma, rho, N=1000):
    """
    Heston model call price using the characteristic function
    """
    # characteristic function
    def cf(u):
        eps = 1e-2
        eps_ = 1e+3
        d = np.sqrt((kappa - 1j * rho * sigma * u)**2 + sigma**2 * (u + 1j * u**2))
        print('d', d)
        g = (kappa - 1j * rho * sigma * u + d) / (kappa - 1j * rho * sigma * u - d)
        print('g', g)
        output = np.exp(np.minimum(1j * u * np.log(S0) + (kappa * theta * T * (kappa - 1j * rho * sigma * u - d)) / (sigma**2) * (
                (kappa - 1j * rho * sigma * u - d) * T - 2 * np.log((1 - g * np.exp(d * T)) / (1 - g))), eps_))
        print('output', output)
        return output

    # integrand
    def integrand(u):
        print('cf(u): ', cf(u))
        output = np.real(np.exp(-1j * u * np.log(K)) * cf(u) / (u**2 + 1))
        print(output)
        return output

    # call price
    return (S0 * np.exp(-r * T) * quad(integrand, 0, N)[0] / np.pi + K * np.exp(-r * T) * quad(integrand, -N, 0)[0] / np.pi)



# calibrate parameters v0, kappa, theta, sigma, rho in heston with maximum likelihood
def calibrate(S0, K, T, r, v0, kappa, theta, sigma, rho, N=1000):
    # likelihood function
    def likelihood(s, params):
        print(s)
        print(params)
        v0, kappa, theta, sigma, rho = params[0]
        return -np.sum(np.log(heston_call_price(S0, K, T, r, v0, kappa, theta, sigma, rho, N)))

    # optimize
    return brentq(likelihood, 0.1, 0.2, args=[(v0, kappa, theta, sigma, rho)])



spx, vix = load_data()

S0 = 3094.04
K = spx['strike_price'].to_numpy()
T = spx['maturity'].to_numpy()
r = 0.01

result = calibrate(S0, K, T, r, 0.1, 0.1, 0.1, 0.1, 0.1)
