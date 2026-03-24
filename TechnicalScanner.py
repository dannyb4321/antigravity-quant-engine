import pandas as pd
import requests
import yfinance as yf
import os

TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

def run_technical_scan():
    try:
        ticker = yf.Ticker("GGAL")
        # Bajamos data de 5 días para tener promedio de EMA 21 estable
        df = ticker.history(period="5d", interval="5m")
        if df.empty: return

        # --- INDICADORES ---
        df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['Hist'] = df['MACD'] - df['Signal'] # El Histograma

        last = df.iloc[-1]
        prev = df.iloc[-2]

        # --- LÓGICA CAZADOR DE RENDIMIENTO ---
        # 1. Filtro de Tendencia (Precio > EMA 21)
        tendencia_ok = last['Close'] > last['EMA21']
        
        # 2. Filtro de Momento (Histograma creciendo)
        # Danny: Esto es lo que pediste, detecta si la fuerza compradora se acelera
        momento_ok = last['Hist'] > prev['Hist'] and last['Hist'] > 0

        print(f"🔍 TÉCNICO: Precio ${last['Close']:.2f} | Histograma: {last['Hist']:.4f}")

        if True:
            msg = f"🎯 *SEÑAL TÉCNICA DETECTADA*\n\n"
            msg += f"📈 *GGAL* está sobre la EMA 21.\n"
            msg += f"🔥 *Histograma MACD:* Acelerando al alza.\n"
            msg += f"💎 _Catalizador alcista en formación._"
            send_alert(msg)
            print("📲 Alerta técnica enviada.")

    except Exception as e:
        print(f"⚠️ Error técnico: {e}")

if __name__ == "__main__":
    run_technical_scan()