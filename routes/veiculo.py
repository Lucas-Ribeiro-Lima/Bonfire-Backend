from flask import Blueprint, jsonify, request
from handlers.veiculos import *
import json

veiculoBlueprint = Blueprint('veiculo', __name__)

@veiculoBlueprint.route("/veiculos", methods=["GET"])
def executeRouteGetVeiculo():
    result = getVeiculos.getVeiculos()
    return jsonify({"veiculos": json.loads(result)})

@veiculoBlueprint.route("/veiculos", methods=["POST"])
def executeRoutePostVeiculos():
    # Get data in JSON request
    veiculos = request.get_json()

    # Basic Validation
    if not checkJson.checkKeysInJson(veiculos):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir num_veiculo e placa para cada veículo a ser cadastrado"}), 400
    
    response, err = insertVeiculos.insertVeiculos(veiculos)

    if err == None:
        return jsonify({"message": f"{str(response)} Veículos inseridos com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500
    
@veiculoBlueprint.route("/veiculos", methods=["DELETE"])
def executeRouteDeleteVeiculos():
    # Get data in JSON request
    veiculos = request.get_json()

    # Basic Validation
    if not checkJson.checkKeysInJson(veiculos):
        return jsonify({"message: ": "Dados incompletos. Certifique-se de incluir num_veiculo e placa para cada veículo a ser cadastrado"}), 400
    
    response, err = deleteVeiculos.deleteVeiculos(veiculos)

    if err == None:
        return jsonify({"message": f"{str(response)} Veículos removidos com sucesso"}), 200
    
    else:
        return jsonify({"message": response}, {"erro": str(err)}), 500    
