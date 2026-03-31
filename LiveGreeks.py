from IOL_Connector import IOL_Client
from SignalValidator import calculate_greeks, get_market_data
import time

# --- CONFIGURACIÓN ---
USER_IOL = "paradisecity"
PASS_IOL = "Inviertaparaganar.5"

def run_live_monitor():
    print("🚀 Iniciando Monitor de Griegas Real-Time...")
    iol = IOL_Client(USER_IOL, PASS_IOL)
    
    while True:
        try:
            _, p_local, tasa = get_market_data() # Traemos el precio Spot
            df_opciones = iol.get_options_data("GGAL")
            
            # Filtramos bases CALL que vencen en Junio (o el mes actual)
            # Solo bases cerca del precio actual para no ensuciar la pantalla
            df_filtrado = df_opciones[
                (df_opciones['simbolo'].str.contains("C")) & 
                (df_opciones['ultimoPrecio'] > 0)
            ].copy()

            print(f"\n🔔 ACTUALIZACIÓN: {time.strftime('%H:%M:%S')} | GGAL: ${p_local}")
            print(f"{'Símbolo':<12} | {'Precio':<8} | {'Delta Δ':<8} | {'Theta θ':<8}")
            print("-" * 45)

            for _, row in df_filtrado.iterrows():
                # Extraemos el Strike del nombre (ej: GFCC69006J -> 6900)
                try:
                    strike = float(''.join(filter(str.isdigit, row['simbolo'])))
                    # Días al vencimiento (ajustar según calendario)
                    t_vto = 18 / 365 
                    iv = 0.85 # Aquí podrías usar tu iv_calc.py para la IV real
                    
                    delta, theta = calculate_greeks(p_local, strike, t_vto, tasa/100, iv)
                    
                    # Filtro de Arquitecto: Solo mostrar bases con Delta entre 0.1 y 0.9
                    if 0.1 < delta < 0.9:
                        print(f"{row['simbolo']:<12} | ${row['ultimoPrecio']:<7} | {delta:<8} | {theta:<8}")
                except:
                    continue
            
            time.sleep(60) # Actualiza cada minuto

        except Exception as e:
            print(f"⚠️ Error en el loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_live_monitor()