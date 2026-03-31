import time
import os
import sqlite3
from dotenv import load_dotenv
from IOL_Connector import IOL_Client
from SignalValidator import calculate_greeks, get_market_data

# --- 1. CARGAR CONFIGURACIÓN SEGURA ---
load_dotenv()
USER_IOL = os.getenv("IOL_USER")
PASS_IOL = os.getenv("IOL_PASS")

# --- 2. CONFIGURACIÓN DE BASE DE DATOS ---
DB_NAME = 'antigravity_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS whale_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            simbolo TEXT,
            precio REAL,
            cantidad INTEGER,
            monto_efectivo REAL,
            delta REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_alert(simbolo, precio, cantidad, monto, delta):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO whale_alerts (simbolo, precio, cantidad, monto_efectivo, delta)
            VALUES (?, ?, ?, ?, ?)
        ''', (simbolo, precio, cantidad, monto, delta))
        conn.commit()
        conn.close()
        print(f"✅ Alerta guardada: {simbolo} | Monto: ${monto:,.2f}")
    except Exception as e:
        print(f"❌ Error al guardar en SQL: {e}")

# --- 3. BUCLE PRINCIPAL DEL BOT ---
def run_whale_monitor():
    print("🚀 Orion Quant - Iniciando Escáner de Ballenas...")
    init_db()
    
    iol = IOL_Client(USER_IOL, PASS_IOL)
    
    while True:
        try:
            # Obtenemos precio spot para el cálculo de Delta
            _, spot, tasa = get_market_data()
            df = iol.get_options_data("GGAL")
            
            if not df.empty:
                # Filtramos operaciones "grandes" (Ballenas)
                # Ejemplo: Operaciones de más de 500.000 ARS en una sola base
                ballenas = df[df['montoOperado'] > 500000].copy()
                
                for _, row in ballenas.iterrows():
                    # Extraer strike para calcular Delta
                    import re
                    strike_match = re.search(r'(\d+)', row['simbolo'])
                    strike = float(strike_match.group(1)) if strike_match else 0
                    
                    # Calculamos el Delta actual de esa ballena
                    delta, _, _, _ = calculate_greeks(spot, strike, 18/365, tasa/100, 0.85)
                    
                    # Guardamos si es una alerta relevante
                    save_alert(
                        row['simbolo'], 
                        row['ultimoPrecio'], 
                        row['cantidadOperada'], 
                        row['montoOperado'], 
                        delta
                    )
            
            print(f"💤 Escaneo finalizado ({time.strftime('%H:%M:%S')}). Esperando 60s...")
            time.sleep(60) # Esperamos 1 minuto para no saturar la API

        except Exception as e:
            print(f"⚠️ Error en el loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_whale_monitor()