"""
# -*- coding: utf-8 -*-
"""

"""Modelo representativo da entidade Entrega."""


class Entrega:
    """Classe que mapeia a tabela 'Entregas' do banco de dados."""

    def __init__(
        self,
        id_entrega=None,
        viagem_id=None,
        descricao_carga="",
        peso_kg=0.0,
        destinatario="",
        endereco_destino="",
        entrega_prevista=None,
        entrega_realizada=None,
        status_entrega="Pendente",
    ):
        """Inicializa um objeto de Entrega contendo os dados do frete.

        Args:
            id_entrega (int, optional): Identificador único (PK).
            viagem_id (int): Chave estrangeira da viagem associada (FK).
            descricao_carga (str): Descrição das mercadorias.
            peso_kg (float): Peso total da carga em quilogramas.
            destinatario (str): Nome da empresa ou pessoa receptora.
            endereco_destino (str): Endereço completo de entrega.
            entrega_prevista (datetime): Data/hora prevista.
            entrega_realizada (datetime, optional): Data/hora real de entrega.
            status_entrega (str): Status (ex: Pendente, Entregue, Atrasada).
        """
        self.id = id_entrega
        self.viagem_id = viagem_id
        self.descricao_carga = descricao_carga
        self.peso_kg = peso_kg
        self.destinatario = destinatario
        self.endereco_destino = endereco_destino
        self.entrega_prevista = entrega_prevista
        self.entrega_realizada = entrega_realizada
        self.status_entrega = status_entrega

    def __repr__(self):
        """Retorna uma representação textual da entrega."""
        return f"<Entrega id={self.id} destinatario='{self.destinatario}' status='{self.status_entrega}'>"
