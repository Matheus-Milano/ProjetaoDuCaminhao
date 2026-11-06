import sqlite3
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GObject, Gtk
from Banco.criar_bancos import inicializar_banco
from Classes.Caminhao import Caminhao
from dados.caminhao_dao import CaminhaoDAO
from dados.usuario_dao import UsuarioDAO


class SistemaFrotion:
    def __init__(self):
        inicializar_banco()

        self.caminhao_dao = CaminhaoDAO()

        self.builder_login = Gtk.Builder()
        self.builder_login.add_from_file("Telas/login.glade")

        self.win_login = self.builder_login.get_object("window_login")
        self.txt_usuario = self.builder_login.get_object("txt_usuario")
        self.txt_senha = self.builder_login.get_object("txt_senha")
        self.btn_entrar = self.builder_login.get_object("btn_entrar")
        self.btn_criar_usuario = self.builder_login.get_object("btn_criar_usuario")
        self.lbl_erro = self.builder_login.get_object("lbl_erro_login")

        if self.lbl_erro:
            self.lbl_erro.set_visible(False)

        self.btn_entrar.connect("clicked", self.autenticar)
        self.btn_criar_usuario.connect("clicked", self.abrir_tela_criar_usuario)
        self.win_login.connect("destroy", Gtk.main_quit)

        self.win_login.show_all()

    def autenticar(self, widget):
        usuario = self.txt_usuario.get_text().strip()
        senha = self.txt_senha.get_text()

        if not usuario or not senha:
            self.lbl_erro.set_text("⚠️ Informe usuário e senha para acessar.")
            self.lbl_erro.set_visible(True)
            return

        try:
            credenciais_validas = UsuarioDAO().autenticar(usuario, senha)
        except sqlite3.Error as erro:
            print(f"Erro ao validar usuário: {erro}")
            self.lbl_erro.set_text("⚠️ Não foi possível validar o acesso.")
            self.lbl_erro.set_visible(True)
            return

        if not credenciais_validas:
            self.lbl_erro.set_text("⚠️ Usuário ou senha inválidos.")
            self.lbl_erro.set_visible(True)
            return

        self.lbl_erro.set_visible(False)
        self.win_login.hide()
        self.abrir_tela_principal()

    def abrir_tela_principal(self):
        self.builder_main = Gtk.Builder()
        self.builder_main.add_from_file("Telas/tela_principal.glade")

        self.win_main = self.builder_main.get_object("window_principal")
        self.treeview = self.builder_main.get_object("treeview_caminhoes")
        self.btn_novo = self.builder_main.get_object("btn_novo_caminhao")
        self.btn_editar = self.builder_main.get_object("btn_editar_caminhao")
        self.btn_excluir = self.builder_main.get_object("btn_excluir_caminhao")
        self.btn_limpar_banco = self.builder_main.get_object("btn_limpar_banco")
        self.btn_catalogo = self.builder_main.get_object("btn_ir_catalogo")
        self.btn_listar_usuarios = self.builder_main.get_object("btn_listar_usuarios")

        self.btn_novo.connect("clicked", self.cadastrar_caminhao_exemplo)
        self.btn_editar.connect("clicked", self.editar_caminhao_selecionado)
        self.btn_excluir.connect("clicked", self.excluir_caminhao_selecionado)
        self.btn_limpar_banco.connect("clicked", self.limpar_banco_completo)
        self.btn_catalogo.connect("clicked", self.abrir_catalogo_pecas)
        self.btn_listar_usuarios.connect("clicked", self.abrir_tela_listar_usuarios)
        self.win_main.connect("destroy", Gtk.main_quit)

        self.configurar_tabela_caminhoes()
        self.atualizar_tabela_caminhoes()

        self.win_main.show_all()

    def configurar_tabela_caminhoes(self):
        self.store_caminhoes = Gtk.ListStore(
            GObject.TYPE_INT64, str, str, str, str
        )
        self.treeview.set_model(self.store_caminhoes)
        self.configurar_colunas(
            self.treeview, ["ID", "Placa", "Marca", "Modelo", "Status"]
        )

    @staticmethod
    def configurar_colunas(treeview, titulos):
        for indice, titulo in enumerate(titulos):
            renderer = Gtk.CellRendererText()
            coluna = Gtk.TreeViewColumn(titulo, renderer, text=indice)
            treeview.append_column(coluna)

    def atualizar_tabela_caminhoes(self):
        self.store_caminhoes.clear()
        caminhoes = self.caminhao_dao.listar_todos()

        for c in caminhoes:
            self.store_caminhoes.append(
                [c.id, c.placa, c.marca, c.modelo, c.status]
            )

    def cadastrar_caminhao_exemplo(self, widget):
        import random

        placa_random = f"ABC-{random.randint(1000, 9999)}"
        renavam_random = str(random.randint(10000000000, 99999999999))

        novo_caminhao = Caminhao(
            placa=placa_random,
            renavam=renavam_random,
            marca="Volvo",
            modelo="FH 540",
            ano_fabricacao=2024,
            tipo_carroceria="Baú",
            carga_maxima_kg=40000.0,
            km_atual=10000,
            status="Disponível",
        )

        self.caminhao_dao.inserir(novo_caminhao)
        self.atualizar_tabela_caminhoes()

    def excluir_caminhao_selecionado(self, widget):
        selecao = self.treeview.get_selection()
        modelo_store, arvore_iter = selecao.get_selected()

        if arvore_iter:
            caminhao_id = modelo_store[arvore_iter][0]
            self.caminhao_dao.excluir(caminhao_id)
            self.atualizar_tabela_caminhoes()

    def limpar_banco_completo(self, widget):
        if not self._confirmar_acao(
            "Isso excluirá todos os caminhões. Viagens vinculadas e suas "
            "entregas também poderão ser excluídas pela relação do banco. "
            "Usuários, motoristas e peças não serão removidos. Deseja continuar?",
            self.win_main,
        ):
            return

        try:
            quantidade_caminhoes = self.caminhao_dao.limpar()
            self.atualizar_tabela_caminhoes()
        except sqlite3.Error as erro:
            print(f"Erro ao limpar os caminhões: {erro}")
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "Não foi possível limpar os caminhões.",
                self.win_main,
            )
            return

        self._mostrar_mensagem(
            Gtk.MessageType.INFO,
            f"{quantidade_caminhoes} caminhão(ões) removido(s).",
            self.win_main,
        )

    def editar_caminhao_selecionado(self, widget):
        selecao = self.treeview.get_selection()
        modelo, arvore_iter = selecao.get_selected()
        if arvore_iter is None:
            self._mostrar_mensagem(
                Gtk.MessageType.WARNING,
                "Selecione um caminhão para editar.",
                self.win_main,
            )
            return

        caminhao_id = modelo[arvore_iter][0]
        caminhao = self.caminhao_dao.buscar_por_id(caminhao_id)
        if caminhao is None:
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "O caminhão selecionado não foi encontrado no banco.",
                self.win_main,
            )
            self.atualizar_tabela_caminhoes()
            return

        builder = Gtk.Builder()
        builder.add_from_file("Telas/editar_caminhao.glade")
        dialogo = builder.get_object("dialog_editar_caminhao")
        dialogo.set_transient_for(self.win_main)

        campos = {
            "txt_placa": caminhao.placa,
            "txt_renavam": caminhao.renavam,
            "txt_marca": caminhao.marca,
            "txt_modelo": caminhao.modelo,
            "txt_ano_fabricacao": str(caminhao.ano_fabricacao),
            "txt_tipo_carroceria": caminhao.tipo_carroceria,
            "txt_carga_maxima_kg": str(caminhao.carga_maxima_kg),
            "txt_km_atual": str(caminhao.km_atual),
            "txt_status": caminhao.status,
        }
        entradas = {nome: builder.get_object(nome) for nome in campos}
        for nome, valor in campos.items():
            entradas[nome].set_text(valor)

        if dialogo.run() != Gtk.ResponseType.OK:
            dialogo.destroy()
            return

        try:
            caminhao.placa = entradas["txt_placa"].get_text().strip()
            caminhao.renavam = entradas["txt_renavam"].get_text().strip()
            caminhao.marca = entradas["txt_marca"].get_text().strip()
            caminhao.modelo = entradas["txt_modelo"].get_text().strip()
            caminhao.ano_fabricacao = int(
                entradas["txt_ano_fabricacao"].get_text().strip()
            )
            caminhao.tipo_carroceria = (
                entradas["txt_tipo_carroceria"].get_text().strip()
            )
            caminhao.carga_maxima_kg = float(
                entradas["txt_carga_maxima_kg"].get_text().strip().replace(",", ".")
            )
            caminhao.km_atual = int(
                entradas["txt_km_atual"].get_text().strip()
            )
            caminhao.status = entradas["txt_status"].get_text().strip()

            if not all(
                (
                    caminhao.placa,
                    caminhao.renavam,
                    caminhao.marca,
                    caminhao.modelo,
                    caminhao.tipo_carroceria,
                    caminhao.status,
                )
            ):
                raise ValueError("Preencha todos os campos.")
            if caminhao.ano_fabricacao <= 0 or caminhao.km_atual < 0:
                raise ValueError("Ano e quilometragem devem ser valores válidos.")
            if caminhao.carga_maxima_kg <= 0:
                raise ValueError("A carga máxima deve ser maior que zero.")

            self.caminhao_dao.atualizar(caminhao)
        except ValueError as erro:
            self._mostrar_mensagem(
                Gtk.MessageType.WARNING, str(erro), self.win_main
            )
            dialogo.destroy()
            return
        except sqlite3.IntegrityError:
            self._mostrar_mensagem(
                Gtk.MessageType.WARNING,
                "Já existe um caminhão com essa placa ou RENAVAM.",
                self.win_main,
            )
            dialogo.destroy()
            return
        except sqlite3.Error as erro:
            print(f"Erro ao atualizar caminhão: {erro}")
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "Não foi possível salvar as alterações do caminhão.",
                self.win_main,
            )
            dialogo.destroy()
            return

        dialogo.destroy()
        self.atualizar_tabela_caminhoes()

    def abrir_catalogo_pecas(self, widget):
        builder_pecas = Gtk.Builder()
        builder_pecas.add_from_file("Telas/catalogo_pecas.glade")
        win_pecas = builder_pecas.get_object("window_pecas")
        win_pecas.show_all()

    def abrir_tela_listar_usuarios(self, widget):
        self.builder_listar_usuarios = Gtk.Builder()
        self.builder_listar_usuarios.add_from_file("Telas/listar_usuarios.glade")

        self.win_listar_usuarios = self.builder_listar_usuarios.get_object(
            "window_listar_usuarios"
        )
        self.treeview_usuarios = self.builder_listar_usuarios.get_object(
            "treeview_usuarios"
        )
        self.btn_excluir_usuario = self.builder_listar_usuarios.get_object(
            "btn_excluir_usuario"
        )
        self.btn_limpar_usuarios = self.builder_listar_usuarios.get_object(
            "btn_limpar_usuarios"
        )
        self.win_listar_usuarios.set_transient_for(self.win_main)

        self.store_usuarios = Gtk.ListStore(GObject.TYPE_INT64, str, str)
        self.treeview_usuarios.set_model(self.store_usuarios)
        self.configurar_colunas(self.treeview_usuarios, ("ID", "Nome", "E-mail"))
        self.btn_excluir_usuario.connect(
            "clicked", self.excluir_usuario_selecionado
        )
        self.btn_limpar_usuarios.connect("clicked", self.limpar_usuarios)

        try:
            self._atualizar_lista_usuarios()
        except sqlite3.Error as erro:
            print(f"Erro ao listar usuários: {erro}")
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "Não foi possível carregar a lista de usuários.",
                self.win_listar_usuarios,
            )
            self.win_listar_usuarios.destroy()
            return

        self.win_listar_usuarios.show_all()

    def _atualizar_lista_usuarios(self):
        self.store_usuarios.clear()
        for usuario in UsuarioDAO().listar():
            self.store_usuarios.append(usuario)

    def excluir_usuario_selecionado(self, widget):
        modelo, arvore_iter = self.treeview_usuarios.get_selection().get_selected()
        if arvore_iter is None:
            self._mostrar_mensagem(
                Gtk.MessageType.WARNING,
                "Selecione um usuário para excluir.",
                self.win_listar_usuarios,
            )
            return

        id_usuario = modelo[arvore_iter][0]
        if not self._confirmar_acao(
            "Deseja excluir o usuário selecionado?", self.win_listar_usuarios
        ):
            return

        try:
            UsuarioDAO().excluir(id_usuario)
            self._atualizar_lista_usuarios()
        except (ValueError, sqlite3.Error) as erro:
            print(f"Erro ao excluir usuário: {erro}")
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "Não foi possível excluir o usuário selecionado.",
                self.win_listar_usuarios,
            )
            return

        self._mostrar_mensagem(
            Gtk.MessageType.INFO,
            "Usuário excluído com sucesso.",
            self.win_listar_usuarios,
        )

    def limpar_usuarios(self, widget):
        try:
            quantidade = len(UsuarioDAO().listar())
        except sqlite3.Error as erro:
            print(f"Erro ao consultar usuários: {erro}")
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "Não foi possível consultar os usuários cadastrados.",
                self.win_listar_usuarios,
            )
            return

        if quantidade == 0:
            self._mostrar_mensagem(
                Gtk.MessageType.INFO,
                "Não há usuários cadastrados.",
                self.win_listar_usuarios,
            )
            return

        if not self._confirmar_acao(
            f"Isso excluirá todos os {quantidade} usuário(s). Deseja continuar?",
            self.win_listar_usuarios,
        ):
            return

        try:
            removidos = UsuarioDAO().limpar()
            self._atualizar_lista_usuarios()
        except sqlite3.Error as erro:
            print(f"Erro ao limpar usuários: {erro}")
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "Não foi possível excluir os usuários.",
                self.win_listar_usuarios,
            )
            return

        self._mostrar_mensagem(
            Gtk.MessageType.INFO,
            f"{removidos} usuário(s) excluído(s).",
            self.win_listar_usuarios,
        )

    def abrir_tela_criar_usuario(self, widget):
        self.builder_usuario = Gtk.Builder()
        self.builder_usuario.add_from_file("Telas/criar_usuario.glade")

        self.win_criar_usuario = self.builder_usuario.get_object(
            "window_criar_usuario"
        )
        self.txt_novo_nome = self.builder_usuario.get_object("txt_novo_nome")
        self.txt_novo_email = self.builder_usuario.get_object("txt_novo_email")
        self.txt_nova_senha = self.builder_usuario.get_object("txt_nova_senha")
        self.btn_salvar_usuario = self.builder_usuario.get_object(
            "btn_salvar_usuario"
        )

        self.win_criar_usuario.set_transient_for(self.win_login)
        self.btn_salvar_usuario.connect("clicked", self.salvar_usuario)
        self.win_criar_usuario.show_all()

    def salvar_usuario(self, widget):
        nome = self.txt_novo_nome.get_text().strip()
        email = self.txt_novo_email.get_text().strip()
        senha = self.txt_nova_senha.get_text()

        if not nome or not email or not senha:
            self._mostrar_mensagem(
                Gtk.MessageType.WARNING,
                "Preencha todos os campos.",
                self.win_criar_usuario,
            )
            return

        partes_email = email.split("@")
        if len(partes_email) != 2 or not partes_email[0] or "." not in partes_email[1]:
            self._mostrar_mensagem(
                Gtk.MessageType.WARNING,
                "Informe um e-mail válido.",
                self.win_criar_usuario,
            )
            return

        try:
            UsuarioDAO().criar(nome, email, senha)
        except sqlite3.IntegrityError:
            self._mostrar_mensagem(
                Gtk.MessageType.WARNING,
                "Já existe um usuário com esse e-mail.",
                self.win_criar_usuario,
            )
            return
        except sqlite3.Error as erro:
            print(f"Erro ao criar usuário: {erro}")
            self._mostrar_mensagem(
                Gtk.MessageType.ERROR,
                "Não foi possível salvar o usuário.",
                self.win_criar_usuario,
            )
            return

        self._mostrar_mensagem(
            Gtk.MessageType.INFO,
            "Usuário criado com sucesso.",
            self.win_criar_usuario,
        )
        self.win_criar_usuario.destroy()

    def _mostrar_mensagem(self, tipo, mensagem, janela_pai):
        dialogo = Gtk.MessageDialog(
            transient_for=janela_pai,
            flags=Gtk.DialogFlags.MODAL,
            message_type=tipo,
            buttons=Gtk.ButtonsType.OK,
            text=mensagem,
        )
        dialogo.run()
        dialogo.destroy()

    @staticmethod
    def _confirmar_acao(mensagem, janela_pai):
        dialogo = Gtk.MessageDialog(
            transient_for=janela_pai,
            flags=Gtk.DialogFlags.MODAL,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=mensagem,
        )
        resposta = dialogo.run()
        dialogo.destroy()
        return resposta == Gtk.ResponseType.YES

if __name__ == "__main__":
    app = SistemaFrotion()
    Gtk.main()