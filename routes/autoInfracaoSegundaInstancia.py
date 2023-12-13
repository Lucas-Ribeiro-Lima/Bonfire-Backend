from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from handlers.autoInfracaoSegundaInstancia import extractorSegundaInstancia, insertAutoInfracaoSegundaInstancia, getAutoInfracaoSegundaInstancia


autoInfracaoSegundaInstanciaBlueprint = Blueprint('autoInfracaoSegundaInstancia', __name__)

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["POST"])
def postAutoInfracaoPrimeiraInstancia():

    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 404

    #elif file.filename == '' or not file.filename.endswith('.pdf'):
    #    return jsonify({"error": "Arquivo inválido"}), 404

    file = request.files['file']
    
    tempFile = NamedTemporaryFile(delete=False)
    file.save(tempFile.name)

    autoInfracaoList = extractorSegundaInstancia.parseDocx(tempFile)

    response = insertAutoInfracaoSegundaInstancia.insertAutoInfracaoSegundaInstancia(autoInfracaoList)

    return jsonify({"message": f"{response} itens Extraidos e armazenados com sucesso!"}), 200

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["GET"])
def getAutoInfracaoSegInstancia():
    result = getAutoInfracaoSegundaInstancia.getAutoInfracaoSegundaInstancia()
    return jsonify({"autos": result }), 200