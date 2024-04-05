import json
from sqlalchemy import create_engine
from Exceptions.CustomExceptions import ErrInvalidDbConfig

class mySQL:
    def __init__(self, configPath='Config/mysql_db_config.json'):
        self.config = self.loadConfig(configPath)
        self.connection = self.createDatabaseStringConnection()

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

        if None in [driver, host, database, user, password]:
             raise ErrInvalidDbConfig("Algumas configurações do banco de dados estão ausentes ou configuradas incorretamente.")

        dbConfig = self.config.get("database", {})
        connectionString = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}".format(host=host, db=database, user=user, pw=password))
        

        return connectionString           