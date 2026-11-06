from datetime import datetime


class Entrega:
    def __init__(
        self,
        id_entrega=None,
        viagem_id=None,
        descricao_carga="",
        peso_kg=0.0,
        destinatario="",
        endereco_destino="",
        entrega_prevista: datetime | None = None,
        entrega_realizada: datetime | None = None,
        status_entrega="Pendente",
    ):
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
        return (
            f"<Entrega id={self.id} destinatario='{self.destinatario}' "
            f"status='{self.status_entrega}'>"
        )
