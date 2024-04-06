from flask import Blueprint, jsonify, request
from Handlers import veiculos
from Handlers import globais
from Exceptions.CustomExceptions import CustomException
import json

veiculoBlueprint = Blueprint('veiculo', __name__)
keys_to_check = ["NUM_VEIC", "IDN_PLAC_VEIC", "VEIC_ATIV_EMPR"]

@veiculoBlueprint.route("/veiculos", methods=["GET"])
def executeRouteGetVeiculo():
    try:
        result = veiculos.getVeiculos()
        return jsonify({"veiculos": json.loads(result)})
    except CustomException as error:
        return jsonify(error.toJson()), 500

@veiculoBlueprint.route("/veiculos", methods=["POST"])
def executeRoutePostVeiculos():
    # Get data in JSON request
    veiculos = request.get_json()

    # Basic Validation
    if not globais.checkKeysInJson(veiculos, keys_to_check):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir num_veiculo e placa para cada veículo a ser cadastrado"}), 400
    
    response, err = veiculos.insertVeiculos(veiculos)

    if err == None:
        return jsonify({"message": f"{str(response)} Veículos inseridos com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500
    
@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
def executeRoutePatchVeiculos():
    # Get data in JSON request
    veiculos = request.get_json()

    # Basic Validation
    if not globais.checkKeysInJson(veiculos, keys_to_check):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir {NUM_VEIC IDN_PLAC_VEIC e VEIC_ATIV_EMPR} para cada veículo a ser cadastrado"}), 400
    
    response, err = veiculos.updateVeiculos(veiculos)

    if err == None:
        return jsonify({"message": f"{str(response)} Veículos removidos com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500    
