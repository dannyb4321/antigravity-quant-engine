import pandas as pd

def run_whale_scanner(csv_file='cinta_ggal.csv', vol_threshold=1500, count_threshold=5):
    # 1. Cargamos la cinta
    df = pd.read_csv(csv_file)
    
    # 2. Calculamos el valor nominal de cada operación (Precio * Volumen)
    df['Amount_USD'] = df['Price'] * df['Volume']
    
    # 3. Filtramos los bloques grandes
    large_trades = df[df['Volume'] >= vol_threshold]
    
    # 4. Agrupamos por precio para encontrar la "pared"
    summary = large_trades.groupby('Price').agg(
        Repeticiones=('Volume', 'count'),
        Total_USD=('Amount_USD', 'sum')
    ).reset_index()

    # 5. Filtramos por tu regla de "X" veces (5 veces)
    whale_levels = summary[summary['Repeticiones'] >= count_threshold]

    print("🔍 ESCANEANDO NIVELES DE ALTA LIQUIDEZ INSTITUCIONAL...")
    
    if not whale_levels.empty:
        for _, row in whale_levels.iterrows():
            print(f"\n🚨 ¡BALLENA DETECTADA EN ${row['Price']}! 🚨")
            print(f"📊 Bloques detectados: {int(row['Repeticiones'])}")
            print(f"💰 CAPITAL EN JUEGO: USD ${row['Total_USD']:,.2f}")
            print(f"🛡️ Fortaleza: Este nivel es un SOPORTE sólido.")
    else:
        print("✅ No se detectan patrones de acumulación masiva aún.")

if __name__ == "__main__":
    run_whale_scanner()