import sqlite3
from config import DATABASE_PATH
from database.models import criar_tabelas

def get_conexao():
    criar_tabelas()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn