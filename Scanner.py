import pandas as pd
import requests
import sys
import os
from datetime import datetime
from SignalValidator import get_signal_score

TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 
PHOTO_PATH = "heatmap_ggal.png" # <--- EL ARCHIVO QUE EXISTE EN TU CARPETA

def analyze_aggression(es_apertura=False):
    print("🐋 Revisando volumen institucional...")
    try:
        # Cargamos la cinta de GGAL
        df = pd.read_csv('cinta_ggal.csv')
        delta = int(df[df['Side'] == 'Buy']['Volume'].sum() - df[df['Side'] == 'Sell']['Volume'].sum())
        price = df['Price'].iloc[-1]

        # --- UMBRAL RECALIBRADO PARA PRUEBA DE CAMPO ---
        # Danny: Usá este código. Yo ya te puse '1000' acá para que te llegue la foto.
        # Una vez que te llegue el mensaje, volvelo a poner en 80000.
        if abs(delta) > 20000: 
            score, detalle, direccion = get_signal_score()
            
            # Clasificación visual
            emoji_side = "🐂 COMPRA" if delta > 0 else "🐻 VENTA"
            estrellas = "⭐" * score
            quality_txt = "BAJA" if score < 3 else "ALTA" if score < 5 else "PREMIUM (A+)"

            msg = f"🚨 *BALLENA DETECTADA ({emoji_side})*\n"
            msg += f"💎 *CALIDAD DE ENTRADA: {score}/5*\n\n"
            msg += f"📊 *Delta:* {delta} acciones\n"
            msg += f"💰 *Precio:* ${price}\n"
            msg += f"🏆 *Nivel:* {quality_txt} {estrellas}"

            # 📸 ¡INTENTO DE ENVIAR EL COMBO CON FOTO!
            if os.path.exists(PHOTO_PATH):
                with open(PHOTO_PATH, 'rb') as photo:
                    # Usamos sendPhoto y el mensaje va en 'caption'
                    payload = {'chat_id': CHAT_ID, 'caption': msg, 'parse_mode': 'Markdown'}
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data=payload, files={'photo': photo}, timeout=15)
                    print("✅ Alerta con FOTO enviada exitosamente.")
            else:
                # Si no hay foto por algún error, manda texto para no perder la señal
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                print("⚠️ Foto no encontrada. Se envió solo texto.")

    except Exception as e:
        print(f"⚠️ Error en el Scanner: {e}")

if __name__ == "__main__":
    analyze_aggression("--apertura" in sys.argv)