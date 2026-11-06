"""
# -*- coding: utf-8 -*-
"""

class Caminhao:
    def __init__(
        self,
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
        id=None,
    ):
        self.id = id
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
        return f"<Caminhao id={self.id} placa='{self.placa}' modelo='{self.modelo}'>"