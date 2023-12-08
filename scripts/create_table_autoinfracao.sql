CREATE TABLE auto_infracao (
    num_auto VARCHAR(10) PRIMARY KEY,
    linha VARCHAR(10),
    veiculo INTEGER,
    placa VARCHAR(10),
    concessionaria VARCHAR(100),
    data DATETIME,
    local VARCHAR(255),
    base_legal VARCHAR(100),
    cod_infracao INTEGER,
    dispositivo VARCHAR(20),
    descricao VARCHAR(255),
    observacao VARCHAR(255),
    agente INTEGER,
    pontuacao REAL,
    data_emissao DATETIME,
    data_lim_recurso DATETIME,
    valor_multa REAL
);

--------------------------------------------------------------------------

CREATE TABLE veiculos (
    num_veiculo INT PRIMARY KEY,
    placa NVARCHAR(10) UNIQUE,
    operadora NVARCHAR(100),
    FOREIGN KEY (operadora) REFERENCES operadora(id)
);

-- Tabela linha
CREATE TABLE linha (
    num_linha NVARCHAR(10),
    id INT PRIMARY KEY,
    compartilhada BIT NOT NULL,
    CHECK (compartilhada IN (0, 1)) -- Garante que compartilhada é um booleano
);

-- Tabela operadora
CREATE TABLE operadora (
    id INT PRIMARY KEY,
    nome NVARCHAR(100),
    concessionaria NVARCHAR(100)
);

-- Tabela auto_infracao
CREATE TABLE auto_infracao (
    numauto NVARCHAR(10) PRIMARY KEY,
    linha NVARCHAR(10),
    veiculo INT,
    placa NVARCHAR(10),
    concessionaria NVARCHAR(100),
    data DATETIME,
    local NVARCHAR(255),
    baselegal NVARCHAR(100),
    codinfracao INT,
    dispositivo NVARCHAR(20),
    descricao NVARCHAR(255),
    observacao NVARCHAR(255),
    agente INT,
    pontuacao FLOAT,
    dataemissao DATETIME,
    datalimrecurso DATETIME,
    valormulta FLOAT,
    FOREIGN KEY (linha) REFERENCES linha(num_linha),
    FOREIGN KEY (veiculo) REFERENCES veiculos(num_veiculo),
    FOREIGN KEY (placa) REFERENCES veiculos(placa),
    FOREIGN KEY (concessionaria) REFERENCES operadora(concessionaria)
);




