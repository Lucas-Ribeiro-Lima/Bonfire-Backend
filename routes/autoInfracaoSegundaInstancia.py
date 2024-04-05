import traceback
from flask import Blueprint, jsonify, request
from tempfile import NamedTemporaryFile
from Exceptions.CustomExceptions import ErrDataPubli, ErrNullInsert, ErrInsertDb, ErrInvalidDbConfig
from handlers.autoInfracaoSegundaInstancia import extractorSegundaInstancia, insertAutoInfracaoSegundaInstancia, getAutoInfracaoSegundaInstancia


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
    except ErrDataPubli as e:
        return jsonify(e.to_dict()), 500
    except ErrNullInsert as e:
        return jsonify(e.to_dict()), 500
    except ErrInsertDb as e:
        return jsonify(e.to_dict()), 500
    except ErrInvalidDbConfig as e:
        return jsonify(e.to_dict()), 500
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred"}), 500         

@autoInfracaoSegundaInstanciaBlueprint.route("/autoInfracao/segundaInstancia", methods=["GET"])
def executeRouteGetAutoInfracaoSegInstancia():
    result = getAutoInfracaoSegundaInstancia.getAutoInfracaoSegundaInstancia()
    return jsonify({"autos": result }), 200