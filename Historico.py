import pandas as pd
import os

LOG_FILE = "trading_log_ggal.csv"

def agregar_historial():
    # Datos de tus jornadas pasadas (Podés editar los valores si recordás el precio exacto)
    data = {
        'Fecha': ['2026-03-20 15:00', '2026-03-25 12:30'],
        'Precio': [51.20, 52.80], # Precios aproximados del ADR
        'Delta':,
        'Score':,
        'Operacion': ['Call C6900 - Seguimiento', 'Call C6900 - Analisis'],
        'Resultado': ['Hold', 'Hold']
    }
    
    df_nuevo = pd.DataFrame(data)
    
    if os.path.exists(LOG_FILE):
        df_actual = pd.read_csv(LOG_FILE)
        df_final = pd.concat([df_actual, df_nuevo]).drop_duplicates()
    else:
        df_final = df_nuevo
        
    df_final.to_csv(LOG_FILE, index=False)
    print("✅ Bitácora de ayer y el viernes pasado sincronizada.")

if __name__ == "__main__":
    agregar_historial()