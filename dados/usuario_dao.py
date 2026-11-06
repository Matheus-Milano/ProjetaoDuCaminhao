import hashlib
import hmac
import secrets
import sqlite3

from Banco.conector_do_banco import obter_conexao

class UsuarioDAO:
    def criar(self, nome: str, email, senha):
        salt = secrets.token_bytes(16)
        senha_hash = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), salt, 310_000
        )

        conexao = obter_conexao()
        try:
            conexao.execute(
                """
                INSERT INTO Usuarios (nome, email, senha_salt, senha_hash)
                VALUES (?, ?, ?, ?)
                """,
                (nome, email, salt.hex(), senha_hash.hex()),
            )
            conexao.commit()
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def autenticar(self, identificador, senha):
        conexao = obter_conexao()
        try:
            usuarios = conexao.execute(
                """
                SELECT senha_salt, senha_hash
                FROM Usuarios
                WHERE email = ? COLLATE NOCASE OR nome = ? COLLATE NOCASE
                """,
                (identificador, identificador),
            ).fetchall()
        finally:
            conexao.close()

        for senha_salt, senha_hash in usuarios:
            salt = bytes.fromhex(senha_salt)
            hash_esperado = bytes.fromhex(senha_hash)
            hash_informado = hashlib.pbkdf2_hmac(
                "sha256", senha.encode("utf-8"), salt, 310_000
            )
            if hmac.compare_digest(hash_informado, hash_esperado):
                return True
        return False

    def listar(self):
        conexao = obter_conexao()
        try:
            return conexao.execute(
                "SELECT id, nome, email FROM Usuarios ORDER BY nome COLLATE NOCASE"
            ).fetchall()
        finally:
            conexao.close()
