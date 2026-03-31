import streamlit as st
import pandas as pd
from IOL_Connector import IOL_Client # Importamos tu conector

# ... (resto del código de cabecera)

st.subheader("⛓️ Cadena de Opciones IOL (Automatizada)")

# 1. Conectamos con IOL
try:
    iol = IOL_Client("ORD")
    df_panel = iol.get_options_data("GGAL")
    
    if not df_panel.empty:
        # 2. Identificamos Calls y Puts automáticamente
        # Buscamos la 'C' para Calls y 'V' para Puts en el símbolo
        df_panel['Tipo'] = df_panel['simbolo'].apply(lambda x: 'CALL 🟢' if 'C' in x[3:5] else 'PUT 🔴')
        
        # 3. Extraemos el Strike (Precio de Ejercicio) del nombre
        df_panel['Strike'] = df_panel['simbolo'].str.extract('(\d+)').astype(float)
        
        # 4. Filtramos solo lo que tiene movimiento hoy
        df_display = df_panel[df_panel['ultimoPrecio'] > 0][['simbolo', 'Tipo', 'Strike', 'ultimoPrecio', 'puntoMedio']]
        
        st.dataframe(df_display, use_container_width=True)
    else:
        st.warning("⚠️ No se pudo obtener el panel de IOL. Usando bases por defecto.")
        
except Exception as e:
    st.error(f"Error de conexión IOL: {e}")

    # Dentro del bucle de la tabla de Streamlit:
for index, row in df_panel.iterrows():
    ticker = row['simbolo']
    # Si la 4ta letra es 'C' es Call, si es 'V' es Put
    tipo = "CALL 🟢" if ticker == 'C' else "PUT 🔴"
    
    # Solo calculamos griegas para lo que nos interesa (Calls de GGAL)
    if ticker.startswith("GFCC"):
        d, t, g, v = calc_greeks_internal(spot, row['Strike'], t_vto, 0.65, iv)
    else:
        d, t, g, v = 0, 0, 0, 0 # Para Puts o otros activos ponemos 0 por ahora
