import numpy as np
from scipy.stats import norm
import yfinance as yf

def get_market_data():
    try:
        # Traemos datos de GGAL para calcular el CCL
        adr = yf.Ticker("GGAL").history(period="2d", interval="5m")
        local = yf.Ticker("GGAL.BA").history(period="2d", interval="5m")
        if adr.empty or local.empty: return 1200.0, 6700.0, 65.0
        p_adr = adr['Close'].iloc[-1]
        p_local = local['Close'].iloc[-1]
        ccl = (p_local * 10) / p_adr
        return round(ccl, 2), round(p_local, 2), 65.0
    except:
        return 1200.0, 6700.0, 65.0

def calculate_greeks(S, K, T, r, sigma):
    """Calcula las 4 griegas principales."""
    try:
        if T <= 0 or S <= 0 or sigma <= 0: return 0.0, 0.0, 0.0, 0.0
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100
        theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        
        return round(float(delta), 3), round(float(theta), 2), round(float(gamma), 4), round(float(vega), 2)
    except:
        return 0.0, 0.0, 0.0, 0.0