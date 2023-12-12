from flask import Blueprint, jsonify, request
from database import sqlServer
from handlers.autoInfracaoSegundaInstancia import extractorSegundaInstancia


autoInfracaoSegundaInstanciaBlueprint = Blueprint('autoInfracaoSegundaInstancia', __name__)

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["POST"])
def postAutoInfracaoPrimeiraInstancia():
    # Check if file is present and has pdf extention
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 404

    #elif file.filename == '' or not file.filename.endswith('.pdf'):
    #    return jsonify({"error": "Arquivo inválido"}), 404

    else:
        file = request.files['file']

    autoInfracaoList, count = extractorSegundaInstancia.parseDocx(file.stream)


    
    return autoInfracaoList
    #jsonify({"message": f"itens Extraidos e armazenados com sucesso!"}), 200