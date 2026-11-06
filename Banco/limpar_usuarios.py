import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path(__file__).with_name("banco.db")


def limpar_usuarios():
    if not CAMINHO_BANCO.is_file():
        raise FileNotFoundError(f"Banco de dados não encontrado: {CAMINHO_BANCO}")

    conexao = sqlite3.connect(CAMINHO_BANCO)
    try:
        conexao.execute("BEGIN IMMEDIATE")
        quantidade = conexao.execute(
            "SELECT COUNT(*) FROM Usuarios"
        ).fetchone()[0]

        if quantidade == 0:
            conexao.rollback()
            print("Não há usuários cadastrados.")
            return

        confirmacao = input(
            f"Isso excluirá {quantidade} usuário(s). "
            "Digite LIMPAR para confirmar: "
        )
        if confirmacao != "LIMPAR":
            conexao.rollback()
            print("Operação cancelada. Nenhum usuário foi removido.")
            return

        cursor = conexao.execute("DELETE FROM Usuarios")
        conexao.commit()
        print(f"{cursor.rowcount} usuário(s) removido(s).")
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


if __name__ == "__main__":
    limpar_usuarios()
