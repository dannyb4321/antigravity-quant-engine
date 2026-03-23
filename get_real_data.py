import yfinance as yf
import pandas as pd

def download_real_galicia():
    print("📡 Conectando con Wall Street para bajar GGAL...")
    
    # 1. Bajamos los datos del ADR de Galicia (Cotiza en USD)
    # Pedimos el último día ('1d') con intervalos de 1 minuto ('1m')
    data = yf.download("GGAL", period="1d", interval="1m")
    
    if data.empty:
        print("❌ No se pudieron bajar datos. El mercado puede estar cerrado.")
        return

    # 2. Transformamos los datos al formato de nuestro Scanner
    df = pd.DataFrame()
    
    # Tomamos el precio de cierre de cada minuto
    df['Price'] = data['Close']
    
    # Tomamos el volumen operado en ese minuto
    df['Volume'] = data['Volume']
    
    # Lógica Quant: Si el precio subió en el minuto, asumimos agresividad de compra (Buy)
    # Si bajó, asumimos agresividad de venta (Sell)
    df['Side'] = ['Buy' if c >= o else 'Sell' for c, o in zip(data['Close'], data['Open'])]
    
    # 3. Guardamos el archivo CSV (sobrescribe el anterior)
    df.to_csv('cinta_ggal.csv', index=False)
    
    print("-" * 45)
    print("✅ ¡DATOS REALES DESCARGADOS!")
    print(f"📂 Archivo 'cinta_ggal.csv' actualizado con {len(df)} registros.")
    print("-" * 45)

if __name__ == "__main__":
    download_real_galicia()