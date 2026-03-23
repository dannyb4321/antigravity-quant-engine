import pandas as pd

def analyze_aggression(csv_file='cinta_ggal.csv'):
    try:
        # Cargamos el archivo que generamos o descargamos
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró {csv_file}")
        return

    # 1. Calculamos volúmenes totales de forma directa y segura
    buy_vol = df[df['Side'] == 'Buy']['Volume'].sum()
    sell_vol = df[df['Side'] == 'Sell']['Volume'].sum()
    
    # 2. Buscamos el precio con más volumen (Punto de mayor absorción)
    vap = df.groupby('Price')['Volume'].sum().reset_index()
    iceberg_level = vap.loc[vap['Volume'].idxmax()]

    print("📊 REPORTE DE INTELIGENCIA - GGAL")
    print("-" * 45)
    print(f"🥊 Volumen de Compra Agresiva: {int(buy_vol)} acciones")
    print(f"🥊 Volumen de Venta Agresiva: {int(sell_vol)} acciones")

    # 3. Cálculo del Delta (La diferencia de poder)
    delta = buy_vol - sell_vol
    print(f"\n📈 DELTA TOTAL: {int(delta)} acciones")
    
    if delta > 0:
        print("🔥 Sentimiento: COMPRADORES AL MANDO.")
    elif delta < 0:
        print("❄️ Sentimiento: VENDEDORES AL MANDO.")
    else:
        print("⚖️ Sentimiento: MERCADO EN EQUILIBRIO.")

    print(f"🛡️ SOPORTE CLAVE (MAYOR ABSORCIÓN): ${iceberg_level['Price']}")
    print("-" * 45)

if __name__ == "__main__":
    analyze_aggression()