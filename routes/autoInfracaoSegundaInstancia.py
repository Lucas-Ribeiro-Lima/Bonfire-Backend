from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from handlers.autoInfracaoSegundaInstancia import extractorSegundaInstancia, insertAutoInfracaoSegundaInstancia, getAutoInfracaoSegundaInstancia


autoInfracaoSegundaInstanciaBlueprint = Blueprint('autoInfracaoSegundaInstancia', __name__)

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["POST"])
def executeRoutePostAutoInfracaoPrimeiraInstancia():

    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 404

    file = request.files['file']
    
    tempFile = NamedTemporaryFile(delete=False)
    file.save(tempFile.name)

    autoSegundaInstanciaList = extractorSegundaInstancia.parseDocx(tempFile)

    response, err = insertAutoInfracaoSegundaInstancia.insertAutoInfracaoSegundaInstancia(autoSegundaInstanciaList)

    if err == None:
        return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["GET"])
def executeRouteGetAutoInfracaoSegInstancia():
    result = getAutoInfracaoSegundaInstancia.getAutoInfracaoSegundaInstancia()
    return jsonify({"autos": result }), 200