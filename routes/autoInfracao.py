from flask import Blueprint, jsonify, request
from handlers.autoInfracao import insertAutoInfracao
from database import sqlServer
from handlers.autoInfracao import extractor
from Classes import AutoInfracao

autoInfracaoBlueprint = Blueprint('autoInfracao', __name__)

@autoInfracaoBlueprint.route("/autoInfracao", methods=["POST"])
def postAutoInfracao():
    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 404

    #elif file.filename == '' or not file.filename.endswith('.pdf'):
    #    return jsonify({"error": "Arquivo inválido"}), 404

    else:
        file = request.files['file']

    autoInfracaoList, count = extractor.parsePdf(file.stream)
    #return jsonify({"message": autoInfracaoList}, {"Itens Processados": count}), 200

    response = insertAutoInfracao.insertAutoInfracao(autoInfracaoList)
    
    return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200


@autoInfracaoBlueprint.route("/autoInfracao", methods=["GET"])
def getAutoInfracao():
    try:
        conn = sqlServer.sqlServer()
        query = '''
            SELECT *
            FROM auto_infracao
            WHERE data_lim_recurso >= '01-01-2023'
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
        return jsonify({"autos": result }), 200
    

    except Exception:
        conn.connection.close()
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500
