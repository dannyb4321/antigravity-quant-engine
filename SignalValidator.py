import pandas as pd
import yfinance as yf

def get_signal_score():
    ticker = yf.Ticker("GGAL")
    # Bajamos data para 1H y 15m
    df_1h = ticker.history(period="5d", interval="1h")
    df_15m = ticker.history(period="2d", interval="15m")
    
    if df_1h.empty or df_15m.empty:
        return 0, "Sin Data"

    score = 0
    detalles = []

    # --- CÁLCULOS TÉCNICOS ---
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

    # --- EVALUACIÓN (SCORE 0-5) ---
    # 1. Tendencia 1H (Precio > EMA21)
    if df_1h['Close'].iloc[-1] > df_1h['EMA21'].iloc[-1]:
        score += 1
        detalles.append("📈 1H sobre EMA21")

    # 2. Momento 1H (Hist MACD subiendo)
    if df_1h['Hist'].iloc[-1] > df_1h['Hist'].iloc[-2]:
        score += 1
        detalles.append("🚀 1H Momento (+) ")

    # 3. Tendencia 15m (Precio > EMA21)
    if df_15m['Close'].iloc[-1] > df_15m['EMA21'].iloc[-1]:
        score += 1
        detalles.append("📈 15m sobre EMA21")

    # 4. Momento 15m (Hist MACD subiendo)
    if df_15m['Hist'].iloc[-1] > df_15m['Hist'].iloc[-2]:
        score += 1
        detalles.append("🔥 15m Momento (+)")

    # 5. Volatilidad (ATR Saludable - No excesivo)
    # Calculamos ATR rápido
    tr = abs(df_15m['High'] - df_15m['Low']).iloc[-1]
    atr_avg = abs(df_15m['High'] - df_15m['Low']).rolling(14).mean().iloc[-1]
    if tr > atr_avg:
        score += 1
        detalles.append("⚡ Movimiento con fuerza")

    return score, "\n".join(detalles)