import pandas as pd
import yfinance as yf

def get_market_data():
    """Trae datos de GGAL (ADR) y GGAL.BA (Local) para calcular el CCL."""
    try:
        ticker_adr = yf.Ticker("GGAL")
        ticker_local = yf.Ticker("GGAL.BA")
        
        df_adr = ticker_adr.history(period="1d", interval="5m")
        df_local = ticker_local.history(period="1d", interval="5m")
        
        if df_adr.empty or df_local.empty:
            return 0, 0, 65.0 # Tasa fija de seguridad
        
        p_adr = df_adr['Close'].iloc[-1]
        p_local = df_local['Close'].iloc[-1]
        
        ccl = (p_local * 10) / p_adr
        return ccl, p_local, 65.0
    except:
        return 0, 0, 0

def get_signal_score():
    """Calcula el puntaje de calidad (0-5) y la dirección (BULL/BEAR)."""
    ticker = yf.Ticker("GGAL")
    df_1h = ticker.history(period="5d", interval="1h")
    df_15m = ticker.history(period="2d", interval="15m")
    
    if df_1h.empty or df_15m.empty:
        return 0, "Sin Data", "Neutral"

    # --- INDICADORES ---
    def add_indicators(df):
        df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Hist'] = df['MACD'] - df['Signal']
        return df

    df_1h = add_indicators(df_1h)
    df_15m = add_indicators(df_15m)

    score = 0
    detalles = []
    
    # 1. Dirección por EMA 21 en 1H
    last_1h = df_1h.iloc[-1]
    if last_1h['Close'] > last_1h['EMA21']:
        direccion = "BULL (Calls)"
        if last_1h['Close'] > last_1h['EMA21']: score += 1; detalles.append("📈 1H sobre EMA21")
        if last_1h['Hist'] > df_1h['Hist'].iloc[-2]: score += 1; detalles.append("🚀 1H Momento (+)")
        if df_15m['Close'].iloc[-1] > df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📈 15m sobre EMA21")
        if df_15m['Hist'].iloc[-1] > df_15m['Hist'].iloc[-2]: score += 1; detalles.append("🔥 15m Momento (+)")
    else:
        direccion = "BEAR (Puts)"
        if last_1h['Close'] < last_1h['EMA21']: score += 1; detalles.append("📉 1H bajo EMA21")
        if last_1h['Hist'] < df_1h['Hist'].iloc[-2]: score += 1; detalles.append("❄️ 1H Debilidad")
        if df_15m['Close'].iloc[-1] < df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📉 15m bajo EMA21")
        if df_15m['Hist'].iloc[-1] < df_15m['Hist'].iloc[-2]: score += 1; detalles.append("🔻 15m Aceleración (-)")

    # Volatilidad (ATR)
    tr = abs(df_15m['High'] - df_15m['Low']).iloc[-1]
    atr_avg = abs(df_15m['High'] - df_15m['Low']).rolling(14).mean().iloc[-1]
    if tr > atr_avg:
        score += 1
        detalles.append("⚡ Movimiento con fuerza")

    return score, "\n".join(detalles), direccion