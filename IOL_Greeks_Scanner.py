import pandas as pd
import numpy as np
from scipy.stats import norm
from SignalValidator import get_market_data, calculate_greeks

def scan_iol_chain():
    # 1. Obtenemos el precio actual (Spot)
    ccl, p_local, tasa = get_market_data()
    if p_local == 0: return print("❌ Error de conexión con los precios.")

    # 2. Definimos las bases a monitorear (Automatización)
    # Buscamos strikes cada 300 pesos, 3 arriba y 3 abajo del precio actual
    strike_base = round(p_local / 100) * 100
    bases_interes = [strike_base + (i * 300) for i in range(-3, 4)]
    
    # Parámetros para Black-Scholes
    t_vto = 18 / 365  # Días al ejercicio (Aprox)
    iv_avg = 0.82     # Volatilidad implícita promedio de la rueda
    
    resultados = []

    print(f"\n🔍 ESCÁNER DE GRIEGAS GGAL - SPOT: ${p_local}")
    print("-" * 50)
    
    for K in bases_interes:
        delta, theta = calculate_greeks(p_local, K, t_vto, tasa/100, iv_avg)
        
        # Clasificación de Arquitecto
        estado = "ITM 💰" if p_local > K else "OTM 🎲"
        if abs(p_local - K) < 150: estado = "ATM 🎯"
        
        resultados.append({
            "Base": f"GFCC{K}A",
            "Estado": estado,
            "Delta": delta,
            "Theta_Diario": theta
        })
        
        print(f"{f'GFCC{K}A':<10} | {estado:<6} | Δ: {delta:<6} | θ: {theta}")

    # 3. Guardar en SQL para tu historial de Arquitecto
    # (Aquí llamaríamos a tu función log_event_sql que creamos antes)

if __name__ == "__main__":
    scan_iol_chain()