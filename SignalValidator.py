import pandas as pd
import yfinance as yf

def get_signal_score():
    ticker = yf.Ticker("GGAL")
    df_1h = ticker.history(period="5d", interval="1h")
    df_15m = ticker.history(period="2d", interval="15m")
    
    if df_1h.empty or df_15m.empty: return 0, "Sin Data", "Neutral"

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

    # Variables de control
    score = 0
    detalles = []
    direccion = "Neutral"

    # --- DETECCIÓN DE DIRECCIÓN ---
    precio_1h = df_1h['Close'].iloc[-1]
    ema_1h = df_1h['EMA21'].iloc[-1]

    if precio_1h > ema_1h:
        direccion = "BULL (Calls)"
        # Lógica Alcista
        if precio_1h > ema_1h: score += 1; detalles.append("📈 1H sobre EMA21")
        if df_1h['Hist'].iloc[-1] > df_1h['Hist'].iloc[-2]: score += 1; detalles.append("🚀 1H Momento (+)")
        if df_15m['Close'].iloc[-1] > df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📈 15m sobre EMA21")
        if df_15m['Hist'].iloc[-1] > df_15m['Hist'].iloc[-2]: score += 1; detalles.append("🔥 15m Momento (+)")
    else:
        direccion = "BEAR (Puts)"
        # Lógica Bajista
        if precio_1h < ema_1h: score += 1; detalles.append("📉 1H bajo EMA21 (Techo)")
        if df_1h['Hist'].iloc[-1] < df_1h['Hist'].iloc[-2]: score += 1; detalles.append("❄️ 1H Debilidad")
        if df_15m['Close'].iloc[-1] < df_15m['EMA21'].iloc[-1]: score += 1; detalles.append("📉 15m bajo EMA21")
        if df_15m['Hist'].iloc[-1] < df_15m['Hist'].iloc[-2]: score += 1; detalles.append("🔻 15m Aceleración Bajista")

    # 5. Volatilidad (ATR)
    tr = abs(df_15m['High'] - df_15m['Low']).iloc[-1]
    atr_avg = abs(df_15m['High'] - df_15m['Low']).rolling(14).mean().iloc[-1]
    if tr > atr_avg:
        score += 1
        detalles.append("⚡ Movimiento con fuerza")

    return score, "\n".join(detalles), direccion