import pandas as pd
import yfinance as yf

def get_market_data():
    """Trae datos de GGAL (ADR) y GGAL.BA (Local) para el monitor."""
    try:
        ticker_adr, ticker_local = yf.Ticker("GGAL"), yf.Ticker("GGAL.BA")
        df_adr = ticker_adr.history(period="5d", interval="5m")
        df_local = ticker_local.history(period="5d", interval="5m")
        
        if df_adr.empty or df_local.empty: return 0, 0, 65.0
        
        p_adr, p_local = df_adr['Close'].iloc[-1], df_local['Close'].iloc[-1]
        ccl = (p_local * 10) / p_adr
        return ccl, p_local, 65.0
    except:
        return 0, 0, 0

def get_signal_score():
    """Calcula Score y Dirección (BULL/BEAR)."""
    ticker = yf.Ticker("GGAL")
    df_1h = ticker.history(period="7d", interval="1h")
    df_15m = ticker.history(period="5d", interval="15m")
    
    if df_1h.empty or df_15m.empty: return 0, "Cargando...", "Neutral"

    def add_indicators(df):
        df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
        exp1, exp2 = df['Close'].ewm(span=12, adjust=False).mean(), df['Close'].ewm(span=26, adjust=False).mean()
        df['Hist'] = (exp1 - exp2) - (exp1 - exp2).ewm(span=9, adjust=False).mean()
        return df

    df_1h, df_15m = add_indicators(df_1h), add_indicators(df_15m)
    score, detalles = 0, []
    
    # Lógica Bidireccional
    if df_1h['Close'].iloc[-1] > df_1h['EMA21'].iloc[-1]:
        direccion = "BULL (Calls)"
        score += 1; detalles.append("📈 1H sobre EMA21")
        if df_1h['Hist'].iloc[-1] > df_1h['Hist'].iloc[-2]: score += 1; detalles.append("🚀 1H Momento (+)")
        if df_15m['Close'].iloc[-1] > df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📈 15m sobre EMA21")
    else:
        direccion = "BEAR (Puts)"
        score += 1; detalles.append("📉 1H bajo EMA21")
        if df_1h['Hist'].iloc[-1] < df_1h['Hist'].iloc[-2]: score += 1; detalles.append("❄️ 1H Debilidad")
        if df_15m['Close'].iloc[-1] < df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📉 15m bajo EMA21")

    return score, "\n".join(detalles), direccion