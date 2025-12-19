import streamlit as st
import pandas as pd
import random # Para simular datos en esta fase de diseño

# --- 1. CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(
    page_title="Fortaleza 2035",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado de navegación si no existe
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "🏠 Inicio"

# Función para cambiar de página desde los botones
def navegar_a(pagina):
    st.session_state.pagina_actual = pagina

# --- 2. ESTILOS CSS "MIDNIGHT FINANCE" (MEJORADO PARA TARJETAS) ---
st.markdown("""
    <style>
        /* FONDO */
        .stApp { background-color: #121417; }
        
        /* TARJETAS DEL INICIO (DASHBOARD CARDS) */
        div.css-card {
            background-color: #1a1c24;
            border: 1px solid #2b2d3e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        div.css-card:hover {
            border-color: #20c997;
            transform: translateY(-5px);
        }
        
        /* TEXTOS */
        h1, h2, h3, p, span { color: #e0e0e0 !important; font-family: 'Helvetica Neue', sans-serif; }
        h1 span, h2 span, .highlight { color: #20c997 !important; }
        
        /* BOTONES PERSONALIZADOS */
        div.stButton > button {
            background-color: #20c997;
            color: #0e1012;
            border: none;
            font-weight: bold;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #1aa179;
            color: white;
        }
        
        /* BARRA LATERAL */
        section[data-testid="stSidebar"] { background-color: #0e1012; border-right: 1px solid #2b2d3e; }
    </style>
""", unsafe_allow_html=True)

# --- 3. BARRA LATERAL (INPUTS GLOBALES Y MENÚ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4256/4256900.png", width=50)
    st.title("Fortaleza 2035")
    st.caption("Centro de Mando v3.0")
    st.markdown("---")
    
    # INPUTS GLOBALES (Disponibles en toda la app)
    st.markdown("### 💼 Tu Billetera")
    inversion_mensual = st.number_input("Depósito Mensual ($)", value=100.0, step=10.0)
    
    # Simulación de Saldo Total (En la versión final, esto vendrá de la suma de tus activos)
    # Por ahora hardcodeado para el diseño
    saldo_total_simulado = 12540.50 
    
    st.metric("Patrimonio Total", f"${saldo_total_simulado:,.2f}", "+2.4%")
    
    st.markdown("---")
    st.markdown("### 🧭 Navegación")
    
    # MENÚ LATERAL (Radio Button funciona como menú de navegación)
    opciones_menu = ["🏠 Inicio", "📊 Visión General", "🧮 Calculadora", "📡 Radar Mercado", "💰 Rentista", "📘 Academia"]
    
    # Sincronizar el radio button con el estado de la sesión
    seleccion = st.radio("Ir a:", opciones_menu, index=opciones_menu.index(st.session_state.pagina_actual), label_visibility="collapsed")
    
    if seleccion != st.session_state.pagina_actual:
        st.session_state.pagina_actual = seleccion
        st.rerun() # Recargar para mostrar la página nueva

# --- 4. CONTROLADOR DE PÁGINAS ---

# === PÁGINA: INICIO (DASHBOARD RESUMEN) ===
if st.session_state.pagina_actual == "🏠 Inicio":
    st.title("Bienvenido al Cuartel General")
    st.markdown("Aquí tienes lo más importante de hoy.")
    st.divider()
    
    # FILA 1 DE TARJETAS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Visión")
            st.metric("Patrimonio", f"${saldo_total_simulado:,.2f}")
            st.caption("Distribución: 85% ETFs / 15% Acciones")
            if st.button("Ver Gráficos Detallados", key="btn_vision"):
                navegar_a("📊 Visión General")
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 🧮 Calculadora")
            st.metric("Depósito Pendiente", f"${inversion_mensual:,.2f}")
            st.caption("El algoritmo está listo para asignar fondos.")
            if st.button("Ejecutar Plan de Compra", key="btn_calc"):
                navegar_a("🧮 Calculadora")
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("### 📡 Radar (VIX)")
            # Simulación de dato
            st.metric("Semáforo Mercado", "21.45", "Cautela", delta_color="off")
            st.caption("Mercado volátil. Mantén la disciplina.")
            if st.button("Ver Noticias Flash", key="btn_radar"):
                navegar_a("📡 Radar Mercado")
                st.rerun()

    st.write(" ") # Espacio
    
    # FILA 2 DE TARJETAS
    col4, col5 = st.columns([2, 1])
    
    with col4:
        with st.container(border=True):
            st.markdown("### 💰 El Rentista")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Sueldo Pasivo Anual", "$452.00", "+$12 este mes")
            with col_b:
                st.metric("Próximo Pago", "Realty Income (O)", "15 Dic")
            
            if st.button("Ver Calendario de Pagos", key="btn_rentas"):
                navegar_a("💰 Rentista")
                st.rerun()
                
    with col5:
        with st.container(border=True):
            st.markdown("### 📘 Academia")
            st.info("💡 Consejo del día: 'El tiempo en el mercado supera al timing del mercado'.")
            if st.button("Leer Manual", key="btn_academy"):
                navegar_a("📘 Academia")
                st.rerun()

# === PÁGINA: VISIÓN GENERAL ===
elif st.session_state.pagina_actual == "📊 Visión General":
    st.title("📊 Visión General de Activos")
    st.markdown("Aquí irá el Módulo 1 con gráficos de pastel interactivos y KPIs.")
    st.info("🚧 En construcción: Gráficos de Plotly conectando con tus datos reales.")

# === PÁGINA: CALCULADORA ===
elif st.session_state.pagina_actual == "🧮 Calculadora":
    st.title("🧮 Calculadora de Rebalanceo")
    st.markdown(f"Planificando compra para: **${inversion_mensual:,.2f}**")
    st.info("🚧 En construcción: Algoritmo Waterfilling y Tabla de Compras.")

# === PÁGINA: RADAR ===
elif st.session_state.pagina_actual == "📡 Radar Mercado":
    st.title("📡 Radar de Inteligencia")
    st.markdown("Semáforo VIX y Noticias Filtradas.")
    st.info("🚧 En construcción: Conexión API con Yahoo Finance.")

# === PÁGINA: RENTISTA ===
elif st.session_state.pagina_actual == "💰 Rentista":
    st.title("💰 Gestión de Rentas Pasivas")
    st.markdown("Proyección de dividendos y Yield on Cost.")
    st.info("🚧 En construcción: Calculadora de Yields.")

# === PÁGINA: ACADEMIA ===
elif st.session_state.pagina_actual == "📘 Academia":
    st.title("📘 Academia Fortaleza")
    st.markdown("### El manual del piloto para no perder el rumbo.")
    st.markdown("Aquí reside la filosofía, la estrategia y la lógica matemática de tu sistema.")
    
    # Dividimos el conocimiento en 4 áreas clave
    tab_filosofia, tab_activos, tab_logica, tab_glosario = st.tabs([
        "🧠 Filosofía", 
        "🏛️ Tus Activos", 
        "🧮 El Algoritmo", 
        "📚 Glosario"
    ])

    # --- PESTAÑA 1: FILOSOFÍA ---
    with tab_filosofia:
        st.header("Los Dos Pilares")
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container(border=True):
                st.subheader("🛡️ Benjamin Graham")
                st.caption("El Padre del Value Investing")
                st.markdown("""
                * **Enfoque:** Seguridad y Valor.
                * **Regla de Oro:** Compra $1 dólar de valor por $0.50 centavos.
                * **Tu Cartera:** Representado por **SCHD, BAC y AVUV**.
                * **Mentalidad:** "Si el mercado cae, me alegro porque compro barato".
                """)
        
        with col2:
            with st.container(border=True):
                st.subheader("🚁 Robert Kiyosaki")
                st.caption("El Padre Rico")
                st.markdown("""
                * **Enfoque:** Flujo de Caja y Activos.
                * **Regla de Oro:** Los activos ponen dinero en tu bolsillo.
                * **Tu Cartera:** Representado por **O (Rentas), MELI (Negocio) y QQQ (Futuro)**.
                * **Mentalidad:** "No trabajo por dinero, mi dinero trabaja para mí".
                """)
        
        st.info("💡 **Tu Estrategia Híbrida:** Usamos la seguridad de Graham para no quebrar, y la agresividad de Kiyosaki para crecer.")

    # --- PESTAÑA 2: TUS ACTIVOS ---
    with tab_activos:
        st.header("¿Qué tienes y por qué?")
        st.markdown("Tu ejército de 7 soldados explicado uno por uno.")

        # Núcleo
        with st.expander("🛡️ VOO - El Núcleo (S&P 500) | 45%", expanded=True):
            st.write("Son las 500 empresas más grandes de EE.UU. Es la apuesta a que la economía americana seguirá dominando. Si VOO cae a cero, el dinero ya no importa.")
        
        # Crecimiento
        with st.expander("🚀 QQQ - El Motor (Nasdaq 100) | 20%"):
            st.write("Tecnología pura. Apple, Microsoft, Nvidia. Aquí está el crecimiento explosivo, pero también la volatilidad. Es el cohete de la cartera.")
            
        # Dividendos & Valor
        with st.expander("💰 SCHD - La Defensa (Dividendos) | 10%"):
            st.write("Empresas aburridas pero ricas (Coca-Cola, Pepsi, Home Depot) que pagan dividendos crecientes. Protege cuando la tecnología cae.")
            
        with st.expander("💎 AVUV - El Outsider (Small Cap Value) | 10%"):
            st.write("Empresas pequeñas y baratas. Históricamente, este sector es el que más dinero da a largo plazo (más que el S&P 500), aunque es volátil.")
            
        # Satélites (Acciones Individuales)
        with st.expander("🐆 MELI - El Ataque (MercadoLibre) | 5%"):
            st.write("El Amazon de Latinoamérica. Crecimiento agresivo en mercados emergentes. Alto riesgo, alta recompensa.")
            
        with st.expander("🏦 BAC - El Valor (Bank of America) | 5%"):
            st.write("La apuesta favorita de Warren Buffett. Un banco sólido comprado a buen precio. Se beneficia cuando suben las tasas de interés.")
            
        with st.expander("🏠 O - El Casero (Realty Income) | 5%"):
            st.write("Dueño de miles de propiedades comerciales (7-Eleven, Walmart). Te paga alquiler (dividendos) todos los meses.")

    # --- PESTAÑA 3: LÓGICA DEL ALGORITMO ---
    with tab_logica:
        st.header("¿Cómo decide la App qué comprar?")
        st.markdown("No usamos corazonadas. Usamos el algoritmo de **'Llenado de Vasos' (Waterfilling)**.")
        
        st.markdown("""
        1.  **Imagina 7 vasos:** Cada activo (VOO, QQQ, etc.) es un vaso que debe tener un nivel de agua específico (tu % ideal).
        2.  **El nivel actual:** Algunos vasos tienen menos agua de la que deberían (porque la acción bajó de precio o porque no has comprado en mucho tiempo).
        3.  **El chorro de agua ($):** Tu depósito mensual es una jarra de agua nueva.
        4.  **La decisión:** La App vierte el agua **SOLO en los vasos que están más vacíos** respecto a su marca ideal.
        """)
        
        st.warning("""
        **¿Por qué es genial esto?**
        Porque te obliga matemáticamente a **COMPRAR BARATO**. 
        Si QQQ sube mucho, su vaso se llena solo (sube de valor). La App dejará de mandar dinero ahí y lo mandará a lo que se haya quedado atrás (ej. SCHD).
        """)

    # --- PESTAÑA 4: GLOSARIO ---
    with tab_glosario:
        st.header("Diccionario Financiero")
        
        # Usamos una lista de definiciones limpia
        terms = {
            "ETF (Exchange Traded Fund)": "Una canasta de acciones. Compras una acción del ETF y eres dueño de cientos de empresas a la vez (ej. VOO).",
            "Yield (Rentabilidad por Dividendo)": "El interés anual que te paga una empresa solo por tenerla. Si tienes $100 y el yield es 3%, te pagan $3 al año.",
            "VIX (Índice del Miedo)": "Mide qué tan asustados están los inversores. VIX alto = Miedo (Oportunidad de compra). VIX bajo = Calma (Todo caro).",
            "Bull Market (Toro)": "Cuando el mercado sube con fuerza y optimismo.",
            "Bear Market (Oso)": "Cuando el mercado cae más del 20% y hay pesimismo.",
            "Broker (Hapi)": "La aplicación intermediaria que te permite comprar y vender acciones en la bolsa de Nueva York.",
            "Rebalanceo": "El acto de vender lo que subió o comprar lo que bajó para volver a tus porcentajes originales."
        }
        
        for term, definition in terms.items():
            st.markdown(f"**{term}:**")
            st.caption(definition)
            st.divider()

