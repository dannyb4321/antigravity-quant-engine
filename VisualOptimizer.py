import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import os
from SignalValidator import get_signal_score

def generate_advanced_chart(df):
    """Genera Candlestick + EMA + MACD (Como en image_a6fb28.jpg)."""
    if df.empty: return None
    
    # 1. Preparamos el DF para mplfinance (necesitaDatetimeIndex)
    df.index = pd.to_datetime(df.index)
    
    # 2. Definimos los indicadores adicionales (EMA y MACD subplots)
    # EMA 21 (La línea roja de tu imagen)
    ema21 = mpf.make_addplot(df['EMA21'], color='red', width=1.5, panel=0)
    
    # subplots del MACD
    macd = mpf.make_addplot(df['MACD'], color='black', width=1, panel=1, ylabel='MACD')
    signal = mpf.make_addplot(df['Signal'], color='blue', width=1, panel=1)
    hist = mpf.make_addplot(df['Hist'], type='bar', color='green', alpha=0.5, panel=1)
    
    # 3. Guardamos el gráfico
    output_image = "dashboard_chart.png"
    
    # Estilo 'Pro'
    mpf.plot(df.iloc[-50:], type='candle', style='charles',
             addplot=[ema21, macd, signal, hist],
             title='GGAL - Mapa Cerebral Quant (EMA21 + MACD)',
             ylabel='Precio (USD)',
             savefig=output_image,
             figsize=(12, 8))
    
    print(f"🎨 Gráfico avanzado guardado como {output_image}")
    return output_image

if __name__ == "__main__":
    _, _, _, df_15m = get_signal_score()
    generate_advanced_chart(df_15m)