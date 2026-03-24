import time
import subprocess
from datetime import datetime

def es_horario_mercado():
    ahora = datetime.now()
    if ahora.weekday() > 4: return False
    # Rango de 10:30 a 18:00
    if (ahora.hour == 10 and ahora.minute >= 30) or (ahora.hour > 10 and ahora.hour < 18):
        return True
    return False

if __name__ == "__main__":
    print("🤖 MODO AUTOPILOTO INTELIGENTE ACTIVADO")
    ya_mande_apertura = False
    ultimo_dia = None

    while True:
        hoy = datetime.now().date()
        if hoy != ultimo_dia: # Resetear al empezar un nuevo día
            ya_mande_apertura = False
            ultimo_dia = hoy

        if es_horario_mercado():
            print(f"🚀 {datetime.now().strftime('%H:%M:%S')} - Ciclo activo")
            subprocess.run(["python", "get_real_data.py"])
            subprocess.run(["python", "visualize_tape.py"])
            
            # Si es el primer ciclo, mandamos reporte de apertura
            if not ya_mande_apertura:
                print("☀️ Enviando reporte de apertura...")
                subprocess.run(["python", "Scanner.py", "--apertura"]) # Nota: el script lo detectará
                ya_mande_apertura = True
            else:
                subprocess.run(["python", "Scanner.py"])
        else:
            print(f"💤 {datetime.now().strftime('%H:%M:%S')} - Fuera de horario.")
        
        time.sleep(300)