import sqlite3
from datetime import date

from Banco.conector_do_banco import obter_conexao
from Classes.Motorista import Motorista


def _para_data(valor):
    return date.fromisoformat(valor) if valor else None


def _para_texto_data(valor):
    return valor.isoformat() if isinstance(valor, date) else valor


def _motorista_da_linha(linha):
    return Motorista(
        id_motorista=linha[0],
        nome_completo=linha[1],
        cpf=linha[2],
        data_nascimento=_para_data(linha[3]),
        telefone=linha[4],
        cnh_numero=linha[5],
        cnh_categoria=linha[6],
        cnh_validade=_para_data(linha[7]),
        data_admissao=_para_data(linha[8]),
        status=linha[9],
    )


class MotoristaDAO:
    _colunas = """
        id, nome_completo, cpf, data_nascimento, telefone, cnh_numero,
        cnh_categoria, cnh_validade, data_admissao, status
    """

    def listar_todos(self):
        conexao = obter_conexao()
        try:
            linhas = conexao.execute(
                f"SELECT {self._colunas} FROM Motoristas ORDER BY nome_completo"
            ).fetchall()
            return [_motorista_da_linha(linha) for linha in linhas]
        finally:
            conexao.close()

    def buscar_por_id(self, id_motorista):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                f"SELECT {self._colunas} FROM Motoristas WHERE id = ?",
                (id_motorista,),
            ).fetchone()
            return _motorista_da_linha(linha) if linha else None
        finally:
            conexao.close()

    def inserir(self, motorista):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                INSERT INTO Motoristas (
                    nome_completo, cpf, data_nascimento, telefone, cnh_numero,
                    cnh_categoria, cnh_validade, data_admissao, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    motorista.nome_completo,
                    motorista.cpf,
                    _para_texto_data(motorista.data_nascimento),
                    motorista.telefone,
                    motorista.cnh_numero,
                    motorista.cnh_categoria,
                    _para_texto_data(motorista.cnh_validade),
                    _para_texto_data(motorista.data_admissao),
                    motorista.status,
                ),
            )
            conexao.commit()
            motorista.id = cursor.lastrowid
            return motorista.id
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def atualizar(self, motorista):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                UPDATE Motoristas SET
                    nome_completo = ?, cpf = ?, data_nascimento = ?, telefone = ?,
                    cnh_numero = ?, cnh_categoria = ?, cnh_validade = ?,
                    data_admissao = ?, status = ?
                WHERE id = ?
                """,
                (
                    motorista.nome_completo,
                    motorista.cpf,
                    _para_texto_data(motorista.data_nascimento),
                    motorista.telefone,
                    motorista.cnh_numero,
                    motorista.cnh_categoria,
                    _para_texto_data(motorista.cnh_validade),
                    _para_texto_data(motorista.data_admissao),
                    motorista.status,
                    motorista.id,
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Motorista {motorista.id} não encontrado.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def excluir(self, id_motorista):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                "DELETE FROM Motoristas WHERE id = ?", (id_motorista,)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Motorista {id_motorista} não encontrado.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
