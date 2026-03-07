import pandas as pd
from sqlalchemy import text
from repositories.database import MySQL
from handlers import log
from exceptions.CustomExceptions import ErrGetData, ErrInsertData, ErrUpdateData

engine = MySQL().get_connection()

def getLinha():
    """Recupera os dados das linhas no banco de dados"""
    query = f"SELECT * FROM linha"
    try:
        with engine.connect():
            data_frame = pd.read_sql(query, engine)
            # dataFrame['COMPARTILHADA'] = dataFrame['COMPARTILHADA'].apply(lambda x: x == b'\x01')
            # dataFrame['LINH_ATIV_EMPR'] = dataFrame['LINH_ATIV_EMPR'].apply(lambda x: x == b'\x01')
            json_data = data_frame.to_json(orient='records')
        engine.dispose()
        return json_data
    except Exception as e:
        log.writeToLogFile(e)
        raise ErrGetData('Erro ao recuperar as linhas', 500)
    
    
def insertLinha(line):
    """Insere uma linnha no banco de dados"""
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
        log.writeToLogFile(e)
        raise ErrInsertData('Erro ao gravar as linhas', 500)
        

def updateLinha(line):
    """Realiza atualização de uma lista de linhas no banco de dados"""
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
        log.writeToLogFile(e)
        raise ErrUpdateData("Erro ao atualizar a linha", 500)

def deleteLinha(line):
    """Realiza a exclusão de uma lista de linhas no banco de dados"""
    line_object = {"COD_LINH": line}
    query = '''DELETE FROM linha WHERE COD_LINH = :COD_LINH '''
    counter = 0    
    try: 
        with engine.connect() as conn:
            result = conn.execute(text(query), line_object)
            counter = result.rowcount
            conn.commit()
        engine.dispose()
        return counter
    except Exception as e:
        log.writeToLogFile(e)
        raise ErrUpdateData("Erro ao excluir a linha", 500)
