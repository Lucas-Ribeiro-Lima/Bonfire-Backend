from flask import Blueprint, jsonify, request
from handlers.veiculos import *
from handlers.globais import checkJson
import json

veiculoBlueprint = Blueprint('veiculo', __name__)
keys_to_check = ["NUM_VEIC", "IDN_PLAC_VEIC", "VEIC_ATIV_EMPR"]

@veiculoBlueprint.route("/veiculos", methods=["GET"])
def executeRouteGetVeiculo():
    result = getVeiculos.getVeiculos()
    return jsonify({"veiculos": json.loads(result)})

@veiculoBlueprint.route("/veiculos", methods=["POST"])
def executeRoutePostVeiculos():
    # Get data in JSON request
    veiculos = request.get_json()

    # Basic Validation
    if not checkJson.checkKeysInJson(veiculos, keys_to_check):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir num_veiculo e placa para cada veículo a ser cadastrado"}), 400
    
    response, err = insertVeiculos.insertVeiculos(veiculos)

    if err == None:
        return jsonify({"message": f"{str(response)} Veículos inseridos com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500
    
@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
def executeRoutePatchVeiculos():
    # Get data in JSON request
    veiculos = request.get_json()

    # Basic Validation
    if not checkJson.checkKeysInJson(veiculos, keys_to_check):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir {NUM_VEIC IDN_PLAC_VEIC e VEIC_ATIV_EMPR} para cada veículo a ser cadastrado"}), 400
    
    response, err = updateVeiculos.updateVeiculos(veiculos)

    if err == None:
        return jsonify({"message": f"{str(response)} Veículos removidos com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500    
