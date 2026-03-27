import yfinance as yf
import pandas as pd

def download_real_galicia():
    print("📡 Conectando con Wall Street para bajar GGAL...")
    
    # Bajamos la data
    data = yf.download("GGAL", period="1d", interval="1m")
    
    if data.empty:
        print("❌ No se pudieron bajar datos. El mercado puede estar cerrado.")
        return

    # --- ARREGLO PARA EL ERROR DE DIMENSIONES ---
    # Usamos .values.flatten() para convertir las tablas en listas simples de números
    prices = data['Close'].values.flatten()
    opens = data['Open'].values.flatten()
    volumes = data['Volume'].values.flatten()

    df = pd.DataFrame()
    df['Price'] = prices
    df['Volume'] = volumes
    
    # Ahora el 'zip' va a funcionar perfecto porque son listas planas
    df['Side'] = ['Buy' if c >= o else 'Sell' for c, o in zip(prices, opens)]
    
    # Guardamos
    df.to_csv('cinta_ggal.csv', index=False)
    
    print("-" * 45)
    print(f"✅ ¡DATOS REALES SIN ERRORES!")
    print(f"📂 Se procesaron {len(df)} minutos de rueda.")
    print("-" * 45)

if __name__ == "__main__":
    download_real_galicia() 