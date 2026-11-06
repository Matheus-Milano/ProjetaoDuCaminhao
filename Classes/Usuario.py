class Usuario:
    def __init__(
        self,
        id_usuario=None,
        nome="",
        email="",
        senha_salt="",
        senha_hash="",
    ):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.senha_salt = senha_salt
        self.senha_hash = senha_hash

    def __repr__(self):
        return f"<Usuario id={self.id} email='{self.email}'>"
