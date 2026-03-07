import json
from handlers import log
from sqlalchemy import create_engine, text
from exceptions.CustomExceptions import ErrInvalidDbConfig, ErrCreatingDbConnection
from classes.Config import config

def check_connection():
    driver = MySQL()
    engine = driver.get_connection()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            driver.print_connection_data()
    except:
        raise ErrCreatingDbConnection("Error ao conectar no banco de dados", 500)


class MySQL:
    def __init__(self):
        self.connection = self.create_database_string_connection()

    def create_database_string_connection(self):
        db_config = config.envs

        driver = db_config.get('DB_DRIVER')
        host = db_config.get('DB_HOST')
        port = db_config.get('DB_PORT')
        database = db_config.get('DB_NAME')
        user = db_config.get('DB_USER')
        password = db_config.get('DB_PASSWORD')

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
                |===============================================
                |Database Information                        
                |Driver: {config.envs.get("DB_DRIVER")}         
                |Host: {config.envs.get("DB_HOST")}             
                |Port: {config.envs.get("DB_PORT")}             
                |Database: {config.envs.get("DB_NAME")}     
                |User: {config.envs.get("DB_USER")}
                |Password: **************
                |===============================================
        ''')
