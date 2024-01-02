from flask import jsonify
from database import mySQL as mySQL
import pandas as pd

def getLinha():
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