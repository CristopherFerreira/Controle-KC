import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "kc_controle.db")

APP_NOME = "Controle Operacional KC"
APP_VERSAO = "2.0.1"

CSS = """
<style>
    /* Força tema claro em tudo */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F5F7FA !important;
        color: #1A202C !important;
    }

    /* Conteúdo principal */
    [data-testid="stMainBlockContainer"] {
        background-color: #F5F7FA !important;
    }

    /* Textos gerais */
    p, span, div, label, h1, h2, h3, h4 {
        color: #1A202C !important;
    }

    /* Sidebar escura */
    [data-testid="stSidebar"] {
        background-color: #1B2A4A !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 20px;
        font-weight: 500;
        color: #4A5568 !important;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1B2A4A !important;
        color: #FFFFFF !important;
    }

    /* Inputs */
    input, textarea, select {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        border: 1px solid #CBD5E0 !important;
        border-radius: 6px !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] * {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
    }
    [data-testid="stSelectbox"] svg {
        fill: #1A202C !important;
    }

    /* Dropdown lista de opções */
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #1B2A4A !important;
    }
    ul[data-testid="stSelectboxVirtualDropdown"] * {
        color: #FFFFFF !important;
    }
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover {
        background-color: #2D4A7A !important;
    }

    /* Number input */
    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
    }
    [data-testid="stNumberInput"] button {
        background-color: #E2E8F0 !important;
        color: #1A202C !important;
        border: none !important;
    }

    /* Botões */
    .stButton > button {
        background-color: #1B2A4A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover {
        background-color: #2D4A7A !important;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #E2E8F0;
    }
    [data-testid="stMetricValue"] {
        color: #1B2A4A !important;
    }

    /* Tabelas */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 8px;
    }
</style>
"""