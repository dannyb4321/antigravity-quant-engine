import pandas as pd
import requests
import sys
import os
from datetime import datetime

TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 
LOG_FILE = "whale_alerts_history.csv" # Nuestra base de datos simple

def log_whale_event(delta, price):
    """Guarda la alerta en un archivo CSV para análisis posterior."""
    file_exists = os.path.isfile(LOG_FILE)
    
    log_data = {
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'delta': [delta],
        'price': [price],
        'side': ['Buy' if delta > 0 else 'Sell']
    }
    df_log = pd.DataFrame(log_data)
    
    # Guardamos (append) sin borrar lo anterior
    df_log.to_csv(LOG_FILE, mode='a', index=False, header=not file_exists)
    print(f"💾 Evento registrado en {LOG_FILE}")

def analyze_aggression(es_apertura=False):
    try:
        df = pd.read_csv('cinta_ggal.csv')
        buy_vol = df[df['Side'] == 'Buy']['Volume'].sum()
        sell_vol = df[df['Side'] == 'Sell']['Volume'].sum()
        delta = int(buy_vol - sell_vol)
        price = df['Price'].iloc[-1]

        # --- LÓGICA DE ALERTA Y LOG ---
        if abs(delta) > 80000:
            log_whale_event(delta, price) # Registramos en la base de datos
            
            side = "🐂 COMPRA" if delta > 0 else "🐻 VENTA"
            msg = f"🚨 *BALLENA DETECTADA ({side})*\n\n"
            msg += f"📊 *Delta:* {delta} acciones\n"
            msg += f"💰 *Precio:* ${price}\n"
            
            # Aquí podrías importar y sumar el reporte de RiskManager
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
    except:
        print("❌ Error en Whale Scan")

if __name__ == "__main__":
    es_apertura = "--apertura" in sys.argv
    analyze_aggression(es_apertura=es_apertura)