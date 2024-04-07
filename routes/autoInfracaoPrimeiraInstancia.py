import json
from flask import Blueprint, jsonify, request
from exceptions.CustomExceptions import CustomException, ErrIncompleteData
from handlers import primeiraInstancia

autoInfracaoPrimeiraInstanciaBlueprint = Blueprint('autoInfracao', __name__)

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstanciaCSV", methods=["POST"])
def executeRoutePostAutoInfracaoPrimeiraInstanciaCSV():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo CSV de primeira instancia não está presente na requisição", 400)
        file = request.files['file']
        response = primeiraInstancia.insertAutoInfracaoPrimeiraInstanciaCSV(file)
        return jsonify({"message": response}), 200

    except CustomException as e:
        jsonify({e.to_json()}), e.status

@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/insertIgnorePrimeiraInstanciaXLS", methods=["POST"])
def executeRoutePostIgnoreAutoInfracaoPrimeiraInstanciaXLS():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo CSV de primeira instancia não está presente na requisição", 400)
        file = request.files['file']
        response = primeiraInstancia.insertIgnoreAutoInfracaoPrimeiraInstanciaXLS(file)
        return jsonify({"message": f"{response} autos inseridos com sucesso"}), 200
    except CustomException as e:
        jsonify({e.to_json()}), e.status


@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstancia/<string:date>", methods=["GET"])
def executeRouteGetAutoInfracaoPrimInstancia(date):
    try:
        if not date:
            raise ErrIncompleteData("É necessário informar a data em que o auto foi emitido", 400)    
        result = primeiraInstancia.getPrimeiraInstancia(date)
        return jsonify({"autos": json.loads(result)}), 200
    
    except CustomException as e:
        return jsonify(e.to_json()), e.status


@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstancia", methods=["POST"])
def executeRouteCheckAutoInfracaoPrimInstancia():
    # Check if file is present and has pdf extention
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo CSV de primeira instancia não está presente na requisição", 400)
        file = request.files['file']
        db_rows, file_rows, rows_notpresent = primeiraInstancia.checkAutoInfracaoPrimeiraInstancia(file)
        return jsonify({"db_rows": f"{db_rows} Entries found in Database", "file_rows": f"{file_rows} Rows present in File", "Not Present": f"{rows_notpresent}"}), 200
    except CustomException as e:
        return jsonify(e.to_json()), e.status


@autoInfracaoPrimeiraInstanciaBlueprint.route("/autoInfracao/primeiraInstanciaXLS", methods=["POST"])
def executeRoutePostAutoInfracaoPrimeiraInstanciaXLS():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo XLS de primeira instancia não está presente na requisição", 400)
        file = request.files['file']
        response = primeiraInstancia.insertAutoInfracaoPrimeiraInstanciaXLS(file)
        return jsonify({"message": response}), 200
    except CustomException as e:
        return jsonify(e.to_json()), e.status
