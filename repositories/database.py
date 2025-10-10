import json
from handlers import log
from sqlalchemy import create_engine, text
from exceptions.CustomExceptions import ErrInvalidDbConfig, ErrCreatingDbConnection

def check_connection():
    driver = MySQL()
    engine = driver.get_connection()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            driver.print_connection_data()
    except:
        raise "Error ao conectar no banco de dados"


class MySQL:
    def __init__(self, config_path='Config/mysql_db_config.json'):
        with open(config_path, 'r') as json_file:
            config = json.load(json_file)
        self.config = config.get("database", {})
        self.connection = self.create_database_string_connection(config)

    def create_database_string_connection(self, config):
        db_config = config.get("database", {})
        driver = db_config.get('driver')
        host = db_config.get('host')
        port = db_config.get('port')
        database = db_config.get('database')
        user = db_config.get('user')
        password = db_config.get('password')

        if None in (driver, host, database, user, password):
            raise ErrInvalidDbConfig(
                "Algumas configurações do banco de dados estão ausentes ou configuradas incorretamente", 401)

        try:
            connectionString = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
        except Exception as e:
            log.HandleErrorLog(e)
            raise ErrCreatingDbConnection("Nao foi possivel estabelecer uma conexao com o banco de dados", 500)

        return connectionString

    def get_connection(self):
        return self.connection

    def print_connection_data(self):
        print(f'''
                |===============================
                |Database Information                        
                |Driver: {self.config.get("driver")}         
                |Host: {self.config.get("host")}             
                |Port: {self.config.get("port")}             
                |Database: {self.config.get("database")}     
                |User: {self.config.get("user")}
                |===============================            
        ''')
