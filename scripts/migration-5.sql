RENAME TABLE segundaInstancia TO recurso_primeira_instancia;

CREATE TABLE recurso_segunda_instancia (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NUM_AI VARCHAR(15) UNIQUE,
    NUM_ATA INT,
    NUM_RECURSO VARCHAR(15),
    NOM_CONC VARCHAR(100),
    RESULTADO BIT NOT NULL
);
