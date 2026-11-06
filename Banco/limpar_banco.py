import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).with_name("banco.db")

conn = sqlite3.connect(CAMINHO_BANCO)
cursor = conn.cursor()

try:
    cursor.execute("PRAGMA foreign_keys = OFF;")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tabelas = cursor.fetchall()

    for tabela in tabelas:
        nome_tabela = tabela[0]
        cursor.execute(f"DROP TABLE IF EXISTS {nome_tabela};")
        print(f"Tabela '{nome_tabela}' excluída.")

    conn.commit()
    cursor.execute("VACUUM;")

    print("\nTodos os dados e tabelas do banco foram limpos com sucesso!")

except Exception as e:
    conn.rollback()
    print(f"Ocorreu um erro ao limpar o banco: {e}")

finally:
    conn.close()