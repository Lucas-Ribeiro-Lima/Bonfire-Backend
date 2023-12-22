from flask import jsonify
from Classes import *
import database.mySQL as mySQL
from sqlalchemy import text
import pandas as pd
from Classes import Conversores
from datetime import datetime

def getAutoInfracaoPrimeiraInstancia(date):
    try:
        engine = mySQL.mySQL()
        engine = engine.createDatabaseStringConnection()

      
        with engine.connect() as connection:
            query = f"SELECT * FROM auto_infracao WHERE DAT_EMIS_NOTF >= {date}"
            
            dataFrame = pd.read_sql(query, engine)
            dataFrame['DAT_EMIS_NOTF'] = pd.to_datetime(dataFrame['DAT_EMIS_NOTF'])
            dataFrame['DAT_LIMT_RECU'] = pd.to_datetime(dataFrame['DAT_LIMT_RECU'])
            dataFrame['DAT_OCOR_INFR'] = pd.to_datetime(dataFrame['DAT_OCOR_INFR'])
            jsonData = dataFrame.to_json(orient='records')
                   
        return jsonData
  
    except Exception:
        #conn.connection.close()
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500