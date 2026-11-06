import sqlite3
from datetime import datetime

from Banco.conector_do_banco import obter_conexao
from Classes.Entrega import Entrega


def _para_datetime(valor):
    return datetime.fromisoformat(valor) if valor else None


def _para_texto_datetime(valor):
    return valor.isoformat(sep=" ") if isinstance(valor, datetime) else valor


def _entrega_da_linha(linha):
    return Entrega(
        id_entrega=linha[0],
        viagem_id=linha[1],
        descricao_carga=linha[2],
        peso_kg=linha[3],
        destinatario=linha[4],
        endereco_destino=linha[5],
        entrega_prevista=_para_datetime(linha[6]),
        entrega_realizada=_para_datetime(linha[7]),
        status_entrega=linha[8],
    )


class EntregaDAO:
    _colunas = """
        id, viagem_id, descricao_carga, peso_kg, destinatario, endereco_destino,
        entrega_prevista, entrega_realizada, status_entrega
    """

    def listar_todos(self):
        conexao = obter_conexao()
        try:
            linhas = conexao.execute(
                f"SELECT {self._colunas} FROM Entregas ORDER BY entrega_prevista"
            ).fetchall()
            return [_entrega_da_linha(linha) for linha in linhas]
        finally:
            conexao.close()

    def buscar_por_id(self, id_entrega):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                f"SELECT {self._colunas} FROM Entregas WHERE id = ?",
                (id_entrega,),
            ).fetchone()
            return _entrega_da_linha(linha) if linha else None
        finally:
            conexao.close()

    def inserir(self, entrega):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                INSERT INTO Entregas (
                    descricao_carga, peso_kg, destinatario, endereco_destino,
                    entrega_prevista, entrega_realizada, status_entrega, viagem_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entrega.descricao_carga,
                    entrega.peso_kg,
                    entrega.destinatario,
                    entrega.endereco_destino,
                    _para_texto_datetime(entrega.entrega_prevista),
                    _para_texto_datetime(entrega.entrega_realizada),
                    entrega.status_entrega,
                    entrega.viagem_id,
                ),
            )
            conexao.commit()
            entrega.id = cursor.lastrowid
            return entrega.id
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def atualizar(self, entrega):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                UPDATE Entregas SET
                    viagem_id = ?, descricao_carga = ?, peso_kg = ?,
                    destinatario = ?, endereco_destino = ?, entrega_prevista = ?,
                    entrega_realizada = ?, status_entrega = ?
                WHERE id = ?
                """,
                (
                    entrega.viagem_id,
                    entrega.descricao_carga,
                    entrega.peso_kg,
                    entrega.destinatario,
                    entrega.endereco_destino,
                    _para_texto_datetime(entrega.entrega_prevista),
                    _para_texto_datetime(entrega.entrega_realizada),
                    entrega.status_entrega,
                    entrega.id,
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Entrega {entrega.id} não encontrada.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def excluir(self, id_entrega):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                "DELETE FROM Entregas WHERE id = ?", (id_entrega,)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Entrega {id_entrega} não encontrada.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
