import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from IOL_Connector import IOL_Client
from SignalValidator import calculate_greeks, get_market_data

# --- 1. CARGAR CONFIGURACIÓN SEGURA ---
load_dotenv() # Lee el archivo .env
USER_IOL = os.getenv("IOL_USER")
PASS_IOL = os.getenv("IOL_PASS")

# --- 2. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Orion Quant Engine - GGAL", layout="wide")
st.title("🛡️ AntiGravity Dashboard - GGAL")

# --- 3. INICIALIZACIÓN DE CONEXIÓN ---
# Usamos session_state para que no pida un token nuevo cada vez que mueves un slider
if 'iol_client' not in st.session_state:
    if USER_IOL and PASS_IOL:
        st.session_state.iol_client = IOL_Client(USER_IOL, PASS_IOL)
    else:
        st.error("❌ ERROR: No se encontraron credenciales en el archivo .env")
        st.stop()

# --- 4. OBTENCIÓN DE DATOS DE MERCADO ---
ccl, spot, tasa = get_market_data()

# --- 5. BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("⚙️ Parámetros de Análisis")
iv = st.sidebar.slider("Volatilidad Implícita (IV)", 0.4, 1.2, 0.85, help="Ajustá la IV según el sentimiento del mercado.")
dias_vto = st.sidebar.number_input("Días al vencimiento", value=18)
tipo_filtro = st.sidebar.multiselect("Filtrar Tipo", ["CALL 🟢", "PUT 🔴"], default=["CALL 🟢", "PUT 🔴"])

# --- 6. CABECERA DE MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("GGAL Local", f"${spot}")
col2.metric("Dólar CCL", f"${ccl:.2f}")
col3.metric("Tasa Ref. (TNA)", f"{tasa}%")

# --- 7. MONITOR DE CADENA COMPLETA ---
st.subheader("⛓️ Cadena de Opciones Automatizada (Real-Time)")

# Pedimos el panel completo a IOL
df_panel = st.session_state.iol_client.get_options_data("GGAL")

if not df_panel.empty:
    # A. Identificación y Limpieza
    # Filtramos solo lo que tiene precio de punta (mercado abierto)
    df_panel = df_panel[df_panel['ultimoPrecio'] > 0].copy()
    
    # Identificamos Call o Put por la 4ta letra del símbolo
    df_panel['Tipo'] = df_panel['simbolo'].apply(lambda x: 'CALL 🟢' if x == 'C' else 'PUT 🔴')
    
    # Extraemos el Strike (Precio de Ejercicio) usando Regex seguro
    df_panel['Strike'] = df_panel['simbolo'].str.extract(r'(\d+)').astype(float)
    
    # Filtramos según la selección del Sidebar
    df_filtrado = df_panel[df_panel['Tipo'].isin(tipo_filtro)].copy()
    
    # B. Cálculo Masivo de Griegas
    griegas_data = []
    t_vto = dias_vto / 365
    
    for _, row in df_filtrado.iterrows():
        # Llamamos al motor matemático (SignalValidator)
        # Nota: Usamos la tasa dividida por 100
        d, t, g, v = calculate_greeks(spot, row['Strike'], t_vto, tasa/100, iv)
        griegas_data.append([d, t, g, v])
    
    # C. Construcción de la Tabla Final
    df_g = pd.DataFrame(griegas_data, columns=['Delta Δ', 'Theta θ', 'Gamma γ', 'Vega ν'])
    df_final = pd.concat([df_filtrado.reset_index(drop=True), df_g], axis=1)
    
    # Ordenamos por Strike para que sea fácil de leer
    df_final = df_final.sort_values('Strike')
    
    # D. Visualización
    columnas_visibles = ['simbolo', 'Tipo', 'Strike', 'ultimoPrecio', 'Delta Δ', 'Theta θ', 'Vega ν']
    st.dataframe(df_final[columnas_visibles], use_container_width=True, hide_index=True)
    
    st.caption(f"💡 Total de bases detectadas: {len(df_final)} | Los datos se actualizan al refrescar o mover parámetros.")

else:
    st.warning("⏳ Esperando respuesta de IOL... Verificá que el mercado esté abierto o tus credenciales en el .env")