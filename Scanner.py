import pandas as pd
import requests
import sys
import os
from datetime import datetime
from SignalValidator import get_signal_score # Importamos el validador

TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 
LOG_FILE = "trading_log_ggal.csv"

def log_event(delta, price, score):
    """Guarda la oportunidad en la base de datos CSV."""
    nuevo = {
        'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M')],
        'Precio': [price],
        'Delta': [delta],
        'Score': [score]
    }
    df = pd.DataFrame(nuevo)
    df.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)

def analyze_aggression(es_apertura=False):
    try:
        df = pd.read_csv('cinta_ggal.csv')
        delta = int(df[df['Side'] == 'Buy']['Volume'].sum() - df[df['Side'] == 'Sell']['Volume'].sum())
        price = df['Price'].iloc[-1]

        # --- SOLO SI HAY BALLENA (>80k) ---
        if abs(delta) > 80000:
            score, detalle_texto = get_signal_score()
            log_event(delta, price, score) # Guardamos en el log profesional

            # Clasificación de Calidad
            estrellas = "⭐" * score
            calidad = "BAJA" if score < 3 else "ALTA" if score < 5 else "PREMIUM (A+)"

            msg = f"🚨 *BALLENA DETECTADA + 💎 CALIDAD {score}/5*\n\n"
            msg += f"📊 *Delta:* {delta} acciones\n"
            msg += f"💰 *Precio:* ${price}\n"
            msg += f"🏆 *Calidad:* {calidad} {estrellas}\n\n"
            msg += f"*Checklist:*\n{detalle_texto}\n\n"
            msg += "📝 _Evento registrado en tu base de datos para análisis._"

            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
            print(f"✅ Alerta Unificada enviada (Score: {score})")

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    analyze_aggression("--apertura" in sys.argv)