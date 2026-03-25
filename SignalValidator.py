import pandas as pd
import yfinance as yf
import numpy as np

def get_market_data():
    """Calcula CCL, precio Local y Tasa."""
    try:
        ticker_adr, ticker_local = yf.Ticker("GGAL"), yf.Ticker("GGAL.BA")
        df_adr = ticker_adr.history(period="5d", interval="5m")
        df_local = ticker_local.history(period="5d", interval="5m")
        if df_adr.empty or df_local.empty: return 0, 0, 65.0
        p_adr, p_local = df_adr['Close'].iloc[-1], df_local['Close'].iloc[-1]
        ccl = (p_local * 10) / p_adr
        return round(ccl, 2), round(p_local, 2), 65.0
    except: return 0, 0, 0

def get_option_greeks(p_local):
    """Calcula Delta simplificado para C6900 (Integrando iv_calc.py)."""
    strike, tna = 6900, 0.65
    distancia = (p_local - strike) / strike
    delta = max(0.1, min(0.9, 0.5 + (distancia * 1.5))) # Delta estimado
    iv = 0.85 # IV promedio estimada
    return round(delta, 2), f"{iv*100}%"

def get_signal_score():
    """Calcula Score (0-5) y Dirección Unificada."""
    try:
        ticker = yf.Ticker("GGAL")
        df_1h = ticker.history(period="7d", interval="1h")
        df_15m = ticker.history(period="5d", interval="15m")
        
        if df_1h.empty or df_15m.empty: return 0, "Cargando...", "Neutral", pd.DataFrame()

        def add_indicators(df):
            # EMA 21 (Red Line de tu imagen 2)
            df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
            # MACD
            ema12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema26 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = ema12 - ema26
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            df['Hist'] = df['MACD'] - df['Signal']
            return df

        df_1h, df_15m = add_indicators(df_1h), add_indicators(df_15m)
        score, detalles = 0, []
        last_1h, prev_1h = df_1h.iloc[-1], df_1h.iloc[-2]
        
        # Lógica de Dirección
        if last_1h['Close'] > last_1h['EMA21']:
            direccion = "BULL (Calls)"
            score += 1; detalles.append("📈 Precio > EMA21 (1H)")
            if last_1h['Hist'] > prev_1h['Hist']: score += 1; detalles.append("🚀 Momento + (1H)")
            if df_15m['Close'].iloc[-1] > df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📈 Precio > EMA21 (15m)")
        else:
            direccion = "BEAR (Puts)"
            score += 1; detalles.append("📉 Precio < EMA21 (1H)")
            if last_1h['Hist'] < prev_1h['Hist']: score += 1; detalles.append("❄️ Debilidad (1H)")
            if df_15m['Close'].iloc[-1] < df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📉 Precio < EMA21 (15m)")

        return score, "\n".join(detalles), direccion, df_15m
    except: return 0, "Error", "Neutral", pd.DataFrame()