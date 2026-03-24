import pandas as pd
import requests
import sys

TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 

def analyze_aggression(es_apertura=False):
    try:
        df = pd.read_csv('cinta_ggal.csv')
        buy_vol = df[df['Side'] == 'Buy']['Volume'].sum()
        sell_vol = df[df['Side'] == 'Sell']['Volume'].sum()
        delta = int(buy_vol - sell_vol)
        price = df['Price'].iloc[-1]

        print(f"🐋 WHALE SCAN: Delta actual {delta}")

        # --- RECALIBRADO: 80,000 en lugar de 120,000 ---
        if abs(delta) > 80000:
            side = "🐂 COMPRA" if delta > 0 else "🐻 VENTA"
            msg = f"🚨 *BALLENA EN ACCIÓN ({side})*\n\n"
            msg += f"📊 *Delta:* {delta} acciones\n"
            msg += f"💰 *Precio:* ${price}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
    except:
        print("❌ Error leyendo cinta")

if __name__ == "__main__":
    es_apertura = "--apertura" in sys.argv
    analyze_aggression(es_apertura=es_apertura)