import pandas as pd
import yfinance as yf
import numpy as np
from scipy.stats import norm

def get_market_data():
    """Trae datos de GGAL para calcular CCL y precio Local."""
    try:
        # Usamos un periodo de 5 días para evitar el error de 'no data'
        adr = yf.Ticker("GGAL").history(period="5d", interval="5m")
        local = yf.Ticker("GGAL.BA").history(period="5d", interval="5m")
        
        if adr.empty or local.empty:
            return 0, 0, 65.0 # Valores por defecto si falla la API
            
        p_adr = adr['Close'].iloc[-1]
        p_local = local['Close'].iloc[-1]
        ccl = (p_local * 10) / p_adr
        return round(ccl, 2), round(p_local, 2), 65.0 # 65 es la tasa TNA estimada
    except Exception as e:
        print(f"⚠️ Error en Market Data: {e}")
        return 0, 0, 65.0

def calculate_greeks(S, K, T, r, sigma):
    """Motor matemático Black-Scholes para Delta y Theta."""
    try:
        if T <= 0 or S <= 0 or sigma <= 0: return 0, 0
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        delta = norm.cdf(d1)
        # Theta diario
        theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        return round(delta, 3), round(theta, 2)
    except:
        return 0, 0

def get_signal_score():
    """Calcula el Score de Calidad (1-5 estrellas)."""
    # ... (Aquí va tu lógica de promedios móviles que ya tenías)
    return 3, "Análisis Técnico Estable", "Neutral"