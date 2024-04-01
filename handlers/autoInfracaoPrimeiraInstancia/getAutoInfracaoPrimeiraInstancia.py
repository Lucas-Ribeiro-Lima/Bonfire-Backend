from flask import jsonify
from Classes import *
import database.mySQL as mySQL
from sqlalchemy import text
import pandas as pd
from Classes import Conversores
from datetime import datetime

def getAutoInfracaoPrimeiraInstanciaPages(date):
    try:
        engine = mySQL.mySQL()
        engine = engine.createDatabaseStringConnection()

        with engine.connect() as connection:

            query = f"SELECT * FROM auto_infracao WHERE DAT_EMIS_NOTF >= '{date}'"
            dataFrame = pd.read_sql(query, engine)
            dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'])
            dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'])
            dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'])

            jsonData = dataFrame.to_json(orient='records')
                   
        return jsonData
    
    except Exception as e:
        #conn.connection.close()
        return {e}
    
def checkAutoInfracaoPrimeiraInstancia(csv):
    try:
        dataFrame = pd.read_csv(csv, header = 0, delimiter='|')

    except Exception as e:
        with open("E:\\Projetos\\Bonfire\\Import\\output.txt", "a") as t:
            err = f"ERRO: problema ao processar o arquivo no Load: {csv}"
            print(err, file=t)
        return err, e, None
    
    engine = mySQL.mySQL()
    engine = engine.createDatabaseStringConnection()

    values = dataFrame['NUM_AI'].unique()

    counter = 0
    rows_counter = 0
    rows_notpresent = []

    for value in values:
        query = f"SELECT * FROM auto_infracao WHERE NUM_AI = '{value}'"

        result_df = pd.read_sql(query, engine)
        rows = result_df.shape[0]

        if rows > 0:
            rows_counter = rows_counter +1
        counter = counter +1

        if rows == 0:
            rows_notpresent.append(value)

    engine.dispose()
    return rows_counter, counter, rows_notpresent