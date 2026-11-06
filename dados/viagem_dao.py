import sqlite3
from datetime import datetime

from Banco.conector_do_banco import gerar_id_aleatorio, obter_conexao
from Classes.Viagem import Viagem


def _para_datetime(valor):
    return datetime.fromisoformat(valor) if valor else None


def _para_texto_datetime(valor):
    return valor.isoformat(sep=" ") if isinstance(valor, datetime) else valor


def _viagem_da_linha(linha):
    return Viagem(
        id_viagem=linha[0],
        caminhao_id=linha[1],
        motorista_id=linha[2],
        entrega_id=linha[3],
        data_chegada_prevista=_para_datetime(linha[4]),
        status_viagem=linha[5],
    )


class ViagemDAO:
    _colunas = """
        id, caminhao_id, motorista_id, entrega_id,
        data_chegada_prevista, status_viagem
    """

    def listar_todos(self):
        conexao = obter_conexao()
        try:
            linhas = conexao.execute(
                f"SELECT {self._colunas} FROM Viagens ORDER BY id ASC"
            ).fetchall()
            return [_viagem_da_linha(linha) for linha in linhas]
        finally:
            conexao.close()

    def buscar_por_id(self, id_viagem):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                f"SELECT {self._colunas} FROM Viagens WHERE id = ?",
                (id_viagem,),
            ).fetchone()
            return _viagem_da_linha(linha) if linha else None
        finally:
            conexao.close()

    def inserir(self, viagem):
        conexao = obter_conexao()
        try:
            conexao.execute("BEGIN IMMEDIATE")
            id_viagem = gerar_id_aleatorio(conexao, "Viagens")
            cursor = conexao.execute(
                """
                INSERT INTO Viagens (
                    id, data_chegada_prevista, status_viagem,
                    caminhao_id, motorista_id, entrega_id
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    id_viagem,
                    _para_texto_datetime(viagem.data_chegada_prevista),
                    viagem.status_viagem,
                    viagem.caminhao_id,
                    viagem.motorista_id,
                    viagem.entrega_id,
                ),
            )
            conexao.commit()
            viagem.id = id_viagem
            return viagem.id
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def atualizar(self, viagem):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                UPDATE Viagens SET
                    data_chegada_prevista = ?, status_viagem = ?,
                    caminhao_id = ?, motorista_id = ?, entrega_id = ?
                WHERE id = ?
                """,
                (
                    _para_texto_datetime(viagem.data_chegada_prevista),
                    viagem.status_viagem,
                    viagem.caminhao_id,
                    viagem.motorista_id,
                    viagem.entrega_id,
                    viagem.id,
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Viagem {viagem.id} não encontrada.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def excluir(self, id_viagem):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                "DELETE FROM Viagens WHERE id = ?", (id_viagem,)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Viagem {id_viagem} não encontrada.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
