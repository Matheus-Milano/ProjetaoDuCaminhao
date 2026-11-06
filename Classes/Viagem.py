from datetime import datetime


class Viagem:
    def __init__(
        self,
        id_viagem=None,
        caminhao_id=None,
        motorista_id=None,
        entrega_id=None,
        data_chegada_prevista: datetime | None = None,
        status_viagem="Agendada",
    ):
        self.id = id_viagem
        self.caminhao_id = caminhao_id
        self.motorista_id = motorista_id
        self.entrega_id = entrega_id
        self.data_chegada_prevista = data_chegada_prevista
        self.status_viagem = status_viagem

    def __repr__(self):
        return (
            f"<Viagem id={self.id} caminhao_id={self.caminhao_id} "
            f"status='{self.status_viagem}'>"
        )
