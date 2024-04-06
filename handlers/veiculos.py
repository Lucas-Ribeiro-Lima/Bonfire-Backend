import pandas as pd
from Handlers import log
from Classes.Veiculo import Veiculo
from Database import databases as databases
from sqlalchemy import text
from Exceptions.CustomExceptions import ErrGetVehicles, ErrInsertVehicles, ErrUpdateVehicles
from typing import List


def getVeiculos() -> List[Veiculo]:
    engine = databases.mySQL().createDatabaseStringConnection()
    try:
        with engine.connect() as connection:
            query = f"SELECT * FROM veiculos"
            dataFrame = pd.read_sql(query, connection)
            jsonData = dataFrame.to_json(orient='records')
    except Exception as e:
        log.HandleLog(e)
        raise ErrGetVehicles("Erro ao recuperar os veiculos")

    engine.dispose()
    return jsonData
    
def insertVeiculos(veiculos: List[Veiculo]):
    # Extrai os dados do veiculo
    engine = databases.mySQL().createDatabaseStringConnection()
    query = '''INSERT INTO veiculos (NUM_VEIC, IDN_PLAC_VEIC, VEIC_ATIV_EMPR) VALUES (:NUM_VEIC, :IDN_PLAC_VEIC, :VEIC_ATIV_EMPR)'''
    counter = 0    
    try: 
        with engine.connect() as connection:
            for veiculo in veiculos:
                result = connection.execute(text(query), veiculo)
                if result.rowcount > 0:
                    counter = counter +1
            connection.commit()
    except Exception as e:
        log(e)
        raise ErrInsertVehicles("Erro ao inserir veiculos")
        
    engine.dispose()
    return counter


def updateVeiculos(veiculos: List[Veiculo]):
    # Extrai os dados do veiculo
    engine = databases.mySQL().createDatabaseStringConnection()
    query = '''UPDATE veiculos set VEIC_ATIV_EMPR = :VEIC_ATIV_EMPR WHERE NUM_VEIC = :NUM_VEIC'''
    counter = 0    
    try: 
        with engine.connect() as connection:
            for veiculo in veiculos:
                result = connection.execute(text(query), veiculo)
                if result.rowcount > 0:
                    counter = counter +1
            connection.commit()
    except Exception as e:
        log(e)
        raise ErrUpdateVehicles("Erro ao atualizar os veiculos")
        
    engine.dispose()
    return counter