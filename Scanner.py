import pandas as pd

def analyze_aggression(csv_file='cinta_ggal.csv'):
    df = pd.read_csv(csv_file)
    
    # 1. Agresividad por bando
    aggression = df.groupby('Side').agg(
        Total_Vol=('Volume', 'sum'),
        Trades=('Volume', 'count')
    ).reset_index()

    # 2. Buscamos el nivel de mayor absorción (Nombres corregidos aquí)
    vap = df.groupby('Price').agg(Total_Vol=('Volume', 'sum')).reset_index()
    iceberg_level = vap.loc[vap['Total_Vol'].idxmax()]

    print("📊 REPORTE DE INTELIGENCIA - GGAL")
    print("-" * 45)
    
    for _, row in aggression.iterrows():
        print(f"🥊 Lado {row['Side']}: {int(row['Total_Vol'])} acciones.")

    # 3. Cálculo del Delta
    buy_vol = aggression.loc[aggression['Side'] == 'Buy', 'Total_Vol'].values
    sell_vol = aggression.loc[aggression['Side'] == 'Sell', 'Total_Vol'].values
    delta = buy_vol - sell_vol
    
    print(f"\n📈 DELTA TOTAL: {int(delta)} acciones")
    print(f"🛡️ SOPORTE CLAVE (MAYOR VOLUMEN): ${iceberg_level['Price']}")
    print("-" * 45)

if __name__ == "__main__":
    analyze_aggression()