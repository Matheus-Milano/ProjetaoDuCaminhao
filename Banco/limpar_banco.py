import sqlite3
import os

# 1. Localiza o caminho exato do banco.db no mesmo diretório do script
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(DIRETORIO_ATUAL, "banco.db")

# 2. Conecta ao banco encontrado
conn = sqlite3.connect(CAMINHO_BANCO)
cursor = conn.cursor()

try:
    # 3. Desativar chaves estrangeiras temporariamente para evitar erros de restrição ao dropar
    cursor.execute("PRAGMA foreign_keys = OFF;")

    # 4. Buscar o nome de todas as tabelas criadas pelo usuário (ignorando as internas do SQLite)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tabelas = cursor.fetchall()

    # 5. Deletar cada tabela encontrada dinamicamente
    for tabela in tabelas:
        nome_tabela = tabela[0]
        cursor.execute(f"DROP TABLE IF EXISTS {nome_tabela};")
        print(f"Tabela '{nome_tabela}' excluída.")

    # 6. Salvar as alterações e otimizar/liberar o espaço em disco com VACUUM
    conn.commit()
    cursor.execute("VACUUM;") 

    print("\nTodos os dados e tabelas do banco foram limpos com sucesso!")

except Exception as e:
    conn.rollback()
    print(f"Ocorreu um erro ao limpar o banco: {e}")

finally:
    # 7. Garantir o fechamento da conexão
    conn.close()