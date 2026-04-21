import streamlit as st
from config import APP_NOME, APP_VERSAO, CSS
from pages.laboratorio import tela_laboratorio

st.set_page_config(
    page_title=APP_NOME,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CSS, unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown(f"## 📡 {APP_NOME}")
    st.markdown("---")
    st.markdown("### Resumo do dia")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kits hoje", "0")
        st.metric("Em estoque", "0")
    with col2:
        st.metric("Aguard. SM", "0")
        st.metric("Pendências", "0")
    st.markdown("---")
    st.caption(f"versão {APP_VERSAO}")

# ─── ABAS ───
aba1, aba2, aba3, aba4 = st.tabs([
    "🔬  Laboratório",
    "📦  Estoque",
    "📋  Histórico",
    "⚙️  Configurações"
])

with aba1:
    tela_laboratorio()

with aba2:
    st.subheader("Estoque")
    st.info("Visualização e separação de kits por equipe e operadora.")

with aba3:
    st.subheader("Histórico")
    st.info("Registro completo de todas as ações.")

with aba4:
    st.subheader("Configurações")
    st.info("Gerenciamento de usuários e equipes.")