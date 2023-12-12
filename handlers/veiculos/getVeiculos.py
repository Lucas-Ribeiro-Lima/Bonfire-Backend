import database.sqlServer as sqlServer
from flask import jsonify

def getVeiculos():
    try:
        conn = sqlServer.sqlServer()
        query = '''
            SELECT *
            FROM veiculos
        '''        
        conn.connection.cursor.execute(query)
        result = conn.connection.cursor.fetchall()

        # Retorna os resultados
        sqlServer.closeConnection()
        return jsonify({"veiculos": result }), 200
    

    except Exception:
        sqlServer.closeConnection()
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500