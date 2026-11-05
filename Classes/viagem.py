"""
# -*- coding: utf-8 -*-
"""

class Viagem:
    def __init__(
        self,
        id_viagem=None,
        caminhao_id=None,
        motorista_id=None,
        entrega_id=None,
        data_chegada_prevista=None,
        status_viagem="Agendada",
    ):
        """Inicializa um registro de viagem.
        Args:
            id_viagem (int, optional): Identificador único (PK).
            caminhao_id (int): Chave estrangeira do caminhão (FK).
            motorista_id (int): Chave estrangeira do motorista (FK).
            entrega_id (int, optional): Chave estrangeira da entrega (FK).
            data_chegada_prevista (datetime): Data e hora previstas para chegada.
            status_viagem (str): Status atual (ex: Em Trânsito, Concluída, Cancelada).
        """
        self.id = id_viagem
        self.caminhao_id = caminhao_id
        self.motorista_id = motorista_id
        self.entrega_id = entrega_id
        self.data_chegada_prevista = data_chegada_prevista
        self.status_viagem = status_viagem

    def __repr__(self):
        """Retorna uma representação textual da viagem."""
        return f"<Viagem id={self.id} caminhao_id={self.caminhao_id} status='{self.status_viagem}'>"