from flask import Blueprint, jsonify, request
from handlers.veiculos import *

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/veiculo", methods=["GET"])
def getVeiculo():
    getVeiculos()

@main_blueprint.route("/veiculo", methods=["POST"])
def postVeiculos():
    # Get data in JSON request
    veiculos = request.get_json()

    # Basic Validation
    if "veiculo" not in veiculos or "num_veiculo" not in veiculos["veiculo"] or "placa" not in veiculos["veiculo"]:
        return jsonify({"Dados incompletos. Certifique-se de incluir veiculo, num_veiculo e placa."}), 400
    else:
        for i in veiculos:
             postVeiculo(i)
    return jsonify({"message": "Veículos inseridos com sucesso"}), 200