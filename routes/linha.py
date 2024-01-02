from flask import Blueprint, jsonify, request
from handlers.linha import *
import json
from handlers.globais import checkJson

linhaBlueprint = Blueprint('linha', __name__)
keys_to_check = ["COD_LINH", "COMPARTILHADA", "ID_OPERADORA", "LINH_ATIV_EMPR"]

@linhaBlueprint.route("/linha", methods=["GET"])
def executeRouteGetLinhao():
    result = getLinha.getLinha()
    return jsonify({"linha": json.loads(result)})

@linhaBlueprint.route("/linha", methods=["POST"])
def executeRoutePostLinha():
    # Get data in JSON request
    linha = request.get_json()

    # Basic Validation
    if not checkJson.checkKeysInJson(linha, keys_to_check):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir {COD_LINH, COMPARTILHADA, ID_OPERADORA, LINH_ATIV_EMPR} para cada linha a ser cadastrada"}), 400
    
    response, err = insertLinha.insertLinha(linha)

    if err == None:
        return jsonify({"message": f"{str(response)} Linhas inseridas com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500
    
@linhaBlueprint.route("/linha", methods=["PATCH"])
def executeRouteUpdateVeiculos():
    # Get data in JSON request
    linha = request.get_json()

    # Basic Validation
    if not checkJson.checkKeysInJson(linha, keys_to_check):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir {COD_LINH, COMPARTILHADA, LINH_ATIV_EMPR} para cada linha a ser cadastrada"}), 400
    
    response, err = updateLinha.updateLinha(linha)

    if err == None:
        return jsonify({"message": f"{str(response)} Veículos removidos com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500    
