import pandas as pd
from sqlalchemy import text
from repositories import database 
from handlers import log
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrUpdateData

def getLinha():
    """Recupera os dados das linhas no banco de dados"""
    engine = database.mySQL().createDatabaseStringConnection()
    query = f"SELECT * FROM linha"
    try:
        with engine.connect():
            dataFrame = pd.read_sql(query, engine)
            # dataFrame['COMPARTILHADA'] = dataFrame['COMPARTILHADA'].apply(lambda x: x == b'\x01')
            # dataFrame['LINH_ATIV_EMPR'] = dataFrame['LINH_ATIV_EMPR'].apply(lambda x: x == b'\x01')
            jsonData = dataFrame.to_json(orient='records')
        engine.dispose()
        return jsonData
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrGetData('Erro ao recuperar as linhas', 500)
    
    
def insertLinha(line):
    """Insere uma linnha no banco de dados"""
    engine = database.mySQL().createDatabaseStringConnection()
    query = '''INSERT INTO linha (COD_LINH, COMPARTILHADA, ID_OPERADORA, LINH_ATIV_EMPR) VALUES (:COD_LINH, :COMPARTILHADA, :ID_OPERADORA, :LINH_ATIV_EMPR)'''
    counter = 0    
    try: 
        with engine.connect() as conn:
            for i in line:
                result = conn.execute(text(query), i)
                if result.rowcount > 0:
                    counter = counter +1
            conn.commit()
        engine.dispose()    
        return counter
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrInsertData('Erro ao gravar as linhas', 500)
        

def updateLinha(line):
    """Realiza atualização de uma lista de linhas no banco de dados"""
    engine = database.mySQL().createDatabaseStringConnection()
    query = '''UPDATE linha set LINH_ATIV_EMPR = :LINH_ATIV_EMPR, COMPARTILHADA = :COMPARTILHADA WHERE COD_LINH = :COD_LINH'''
    counter = 0    
    try: 
        with engine.connect() as conn:
            for i in line:
                result = conn.execute(text(query), i)
                if result.rowcount > 0:
                    counter = counter +1
            conn.commit()
        engine.dispose()
        return counter
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrUpdateData("Erro ao atualizar a linha", 500)

def deleteLinha(line):
    """Realiza a exclusão de uma lista de linhas no banco de dados"""
    lineObject = {"COD_LINH": line}
    engine = database.mySQL().createDatabaseStringConnection()
    query = '''DELETE FROM linha WHERE COD_LINH = :COD_LINH '''
    counter = 0    
    try: 
        with engine.connect() as conn:
            result = conn.execute(text(query), lineObject)
            counter = result.rowcount
            conn.commit()
        engine.dispose()
        return counter
    except Exception as e:
        log.HandleErrorLog(e)
        raise ErrUpdateData("Erro ao excluir a linha", 500)