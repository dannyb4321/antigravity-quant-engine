import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def create_whale_chart(csv_file='cinta_ggal.csv'):
    # 1. Cargamos los datos
    df = pd.read_csv(csv_file)
    
    # Convertimos la columna Time a formato de tiempo real para graficar
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

    # 2. Separamos los datos para graficar con estilos diferentes
    whales = df[df['Is_Whale'] == True]
    retail = df[df['Is_Whale'] == False]

    # 3. Configuramos el gráfico
    plt.figure(figsize=(12, 6))
    plt.style.use('seaborn-v0_8-darkgrid') # Le da un toque profesional

    # Graficamos a los minoristas (puntos grises, pequeños y transparentes)
    plt.scatter(retail['Time'], retail['Price'], 
                s=retail['Volume']/10, # Usamos TAMAÑO para volumen (dividido para que no tape)
                color='gray', alpha=0.4, label='Minoristas (Ruido)')

    # --- ACÁ APLICAMOS TU IDEA ---
    # Graficamos a las ballenas (puntos rojos, GRANDES y visibles)
    plt.scatter(whales['Time'], whales['Price'], 
                s=whales['Volume']/5, # Mucho más grandes
                color='red', alpha=0.9, edgecolors='black', label='Ballena (Bloque ~70k USD)')

    # 4. Formateamos los ejes (para que se vean las horas bien)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    
    plt.title('Detección Visual de Ballenas en GGAL (Simulación)')
    plt.xlabel('Tiempo (Hora de la Rueda)')
    plt.ylabel('Precio (USD)')
    plt.legend()
    plt.tight_layout()

    # Guardamos el gráfico
    output_image = 'whale_visualization.png'
    plt.savefig(output_image)
    print(f"✅ Visualización guardada con éxito como '{output_image}'")

if __name__ == "__main__":
    create_whale_chart()