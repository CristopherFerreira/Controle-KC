import streamlit as st
import pandas as pd
from database.conexao import get_conexao
from datetime import date

BASE_FIXA = "Tobace Oeste"

def get_equipes():
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM equipes ORDER BY nome")
    equipes = cursor.fetchall()
    conn.close()
    return equipes

def verificar_duplicidade(campo, valor, onda):
    for k in onda:
        if k.get(campo) == valor and valor:
            return "duplicado na onda atual"
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute(f"SELECT sm, operadora FROM kits WHERE {campo} = ?", (valor,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return f"já existe no banco (Kit: {resultado[0]} | {resultado[1]})"
    return None

def tela_laboratorio():
    st.subheader("🔬 Laboratório — Onda do dia")

    # ─── INICIALIZA SESSÃO ───
    if "onda" not in st.session_state:
        st.session_state.onda = []
    if "onda_pronta" not in st.session_state:
        st.session_state.onda_pronta = False
    if "grupos" not in st.session_state:
        st.session_state.grupos = []
    if "coluna_ativa" not in st.session_state:
        st.session_state.coluna_ativa = "lvm"
    if "idx" not in st.session_state:
        st.session_state.idx = 0

    # ─── TELA 1: CONFIGURAR ONDA ───
    if not st.session_state.onda_pronta:
        st.markdown("### Configurar onda")

        equipes = get_equipes()
        nomes = [e[1] for e in equipes]
        ids = {e[1]: e[0] for e in equipes}

        # KITO inicial
        kito_inicial = st.text_input(
            "KITO inicial",
            placeholder="Ex: KITO-4349",
            help="Sistema gera os próximos automaticamente"
        )

        st.markdown("#### Adicionar grupos à onda")
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        with col1:
            equipe_sel = st.selectbox("Equipe", nomes, key="eq_sel")
        with col2:
            op_sel = st.selectbox("Operadora", ["Vivo", "Claro"], key="op_sel")
        with col3:
            qtd_sel = st.number_input("Qtd", min_value=1, max_value=22, value=12, key="qtd_sel")
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Adicionar"):
                st.session_state.grupos.append({
                    "equipe": equipe_sel,
                    "equipe_id": ids[equipe_sel],
                    "operadora": op_sel,
                    "quantidade": int(qtd_sel)
                })
                st.rerun()

        # Mostra grupos adicionados
        if st.session_state.grupos:
            st.markdown("#### Grupos da onda")
            total_kits = sum(g["quantidade"] for g in st.session_state.grupos)

            df_grupos = pd.DataFrame([{
                "Equipe": g["equipe"],
                "Operadora": g["operadora"],
                "Quantidade": g["quantidade"]
            } for g in st.session_state.grupos])
            st.dataframe(df_grupos, use_container_width=True, hide_index=True)
            st.info(f"Total da onda: **{total_kits} kits**")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 Gerar onda", type="primary"):
                    if not kito_inicial.strip():
                        st.error("Informe o KITO inicial.")
                        return
                    try:
                        numero_inicial = int(kito_inicial.strip().upper().replace("KITO-", ""))
                    except:
                        st.error("Formato inválido. Use ex: KITO-4349")
                        return

                    onda = []
                    contador = numero_inicial
                    for g in st.session_state.grupos:
                        for _ in range(g["quantidade"]):
                            onda.append({
                                "kito": f"KITO-{contador}",
                                "equipe": g["equipe"],
                                "equipe_id": g["equipe_id"],
                                "operadora": g["operadora"],
                                "base": BASE_FIXA,
                                "data": str(date.today()),
                                "lvm": "",
                                "modem": "",
                                "sim_card": "",
                                "linha": ""
                            })
                            contador += 1

                    st.session_state.onda = onda
                    st.session_state.onda_pronta = True
                    st.session_state.coluna_ativa = "lvm"
                    st.session_state.idx = 0
                    st.rerun()

            with col2:
                if st.button("🗑️ Limpar grupos"):
                    st.session_state.grupos = []
                    st.rerun()
        return

    # ─── TELA 2: BIPAGEM ───
    onda = st.session_state.onda
    total = len(onda)
    coluna = st.session_state.coluna_ativa
    idx = st.session_state.idx

    colunas = ["lvm", "modem", "sim_card", "linha"]
    labels = {
        "lvm": "Concentradora (LVM)",
        "modem": "Modem",
        "sim_card": "SIM Card",
        "linha": "Linha"
    }

    # Métricas
    prontos = sum(1 for k in onda if k["lvm"] and k["modem"] and k["sim_card"] and k["linha"])
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de kits", total)
    with col2:
        st.metric("Completos", prontos)
    with col3:
        st.metric("Pendentes", total - prontos)
    with col4:
        st.metric("Base", BASE_FIXA)

    st.markdown("---")

    # Campo de bipagem
    if coluna in colunas and idx < total:
        kit_atual = onda[idx]
        st.markdown(f"### ▶ {labels[coluna]} — Kit **{kit_atual['kito']}** ({idx + 1}/{total})")
        st.caption(f"Equipe: {kit_atual['equipe']} | Operadora: {kit_atual['operadora']}")

        entrada = st.text_input(
            f"Bipe o {labels[coluna]}",
            key=f"bip_{coluna}_{idx}",
            placeholder="Aguardando bipagem..."
        )

        if entrada and entrada.strip():
            valor = entrada.strip().upper()
            erro = verificar_duplicidade(coluna, valor, onda)
            if erro:
                st.error(f"⚠️ **{valor}** — {erro}")
            else:
                st.session_state.onda[idx][coluna] = valor
                proximo = idx + 1
                if proximo < total:
                    st.session_state.idx = proximo
                else:
                    idx_col = colunas.index(coluna)
                    if idx_col + 1 < len(colunas):
                        st.session_state.coluna_ativa = colunas[idx_col + 1]
                        st.session_state.idx = 0
                    else:
                        st.session_state.coluna_ativa = "concluido"
                st.rerun()

    elif coluna == "concluido":
        st.success("✅ Todos os componentes bipados! Revise e salve.")

    st.markdown("---")

    # ─── TABELA DA ONDA ───
    st.markdown("### Planilha da onda")

    df = pd.DataFrame([{
        "Kit": k["kito"],
        "Equipe": k["equipe"],
        "Operadora": k["operadora"],
        "LVM": k["lvm"] or "—",
        "Modem": k["modem"] or "—",
        "SIM Card": k["sim_card"] or "—",
        "Linha": k["linha"] or "—",
        "Base": k["base"],
        "Data": k["data"],
        "Status": "✅" if (k["lvm"] and k["modem"] and k["sim_card"] and k["linha"]) else "⏳"
    } for k in onda])

    # Destaca linhas pendentes
    def colorir(row):
        if row["Status"] == "⏳":
            return ["background-color: #F0F0F0; color: #1A202C"] * len(row)
        return ["background-color: #E8F5E9; color: #1A202C"] * len(row)
    
    st.dataframe(
        df.style.apply(colorir, axis=1),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ─── BOTÕES ───
    col1, col2 = st.columns(2)

    with col1:
        todos_prontos = all(
            k["lvm"] and k["modem"] and k["sim_card"] and k["linha"]
            for k in onda
        )
        if todos_prontos:
            if st.button("✅ Salvar onda no estoque", type="primary"):
                conn = get_conexao()
                cursor = conn.cursor()
                salvos = 0
                for k in onda:
                    try:
                        cursor.execute("""
                            INSERT INTO kits (sm, lvm, modem, sim_card, linha, operadora, equipe_id, local, status)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'estoque')
                        """, (k["kito"], k["lvm"], k["modem"], k["sim_card"],
                              k["linha"], k["operadora"], k["equipe_id"], k["base"]))
                        salvos += 1
                    except Exception as e:
                        st.error(f"Erro ao salvar {k['kito']}: {e}")
                conn.commit()
                conn.close()
                st.success(f"✅ {salvos} kits salvos no estoque!")
                st.session_state.onda = []
                st.session_state.onda_pronta = False
                st.session_state.grupos = []
                st.session_state.coluna_ativa = "lvm"
                st.session_state.idx = 0
                st.rerun()
        else:
            st.info(f"⏳ {prontos} de {total} kits completos.")

    with col2:
        if st.button("🗑️ Cancelar onda"):
            st.session_state.onda = []
            st.session_state.onda_pronta = False
            st.session_state.grupos = []
            st.session_state.coluna_ativa = "lvm"
            st.session_state.idx = 0
            st.rerun()