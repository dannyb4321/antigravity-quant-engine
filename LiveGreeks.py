from IOL_Connector import IOL_Client
from SignalValidator import calculate_greeks, get_market_data
import time

# --- CONFIGURACIÓN ---
USER_IOL = "paradisecity"  # Tu usuario de IOL
PASS_IOL = "Inviertaparaganar.5" # Tu contraseña de IOL


def run_live_monitor():
    print("🚀 Iniciando Motor IOL...")
    try:
        iol = IOL_Client(USER_IOL, PASS_IOL)
    except:
        print("❌ Error de credenciales. Revisá usuario/pass.")
        return

    while True:
        try:
            _, p_local, tasa = get_market_data()
            df = iol.get_options_data("GGAL")
            
            # PROTECCIÓN: Si el panel viene vacío, no explotar
            if df.empty or 'simbolo' not in df.columns:
                print("⏳ Esperando datos frescos de IOL...")
                time.sleep(10)
                continue

            print(f"✅ Datos recibidos. GGAL: ${p_local}")
            # Filtrar calls
            df_calls = df[df['simbolo'].str.contains("C")].copy()
            
            # Aquí podrías agregar el guardado en SQL si quisieras
            time.sleep(30) # Actualiza cada 30 segs

        except Exception as e:
            print(f"⚠️ Reintentando conexión... {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_live_monitor()