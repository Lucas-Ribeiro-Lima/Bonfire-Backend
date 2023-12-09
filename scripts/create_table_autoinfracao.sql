CREATE TABLE veiculos (
    num_veiculo INT PRIMARY KEY,
    placa NVARCHAR(10) UNIQUE
);

-- Tabela operadora
CREATE TABLE operadora (
    id INT PRIMARY KEY,
    nome NVARCHAR(100),
    concessionaria NVARCHAR(100)
);

-- Tabela linha
CREATE TABLE linha (
    num_linha NVARCHAR(10) PRIMARY KEY,
    id_operadora INT,
    FOREIGN KEY (id_operadora) REFERENCES operadora(id),
    compartilhada BIT NOT NULL,
    CHECK (compartilhada IN (0, 1)) -- Garante que compartilhada é um booleano
);

-- Tabela auto_infracao
CREATE TABLE auto_infracao (
    num_auto NVARCHAR(10) PRIMARY KEY,
    linha NVARCHAR(10),
    veiculo INT,
    placa NVARCHAR(10),
    concessionaria NVARCHAR(100),
    data DATETIME,
    local NVARCHAR(255),
    base_legal NVARCHAR(100),
    cod_infracao INT,
    dispositivo NVARCHAR(20),
    descricao NVARCHAR(255),
    observacao NVARCHAR(255),
    agente INT,
    pontuacao FLOAT,
    data_emissao DATETIME,
    data_lim_recurso DATETIME,
    valor_multa FLOAT
);


INSERT INTO operadora (id, nome, concessionaria) VALUES
(107, 'MILENIO TRANSPORTES', 'CONSORCIO PAMPULHA'), (123, 'BOA VISTA COLETIVOS', 'CONSORCIO BHLESTE'),
(113, 'VIA BH COLETIVOS', 'CONSORCIO DEZ'), (37, 'VIACAO ANCHIETA', 'CONSORCIO DOM PEDRO II')

