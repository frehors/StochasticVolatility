import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import brentq

def heston_call_price(S0, K, T, r, v0, kappa, theta, sigma, rho, N=1000):
    """
    Heston model call price using the characteristic function
    """
    # characteristic function
    def cf(u):
        d = np.sqrt((kappa - 1j * rho * sigma * u)**2 + sigma**2 * (u + 1j * u**2))
        g = (kappa - 1j * rho * sigma * u - d) / (kappa - 1j * rho * sigma * u + d)
        return np.exp(1j * u * np.log(S0) + (kappa * theta * T * (kappa - 1j * rho * sigma * u - d)) / (sigma**2) * (
                (kappa - 1j * rho * sigma * u - d) * T - 2 * np.log((1 - g * np.exp(d * T)) / (1 - g))))

    # integrand
    def integrand(u):
        return np.real(np.exp(-1j * u * np.log(K)) * cf(u) / (u**2 + 1))

    # call price
    return (S0 * np.exp(-r * T) * quad(integrand, 0, N)[0] / np.pi + K * np.exp(-r * T) * quad(integrand, -N, 0)[0] / np.pi)
