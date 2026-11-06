import hashlib
import hmac
import secrets
import sqlite3

from Banco.conector_do_banco import gerar_id_aleatorio, obter_conexao

class UsuarioDAO:
    def criar(self, nome: str, email: str, senha):
        salt = secrets.token_bytes(16)
        senha_hash = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), salt, 310_000
        )

        conexao = obter_conexao()
        try:
            conexao.execute("BEGIN IMMEDIATE")
            id_usuario = gerar_id_aleatorio(conexao, "Usuarios")
            conexao.execute(
                """
                INSERT INTO Usuarios (id, nome, email, senha_salt, senha_hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (id_usuario, nome, email, salt.hex(), senha_hash.hex()),
            )
            conexao.commit()
            return id_usuario
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
                "SELECT id, nome, email FROM Usuarios ORDER BY id ASC"
            ).fetchall()
        finally:
            conexao.close()

    def excluir(self, id_usuario):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                "DELETE FROM Usuarios WHERE id = ?", (id_usuario,)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Usuário {id_usuario} não encontrado.")
            conexao.commit()
            return cursor.rowcount
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def limpar(self):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute("DELETE FROM Usuarios")
            conexao.commit()
            return cursor.rowcount
        except sqlite3.Error:
            conexao.rollback()
            raise
        finally:
            conexao.close()
