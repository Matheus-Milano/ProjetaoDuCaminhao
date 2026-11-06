class Peca:
    def __init__(
        self,
        id_peca=None,
        manutencao_id=None,
        nome="",
        codigo="",
        quantidade=1,
        valor_unitario=0.0,
    ):
        self.id = id_peca
        self.manutencao_id = manutencao_id
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario

    def calcular_subtotal(self):
        return self.quantidade * self.valor_unitario

    def __repr__(self):
        return f"<Peca id={self.id} nome='{self.nome}' qtd={self.quantidade}>"
