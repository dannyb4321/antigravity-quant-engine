import pandas as pd
import requests
import sys
import os
from datetime import datetime
from SignalValidator import get_signal_score # ESTO ES LO QUE TIRABA ERROR

TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 

def analyze_aggression(es_apertura=False):
    try:
        df = pd.read_csv('cinta_ggal.csv')
        delta = int(df[df['Side'] == 'Buy']['Volume'].sum() - df[df['Side'] == 'Sell']['Volume'].sum())
        price = df['Price'].iloc[-1]

        if abs(delta) > 80000:
            score, detalle_texto, direccion = get_signal_score()
            msg = f"🚨 *BALLENA ({direccion})*\n💎 *Score: {score}/5*\n📊 *Delta:* {delta}\n💰 *Precio:* ${price}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_aggression("--apertura" in sys.argv)