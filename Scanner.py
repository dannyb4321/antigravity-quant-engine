import pandas as pd

def analyze_aggression(csv_file='cinta_ggal.csv'):
    # 1. Cargamos los datos de la cinta
    df = pd.read_csv(csv_file)
    
    # 2. Calculamos el volumen por bando (Agresividad)
    # Agrupamos por 'Side' (Buy/Sell) para ver quién golpeó más fuerte
    aggression = df.groupby('Side').agg(
        Total_Vol=('Volume', 'sum'),
        Avg_Price=('Price', 'mean'),
        Trades=('Volume', 'count')
    ).reset_index()

    # 3. Buscamos el nivel de mayor absorción (donde hubo más volumen total)
    vap = df.groupby('Price').agg(Total_Vol=('Volume', 'sum')).reset_index()
    iceberg_level = vap.loc[vap['Total_Volume'].idxmax()]

    print("📊 REPORTE DE INTELIGENCIA DE MERCADO - GGAL")
    print("-" * 45)
    
    for _, row in aggression.iterrows():
        print(f"🥊 Lado {row['Side']}: {int(row['Total_Vol'])} acciones en {row['Trades']} ataques.")

    # 4. Cálculo del Delta (Diferencia entre compras y ventas agresivas)
    buy_vol = aggression.loc[aggression['Side'] == 'Buy', 'Total_Vol'].values
    sell_vol = aggression.loc[aggression['Side'] == 'Sell', 'Total_Vol'].values
    
    delta = buy_vol - sell_vol
    print(f"\n📈 DELTA TOTAL: {int(delta)} acciones")
    
    if delta > 0:
        print("🔥 Sentimiento: COMPRADORES AGRESIVOS dominando el campo.")
    else:
        print("❄️ Sentimiento: VENDEDORES AGRESIVOS presionando el precio.")

    print(f"\n🛡️ NIVEL DE MAYOR ABSORCIÓN: ${iceberg_level['Price']}")
    print("-" * 45)

if __name__ == "__main__":
    analyze_aggression()