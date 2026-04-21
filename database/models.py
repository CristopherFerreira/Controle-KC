import sqlite3
from config import DATABASE_PATH

def criar_tabelas():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            papel TEXT NOT NULL,
            criado_em TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sm TEXT UNIQUE,
            lvm TEXT NOT NULL UNIQUE,
            modem TEXT NOT NULL UNIQUE,
            sim_card TEXT NOT NULL UNIQUE,
            linha TEXT,
            operadora TEXT NOT NULL,
            equipe_id INTEGER,
            local TEXT,
            status TEXT NOT NULL DEFAULT 'montagem',
            criado_por INTEGER,
            criado_em TEXT DEFAULT (datetime('now', 'localtime')),
            atualizado_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (equipe_id) REFERENCES equipes(id),
            FOREIGN KEY (criado_por) REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_lab (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kit_id INTEGER NOT NULL,
            etapa TEXT NOT NULL,
            status TEXT NOT NULL,
            observacao TEXT,
            usuario_id INTEGER,
            feito_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (kit_id) REFERENCES kits(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabela TEXT NOT NULL,
            registro_id INTEGER NOT NULL,
            acao TEXT NOT NULL,
            detalhe TEXT,
            usuario_id INTEGER,
            feito_em TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso!")

def popular_equipes():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    equipes = []

    for i in range(200, 206):
        equipes.append(f"STB{i}")

    for i in range(210, 216):
        equipes.append(f"STB{i}")

    for i in range(220, 226):
        equipes.append(f"STB{i}")

    for i in range(310, 314):
        equipes.append(f"STB{i}")

    for nome in equipes:
        cursor.execute("""
            INSERT OR IGNORE INTO equipes (nome) VALUES (?)
        """, (nome,))

    conn.commit()
    conn.close()
    print(f"{len(equipes)} equipes inseridas!")