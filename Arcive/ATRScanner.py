import pandas as pd
import requests
import yfinance as yf

# 🚨 CONFIGURACIÓN DE TELEGRAM
TOKEN = "8765737672:AAHXXYm3JkucM-3TtafoZpcuEiOtszHQckY" 
CHAT_ID = "7566636061" 

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

def calculate_atr(df, period=14):
    # Cálculo del True Range (TR)
    df['high_low'] = df['High'] - df['Low']
    df['high_cp'] = abs(df['High'] - df['Close'].shift())
    df['low_cp'] = abs(df['Low'] - df['Close'].shift())
    df['TR'] = df[['high_low', 'high_cp', 'low_cp']].max(axis=1)
    # ATR es la media móvil del TR
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df

def run_atr_scan():
    print(f"\n🌡️ ANALIZANDO VOLATILIDAD (ATR)...")
    try:
        ticker = yf.Ticker("GGAL")
        # Usamos 15m para detectar volatilidad intradía rápida
        df = ticker.history(period="5d", interval="15m")
        if df.empty: return

        df = calculate_atr(df)
        
        current_atr = df['ATR'].iloc[-1]
        prev_atr = df['ATR'].iloc[-2]
        price = df['Close'].iloc[-1]

        # --- LÓGICA DE ALERTA: EXPLOSIÓN DE VOLATILIDAD ---
        # Si la volatilidad actual es un 20% mayor a la anterior
        spike_volatilidad = current_atr > (prev_atr * 1.20)

        print(f"📊 ATR Actual: {current_atr:.4f} | ATR Anterior: {prev_atr:.4f}")

        if spike_volatilidad:
            msg = "⚡ *ALERTA: EXPLOSIÓN DE VOLATILIDAD (ATR)*\n\n"
            msg += f"📈 *ATR subió a:* {current_atr:.4f}\n"
            msg += f"🛡️ *Stop Loss sugerido (2x ATR):* ${(price - (2 * current_atr)):.2f}\n"
            msg += f"💰 *Precio actual:* ${price:.2f}\n\n"
            msg += "_Ojo: Un pico de ATR suele ser el inicio de un movimiento institucional._"
            send_alert(msg)
            print("📲 Alerta de ATR enviada.")

    except Exception as e:
        print(f"⚠️ Error en ATRScanner: {e}")

if __name__ == "__main__":
    run_atr_scan()