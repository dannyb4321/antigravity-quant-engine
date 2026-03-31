import pandas as pd
import yfinance as yf

# CONFIGURACIÓN DE TU ESTRATEGIA
CAPITAL_TOTAL_ARS = 117000 
RIESGO_POR_OPERACION = 0.02 # Arriesgar el 2% del capital total por trade

def calculate_position_size(price, atr):
    """
    Calcula el tamaño de la posición basándose en el ATR y el Stop Loss del 15%.
    """
    # Usamos 2 veces el ATR para el Stop Loss Técnico
    stop_loss_dist = 2 * atr
    
    # Comparamos con el 15% de tu estrategia; usamos el que sea más amplio para dar aire
    stop_loss_final = max(stop_loss_dist, price * 0.15)
    
    # Cálculo del riesgo monetario
    riesgo_monetario = CAPITAL_TOTAL_ARS * RIESGO_POR_OPERACION
    
    # Cantidad de acciones = Riesgo / Distancia al Stop
    if stop_loss_final > 0:
        cantidad_acciones = riesgo_monetario / stop_loss_final
    else:
        cantidad_acciones = 0
    
    return round(cantidad_acciones), round(price - stop_loss_final, 2)

def get_risk_report():
    try:
        ticker = yf.Ticker("GGAL")
        df = ticker.history(period="5d", interval="15m")
        if df.empty: return "⚠️ No hay data para riesgo."

        # Cálculo de ATR
        df['high_low'] = df['High'] - df['Low']
        df['high_cp'] = abs(df['High'] - df['Close'].shift())
        df['low_cp'] = abs(df['Low'] - df['Close'].shift())
        df['TR'] = df[['high_low', 'high_cp', 'low_cp']].max(axis=1)
        atr = df['TR'].rolling(window=14).mean().iloc[-1]
        
        price = df['Close'].iloc[-1]
        cantidad, sl_precio = calculate_position_size(price, atr)
        
        reporte = f"📏 *REPORTE DE GESTIÓN*\n"
        reporte += f"💰 *Acciones sugeridas:* {cantidad}\n"
        reporte += f"🛡️ *Stop Loss (ATR/15%):* ${sl_precio}\n"
        reporte += f"💵 *Riesgo Máximo:* ${round(CAPITAL_TOTAL_ARS * RIESGO_POR_OPERACION)} ARS"
        return reporte
    except:
        return "⚠️ Error calculando riesgo."

if __name__ == "__main__":
    print(get_risk_report())