"""
# -*- coding: utf-8 -*-
"""

class Caminhao:
    def __init__(
        self,
        id_caminhao=None,
        placa="",
        renavam="",
        marca="",
        modelo="",
        ano_fabricacao=0,
        tipo_carroceria="",
        carga_maxima_kg=0.0,
        km_atual=0,
        status="Disponível",
        motorista_responsavel_id=None,
    ):
        """Inicializa um objeto Caminhao com os atributos do DER."""
        self.id = id_caminhao
        self.placa = placa
        self.renavam = renavam
        self.marca = marca
        self.modelo = modelo
        self.ano_fabricacao = ano_fabricacao
        self.tipo_carroceria = tipo_carroceria
        self.carga_maxima_kg = carga_maxima_kg
        self.km_atual = km_atual
        self.status = status
        self.motorista_responsavel_id = motorista_responsavel_id

    def __repr__(self):
        """Retorna uma representação textual legível do caminhão."""
        return f"<Caminhao id={self.id} placa='{self.placa}' modelo='{self.modelo}'>"