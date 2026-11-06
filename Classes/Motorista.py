from datetime import date


class Motorista:
    def __init__(
        self,
        id_motorista=None,
        nome_completo="",
        cpf="",
        data_nascimento: date | None = None,
        telefone="",
        cnh_numero="",
        cnh_categoria="",
        cnh_validade: date | None = None,
        data_admissao: date | None = None,
        status="Ativo",
    ):
        self.id = id_motorista
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.cnh_numero = cnh_numero
        self.cnh_categoria = cnh_categoria
        self.cnh_validade = cnh_validade
        self.data_admissao = data_admissao
        self.status = status

    def __repr__(self):
        return f"<Motorista id={self.id} nome='{self.nome_completo}'>"
