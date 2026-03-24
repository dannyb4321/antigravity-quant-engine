 import pandas as pd
import requests
import os
import yfinance as yf
import time

# 🚨 CONFIGURACIÓN DE TELEGRAM (LISTO PARA USAR)
TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.get(url, params=params)
    except Exception as e:
        print(f"⚠️ Error al conectar con Telegram: {e}")

def run_technical_scan():
    print(f"\n📊 Analizando Indicadores Técnicos (MACD + EMA 21)...")
    try:
        # Bajamos datos históricos (5 días, velas de 5 min)
        ticker = yf.Ticker("GGAL")
        hist = ticker.history(period="5d", interval="5m")
        if hist.empty: return
        
        # --- 📈 CÁLCULOS TÉCNICOS ---
        
        # 1. EMA 21 (Tendencia)
        hist['EMA21'] = hist['Close'].ewm(span=21, adjust=False).mean()
        
        # 2. MACD (12, 26, 9)
        exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = exp1 - exp2
        hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
        
        # !!! EL HITOGRAMA !!! (Danny, esto es lo que pediste)
        hist['Histogram'] = hist['MACD'] - hist['Signal']

        # Valores actuales (última vela cerrada)
        precio_actual = hist['Close'].iloc[-1]
        ema_actual = hist['EMA21'].iloc[-1]
        macd_actual = hist['MACD'].iloc[-1]
        hist_actual = hist['Histogram'].iloc[-1]
        hist_anterior = hist['Histogram'].iloc[-2]

        # --- 🚨 LÓGICA DE ALERTA ÁGIL (MOMENTUM) ---
        
        # Condición 1: Tendencia Saludable (Precio por encima de EMA 21)
        confirmacion_tendencia = precio_actual > ema_actual
        
        # Condición 2: Aceleración de Momentum (Histograma se expande)
        # Danny, esto te avisa antes que el cruce: el hist_actual es mayor que el anterior y está sobre cero.
        aceleracion_momentum = hist_actual > hist_anterior and hist_actual > 0

        # Alerta Estratégica
        if confirmacion_tendencia and aceleracion_momentum:
            msg = f"🎯 *SEÑAL DE ENTRADA ÁGIL (GGAL)*\n\n"
            msg += f"✅ *Tendencia:* Precio sobre EMA 21 (${precio_actual:.2f})\n"
            msg += f"🔥 *Momentum (Histograma):* Expandiéndose (${hist_actual:.4f})\n"
            msg += f"🚀 _El motor Anti-Gravity detectó aceleración institucional._"
            send_telegram_alert(msg)
            print("📲 Alerta técnica enviada a Telegram.")

    except Exception as e:
        print(f"⚠️ Error en TechnicalScanner: {e}")

if __name__ == "__main__":
    run_technical_scan()