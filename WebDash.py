import streamlit as st
import pandas as pd
import sqlite3
from IOL_Connector import IOL_Client
from SignalValidator import calculate_greeks, get_market_data

# CONFIGURACIÓN (Poné tus datos acá)
USER_IOL = "TU_MAIL@EJEMPLO.COM"
PASS_IOL = "TU_PASSWORD"

st.set_page_config(page_title="Orion Quant", layout="wide")
st.title("🛡️ AntiGravity Engine - GGAL")

# --- LÓGICA DE DATOS ---
ccl, spot, tasa = get_market_data()
iol = IOL_Client(USER_IOL, PASS_IOL)

col1, col2 = st.columns(2)
col1.metric("GGAL Local", f"${spot}")
col2.metric("Dólar CCL", f"${ccl}")

# --- PANEL DE OPCIONES ---
st.subheader("⛓️ Cadena de Opciones en Tiempo Real")
df_panel = iol.get_options_data("GGAL")

if not df_panel.empty:
    # Filtro rápido y extracción de Strike
    df_panel = df_panel[df_panel['ultimoPrecio'] > 0].copy()
    df_panel['Strike'] = df_panel['simbolo'].str.extract(r'(\d+)').astype(float)
    
    iv = st.sidebar.slider("Volatilidad (IV)", 0.4, 1.2, 0.85)
    t_vto = 18 / 365
    
    griegas = []
    for _, row in df_panel.iterrows():
        # Solo calculamos griegas para lo que empieza con GFC (Galicia)
        d, t, g, v = calculate_greeks(spot, row['Strike'], t_vto, 0.65, iv)
        griegas.append([d, t, g, v])
    
    df_g = pd.DataFrame(griegas, columns=['Δ Delta', 'θ Theta', 'γ Gamma', 'ν Vega'])
    df_final = pd.concat([df_panel.reset_index(drop=True), df_g], axis=1)
    
    st.dataframe(df_final[['simbolo', 'ultimoPrecio', 'Strike', 'Δ Delta', 'θ Theta', 'ν Vega']], use_container_width=True)
else:
    st.error("❌ No se pudo conectar con IOL. Revisá tus credenciales en el código.")