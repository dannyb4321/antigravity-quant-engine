import pandas as pd
import requests
import sys
import os
from datetime import datetime
from SignalValidator import get_signal_score

TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 
LOG_FILE = "trading_log_ggal.csv"
PHOTO_PATH = "heatmap_ggal.png" # La ruta de la foto

def send_full_alert(message, photo_path):
    """Envía la foto con el mensaje como descripción."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': message, 'parse_mode': 'Markdown'}, files={'photo': photo}, timeout=15)
            print("📲 Alerta con FOTO enviada.")
        else:
            # Si no hay foto, manda solo texto
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})
            print("📲 Foto no encontrada, enviada solo como texto.")
    except Exception as e:
        print(f"⚠️ Error enviando alerta: {e}")

def log_event(delta, price, score):
    file_exists = os.path.isfile(LOG_FILE)
    nuevo = pd.DataFrame({
        'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M')],
        'Precio': [price],
        'Delta': [delta],
        'Score': [score]
    })
    nuevo.to_csv(LOG_FILE, mode='a', header=not file_exists, index=False)

def analyze_aggression(es_apertura=False):
    try:
        df = pd.read_csv('cinta_ggal.csv')
        delta = int(df[df['Side'] == 'Buy']['Volume'].sum() - df[df['Side'] == 'Sell']['Volume'].sum())
        price = df['Price'].iloc[-1]

        if abs(delta) > 80000:
            score, detalle_texto = get_signal_score()
            log_event(delta, price, score)

            estrellas = "⭐" * score
            calidad = "BAJA" if score < 3 else "ALTA" if score < 5 else "PREMIUM (A+)"
            side = "🐂 COMPRA" if delta > 0 else "🐻 VENTA"

            msg = f"🚨 *BALLENA DETECTADA ({side})*\n"
            msg += f"💎 *CALIDAD DE ENTRADA: {score}/5*\n\n"
            msg += f"📊 *Delta:* {delta} acciones\n"
            msg += f"💰 *Precio:* ${price}\n"
            msg += f"🏆 *Nivel:* {calidad} {estrellas}\n\n"
            msg += f"*Checklist:*\n{detalle_texto}"

            # 📸 ¡ACÁ MANDAMOS TODO JUNTO!
            send_full_alert(msg, PHOTO_PATH)

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    analyze_aggression("--apertura" in sys.argv)