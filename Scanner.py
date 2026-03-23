import pandas as pd

def detect_icebergs(csv_file='cinta_ggal.csv', vol_threshold=10000):
    df = pd.read_csv(csv_file)
    df['Amount_USD'] = df['Price'] * df['Volume']
    
    # Agrupamos por precio para ver el volumen TOTAL en cada nivel
    vap = df.groupby('Price').agg(
        Total_Volume=('Volume', 'sum'),
        Total_USD=('Amount_USD', 'sum'),
        Trades=('Volume', 'count')
    ).reset_index()

    # Definimos que un Iceberg es donde el Volumen Total es enorme (ej > 10.000 acciones)
    icebergs = vap[vap['Total_Volume'] >= vol_threshold]

    print("🧊 BUSCANDO ÓRDENES ICEBERG ESCONDIDAS...")
    
    if not icebergs.empty:
        for _, row in icebergs.iterrows():
            print(f"\n❄️ ¡ICEBERG DETECTADO EN ${row['Price']}!")
            print(f"📊 Volumen Absorbido: {int(row['Total_Volume'])} acciones")
            print(f"🔄 Cantidad de Trades: {row['Trades']} (Puntas de iceberg)")
            print(f"💰 Capital Total: USD ${row['Total_USD']:,.2f}")
    else:
        print("🌊 El mar está tranquilo. No hay hielos a la vista.")

if __name__ == "__main__":
    # Bajamos el umbral para que detecte lo que generamos en nuestra simulación
    detect_icebergs(vol_threshold=5000)