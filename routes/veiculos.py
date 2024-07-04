import json
from flask import Blueprint, jsonify, request
from handlers import veiculos
from handlers import globais
from exceptions.CustomExceptions import CustomException

veiculoBlueprint = Blueprint('veiculo', __name__)
keys_to_check = ["NUM_VEIC", "IDN_PLAC_VEIC", "VEIC_ATIV_EMPR"]

@veiculoBlueprint.route("/veiculos", methods=["GET"])
def executeRouteGetVeiculo():
    try:
        result = veiculos.getVeiculos()
        return jsonify({"veiculos": json.loads(result)})
    except CustomException as e:
        return jsonify(e.to_json()), e.status

@veiculoBlueprint.route("/veiculos", methods=["POST"])
def executeRoutePostVeiculos():
    try:
        jsonData = request.get_json()
        globais.checkKeysInJson(jsonData, keys_to_check, "veiculo")
        response = veiculos.insertVeiculos(jsonData)
        return jsonify({"message": "Veículos inseridos com sucesso", "counter": response}), 201
    except CustomException as e:
        return jsonify(e.to_json()), e.status
    
    
@veiculoBlueprint.route("/veiculos", methods=["PATCH"])
def executeRoutePatchVeiculos():
    try:
        jsonData = request.get_json()
        globais.checkKeysInJson(jsonData, keys_to_check, "veiculo")
        response = veiculos.updateVeiculos(jsonData)
        return jsonify({"message": "Veículos atualizados com sucesso", "counter": response}), 202    
    except CustomException as e:
        return jsonify(e.to_json()), e.status
    
@veiculoBlueprint.route("/veiculos", methods=["DELETE"])
def executeRouteDeleteVeiculos():
    try:
        jsonData = request.get_json()
        response = veiculos.deleteVeiculos(jsonData)
        return jsonify({"message": "Veículos deletados com sucesso", "counter": response}), 202
    except CustomException as e:
        return jsonify(e.to_json()), e.status
