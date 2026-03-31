import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def simulate_whale_tape(symbol="GGAL", duration_mins=30):
    data = []
    current_time = datetime.now()
    base_price = 43.50 # Precio inicial simulado
    
    # Simulamos aproximadamente un trade cada 1-4 segundos
    for i in range(duration_mins * 20): 
        current_time += timedelta(seconds=np.random.randint(1, 5))
        
        # --- Operación Normal (Minoristas) ---
        price = round(base_price + np.random.normal(0, 0.02), 2)
        volume = np.random.randint(100, 2000)
        side = np.random.choice(['Buy', 'Sell'])
        is_whale = False
        
        # --- Aparición de la Ballena (Algoritmo Institucional) ---
        # Cada 25 operaciones, entra un bloque de ~70k USD
        if i > 0 and i % 25 == 0:
            volume = 1600 # 1600 acciones * 43.75 USD ≈ 70.000 USD
            side = 'Buy'
            price = round(base_price + 0.05, 2) # La ballena "paga" más para barrer
            is_whale = True

        data.append([current_time.strftime('%H:%M:%S'), price, volume, side, is_whale])

    # Creamos el DataFrame y lo guardamos
    df = pd.DataFrame(data, columns=['Time', 'Price', 'Volume', 'Side', 'Is_Whale'])
    df.to_csv('cinta_ggal.csv', index=False)
    print(f"✅ ¡Cinta de {symbol} generada con éxito en 'cinta_ggal.csv'!")

if __name__ == "__main__":
    simulate_whale_tape()