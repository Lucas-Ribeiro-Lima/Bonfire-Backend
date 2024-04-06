import traceback
from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from Exceptions.CustomExceptions import *
from Handlers.autoInfracaoSegundaInstancia import extractorSegundaInstancia, insertAutoInfracaoSegundaInstancia, getAutoInfracaoSegundaInstancia


autoInfracaoSegundaInstanciaBlueprint = Blueprint('autoInfracaoSegundaInstancia', __name__)

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["POST"])
def executeRoutePostAutoInfracaoSegundaInstancia():

    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 404

    file = request.files['file']
    
    tempFile = NamedTemporaryFile(delete=False)
    file.save(tempFile.name)

    try:
        autoSegundaInstanciaList = extractorSegundaInstancia.parseDocx(tempFile)
        response = insertAutoInfracaoSegundaInstancia.insertAutoInfracaoSegundaInstancia(autoSegundaInstanciaList)
        return jsonify({"status": 200, "message": "itens Extraidos e armazenados com sucesso!", "counter": response}), 200
    except CustomException as e:
        return jsonify({e.to_dict()}), 500         

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["GET"])
def executeRouteGetAutoInfracaoSegInstancia():
    result = getAutoInfracaoSegundaInstancia.getAutoInfracaoSegundaInstancia()
    return jsonify({"autos": result }), 200