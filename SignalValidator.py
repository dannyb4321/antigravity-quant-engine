import numpy as np
from scipy.stats import norm

def calculate_greeks(S, K, T, r, sigma):
    """
    S: Precio Spot (GGAL local)
    K: Strike (ej: 6900)
    T: Tiempo al vto en años (días/365)
    r: Tasa de interés (0.65 para 65%)
    sigma: Volatilidad Implícita (ej: 0.80 para 80%)
    """
    if T <= 0: return 0, 0
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    delta = norm.cdf(d1)
    # Theta diaria (dividido 365)
    theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    
    return round(delta, 3), round(theta, 2)