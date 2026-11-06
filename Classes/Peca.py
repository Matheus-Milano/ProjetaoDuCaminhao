class Peca:
    def __init__(
        self,
        nome="",
        codigo="",
        quantidade=1,
        valor_unitario=0.0,
    ):
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario

    def calcular_subtotal(self):
        return self.quantidade * self.valor_unitario

    def __repr__(self):
        return f"<Peca id={self.codigo} nome='{self.nome}' qtd={self.quantidade}>"
