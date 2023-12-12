import json
import pyodbc

class sqlServer:
    def __init__(self, configPath='Config/db_config.json'):
        self.config = self.loadConfig(configPath)
        self.connection = self.createDatabaseStringConnection()

    def loadConfig(self, configPath):
        with open(configPath, 'r') as configFile:
            return json.load(configFile)

    def createDatabaseStringConnection(self):
        dbConfig = self.config.get("database", {}) 
        driver = dbConfig.get('driver')
        server = dbConfig.get('server')
        port = dbConfig.get('port')
        database = dbConfig.get('database')
        uid = dbConfig.get('uid')
        pwd = dbConfig.get('pwd')

        if None in [driver, server, database, uid, pwd]:
             raise ValueError("Algumas configurações do banco de dados estão ausentes ou configuradas incorretamente.")

        dbConfig = self.config.get("database", {})
        connectionString = f"DRIVER={driver};SERVER={server},{port};DATABASE={database};UID={uid};PWD={pwd}"

        return pyodbc.connect(connectionString)
    
    def closeConnection(self):
        self.connection.close()