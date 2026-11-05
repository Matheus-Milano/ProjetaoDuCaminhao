"""
# -*- coding: utf-8 -*-
"""

"""Modelo representativo da entidade Motorista."""


class Motorista:
    """Classe que mapeia a tabela 'Motoristas' do banco de dados."""

    def __init__(
        self,
        id_motorista=None,
        perfil_id=None,
        nome_completo="",
        cpf="",
        data_nascimento=None,
        telefone="",
        cnh_numero="",
        cnh_categoria="",
        cnh_validade=None,
        data_admissao=None,
        status="Ativo",
    ):
        """Inicializa um objeto de Motorista.

        Args:
            id_motorista (int, optional): Identificador único (PK).
            perfil_id (int): Chave estrangeira para a tabela Perfis (FK).
            nome_completo (str): Nome completo do motorista.
            cpf (str): Número do CPF (11 caracteres).
            data_nascimento (date): Data de nascimento.
            telefone (str): Telefone de contato.
            cnh_numero (str): Número da CNH.
            cnh_categoria (str): Categoria da CNH (ex: C, D, E).
            cnh_validade (date): Data de validade da CNH.
            data_admissao (date): Data de contratação do motorista.
            status (str): Status atual (ex: Ativo, Em Viagem, Inativo).
        """
        self.id = id_motorista
        self.perfil_id = perfil_id
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.cnh_numero = cnh_numero
        self.cnh_categoria = cnh_categoria
        self.cnh_validade = cnh_validade
        self.data_admissao = data_admissao
        self.status = status

    def __repr__(self):
        """Retorna uma representação textual legível do motorista."""
        return f"<Motorista id={self.id} nome='{self.nome_completo}'>"