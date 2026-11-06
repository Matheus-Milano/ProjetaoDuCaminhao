
import os
import secrets
import sqlite3

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(DIRETORIO_ATUAL, "banco.db")

TABELAS_COM_ID = {
    "Usuarios",
    "Motoristas",
    "Caminhoes",
    "Viagens",
    "Entregas",
    "PecasReposicao",
}
ID_MAXIMO = 99_999


def obter_conexao():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao


def gerar_id_aleatorio(conexao, tabela):
    if tabela not in TABELAS_COM_ID:
        raise ValueError(f"Tabela sem geração de ID configurada: {tabela}")

    quantidade = conexao.execute(
        f"SELECT COUNT(*) FROM {tabela} WHERE id BETWEEN 1 AND ?",
        (ID_MAXIMO,),
    ).fetchone()[0]
    if quantidade >= ID_MAXIMO:
        raise RuntimeError(f"Todos os IDs de 1 a {ID_MAXIMO} estão ocupados em {tabela}.")

    while True:
        id_aleatorio = secrets.randbelow(ID_MAXIMO) + 1
        existente = conexao.execute(
            f"SELECT 1 FROM {tabela} WHERE id = ?", (id_aleatorio,)
        ).fetchone()
        if existente is None:
            return id_aleatorio