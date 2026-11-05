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
        """Inicializa um objeto Caminhao com os atributos do DER.

        Args:
            id_caminhao (int, optional): Identificador único (PK).
            placa (str): Placa do caminhão.
            renavam (str): Código RENAVAM.
            marca (str): Marca do veículo.
            modelo (str): Modelo do veículo.
            ano_fabricacao (int): Ano de fabricação.
            tipo_carroceria (str): Tipo de baú/carroceria.
            carga_maxima_kg (float): Capacidade máxima em kg.
            km_atual (int): Quilometragem atual.
            status (str): Status operacional (ex: Disponível, Em Rota, Manutenção).
            motorista_responsavel_id (int, optional): FK para Motoristas.
        """
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