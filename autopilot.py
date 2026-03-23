import time
import subprocess
import os

# Danny: Definimos los nombres de los archivos para evitar errores
DATA_SCRIPT = "get_real_data.py"
SCANNER_SCRIPT = "Scanner.py"
GRAPH_SCRIPT = "visualize_tape.py"

def run_engine():
    current_time = time.strftime('%H:%M:%S')
    print(f"\n🚀 {current_time} - INICIANDO CICLO DE ACTUALIZACIÓN QUANTS...")
    print("-" * 50)

    try:
        # 1. Bajamos la data de Wall Street
        print(f"📥 Paso 1: Ejecutando {DATA_SCRIPT}...")
        subprocess.run(["python", DATA_SCRIPT], check=True)

        # 2. Actualizamos el gráfico (Heatmap) -> ¡IMPORTANTE: AHORA VA SEGUNDO!
        # Así la foto 'heatmap_ggal.png' está lista antes de escanear.
        print(f"📊 Paso 2: Ejecutando {GRAPH_SCRIPT}...")
        subprocess.run(["python", GRAPH_SCRIPT], check=True)

        # 3. Corremos el Scanner para detectar ballenas y enviar alertas con foto
        print(f"🔍 Paso 3: Ejecutando {SCANNER_SCRIPT}...")
        subprocess.run(["python", SCANNER_SCRIPT], check=True)

        print("-" * 50)
        print(f"✅ CICLO COMPLETADO CON ÉXITO.")
        print("⏳ Próxima actualización en 5 minutos. No cierres esta ventana.")

    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error al ejecutar un script: {e}")
    except Exception as e:
        print(f"⚠️ Hubo un error inesperado: {e}")

if __name__ == "__main__":
    print("🤖 MODO AUTOPILOTO ACTIVADO - GGAL ANTI-GRAVITY ENGINE")
    while True:
        run_engine()
        time.sleep(300) # Espera 5 minutos