import streamlit as st
import pandas as pd
import sqlite3
from SignalValidator import calculate_greeks, get_market_data

st.set_page_config(page_title="Orion Quant - GGAL", layout="wide")

st.title("🛡️ AntiGravity Quant Engine - GGAL")

# --- CONEXIÓN A LA BASE DE DATOS ---
def load_data():
    conn = sqlite3.connect('antigravity_data.db')
    df = pd.read_sql_query("SELECT * FROM whale_alerts ORDER BY timestamp DESC LIMIT 50", conn)
    conn.close()
    return df

# --- SIDEBAR: MONITOR DE GRIEGAS ---
st.sidebar.header("⚙️ Parámetros de Opciones")
strike = st.sidebar.number_input("Strike (Base)", value=6900)
iv = st.sidebar.slider("Volatilidad Implícita (IV)", 0.4, 1.2, 0.85)

# --- MÉTRICAS EN TIEMPO REAL ---
ccl, p_local, tasa = get_market_data()
delta, theta = calculate_greeks(p_local, strike, 18/365, tasa/100, iv)

col1, col2, col3, col4 = st.columns(4)
col1.metric("GGAL Local", f"${p_local}", f"{round((p_local/6710-1)*100, 2)}%")
col2.metric("Dólar CCL", f"${ccl}")
col3.metric("Delta Δ (Base {strike})", delta)
col4.metric("Theta θ (Decaimiento)", f"{theta} ARS")

# --- TABLA DE DATOS (SQL) ---
st.subheader("🐋 Historial de Ballenas y Alertas")
data = load_data()
st.dataframe(data, use_container_width=True)

if st.button("🔄 Actualizar Datos"):
    st.rerun()