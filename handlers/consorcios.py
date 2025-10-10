import pandas as pd
from repositories.database import MySQL
from handlers import log
from exceptions.CustomExceptions import ErrGetData

def get_consorcios():
    """Retorna todos os consórcios cadastrados."""
    engine = MySQL().get_connection()
    query = f'SELECT * FROM operadora'
    try:
        with engine.connect():
            dataframe = pd.read_sql(query, engine)
            json_data = dataframe.to_json(orient='records')
        engine.dispose()
        return json_data
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrGetData('Erro ao recuperar os consórcios', 500)