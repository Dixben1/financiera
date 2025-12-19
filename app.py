import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN VISUAL (MODO DARK PRO) ---
st.set_page_config(
    page_title="Fortaleza 2035 Elite", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS avanzados para las métricas y tablas
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    /* Títulos Neón */
    h1, h2, h3 {color: #00e5ff !important; font-family: 'Roboto', sans-serif;}
    
    /* Cajas de métricas */
    div[data-testid="metric-container"] {
        background-color: #1a1c24;
        border: 1px solid #2b2d3e;
        padding: 10px;
        border-radius: 10px;
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1c24;
        border-radius: 5px;
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00e5ff !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ESTRATEGIA DEFINIDA ---
ESTRATEGIA = {
    "VOO": 0.45,  "QQQ": 0.20, "SCHD": 0.10, "AVUV": 0.10,
    "MELI": 0.05, "BAC": 0.05, "O": 0.05
}

# --- 3. FUNCIONES DE DATOS (EL CEREBRO) ---

@st.cache_data(ttl=300) # Caché de 5 min
def get_market_mood():
    """Obtiene el índice VIX (Miedo)"""
    try:
        vix = yf.Ticker("^VIX")
        price = vix.fast_info['last_price']
        
        if price < 15:
            return price, "Codicia (Mercado Tranquilo)", "normal" # Verde
        elif price < 25:
            return price, "Cautela (Normal)", "off" # Gris/Amarillo
        else:
            return price, "MIEDO (Alta Volatilidad)", "inverse" # Rojo
    except:
        return 0, "Desconectado", "off"

@st.cache_data(ttl=600)
def get_stock_info_safe(ticker):
    """Obtiene precio y dividendo de forma segura"""
    try:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        
        # Intentar obtener yield (rentabilidad dividendo)
        # Nota: info es pesado, a veces falla, usamos try interno
        div_yield = 0.0
        try:
            # Truco: Si falla info, asumimos 0 por velocidad en esta demo
            # Para producción real, esto requiere manejo de errores más lento
            info = stock.info
            div_yield = info.get('dividendYield', 0)
            if div_yield is None: div_yield = 0
        except:
            div_yield = 0.0
            
        if not price: # Si fast_info falla
            hist = stock.history(period="1d")
            price = hist['Close'].iloc[-1] if not hist.empty else 0.0
            
        return price, div_yield
    except:
        return 0.0, 0.0

def get_news_feed(tickers_list):
    """Busca noticias recientes de los activos principales"""
    news_items = []
    try:
        # Solo buscamos noticias de los grandes para no saturar
        for t in ["QQQ", "MELI", "VOO"]: 
            stock = yf.Ticker(t)
            noticias = stock.news
            if noticias:
                for n in noticias[:2]: # Top 2 noticias por activo
                    news_items.append({
                        "Ticker": t,
                        "Title": n['title'],
                        "Link": n['link'],
                        "PubDate": n.get('providerPublishTime', 0)
                    })
    except:
        pass
    return news_items

# --- 4. BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4256/4256900.png", width=50)
    st.title("Centro de Mando")
    
    inversion_mensual = st.number_input("💵 Depósito Mensual ($)", value=100.0, step=10.0)
    
    st.divider()
    st.markdown("### 🏦 Tu Portafolio (USD)")
    
    current_holdings = {}
    total_cartera = 0.0
    
    # Inputs compactos
    for ticker in ESTRATEGIA.keys():
        col_in1, col_in2 = st.columns([1, 2])
        with col_in1:
            st.markdown(f"**{ticker}**")
        with col_in2:
            val = st.number_input(f"", value=0.0, step=10.0, key=f"v_{ticker}", label_visibility="collapsed")
            current_holdings[ticker] = val
            total_cartera += val
            
    st.success(f"💰 Total: **${total_cartera:,.2f}**")

# --- 5. DASHBOARD PRINCIPAL ---

# A) MÓDULO MARKET MOOD (SEMÁFORO)
col_title, col_vix = st.columns([3, 1])
with col_title:
    st.title("Fortaleza 2035")
    st.caption(f"Estrategia Híbrida | Última actualización: {datetime.now().strftime('%H:%M')}")

with col_vix:
    vix_price, vix_label, vix_color = get_market_mood()
    st.metric("Semáforo del Mercado (VIX)", f"{vix_price:.2f}", vix_label, delta_color=vix_color)

# PESTAÑAS DE NAVEGACIÓN
tab1, tab2, tab3 = st.tabs(["📊 Visión General", "🧮 Calculadora de Compra", "📰 Noticias Flash"])

# --- TAB 1: VISIÓN GENERAL Y DIVIDENDOS ---
with tab1:
    # 1. Cálculo de Dividendos en Vivo
    st.markdown("### 👑 Rentas Pasivas Estimadas")
    
    col_divs = st.columns(len(ESTRATEGIA))
    total_dividendo_anual = 0.0
    
    # Procesamiento (Puede tardar unos segundos la primera vez)
    if total_cartera > 0:
        with st.spinner("Analizando Wall Street..."):
            stock_data = {} # Guardamos precios para no volver a llamar
            
            for ticker, valor_actual in current_holdings.items():
                if valor_actual > 0:
                    prec, yield_pct = get_stock_info_safe(ticker)
                    stock_data[ticker] = prec # Guardar precio para luego
                    
                    ingreso_anual = valor_actual * yield_pct
                    total_dividendo_anual += ingreso_anual
    
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
             st.metric("Sueldo Anual Pasivo", f"${total_dividendo_anual:.2f}", "+Reinvertir")
        with col_res2:
             st.metric("Yield Promedio Cartera", f"{(total_dividendo_anual/total_cartera)*100:.2f}%" if total_cartera else "0%")
        with col_res3:
             st.metric("Meta de Patrimonio", "$1,000,000", f"{total_cartera/10000:.2f}%")

        st.divider()
        
        # 2. Gráfico de Pastel
        st.markdown("### 🍰 Composición Actual")
        col_chart, col_target = st.columns([2, 1])
        
        with col_chart:
            df_pie = pd.DataFrame(list(current_holdings.items()), columns=['Ticker', 'Valor'])
            # Usamos paleta segura 'Tealgrn'
            fig = px.pie(df_pie, values='Valor', names='Ticker', hole=0.5, 
                         color_discrete_sequence=px.colors.sequential.Tealgrn_r)
            fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_target:
            st.markdown("**Meta Objetivo**")
            df_targets = pd.DataFrame(list(ESTRATEGIA.items()), columns=['Ticker', 'Meta'])
            df_targets['Meta'] = (df_targets['Meta'] * 100).astype(int).astype(str) + "%"
            st.dataframe(df_targets, hide_index=True, use_container_width=True)

    else:
        st.info("👈 Ingresa tus datos en la izquierda para ver el análisis.")

# --- TAB 2: CALCULADORA (EL CEREBRO) ---
with tab2:
    st.subheader(f"🛒 Plan de Compra para tus ${inversion_mensual}")
    
    if inversion_mensual > 0:
        capital_futuro = total_cartera + inversion_mensual
        plan_compra = []
        
        # Algoritmo de Rebalanceo
        for ticker, target in ESTRATEGIA.items():
            ideal = capital_futuro * target
            actual = current_holdings[ticker]
            falta = ideal - actual
            if falta < 0: falta = 0 
            plan_compra.append({"Ticker": ticker, "Falta": falta})
            
        df_calc = pd.DataFrame(plan_compra)
        total_falta = df_calc['Falta'].sum()
        
        # Prorrateo
        if total_falta > 0:
            df_calc['Invertir ($)'] = (df_calc['Falta'] / total_falta) * inversion_mensual
        else:
            df_calc['Invertir ($)'] = inversion_mensual * pd.Series(ESTRATEGIA.values())

        # Filtrar montos relevantes
        df_final = df_calc[df_calc['Invertir ($)'] > 0.5].copy()
        
        # Mostrar Tabla "Bacan"
        st.dataframe(
            df_final[['Ticker', 'Invertir ($)']].style
            .format({'Invertir ($)': '${:.2f}'})
            .background_gradient(cmap='Greens', subset=['Invertir ($)']), # 'Greens' es seguro
            use_container_width=True,
            hide_index=True
        )
        
        st.success("✅ Ejecuta estas órdenes en Hapi seleccionando 'Comprar en Dólares'.")
        
        # Botón de Guardar (CSV)
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Descargar Plan (CSV)", csv, "plan_fortaleza.csv", "text/csv")
        
    else:
        st.warning("Ingresa un monto de depósito mayor a 0.")

# --- TAB 3: NOTICIAS (MODULO FLASH) ---
with tab3:
    st.subheader("📰 Radar de Noticias")
    if st.button("🔄 Actualizar Noticias"):
        with st.spinner("Buscando titulares..."):
            news = get_news_feed(list(ESTRATEGIA.keys()))
            if news:
                for item in news:
                    with st.expander(f"{item['Ticker']} - {item['Title']}"):
                        st.write(f"Publicado: {datetime.fromtimestamp(item['PubDate']).strftime('%Y-%m-%d %H:%M')}")
                        st.markdown(f"[Leer Noticia Completa]({item['Link']})")
            else:
                st.info("No se encontraron noticias urgentes hoy.")
    else:
        st.write("Haz clic para escanear el mercado.")
