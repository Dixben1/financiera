import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN VISUAL "PRO" ---
st.set_page_config(
    page_title="Fortaleza 2035", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para el look "Dark Mode Financiero"
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    h1, h2, h3 {color: #00e5ff !important; font-family: 'Roboto', sans-serif;}
    .stMetricLabel {color: #a0a0a0 !important;}
    .stMetricValue {color: #00e5ff !important; font-weight: bold;}
    /* Tablas más limpias */
    [data-testid="stDataFrame"] {border: 1px solid #2b2d3e;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. TU ESTRATEGIA DE INVERSIÓN ---
ESTRATEGIA = {
    "VOO": 0.45,  # Núcleo
    "QQQ": 0.20,  # Crecimiento
    "SCHD": 0.10, # Dividendos
    "AVUV": 0.10, # Small Cap Value
    "MELI": 0.05, # LatAm
    "BAC": 0.05,  # Valor Banco
    "O": 0.05     # Renta Mensual
}

# --- 3. BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.title("💰 Centro de Mando")
    st.markdown("---")
    
    # Capital a inyectar
    inversion_mensual = st.number_input(
        "💵 Depósito Mensual ($)", 
        value=100.0, step=10.0,
        help="Dinero nuevo que vas a ingresar a Hapi."
    )
    
    st.markdown("### 🏦 Tu Portafolio Actual")
    st.caption("Ingresa el valor actual en USD de cada activo:")
    
    # Inputs dinámicos para cada activo
    current_holdings = {}
    total_cartera = 0.0
    
    for ticker in ESTRATEGIA.keys():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**{ticker}**")
        with col2:
            val = st.number_input(
                f"$$", 
                value=0.0, step=10.0, 
                key=f"val_{ticker}", 
                label_visibility="collapsed"
            )
            current_holdings[ticker] = val
            total_cartera += val
            
    st.divider()
    st.metric("Total Patrimonio", f"${total_cartera:,.2f}")
    st.metric("Nuevo Total Proyectado", f"${total_cartera + inversion_mensual:,.2f}")

# --- 4. FUNCIÓN SEGURA DE PRECIOS (ANTI-ERRORES) ---
@st.cache_data(ttl=600) # Guarda datos 10 min para no saturar
def get_safe_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Intentamos obtener el precio actual
        price = stock.fast_info['last_price']
        if price and price > 0:
            return price
        # Si falla, intentamos historial de 1 día
        hist = stock.history(period="1d")
        if not hist.empty:
            return hist['Close'].iloc[-1]
        return 0.0
    except:
        return 0.0

# --- 5. PANEL PRINCIPAL ---
st.title("🏛️ ESTRATEGIA FORTALEZA 2035")
st.markdown("Algoritmo de Rebalanceo Inteligente | Graham & Kiyosaki")

if total_cartera > 0 or inversion_mensual > 0:
    
    # Crear pestañas para organizar la info
    tab1, tab2 = st.tabs(["📊 Análisis Visual", "🛒 Plan de Compra"])
    
    # --- PESTAÑA 1: GRÁFICOS ---
    with tab1:
        col_graf, col_info = st.columns([2, 1])
        
        with col_graf:
            if total_cartera > 0:
                df_pie = pd.DataFrame(list(current_holdings.items()), columns=['Ticker', 'Valor'])
                fig = px.pie(
                    df_pie, values='Valor', names='Ticker', hole=0.6,
                    color_discrete_sequence=px.colors.sequential.Tealgrn_r
                )
                fig.update_layout(
                    showlegend=True, 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white")
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Ingresa tus datos en la barra lateral para ver el gráfico.")
        
        with col_info:
            st.markdown("#### 🎯 Objetivos")
            df_target = pd.DataFrame(list(ESTRATEGIA.items()), columns=['Ticker', 'Meta %'])
            df_target['Meta %'] = (df_target['Meta %'] * 100).astype(int).astype(str) + "%"
            st.dataframe(df_target, hide_index=True, use_container_width=True)

    # --- PESTAÑA 2: CÁLCULOS ---
    with tab2:
        st.subheader(f"Plan para tus ${inversion_mensual}")
        
        # 1. Calcular Capital Futuro Ideal
        capital_futuro = total_cartera + inversion_mensual
        plan = []
        
        # 2. Algoritmo de llenado de vasos (Waterfilling)
        for ticker, target in ESTRATEGIA.items():
            ideal = capital_futuro * target
            actual = current_holdings[ticker]
            falta = ideal - actual
            if falta < 0: falta = 0 # No vender, solo comprar
            plan.append({"Ticker": ticker, "Falta": falta})
            
        df_plan = pd.DataFrame(plan)
        
        # 3. Ajuste para sumar exactamente el depósito
        total_falta = df_plan['Falta'].sum()
        if total_falta > 0:
            df_plan['A Invertir ($)'] = (df_plan['Falta'] / total_falta) * inversion_mensual
        else:
            # Si está perfecto (raro), distribuir según % base
            df_plan['A Invertir ($)'] = inversion_mensual * df_plan['Falta'] # Placeholder
            
        # Filtrar montos pequeños (< $1)
        df_final = df_plan[df_plan['A Invertir ($)'] > 1.0].copy()
        
        # 4. Obtener precios (Con barra de progreso)
        if not df_final.empty:
            progress_bar = st.progress(0)
            df_final['Precio Unit. ($)'] = 0.0
            
            for idx, row in df_final.iterrows():
                # Actualizar barra
                progress_bar.progress((idx + 1) / len(df_final))
                
                # Bajar precio
                precio = get_safe_price(row['Ticker'])
                df_final.at[idx, 'Precio Unit. ($)'] = precio
            
            progress_bar.empty() # Borrar barra al terminar

            # Calcular acciones estimadas
            df_final['Acciones Est.'] = df_final.apply(
                lambda x: x['A Invertir ($)'] / x['Precio Unit. ($)'] if x['Precio Unit. ($)'] > 0 else 0, axis=1
            )
            
            # 5. MOSTRAR TABLA FINAL (CORRECCIÓN DE COLOR APLICADA)
            # Usamos 'Greens' que sí existe en matplotlib
            st.dataframe(
                df_final[['Ticker', 'A Invertir ($)', 'Precio Unit. ($)', 'Acciones Est.']]
                .style.format({
                    'A Invertir ($)': '${:.2f}',
                    'Precio Unit. ($)': '${:.2f}',
                    'Acciones Est.': '{:.4f}'
                })
                .background_gradient(cmap='Greens', subset=['A Invertir ($)']),
                use_container_width=True,
                hide_index=True
            )
            
            st.success("✅ Abre Hapi y ejecuta las órdenes de la columna 'A Invertir ($)'")
            
            # --- BOTÓN DE DESCARGA (MEMORIA PORTÁTIL) ---
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Plan de Compra (CSV)",
                data=csv,
                file_name='plan_fortaleza.csv',
                mime='text/csv',
            )
        else:
            st.warning("No hay compras recomendadas. Revisa los montos ingresados.")

else:
    st.info("👈 Ingresa tus datos en la barra lateral para comenzar.")
