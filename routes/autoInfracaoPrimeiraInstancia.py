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

    response = insertAutoInfracaoPrimeiraInstancia.insertAutoInfracaoPrimeiraInstanciaCSV(file)
    return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200


@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstancia", methods=["GET"])
def getAutoInfracaoPrimInstancia():
    if 'data' not in request.form:
        return jsonify({"error": "É necessário informar a data em que a o auto foi emitido"}), 404

    date = request.form['data']

    result = getAutoInfracaoPrimeiraInstancia.getAutoInfracaoPrimeiraInstancia(date)

    return jsonify({"autos": json.loads(result)}), 200