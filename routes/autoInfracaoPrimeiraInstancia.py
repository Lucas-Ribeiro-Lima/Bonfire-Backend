from flask import Blueprint, jsonify, request
from handlers.autoInfracaoPrimeiraInstancia import getAutoInfracaoPrimeiraInstancia, insertAutoInfracaoPrimeiraInstancia
import json


autoInfracaoPrimeiraInstanciaBlueprint = Blueprint('autoInfracao', __name__)

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstanciaCSV", methods=["POST"])
def postAutoInfracaoPrimeiraInstanciaCSV():
    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    else:
        file = request.files['file']

    response, err = insertAutoInfracaoPrimeiraInstancia.insertAutoInfracaoPrimeiraInstanciaCSV(file)
    if err == None:
        return jsonify({"message": response}), 200
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500
        #return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/insertIgnorePrimeiraInstanciaXLS", methods=["POST"])
def postIgnoreAutoInfracaoPrimeiraInstanciaXLS():
    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    else:
        file = request.files['file']

    response, err = insertAutoInfracaoPrimeiraInstancia.insertIgnoreAutoInfracaoPrimeiraInstanciaXLS(file)

    if err == None:
        return jsonify({"message": f"{str(response)} autos inseridos com sucesso"}), 200
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500
        #return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstancia", methods=["GET"])
def getAutoInfracaoPrimInstancia():
    if 'data' not in request.form:
        return jsonify({"error": "É necessário informar a data em que a o auto foi emitido"}), 404

    date = request.form['data']

    result = getAutoInfracaoPrimeiraInstancia.getAutoInfracaoPrimeiraInstancia(date)

    return jsonify({"autos": json.loads(result)}), 200

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstancia", methods=["POST"])
def checkAutoInfracaoPrimInstancia():
    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    else:
        file = request.files['file']

    db_rows, file_rows, rows_notpresent = getAutoInfracaoPrimeiraInstancia.checkAutoInfracaoPrimeiraInstancia(file)

    return jsonify({"db_rows": f"{db_rows} Entries found in Database", "file_rows": f"{file_rows} Rows present in File", "Not Present": f"{rows_notpresent}"}), 200

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstanciaXLS", methods=["POST"])
def postAutoInfracaoPrimeiraInstanciaXLS():
    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    else:
        file = request.files['file']

    response, err = insertAutoInfracaoPrimeiraInstancia.insertAutoInfracaoPrimeiraInstanciaXLS(file)
    if err == None:
        return jsonify({"message": response}), 200
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500
        #return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200