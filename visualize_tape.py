import pandas as pd
import matplotlib.pyplot as plt

def plot_real_market():
    try:
        df = pd.read_csv('cinta_ggal.csv')
    except FileNotFoundError:
        print("❌ No hay datos. Corré primero get_real_data.py")
        return

    plt.figure(figsize=(12, 6))
    
    # 1. Graficamos el precio (línea azul)
    plt.plot(df.index, df['Price'], color='blue', alpha=0.3, label='Precio GGAL (Minutos)')
    
    # 2. Resaltamos las Compras (Verde) y Ventas (Rojo)
    buys = df[df['Side'] == 'Buy']
    sells = df[df['Side'] == 'Sell']
    
    plt.scatter(buys.index, buys['Price'], color='green', s=buys['Volume']/500, label='Compras Agresivas', alpha=0.6)
    plt.scatter(sells.index, sells['Price'], color='red', s=sells['Volume']/500, label='Ventas Agresivas', alpha=0.6)

    # 3. Marcamos la "MURALLA" de la ballena ($44.65)
    plt.axhline(y=44.65, color='purple', linestyle='--', linewidth=2, label='SOPORTE BALLENA ($44.65)')

    plt.title("📊 GGAL - Mapa de Liquidez en Wall Street (Real Time)")
    plt.xlabel("Minutos de la rueda")
    plt.ylabel("Precio USD")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    plt.savefig('heatmap_ggal.png') # Crea una foto que podés tener abierta
    print("📸 Imagen 'heatmap_ggal.png' actualizada.")
    plt.close() # Cierra el gráfico internamente para no consumir memoria

if __name__ == "__main__":
    plot_real_market()