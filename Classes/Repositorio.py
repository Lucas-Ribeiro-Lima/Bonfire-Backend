import json
import pyodbc

class Repositorio:
    def __init__(self, config_path='Config/db_config.json'):
        self.config = self.load_config(config_path)
        self.connection = self.get_database_connection()

    def load_config(self, config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def get_database_connection(self):
        db_config = self.config.get("database", {}) 
        driver = db_config.get('driver')
        server = db_config.get('server')
        port = db_config.get('port')
        database = db_config.get('database')
        uid = db_config.get('uid')
        pwd = db_config.get('pwd')

        if None in [driver, server, database, uid, pwd]:
             raise ValueError("Algumas configurações do banco de dados estão ausentes ou configuradas incorretamente.")

        db_config = self.config.get("database", {})
        connection_string = f"DRIVER={driver};SERVER={server},{port};DATABASE={database};UID={uid};PWD={pwd}"

        return pyodbc.connect(connection_string)
    

    def insert_auto_infracao(self, data):
        query = '''
            INSERT INTO auto_infracao (
                linha, veiculo, placa, num_auto, concessionaria, data, local,
                base_legal, cod_infracao, dispositivo, descricao, observacao, agente,
                pontuacao, data_emissao, data_lim_recurso, valor_multa
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        with self.connection.cursor() as cursor:
            cursor.execute(query, tuple(data.values()))

        # Commit the transaction
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
