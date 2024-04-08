import json
import sqlite3
from handlers import log
from sqlalchemy import create_engine
from exceptions.CustomExceptions import ErrInvalidDbConfig, ErrCreatingDbConnection

class mySQL:
    def __init__(self, configPath='Config/mysql_db_config.json'):
        self.config = self.loadConfig(configPath)

    def loadConfig(self, configPath):
        with open(configPath, 'r') as configFile:
            return json.load(configFile)
        
    def createDatabaseStringConnection(self):
        dbConfig = self.config.get("database", {}) 
        driver = dbConfig.get('driver')
        host = dbConfig.get('host')
        port = dbConfig.get('port')
        database = dbConfig.get('database')
        user = dbConfig.get('user')
        password = dbConfig.get('password')

        if None in (driver, host, database, user, password):
            raise ErrInvalidDbConfig("Algumas configurações do banco de dados estão ausentes ou configuradas incorretamente", 401)

        try:
            connectionString = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        except Exception as e:
            log.HandleErrorLog(e)
            raise ErrCreatingDbConnection("Nao foi possivel estabelecer uma conexao com o banco de dados", 500)

        return connectionString           
    
class sqlite3Db:
  """SQlite3 temporary database for unitary testing"""
  def create_temp_database():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    autoInfracaoTable = [
      "NUM_AI", "NUM_NOTF", "TIP_PENL", "NOM_CONC", "COD_LINH", "NOM_LINH", "NUM_VEIC", 
      "IDN_PLAC_VEIC", "DAT_OCOR_INFR", "DES_LOCA", "COD_IRRG_FISC", "ARTIGO", "DESC_OBSE", 
      "NUM_MATR_FISC", "QTE_PONT", "DAT_EMIS_NOTF", "DAT_LIMT_RECU", "VAL_INFR", "DAT_CANC"
    ]
    segundaInstanciaTable = ["ID", "NUM_AI", "NUM_ATA", "NUM_RECURSO", "NOM_CONC", "RESULTADO", "DAT_PUBL"]
    veiculosTable = ["NUM_VEIC", "IDN_PLAC_VEIC", "VEIC_ATIV_EMPR"]
    linhaTable = ["COD_LINH", "ID_OPERADORA", "COMPARTILHADA", "LINH_ATIV_EMPR"]
    operadoraTable = ["NOME", "CONCESSIONARIA"]

    cursor.execute(f"CREATE TABLE auto_infracao({",".join(autoInfracaoTable)})")
    cursor.execute(f"CREATE TABLE segundaInstancia({",".join(segundaInstanciaTable)})")
    cursor.execute(f"CREATE TABLE operadora({",".join(operadoraTable)})")
    cursor.execute(f"CREATE TABLE veiculos({",".join(veiculosTable)})")
    cursor.execute(f"CREATE TABLE linha({",".join(linhaTable)})")

    cursor.close()

    return connection