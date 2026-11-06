import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).with_name("banco.db")


def limpar_banco():
    if not CAMINHO_BANCO.is_file():
        raise FileNotFoundError(f"Banco de dados não encontrado: {CAMINHO_BANCO}")

    conexao = sqlite3.connect(CAMINHO_BANCO)
    try:
        conexao.execute("PRAGMA foreign_keys = OFF;")
        conexao.execute("BEGIN IMMEDIATE")
        tabelas = conexao.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()

        for (nome_tabela,) in tabelas:
            nome_seguro = nome_tabela.replace('"', '""')
            conexao.execute(f'DROP TABLE "{nome_seguro}"')

        conexao.commit()
        conexao.execute("VACUUM")
        return len(tabelas)
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


if __name__ == "__main__":
    confirmacao = input(
        "Isso apagará todas as tabelas do banco. Digite LIMPAR para confirmar: "
    )
    if confirmacao == "LIMPAR":
        quantidade = limpar_banco()
        print(f"{quantidade} tabela(s) removida(s).")
    else:
        print("Operação cancelada. Nenhuma tabela foi removida.")