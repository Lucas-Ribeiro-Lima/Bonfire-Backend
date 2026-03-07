import pandas as pd
from handlers import log
from classes.Veiculo import Veiculo
from repositories.database import MySQL
from sqlalchemy import text
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrUpdateData
from typing import List

engine = MySQL().get_connection()

def getVeiculos() -> List[Veiculo]:
    """Recupera os veiculos do banco de dados"""
    query = f"SELECT * FROM veiculos"
    try:
        with engine.connect() as connection:
            data_frame = pd.read_sql(query, connection)
            json_data = data_frame.to_json(orient='records')
        engine.dispose()
        return json_data or []
    except Exception as e:
        log.writeToLogFile(e)
        raise ErrGetData("Erro ao recuperar os veiculos", 500)
    

def insertVeiculos(veiculos: List[Veiculo]):
    """Insere uma lista de veículos no banco de dados"""
    query = '''INSERT INTO veiculos (NUM_VEIC, IDN_PLAC_VEIC, VEIC_ATIV_EMPR) VALUES (:NUM_VEIC, :IDN_PLAC_VEIC, :VEIC_ATIV_EMPR)'''
    counter = 0    
    try: 
        with engine.connect() as conn:
            for veiculo in veiculos:
                result = conn.execute(text(query), veiculo)
                if result.rowcount > 0:
                    counter = counter +1
            conn.commit()
        engine.dispose()
        return counter
    except Exception as e:
        log.writeToLogFile(e)
        raise ErrInsertData("Erro ao inserir veiculos", 500)
        

def updateVeiculos(veiculos: List[Veiculo]):
    """Atualiza uma lista de veículos no banco de dados"""
    query = '''UPDATE veiculos set VEIC_ATIV_EMPR = :VEIC_ATIV_EMPR, IDN_PLAC_VEIC = :IDN_PLAC_VEIC WHERE NUM_VEIC = :NUM_VEIC'''
    counter = 0    
    try: 
        with engine.connect() as conn:
            for item in veiculos:
                result = conn.execute(text(query), item)
                if result.rowcount > 0:
                    counter = counter +1
            conn.commit()
        engine.dispose()
        return counter
    except Exception as e:
        log.writeToLogFile(e)
        raise ErrUpdateData("Erro ao atualizar os veiculos", 500)
    
def deleteVeiculos(veiculo):
    """Deleta uma lista de veiculos no banco de dados"""
    veiculo_object = {"NUM_VEIC": veiculo}
    query = '''DELETE FROM veiculos WHERE NUM_VEIC = :NUM_VEIC'''
    counter = 0    
    try: 
        with engine.connect() as conn:
            result = conn.execute(text(query), veiculo_object)
            counter = result.rowcount
            conn.commit()
        engine.dispose()
        return counter
    except Exception as e:
        log.writeToLogFile(e)
        raise ErrUpdateData("Erro ao deletar os veiculos", 500)
