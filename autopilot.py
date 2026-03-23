import time
import subprocess
import os

def run_engine():
    # Obtenemos la hora actual para el reporte
    current_time = time.strftime('%H:%M:%S')
    print(f"\n🚀 {current_time} - INICIANDO CICLO DE ACTUALIZACIÓN QUANTS...")
    print("-" * 50)

    try:
        # 1. Bajamos la data de Wall Street
        print("📥 Paso 1: Descargando datos de GGAL...")
        subprocess.run(["python", "get_real_data.py"], check=True)

        # 2. Corremos el Scanner para detectar ballenas
        print("🔍 Paso 2: Escaneando flujos institucionales...")
        subprocess.run(["python", "Scanner.py"], check=True)

        # 3. Actualizamos el gráfico (el Mapa de Calor)
        print("📊 Paso 3: Generando nuevo mapa de calor...")
        subprocess.run(["python", "visualize_tape.py"], check=True)

        print("-" * 50)
        print(f"✅ CICLO COMPLETADO CON ÉXITO.")
        print("⏳ Próxima actualización en 5 minutos. No cierres esta ventana.")

    except Exception as e:
        print(f"⚠️ Hubo un error en el ciclo: {e}")

if __name__ == "__main__":
    print("🤖 MODO AUTOPILOTO ACTIVADO - GGAL ANTI-GRAVITY ENGINE")
    while True:
        run_engine()
        # Espera 300 segundos (5 minutos)
        time.sleep(300)