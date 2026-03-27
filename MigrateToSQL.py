import sqlite3
import pandas as pd
import os

DB_NAME = "antigravity_data.db"
CSV_FILE = "trading_log_ggal.csv"

def migrate():
    print("🏗️  Arquitecto de Datos: Iniciando migración a SQLite...")
    conn = sqlite3.connect(DB_NAME)
    
    # Definimos el Schema (La estructura de la tabla)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS whale_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            precio REAL,
            delta INTEGER,
            score INTEGER,
            direccion TEXT,
            ccl REAL
        )
    ''')

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        # Migramos los datos a SQL
        df.to_sql('whale_alerts', conn, if_exists='append', index=False)
        print(f"✅ ¡Éxito! Registros migrados a {DB_NAME}")
    else:
        print("⚠️ No hay CSV previo. Base de Datos iniciada desde cero.")
    
    conn.close()

if __name__ == "__main__":
    migrate()