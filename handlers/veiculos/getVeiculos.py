from flask import jsonify
from database import mySQL as mySQL
import pandas as pd

def getVeiculos():
    try:
        engine = mySQL.mySQL()
        engine = engine.createDatabaseStringConnection()

      
        with engine.connect() as connection:
            query = f"SELECT * FROM veiculos"
            
            dataFrame = pd.read_sql(query, engine)
            jsonData = dataFrame.to_json(orient='records')
                   
        return jsonData
    

    except Exception:
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500