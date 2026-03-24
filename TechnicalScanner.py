import pandas as pd
import requests
import yfinance as yf

# 🚨 CONFIGURACIÓN
TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

def get_indicators(df):
    df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Hist'] = df['MACD'] - df['Signal']
    return df

def run_technical_scan():
    print(f"\n🔍 ANALIZANDO 15M Y 1H (ALCISTA/BAJISTA)...")
    try:
        ticker = yf.Ticker("GGAL")
        df_1h = get_indicators(ticker.history(period="1mo", interval="1h"))
        df_15m = get_indicators(ticker.history(period="5d", interval="15m"))

        # --- LÓGICA 1H (Tendencia) ---
        bull_1h = df_1h['Close'].iloc[-1] > df_1h['EMA21'].iloc[-1]
        bear_1h = df_1h['Close'].iloc[-1] < df_1h['EMA21'].iloc[-1]

        # --- LÓGICA 15M (Momento) ---
        bull_15m = df_15m['Hist'].iloc[-1] > 0 and df_15m['Hist'].iloc[-1] > df_15m['Hist'].iloc[-2]
        bear_15m = df_15m['Hist'].iloc[-1] < 0 and df_15m['Hist'].iloc[-1] < df_15m['Hist'].iloc[-2]

        print(f"📊 [1H: {'🐂' if bull_1h else '🐻'}] | [15m: {'🐂' if bull_15m else '🐻'}]")

        # 🟢 ESCENARIO ALCISTA
        if bull_1h and bull_15m:
            msg = "🚀 *GGAL: ESCENARIO ALCISTA CONFIRMADO*\n\n"
            msg += f"✅ *1H:* Tendencia sobre EMA 21\n"
            msg += f"🔥 *15m:* Histograma MACD acelerando al alza\n"
            msg += f"💰 *Precio:* ${df_15m['Close'].iloc[-1]:.2f}"
            send_alert(msg)

        # 🔴 ESCENARIO BAJISTA
        elif bear_1h and bear_15m:
            msg = "⚠️ *GGAL: ESCENARIO BAJISTA DETECTADO*\n\n"
            msg += f"📉 *1H:* Precio debajo de EMA 21\n"
            msg += f"❄️ *15m:* Histograma MACD hundiéndose\n"
            msg += f"💰 *Precio:* ${df_15m['Close'].iloc[-1]:.2f}"
            send_alert(msg)

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    run_technical_scan()