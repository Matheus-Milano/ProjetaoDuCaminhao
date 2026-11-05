import sqlite3
import os

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(DIRETORIO_ATUAL, "banco.db")

""" 
nome = "Nathan"
nome2 = "Bulacha"
cursor.execute("INSERT INTO alunos (nome) VALUES (?);", (nome,))
cursor.execute("INSERT INTO alunos (nome) VALUES (?);", (nome2,))


cursor.execute("INSERT INTO pessoa (nome) VALUES (?);", (nome,))
cursor.execute("INSERT INTO pessoa (nome) VALUES (?);", (nome2,))

print(f"Aluno {nome} cadastrado!")
print(f"Aluno {nome2} cadastrado!")
"""


conexao = sqlite3.connect(CAMINHO_BANCO)
cursor = conexao.cursor()

conexao.commit()
conexao.close()

