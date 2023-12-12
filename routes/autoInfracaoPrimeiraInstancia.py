from flask import Blueprint, jsonify, request
from handlers.autoInfracaoPrimeiraInstancia import insertAutoInfracaoPrimeiraInstancia
from database import sqlServer
from handlers.autoInfracaoPrimeiraInstancia import extractorPrimeiraInstancia
from handlers.autoInfracaoPrimeiraInstancia import getAutoInfracaoPrimeiraInstancia


autoInfracaoPrimeiraInstanciaBlueprint = Blueprint('autoInfracao', __name__)

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstancia", methods=["POST"])
def postAutoInfracaoPrimeiraInstancia():
    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 404

    #elif file.filename == '' or not file.filename.endswith('.pdf'):
    #    return jsonify({"error": "Arquivo inválido"}), 404

    else:
        file = request.files['file']

    autoInfracaoList, count = extractorPrimeiraInstancia.parsePdf(file.stream)

    response = insertAutoInfracaoPrimeiraInstancia.insertAutoInfracaoPrimeiraInstancia(autoInfracaoList)
    
    return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200


@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstancia", methods=["GET"])
def getAutoInfracaoPrimInstancia():
    if 'data' not in request.form:
        return jsonify({"error": "É necessário informar a data em que a o auto foi emitido"}), 404

    date = request.form['data']

    result = getAutoInfracaoPrimeiraInstancia.getAutoInfracaoPrimeiraInstancia(date)
    return jsonify({"autos": result }), 200