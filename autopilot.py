import time
import subprocess
from datetime import datetime

def es_horario_mercado():
    # Obtenemos la hora actual (Argentina)
    ahora = datetime.now()
    hora = ahora.hour
    minuto = ahora.minute
    dia_semana = ahora.weekday() # 0 es Lunes, 6 es Domingo

    # 1. ¿Es fin de semana? (Sábado=5 o Domingo=6)
    if dia_semana > 4:
        return False, "Es fin de semana. El mercado está cerrado."

    # 2. ¿Está dentro del rango operativo? (De 10:30 a 17:30 ART para cubrir el cierre)
    # Ajustamos a las 18:00 para que capture el post-market inicial si querés.
    if hora < 10 or hora >= 18:
        return False, "Mercado cerrado. El motor retomará mañana a las 10:00."

    return True, "Mercado abierto. Operando..."

def run_engine():
    mercado_activo, mensaje_estado = es_horario_mercado()
    
    if not mercado_activo:
        print(f"\n💤 {time.strftime('%H:%M:%S')} - {mensaje_estado}")
        return

    print(f"\n🚀 {time.strftime('%H:%M:%S')} - INICIANDO CICLO DE ACTUALIZACIÓN...")
    print("-" * 50)

    try:
        subprocess.run(["python", "get_real_data.py"], check=True)
        subprocess.run(["python", "visualize_tape.py"], check=True)
        subprocess.run(["python", "Scanner.py"], check=True)
        print("-" * 50)
        print(f"✅ CICLO COMPLETADO.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    print("🤖 MODO AUTOPILOTO CON HORARIO INTELIGENTE - GGAL")
    while True:
        run_engine()
        # Espera 5 minutos para el próximo check
        time.sleep(300)