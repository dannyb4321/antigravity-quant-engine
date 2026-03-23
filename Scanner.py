import pandas as pd
import requests

# 🚨 CONFIGURACIÓN DE TELEGRAM (LISTO PARA USAR)
TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.get(url, params=params)
        print("📲 Alerta enviada a mensajeroballenas_bot.")
    except Exception as e:
        print(f"⚠️ Error de conexión con Telegram: {e}")

def analyze_aggression(csv_file='cinta_ggal.csv'):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró {csv_file}")
        return

    # Cálculos Quant
    buy_vol = df[df['Side'] == 'Buy']['Volume'].sum()
    sell_vol = df[df['Side'] == 'Sell']['Volume'].sum()
    vap = df.groupby('Price')['Volume'].sum().reset_index()
    iceberg_level = vap.loc[vap['Volume'].idxmax()]
    delta = buy_vol - sell_vol

    # Reporte en Terminal
    current_delta = int(delta)
    print(f"📊 REPORTE GGAL | DELTA: {current_delta} | SOPORTE: ${iceberg_level['Price']}")

    # 🤖 ALERTA: Si el Delta supera las 120,000 acciones. 
    # (Podés bajar este número si querés recibir alertas más seguido)
    if abs(current_delta) > 120000:
        msg = f"🚨 BALLENA DETECTADA (GGAL)\n\n📈 Delta: {current_delta} acciones\n🛡️ Soporte: ${iceberg_level['Price']}\n🚀 El motor Anti-Gravity detectó presión institucional."
        send_telegram_alert(msg)

if __name__ == "__main__":
    analyze_aggression()