import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIGURACIÓN DE LA APP (ESTILO PIOLA / MODO OSCURO) ---
st.set_page_config(
    page_title="Fortaleza 2035 Pro", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar CSS personalizado para un look "cyberpunk financiero"
st.markdown("""
    <style>
    /* Fondo principal oscuro */
    .stApp {
        background-color: #0e1117;
    }
    /* Títulos en azul neón */
    h1, h2, h3, h4 {
        color: #00e5ff !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Ajuste de métricas y textos */
    .stMetricLabel {color: #b4c6e7 !important;}
    .stMetricValue {color: #00e5ff !important;}
    p, ol, ul, dl, li {color: #e0e0e0;}
    
    /* Estilo para las tablas de datos */
    [data-testid="stDataFrame"] {
        background-color: #1a1c24;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LA ESTRATEGIA MAESTRA (TUS PORCENTAJES OBJETIVO) ---
ESTRATEGIA = {
    "VOO": 0.45,  # 45% Núcleo S&P 500
    "QQQ": 0.20,  # 20% Crecimiento Tech
    "SCHD": 0.10, # 10% Dividendos
    "AVUV": 0.10, # 10% Small Cap Value
    "MELI": 0.05, # 5% LatAm Growth
    "BAC": 0.05,  # 5% Valor Bancario
    "O": 0.05     # 5% Renta Inmobiliaria
}

# Título Principal con estilo
st.title("🏛️ PORTAFOLIO FORTALEZA 2035")
st.markdown("### 🚀 Tu sistema de inversión automatizado")
st.divider()

# --- 3. BARRA LATERAL: LA BILLETERA (INPUTS) ---
with st.sidebar:
    st.header("💰 Centro de Comando")
    st.markdown("---")
    
    # Input del depósito mensual
    st.subheader("1️⃣ Inyección de Capital")
    inversion_mensual = st.number_input(
        "¿Cuánto depositarás este mes ($)?", 
        value=100.0, 
        step=10.0,
        help="El dinero fresco que vas a meter a Hapi hoy."
    )
    
    st.markdown("---")
    
    # Inputs de las tenencias actuales (Manual por ahora)
    st.subheader("2️⃣ Estado Actual del Portafolio")
    st.caption("Ingresa el valor en dólares ($) que tienes HOY en cada activo en Hapi.")
    
    current_holdings = {}
    total_cartera = 0.0
    
    # Creamos los inputs dinámicamente
    for ticker in ESTRATEGIA.keys():
        # Usamos columnas pequeñas para que se vea ordenado en la sidebar
        col_tick, col_val = st.columns([1, 2])
        with col_tick:
            st.markdown(f"**{ticker}**")
        with col_val:
            val = st.number_input(
                f"$$ en {ticker}", 
                value=0.0, 
                step=5.0, 
                key=f"input_{ticker}",
                label_visibility="collapsed"
            )
            current_holdings[ticker] = val
            total_cartera += val

    st.markdown("---")
    # Métrica de resumen en la sidebar
    st.metric("Valor Total Cartera", f"${total_cartera:,.2f}")


# --- 4. FUNCIÓN ROBUSTA PARA OBTENER PRECIOS (BLINDADA) ---
# Usamos caché para no saturar la API si recargas la página rápido
@st.cache_data(ttl=300, show_spinner=False) 
def get_current_price_safe(ticker):
    """
    Intenta obtener el precio más reciente de forma segura.
    Si falla, devuelve 0.0 en lugar de romper la app.
    """
    try:
        # Descargamos solo el último día
        ticker_obj = yf.Ticker(ticker)
        # Usamos 'fast_info' que a veces es más rápido y estable para el último precio
        price = ticker_obj.fast_info['last_price']
        if pd.isna(price) or price <= 0:
             # Plan B: history normal
             hist = ticker_obj.history(period="1d")
             if not hist.empty:
                 price = hist['Close'].iloc[-1]
             else:
                 price = 0.0
        return price
    except Exception:
        return 0.0

# --- 5. LÓGICA PRINCIPAL DEL DASHBOARD ---

# Solo mostramos el dashboard si hay dinero en la cartera
if total_cartera > 0 or inversion_mensual > 0:
    
    # Diseño de 2 columnas: Izquierda (Gráfico), Derecha (Tabla de Compra)
    col_izq, col_der = st.columns([4, 5], gap="medium")
    
    with col_izq:
        st.subheader("📊 Distribución Actual")
        
        if total_cartera > 0:
            # Preparamos datos para el gráfico
            df_chart = pd.DataFrame(list(current_holdings.items()), columns=['Ticker', 'Valor ($)'])
            df_chart['Porcentaje'] = (df_chart['Valor ($)'] / total_cartera) * 100
            
            # Gráfico de Donut "Piola" con Plotly
            # Usamos una paleta de colores moderna (Plasma o Viridis funcionan bien en oscuro)
            fig = px.pie(
                df_chart, 
                values='Valor ($)', 
                names='Ticker', 
                hole=0.55, # Hace el agujero del donut
                color_discrete_sequence=px.colors.sequential.Plasma_r,
                hover_data=['Porcentaje']
            )
            
            # Ajustes finos del diseño del gráfico para que se integre al fondo oscuro
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0') # Texto claro
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Métrica rápida debajo del gráfico
            st.info(f"Capital Total Proyectado: **${total_cartera + inversion_mensual:,.2f}**")
        else:
            st.info("Ingresa tus tenencias en la barra lateral para ver el gráfico.")

    with col_der:
        st.subheader("⚖️ Algoritmo de Rebalanceo Inteligente")
        st.write(f"Objetivo: Distribuir tus **${inversion_mensual}** para volver al equilibrio perfecto.")
        
        # --- CÁLCULO MATEMÁTICO ---
        capital_futuro = total_cartera + inversion_mensual
        plan_compra_data = []
        
        # 1. Calcular cuánto falta en cada activo para llegar a su % ideal
        for ticker, target_pct in ESTRATEGIA.items():
            meta_dinero_ideal = capital_futuro * target_pct
            tienes_ahora = current_holdings[ticker]
            falta_para_meta = meta_dinero_ideal - tienes_ahora
            
            # Si falta es negativo, significa que tenemos de más. No vendemos, ponemos 0 compra.
            if falta_para_meta < 0:
                falta_para_meta = 0
                
            plan_compra_data.append({"Ticker": ticker, "Target %": target_pct, "Falta ($)": falta_para_meta})
            
        df_plan = pd.DataFrame(plan_compra_data)
        
        # 2. Ajuste Proporcional (Prorrateo)
        # Esto asegura que la suma de las compras sea EXACTAMENTE el depósito mensual
        total_necesidad_compra = df_plan['Falta ($)'].sum()
        
        if total_necesidad_compra > 0:
            # Regla de tres simple para repartir el depósito
            df_plan['A Comprar ($)'] = (df_plan['Falta ($)'] / total_necesidad_compra) * inversion_mensual
        else:
            # Si la cartera está perfectamente balanceada (raro), se reparte según target
            df_plan['A Comprar ($)'] = inversion_mensual * df_plan['Target %']

        # Filtrar solo los que necesitan compra (mayores a 1 centavo)
        df_final = df_plan[df_plan['A Comprar ($)'] > 0.01].copy()
        
        # --- OBTENCIÓN DE PRECIOS EN VIVO ---
        with st.spinner('📡 Conectando con Wall Street para obtener precios en tiempo real...'):
            # Creamos columnas vacías
            df_final['Precio Aprox ($)'] = 0.0
            df_final['Acciones Est.'] = 0.0
            precios_exitosos = False
            
            # Iteramos y buscamos precio uno por uno de forma segura
            for index, row in df_final.iterrows():
                precio = get_current_price_safe(row['Ticker'])
                if precio > 0:
                    df_final.at[index, 'Precio Aprox ($)'] = precio
                    df_final.at[index, 'Acciones Est.'] = row['A Comprar ($)'] / precio
                    precios_exitosos = True
                # Pequeña pausa para no ser bloqueados por Yahoo
                time.sleep(0.1)

        # --- MOSTRAR RESULTADOS ---
        if not df_final.empty:
            st.success(f"✅ ¡Cálculo completado! Ve a Hapi y ejecuta estas órdenes:")
            
            # Definir qué columnas mostrar (si fallaron los precios, mostramos menos)
            if precios_exitosos:
                columnas_visibles = ['Ticker', 'A Comprar ($)', 'Precio Aprox ($)', 'Acciones Est.']
                formato = {
                    "A Comprar ($)": "${:.2f}", 
                    "Precio Aprox ($)": "${:.2f}", 
                    "Acciones Est.": "{:.4f}"
                }
            else:
                 st.warning("⚠️ No se pudieron obtener precios en vivo, pero los montos en dólares son correctos.")
                 columnas_visibles = ['Ticker', 'A Comprar ($)']
                 formato = {"A Comprar ($)": "${:.2f}"}

            # Mostrar la tabla con estilo "bacan" (gradiente verde en la columna importante)
            st.dataframe(
                df_final[columnas_visibles].style
                .format(formato)
                .background_gradient(cmap="teal", subset=['A Comprar ($)']) # Color neón para resaltar
                .set_properties(**{'background-color': '#262730', 'color': 'white', 'border-color': '#41444e'}),
                use_container_width=True,
                hide_index=True
            )
            
            st.caption("Nota: 'Acciones Est.' es estimado. En Hapi usa la opción 'Comprar en Dólares' y pon el monto exacto de la columna 'A Comprar ($)'.")
            
        else:
            st.info("Tu cartera está perfectamente balanceada. No se requieren compras específicas, o no has ingresado el depósito.")

else:
    # Pantalla de bienvenida si no hay datos
    st.container()
    st.warning("👈 **¡Acción requerida!** Ingresa tus datos en la barra lateral izquierda para iniciar el sistema.")
    st.markdown("""
        Esta app calculará automáticamente cómo distribuir tu próximo depósito para mantener tu portafolio
        alineado con la estrategia **Fortaleza 2035**.
    """)

# --- PIE DE PÁGINA (Futura Memoria) ---
st.divider()
st.markdown("### 🧠 Memoria del Sistema (Próximamente)")
col_db1, col_db2 = st.columns([3,1])
with col_db1:
    st.caption("Aquí conectaremos una base de datos (Google Sheets) para que no tengas que ingresar tus tenencias manualmente cada mes y puedas ver tu histórico de crecimiento.")
with col_db2:
    st.button("Guardar Estado (Demo)", disabled=True, help="Habilitaremos esto en la próxima versión")
