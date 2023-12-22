from flask import jsonify
from Classes import *
import database.mySQL as mySQL
from sqlalchemy import text
import pandas as pd

def getAutoInfracaoPrimeiraInstancia(date):
    try:
        engine = mySQL.mySQL()
        engine = engine.createDatabaseStringConnection()

        dataFrame = pd.read_sql('auto_infracao', engine, if_exists='append', index=False)
        
        with engine.connect() as connection:
            query = text("SELECT * FROM auto_infracao WHERE data_emissao >= :date}")
            dataFrame = pd.read_sql(query, connection, params={"date": date})
            jsonData = dataFrame.to_json()
        
        return dataFrame


        # conn = sqlServer.sqlServer()
        # query = f'''
        #     SELECT *
        #     FROM auto_infracao
        #     WHERE data_emissao >= '{date}'
        # '''        
        # cursor = conn.connection.cursor()
        # cursor.execute(query)
        # row = cursor.fetchall()

        # columns = [column[0] for column in cursor.description]
        # result = []
        # for row in row:
        #     result.append(dict(zip(columns, row)))

        # # Retorna os resultados
        # conn.connection.close()
        # return result
    

    except Exception:
        #conn.connection.close()
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500