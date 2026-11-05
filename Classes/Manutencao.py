"""
# -*- coding: utf-8 -*-
"""

"""Modelo representativo da entidade Manutenção."""


class Manutencao:
    """Classe que mapeia a tabela 'Manutenções' do banco de dados."""

    def __init__(
        self,
        id_manutencao=None,
        caminhao_id=None,
        data_manutencao=None,
        tipo="Preventiva",
        descricao="",
        km_manutencao=0,
        custo_total=0.0,
    ):
        """Inicializa um registro de manutenção.

        Args:
            id_manutencao (int, optional): Identificador único (PK).
            caminhao_id (int): Chave estrangeira do caminhão (FK).
            data_manutencao (date): Data da realização da manutenção.
            tipo (str): Tipo de manutenção (Preventiva / Corretiva).
            descricao (str): Detalhes dos serviços efetuados.
            km_manutencao (int): Odômetro no momento da manutenção.
            custo_total (float): Custo total acumulado.
        """
        self.id = id_manutencao
        self.caminhao_id = caminhao_id
        self.data_manutencao = data_manutencao
        self.tipo = tipo
        self.descricao = descricao
        self.km_manutencao = km_manutencao
        self.custo_total = custo_total

    def __repr__(self):
        """Retorna uma representação textual legível da manutenção."""
        return f"<Manutencao id={self.id} caminhao_id={self.caminhao_id} tipo='{self.tipo}'>"