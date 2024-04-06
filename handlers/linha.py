from flask import jsonify
import pandas as pd
from sqlalchemy import text
from Database.databases import mySQL


def getLine():
    try:
        engine = mySQL.mySQL()
        engine = engine.createDatabaseStringConnection()

      
        with engine.connect() as connection:
            query = f"SELECT * FROM linha"
            
            dataFrame = pd.read_sql(query, engine)

            #this lambda function get the value of the dataframe (COMPARTILHADA) as X, then verifies if x == b'\x01'. and if is, apply the value TRUE to the item in dataframe
            # i use this to convert the data returned from mysql to TRUE or FALSE for JSON
            dataFrame['COMPARTILHADA'] = dataFrame['COMPARTILHADA'].apply(lambda x: x == b'\x01')
            dataFrame['LINH_ATIV_EMPR'] = dataFrame['LINH_ATIV_EMPR'].apply(lambda x: x == b'\x01')
            jsonData = dataFrame.to_json(orient='records')
                   
        return jsonData
    

    except Exception:
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500
    
def insertLine(line):
    # Extrai os dados do veiculo
    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()
    query = '''INSERT INTO linha (COD_LINH, COMPARTILHADA, ID_OPERADORA, LINH_ATIV_EMPR) VALUES (:COD_LINH, :COMPARTILHADA, :ID_OPERADORA, :LINH_ATIV_EMPR)'''
    counter = 0    
    try: 
        with engine.connect() as connection:
            for i in line:
                result = connection.execute(text(query), i)
                if result.rowcount > 0:
                    counter = counter +1
            connection.commit()
    

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\log\\bonfire.log", "a") as t:                
            err = f"ERRO: problema ao realizar o insert das Linhas"
            return err, e
        
    engine.dispose()
    return counter, None

def updateLine(line):
    # Extrai os dados do veiculo
    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()
    query = '''UPDATE linha set LINH_ATIV_EMPR = :LINH_ATIV_EMPR, COMPARTILHADA = :COMPARTILHADA WHERE COD_LINH = :COD_LINH'''
    counter = 0    
    try: 
        with engine.connect() as connection:
            for i in line:
                result = connection.execute(text(query), i)
                if result.rowcount > 0:
                    counter = counter +1
            connection.commit()
        

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\log\\bonfire.log", "a") as t:                
            err = f"ERRO: problema ao realizar o update dos veículos"
            return err, e
        
    engine.dispose()
    return counter, None