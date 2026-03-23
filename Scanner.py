import pandas as pd
import requests
import os
import time

# 🚨 CONFIGURACIÓN DE TELEGRAM (LISTO PARA USAR)
# Danny: Ya están tus datos verificados. No tocar.
TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 
PHOTO_PATH = "heatmap_ggal.png" # La foto que genera visualize_tape.py

def send_telegram_alert_with_photo(message, photo_path):
    """Envía un mensaje de texto y una foto adjunta al bot de Telegram."""
    
    # Base URL para la API de Telegram
    base_url = f"https://api.telegram.org/bot{TOKEN}"
    
    # 1. Intentamos enviar la foto con el mensaje como 'caption' (epígrafe)
    if os.path.exists(photo_path):
        url_photo = f"{base_url}/sendPhoto"
        try:
            # Reintentos para dar tiempo a que se cierre el archivo de imagen
            for i in range(3):
                try:
                    with open(photo_path, 'rb') as photo_file:
                        files = {'photo': photo_file}
                        data = {'chat_id': CHAT_ID, 'caption': message, 'parse_mode': 'Markdown'}
                        response = requests.post(url_photo, data=data, files=files, timeout=10)
                    
                    if response.status_code == 200:
                        print("📲 Alerta con FOTO enviada exitosamente.")
                        return # Éxito, salimos de la función
                    else:
                        print(f"⚠️ Error al enviar foto (Código {response.status_code}). Intentando solo texto...")
                        break # Falla la foto, vamos a texto
                except IOError:
                    # El archivo puede estar bloqueado por visualize_tape.py, esperamos 1 seg.
                    time.sleep(1)
        except Exception as e:
            print(f"⚠️ Error inesperado al enviar foto: {e}")
    
    # 2. Si la foto no existe o falló el envío, mandamos solo el texto
    url_text = f"{base_url}/sendMessage"
    try:
        data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
        requests.post(url_text, data=data, timeout=10)
        print("📲 Alerta de SOLO TEXTO enviada (la foto falló o no existía).")
    except Exception as e:
        print(f"⚠️ Error fatal de conexión con Telegram: {e}")

def analyze_aggression(csv_file='cinta_ggal.csv'):
    try:
        # Cargamos los datos más recientes descargados por get_real_data.py
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró {csv_file}")
        return

    # --- 📊 CÁLCULOS QUANT AVANZADOS ---
    
    # 1. Imbalance (Delta)
    buy_vol = df[df['Side'] == 'Buy']['Volume'].sum()
    sell_vol = df[df['Side'] == 'Sell']['Volume'].sum()
    total_volume_today = df['Volume'].sum()
    
    # 2. Nivel de Absorción (Soporte/Resistencia Ballena)
    vap = df.groupby('Price')['Volume'].sum().reset_index()
    iceberg_level = vap.loc[vap['Volume'].idxmax()]
    delta = buy_vol - sell_vol
    current_delta = int(delta)

    # --- 🧠 CÁLCULO DEL RVOL (VOLUMEN RELATIVO) ---
    # Danny: Definimos técnicamente el "Ingreso Institucional" para GGAL ADR.
    # Usamos un benchmark histórico de un día promedio para GGAL: ~750,000 acciones.
    # Esto nos dice cuántas veces estamos superando la media histórica *en lo que va del día*.
    HISTORICAL_DAILY_AVG = 750000 
    
    if total_volume_today > 0:
        rvol = total_volume_today / HISTORICAL_DAILY_AVG
    else:
        rvol = 0

    # Reporte detallado en Terminal de VS Code
    print("-" * 30)
    print(f"📊 REPORTE GGAL QUANT")
    print(f"🔹 Delta Total: {current_delta} acciones")
    print(f"🔹 Soporte Ballena: ${iceberg_level['Price']}")
    print(f"🔹 Volumen Total Hoy: {int(total_volume_today)}")
    print(f"🔥 RVOL (Vol. Relativo): {rvol:.2f}x de la media diaria")
    print("-" * 30)

    # --- 🤖 LÓGICA DE ALERTA INTELIGENTE ---
    alert_triggered = False
    alert_msg = ""

    # Condición 1: Gran Imbalance (Ballena comprando/vendiendo fuerte)
    if abs(current_delta) > 120000:
        alert_triggered = True
        alert_msg = f"🚨 *¡BALLENA DETECTADA (GGAL)!*\n\n📈 *Delta Brutal:* {current_delta} acciones.\n🛡️ *Soporte Institucional:* ${iceberg_level['Price']}\n"

    # Condición 2: Alto RVOL (Anomalía de Volumen, Smart Money entrando)
    # Danny: Si el volumen total de hoy ya duplicó la media histórica (RVOL > 2.0)
    if rvol > 2.0:
        if not alert_triggered:
            alert_msg = f"🔥 *¡ANOMALÍA DE VOLUMEN (GGAL)!*\n\n"
        alert_triggered = True
        alert_msg += f"📊 *RVOL:* {rvol:.2f}x (Superando {HISTORICAL_DAILY_AVG} acciones de media).\n💰 *Volumen Total:* {int(total_volume_today)} acciones."

    # Si se activó alguna alerta, enviamos el mensaje completo con la foto
    if alert_triggered:
        # Añadimos un pie de mensaje estándar
        final_msg = alert_msg + "\n\n🚀 _El motor Anti-Gravity detectó actividad Smart Money en Wall Street._"
        # Llamamos a la nueva función que envía foto
        send_telegram_alert_with_photo(final_msg, PHOTO_PATH)

if __name__ == "__main__":
    analyze_aggression()