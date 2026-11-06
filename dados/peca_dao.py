import sqlite3

from Banco.conector_do_banco import obter_conexao
from Classes.Peca import Peca


class PecaDAO:
    def listar_todos(self):
        conexao = obter_conexao()
        try:
            linhas = conexao.execute(
                """
                SELECT id, manutencao_id, nome, codigo, quantidade, valor_unitario
                FROM PecasReposicao
                ORDER BY nome
                """
            ).fetchall()
            return [Peca(*linha) for linha in linhas]
        finally:
            conexao.close()

    def buscar_por_id(self, id_peca):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                """
                SELECT id, manutencao_id, nome, codigo, quantidade, valor_unitario
                FROM PecasReposicao WHERE id = ?
                """,
                (id_peca,),
            ).fetchone()
            return Peca(*linha) if linha else None
        finally:
            conexao.close()

    def inserir(self, peca):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                INSERT INTO PecasReposicao (
                    manutencao_id, nome, codigo, quantidade, valor_unitario
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    peca.manutencao_id,
                    peca.nome,
                    peca.codigo,
                    peca.quantidade,
                    peca.valor_unitario,
                ),
            )
            conexao.commit()
            peca.id = cursor.lastrowid
            return peca.id
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def atualizar(self, peca):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                UPDATE PecasReposicao SET
                    manutencao_id = ?, nome = ?, codigo = ?,
                    quantidade = ?, valor_unitario = ?
                WHERE id = ?
                """,
                (
                    peca.manutencao_id,
                    peca.nome,
                    peca.codigo,
                    peca.quantidade,
                    peca.valor_unitario,
                    peca.id,
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Peça {peca.id} não encontrada.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def excluir(self, id_peca):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                "DELETE FROM PecasReposicao WHERE id = ?", (id_peca,)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Peça {id_peca} não encontrada.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
