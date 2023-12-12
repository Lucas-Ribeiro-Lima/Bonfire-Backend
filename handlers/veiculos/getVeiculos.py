import database.sqlServer as sqlServer
from flask import jsonify

def getVeiculos():
    try:
        conn = sqlServer.sqlServer()
        query = '''
            SELECT *
            FROM veiculos
        '''        
        cursor = conn.connection.cursor()
        cursor.execute(query)
        row = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        result = []
        for row in row:
            result.append(dict(zip(columns, row)))

        # Retorna os resultados
        conn.connection.close()
        return result
    

    except Exception:
        conn.connection.close()
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500