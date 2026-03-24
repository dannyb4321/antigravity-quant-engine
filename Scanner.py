import pandas as pd
import requests
import os
import time
import yfinance as yf

# 🚨 CONFIGURACIÓN DE TELEGRAM
TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 
PHOTO_PATH = "heatmap_ggal.png"

def send_telegram_alert_with_photo(message, photo_path=None):
    base_url = f"https://api.telegram.org/bot{TOKEN}"
    if photo_path and os.path.exists(photo_path):
        url = f"{base_url}/sendPhoto"
        try:
            with open(photo_path, 'rb') as photo:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': message, 'parse_mode': 'Markdown'}, files={'photo': photo})
            return
        except:
            pass
    
    requests.post(f"{base_url}/sendMessage", data={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})

def analyze_aggression(es_apertura=False):
    try:
        df = pd.read_csv('cinta_ggal.csv')
    except: return

    # Cálculos básicos
    buy_vol = df[df['Side'] == 'Buy']['Volume'].sum()
    sell_vol = df[df['Side'] == 'Sell']['Volume'].sum()
    delta = int(buy_vol - sell_vol)
    price_now = df['Price'].iloc[-1]

    # --- LÓGICA DE APERTURA (GAP) ---
    if es_apertura:
        ticker = yf.Ticker("GGAL")
        prev_close = ticker.info.get('previousClose', price_now)
        gap = ((price_now - prev_close) / prev_close) * 100
        
        msg = f"☀️ *REPORTE DE APERTURA - GGAL*\n\n"
        msg += f"💵 *Precio Inicio:* ${price_now:.2f}\n"
        msg += f"📊 *Gap:* {gap:+.2f}%\n"
        msg += f"🥊 *Delta Inicial:* {delta} acciones\n\n"
        msg += "🚀 _El mercado está en marcha. Buscando huellas institucionales..._"
        send_telegram_alert_with_photo(msg, PHOTO_PATH)
        return

    # --- LÓGICA DE ALERTA NORMAL (DURANTE LA RUEDA) ---
    rvol = df['Volume'].sum() / 750000
    if abs(delta) > 120000 or rvol > 2.0:
        msg = f"🚨 *BALLENA DETECTADA*\n\n📈 *Delta:* {delta}\n🔥 *RVOL:* {rvol:.2f}x\n💰 *Precio:* ${price_now}"
        send_telegram_alert_with_photo(msg, PHOTO_PATH)

if __name__ == "__main__":
    analyze_aggression()