"""
# -*- coding: utf-8 -*-
"""

from Banco.conector_do_banco import gerar_id_aleatorio, obter_conexao
from Classes.Caminhao import Caminhao

class CaminhaoDAO:
    def buscar_por_id(self, id_caminhao):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                """
                SELECT id, placa, renavam, marca, modelo, ano_fabricacao,
                       tipo_carroceria, carga_maxima_kg, km_atual, status,
                       motorista_responsavel_id
                FROM Caminhoes
                WHERE id = ?
                """,
                (id_caminhao,),
            ).fetchone()
        finally:
            conexao.close()

        if linha is None:
            return None

        return Caminhao(
            id_caminhao=linha[0],
            placa=linha[1],
            renavam=linha[2],
            marca=linha[3],
            modelo=linha[4],
            ano_fabricacao=linha[5],
            tipo_carroceria=linha[6],
            carga_maxima_kg=linha[7],
            km_atual=linha[8],
            status=linha[9],
            motorista_responsavel_id=linha[10],
        )

    def listar_todos(self):
        """Retorna uma lista de objetos Caminhao do banco."""
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, placa, renavam, marca, modelo, ano_fabricacao, tipo_carroceria, carga_maxima_kg, km_atual, status, motorista_responsavel_id FROM Caminhoes ORDER BY id ASC"
        )
        linhas = cursor.fetchall()
        conexao.close()
        caminhoes = []
        for l in linhas:
            caminhoes.append(
                Caminhao(
                    id_caminhao=l[0],
                    placa=l[1],
                    renavam=l[2],
                    marca=l[3],
                    modelo=l[4],
                    ano_fabricacao=l[5],
                    tipo_carroceria=l[6],
                    carga_maxima_kg=l[7],
                    km_atual=l[8],
                    status=l[9],
                    motorista_responsavel_id=l[10],
                )
            )
        return caminhoes

    def inserir(self, caminhao: Caminhao):
        conexao = obter_conexao()
        try:
            conexao.execute("BEGIN IMMEDIATE")
            id_caminhao = gerar_id_aleatorio(conexao, "Caminhoes")
            cursor = conexao.execute(
                """
                INSERT INTO Caminhoes (
                    id, placa, renavam, marca, modelo, ano_fabricacao,
                    tipo_carroceria, carga_maxima_kg, km_atual, status,
                    motorista_responsavel_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_caminhao,
                    caminhao.placa,
                    caminhao.renavam,
                    caminhao.marca,
                    caminhao.modelo,
                    caminhao.ano_fabricacao,
                    caminhao.tipo_carroceria,
                    caminhao.carga_maxima_kg,
                    caminhao.km_atual,
                    caminhao.status,
                    caminhao.motorista_responsavel_id,
                ),
            )
            conexao.commit()
            caminhao.id = id_caminhao
            return caminhao.id
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def excluir(self, id_caminhao: Caminhao.id_caminhao):
        conexao = obter_conexao()
        try:
            conexao.execute("DELETE FROM Caminhoes WHERE id = ?", (id_caminhao,))
            conexao.commit()
        finally:
            conexao.close()

    def limpar(self):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute("DELETE FROM Caminhoes")
            conexao.commit()
            return cursor.rowcount
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def atualizar(self, caminhao: Caminhao):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                """
                UPDATE Caminhoes
                SET placa = ?, renavam = ?, marca = ?, modelo = ?,
                    ano_fabricacao = ?, tipo_carroceria = ?,
                    carga_maxima_kg = ?, km_atual = ?, status = ?
                WHERE id = ?
                """,
                (
                    caminhao.placa,
                    caminhao.renavam,
                    caminhao.marca,
                    caminhao.modelo,
                    caminhao.ano_fabricacao,
                    caminhao.tipo_carroceria,
                    caminhao.carga_maxima_kg,
                    caminhao.km_atual,
                    caminhao.status,
                    caminhao.id,
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Caminhão {caminhao.id} não encontrado.")
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()