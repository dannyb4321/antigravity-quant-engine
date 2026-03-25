import pandas as pd
import yfinance as yf

def get_market_data():
    ticker_adr = yf.Ticker("GGAL")
    ticker_local = yf.Ticker("GGAL.BA") # La local en Buenos Aires
    
    df_adr = ticker_adr.history(period="1d", interval="5m")
    df_local = ticker_local.history(period="1d", interval="5m")
    
    if df_adr.empty or df_local.empty:
        return 0, 0, 0
    
    precio_adr = df_adr['Close'].iloc[-1]
    precio_local = df_local['Close'].iloc[-1]
    
    # Cálculo del CCL (Ratio 10 a 1 para GGAL)
    ccl = (precio_local * 10) / precio_adr
    
    # Tasa de referencia (Simulada o podés traerla de una API de bonos)
    # Por ahora la dejamos fija en la TNA actual del mercado (~60-70%)
    tasa_tna = 65.0 
    
    return ccl, precio_local, tasa_tna

# ... (Mantené tu función get_signal_score pero sumale el retorno de estos datos)