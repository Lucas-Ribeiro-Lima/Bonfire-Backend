import json
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