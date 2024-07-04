import json
from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from exceptions.CustomExceptions import *
from handlers import segundaInstancia

autoInfracaoSegundaInstanciaBlueprint = Blueprint('autoInfracaoSegundaInstancia', __name__)

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["POST"])
def executeRoutePostAutoInfracaoSegundaInstancia():
    try:
        if 'file' not in request.files:
            raise ErrIncompleteData("Arquivo de segunda instancia não está presente na requisição", 400)

        file = request.files['file']
        tempFile = NamedTemporaryFile(delete=False)
        file.save(tempFile.name)

        autoSegundaInstanciaList = segundaInstancia.parseDocx(tempFile)
        response = segundaInstancia.insertAutoInfracaoSegundaInstancia(autoSegundaInstanciaList)
        return jsonify({"message": "itens Extraidos e armazenados com sucesso!", "counter": response}), 200

    except CustomException as e:
        return jsonify(e.to_json()), e.status     

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia/<string:date>", methods=["GET"])
def executeRouteGetAutoInfracaoSegundaInstancia(date):
    try:
        result = segundaInstancia.getSegundaInstancia(date)
        return jsonify({"autos": json.loads(result) }), 200    
    except CustomException as e:
        return jsonify(e.to_json()), e.status