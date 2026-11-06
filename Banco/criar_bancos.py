import sqlite3

from Banco.conector_do_banco import CAMINHO_BANCO

def inicializar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = OFF;")

    colunas_motoristas = {
        linha[1] for linha in cursor.execute("PRAGMA table_info(Motoristas)")
    }
    if "perfil_id" in colunas_motoristas:
        cursor.execute("""
            CREATE TABLE Motoristas_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo VARCHAR(100) NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                data_nascimento DATE NOT NULL,
                telefone VARCHAR(15) NOT NULL,
                cnh_numero VARCHAR(11) NOT NULL UNIQUE,
                cnh_categoria VARCHAR(2) NOT NULL,
                cnh_validade DATE NOT NULL,
                data_admissao DATE NOT NULL,
                status VARCHAR(20) NOT NULL
            );
        """)
        if colunas_motoristas:
            cursor.execute("""
                INSERT INTO Motoristas_nova (
                    id, nome_completo, cpf, data_nascimento, telefone,
                    cnh_numero, cnh_categoria, cnh_validade, data_admissao, status
                )
                SELECT id, nome_completo, cpf, data_nascimento, telefone,
                       cnh_numero, cnh_categoria, cnh_validade, data_admissao, status
                FROM Motoristas;
            """)
            cursor.execute("DROP TABLE Motoristas;")
        cursor.execute("ALTER TABLE Motoristas_nova RENAME TO Motoristas;")

    cursor.execute("DROP TABLE IF EXISTS Perfis;")

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(254) NOT NULL COLLATE NOCASE UNIQUE,
            senha_salt TEXT NOT NULL,
            senha_hash TEXT NOT NULL
        );
    """)

    # Tabela de motoristas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Motoristas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo VARCHAR(100) NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            data_nascimento DATE NOT NULL,
            telefone VARCHAR(15) NOT NULL,
            cnh_numero VARCHAR(11) NOT NULL UNIQUE,
            cnh_categoria VARCHAR(2) NOT NULL,
            cnh_validade DATE NOT NULL,
            data_admissao DATE NOT NULL,
            status VARCHAR(20) NOT NULL
        );
    """)

    # Tabela de caminhões
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Caminhoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa VARCHAR(8) NOT NULL UNIQUE,
            renavam CHAR(11) NOT NULL UNIQUE,
            marca VaRCHAR(30) NOT NULL,
            modelo VARCHAR(50) NOT NULL,
            ano_fabricacao INT NOT NULL,
            tipo_carroceria VARCHAR(30) NOT NULL,
            carga_maxima_kg DECIMAL(10, 2) NOT NULL,
            km_atual DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) NOT NULL,
            motorista_responsavel_id INTEGER,

            -- Definindo a chave estrangeira para o motorista responsável
            FOREIGN KEY (motorista_responsavel_id) REFERENCES Motoristas(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """)

    # Tabela de viagens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Viagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_chegada_prevista DATETIME NOT NULL,
            status_viagem VARCHAR(20) NOT NULL,
            caminhao_id INTEGER NOT NULL,
            motorista_id INTEGER NOT NULL,
            entrega_id INTEGER,

            -- Definindo as chaves estrangeiras para caminhão
            FOREIGN KEY (caminhao_id) REFERENCES Caminhoes(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            
            -- Definindo as chaves estrangeiras para motorista
            FOREIGN KEY (motorista_id) REFERENCES Motoristas(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,

            -- Definindo as chaves estrangeiras para entrega
            FOREIGN KEY (entrega_id) REFERENCES Entregas(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """)

    colunas_viagens = {
        linha[1]: linha for linha in cursor.execute("PRAGMA table_info(Viagens)")
    }
    if colunas_viagens["entrega_id"][3]:
        cursor.execute("""
            CREATE TABLE Viagens_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_chegada_prevista DATETIME NOT NULL,
                status_viagem VARCHAR(20) NOT NULL,
                caminhao_id INTEGER NOT NULL,
                motorista_id INTEGER NOT NULL,
                entrega_id INTEGER,
                FOREIGN KEY (caminhao_id) REFERENCES Caminhoes(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (motorista_id) REFERENCES Motoristas(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (entrega_id) REFERENCES Entregas(id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            );
        """)
        cursor.execute("""
            INSERT INTO Viagens_nova (
                id, data_chegada_prevista, status_viagem,
                caminhao_id, motorista_id, entrega_id
            )
            SELECT id, data_chegada_prevista, status_viagem,
                   caminhao_id, motorista_id, entrega_id
            FROM Viagens;
        """)
        cursor.execute("DROP TABLE Viagens;")
        cursor.execute("ALTER TABLE Viagens_nova RENAME TO Viagens;")

    # Tabela de entregas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Entregas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao_carga VARCHAR(100) NOT NULL,
            peso_kg DECIMAL(10, 2) NOT NULL,
            destinatario VARCHAR(100) NOT NULL,
            endereco_destino VARCHAR(200) NOT NULL,
            entrega_prevista DATETIME NOT NULL,
            entrega_realizada DATETIME,
            status_entrega VARCHAR(20) NOT NULL,
            viagem_id INTEGER NOT NULL,

            -- Definindo a chave estrangeira para viagem
            FOREIGN KEY (viagem_id) REFERENCES Viagens(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """)

    # Tabela de peças de reposição
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PecasReposicao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(60) NOT NULL,
            codigo VARCHAR(20),
            quantidade INT NOT NULL,
            valor_unitario DECIMAL(10, 2) NOT NULL,
            manutencao_id INTEGER
        );
    """)

    colunas_pecas = {
        linha[1] for linha in cursor.execute("PRAGMA table_info(PecasReposicao)")
    }
    if "codigo" not in colunas_pecas:
        cursor.execute("ALTER TABLE PecasReposicao ADD COLUMN codigo VARCHAR(20);")
    if "manutencao_id" not in colunas_pecas:
        cursor.execute("ALTER TABLE PecasReposicao ADD COLUMN manutencao_id INTEGER;")

    conexao.commit()
    cursor.execute("PRAGMA foreign_keys = ON;")
    conexao.close()

if __name__ == "__main__":
    inicializar_banco()
    print(f"Banco de dados pronto em: {CAMINHO_BANCO}")