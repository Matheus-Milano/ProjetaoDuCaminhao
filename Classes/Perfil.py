"""
# -*- coding: utf-8 -*-
"""

class Perfil:
    def __init__(self, id_perfil=None, nome="", descricao="", nivel_acesso=1):
        """Inicializa um novo objeto de Perfil com seus atributos.

        Args:
            id_perfil (int, optional): Identificador único (PK).
            nome (str): Nome do perfil (ex: Administrador, Motorista).
            descricao (str): Descrição das permissões do perfil.
            nivel_acesso (int): Nível numérico de permissão.
        """
        self.id = id_perfil
        self.nome = nome
        self.descricao = descricao
        self.nivel_acesso = nivel_acesso

    def __repr__(self):
        """Retorna uma representação textual legível do objeto."""
        return f"<Perfil id={self.id} nome='{self.nome}'>"