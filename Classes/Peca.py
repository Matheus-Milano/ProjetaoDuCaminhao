"""
# -*- coding: utf-8 -*-
"""

"""Modelo representativo da entidade Peça usada em manutenções."""


class Peca:
    """Classe que mapeia a tabela 'Peças' do banco de dados."""

    def __init__(
        self,
        id_peca=None,
        manutencao_id=None,
        nome="",
        codigo="",
        quantidade=1,
        valor_unitario=0.0,
    ):
        """Inicializa uma peça utilizada em uma manutenção.

        Args:
            id_peca (int, optional): Identificador único (PK).
            manutencao_id (int): Chave estrangeira da Manutenção (FK).
            nome (str): Nome do componente/peça.
            codigo (str): Código de identificação do fabricante/peça.
            quantidade (int): Quantidade utilizada.
            valor_unitario (float): Preço unitário da peça.
        """
        self.id = id_peca
        self.manutencao_id = manutencao_id
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario

    def calcular_subtotal(self):
        """Calcula o valor total gasto nesta peça específica."""
        return self.quantidade * self.valor_unitario

    def __repr__(self):
        """Retorna uma representação textual legível da peça."""
        return f"<Peca id={self.id} nome='{self.nome}' qtd={self.quantidade}>"