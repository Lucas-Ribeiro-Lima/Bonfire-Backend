import json
from flask import Blueprint, jsonify, request
from handlers import linha, globais
from exceptions.CustomExceptions import CustomException

linhaBlueprint = Blueprint('linha', __name__)
keys_to_check = ["COD_LINH", "ID_OPERADORA", "COMPARTILHADA",  "LINH_ATIV_EMPR"]

@linhaBlueprint.route("/linha", methods=["GET"])
def executeRouteGetLinha():
    try:
        result = linha.getLinha()
        return jsonify({"linha": json.loads(result)})
    except CustomException as e:
        return jsonify(e.to_json()), e.status

@linhaBlueprint.route("/linha", methods=["POST"])
def executeRoutePostLinha():
    try:
        jsonData = request.get_json()
        globais.checkKeysInJson(jsonData, keys_to_check, "linha")
        response = linha.insertLinha(jsonData)
        return jsonify({"message": "linhas inseridas com sucesso", "counter": response}), 201
    except CustomException as e:
        return jsonify(e.to_json()), e.status

    
@linhaBlueprint.route("/linha", methods=["PATCH"])
def executeRouteUpdateLinha():
    try:
        jsonData = request.get_json()
        globais.checkKeysInJson(jsonData, keys_to_check, "linha")
        response = linha.updateLinha(jsonData)
        return jsonify({"message": "linha atualizada com sucesso", "counter": response}), 200
    except CustomException as e:
        return jsonify(e.to_json()), e.status
    

@linhaBlueprint.route("/linha/<string:COD_LINH>", methods=["DELETE"])
def executeRouteDeleteLinha(COD_LINH):
    try:
        response = linha.deleteLinha(COD_LINH)
        return jsonify({"message": "linha deletada com sucesso", "counter": response}), 200
    except CustomException as e:
        return jsonify(e.to_json()), e.status
    
