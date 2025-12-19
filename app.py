import streamlit as st

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Fortaleza 2035",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded" # En PC abierto, en móvil se contrae solo
)

# --- 2. DISEÑO VISUAL (CSS PERSONALIZADO) ---
# Aquí definimos la paleta de colores "Decente y No Chillona"
st.markdown("""
    <style>
        /* FONDO PRINCIPAL: Gris Oscuro Elegante (No negro puro) */
        .stApp {
            background-color: #121417;
        }
        
        /* BARRA LATERAL: Un tono ligeramente distinto para separar */
        section[data-testid="stSidebar"] {
            background-color: #0e1012;
            border-right: 1px solid #2b2d3e;
        }
        
        /* TEXTOS: Blanco Suave para lectura fácil */
        h1, h2, h3, p, label {
            color: #e0e0e0 !important;
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* ACENTOS: Verde "Financiero" (Teal) para títulos importantes */
        h1 span, h2 span {
            color: #20c997 !important; /* Muted Teal */
        }
        
        /* PESTAÑAS (TABS): Diseño profesional tipo tarjeta */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #1a1c24;
            border-radius: 5px;
            color: #a0a0a0;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #20c997 !important; /* Color Activo */
            color: #121417 !important; /* Texto oscuro sobre fondo claro */
        }
        
        /* CAJAS/CONTENEDORES: Bordes sutiles */
        div[data-testid="stExpander"] {
            border: 1px solid #2b2d3e;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. BARRA LATERAL (Navegación y Billetera) ---
with st.sidebar:
    st.markdown("### 🏛️ Centro de Mando")
    st.write("---")
    # Placeholder para inputs futuros
    st.info("📍 Aquí irán los controles de depósito y saldos.")
    st.write("---")
    st.caption("v1.0 - Estructura Base")

# --- 4. ÁREA PRINCIPAL ---
st.title("Fortaleza 2035")
st.markdown("### Dashboard de Patrimonio")

# Creamos los contenedores para los 6 Módulos
# Usamos Tabs para que en celular sea fácil navegar tocando botones
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Visión", 
    "🧮 Calcular", 
    "📡 Radar", 
    "💰 Rentas", 
    "💾 Datos", 
    "📘 Academia"
])

# --- 5. PLACEHOLDERS (ESPACIOS RESERVADOS) ---
with tab1:
    st.header("Módulo 1: Visión General")
    st.caption("Aquí irán los gráficos de pastel y tu patrimonio total.")
    st.container(border=True).write("🚧 Espacio reservado para Gráficos")

with tab2:
    st.header("Módulo 2: La Calculadora")
    st.caption("Aquí irá el algoritmo de rebalanceo y la lista de compra.")
    st.container(border=True).write("🚧 Espacio reservado para Algoritmo")

with tab3:
    st.header("Módulo 3: Radar de Mercado")
    st.caption("Aquí irá el Semáforo VIX y Noticias.")
    st.container(border=True).write("🚧 Espacio reservado para API Yahoo Finance")

with tab4:
    st.header("Módulo 4: El Rentista")
    st.caption("Aquí verás tus dividendos proyectados.")
    st.container(border=True).write("🚧 Espacio reservado para Cálculo de Yield")

with tab5:
    st.header("Módulo 5: Memoria")
    st.caption("Aquí podrás descargar tu backup.")
    st.container(border=True).write("🚧 Espacio reservado para CSV/Excel")

with tab6:
    st.header("Módulo 6: La Academia")
    st.caption("Aquí irá tu manual y glosario.")
    st.container(border=True).write("🚧 Espacio reservado para Texto Educativo")
