from flask import Blueprint, jsonify, request
from handlers.autoInfracao import insertAutoInfracao
from database import sqlServer
from handlers.autoInfracao import extractor

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

    autoInfracaoList = extractor.parsePdf(file.stream)

    for i in autoInfracaoList:
        insertAutoInfracao(i)
    return jsonify({"message": "Extração e armazenamento concluídos com sucesso!"}), 200

@autoInfracaoBlueprint.route("/autoInfracao", methods=["GET"])
def getAutoInfracao():
    try:
        conn = sqlServer.sqlServer()
        query = '''
            SELECT *
            FROM auto_infracao
            WHERE data_lim_recurso >= '01-01-2023'
        '''        
        conn.connection.cursor.execute(query)
        result = conn.connection.cursor.fetchall()

        # Retorna os resultados
        sqlServer.closeConnection()
        return jsonify({"veiculos": result }), 200
    

    except Exception:
        sqlServer.closeConnection()
        return jsonify({"error": f"Um erro ocorreu: {Exception}"}), 500
