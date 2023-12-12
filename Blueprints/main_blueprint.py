from flask import Blueprint, jsonify, request
from Classes.Repositorio import Repositorio
from Classes.Extractor import Extractor
from Classes.Veiculo import Veiculo

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def Bonfire():
    return "Bonfire - Autos de Infração"

@main_blueprint.route("/postAutos", methods=["POST"])
def extract_and_store():
    
    
    # Verifica se o arquivo está presente na requisição
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 401

    file = request.files['file']

    # Verifica se o arquivo tem uma extensão válida (PDF)
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({"error": "Arquivo inválido"}), 402

    repositorio = Repositorio()
    try:

        # Extrai as informações do PDF e armazena no banco de dados
        auto_infracao_list = Extractor.parse_pdf(file.stream)
        for auto_infracao_data in auto_infracao_list:
            repositorio.insert_auto_infracao(auto_infracao_data)

        return jsonify({"message": "Extração e armazenamento concluídos com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": f"Um erro ocorreu: {e}"}), 500

    finally:
        repositorio.close_connection()

@main_blueprint.route("/getVeiculo", methods=["GET"])
def get_veiculo():
    try:
        with Repositorio() as repositorio:
            veiculo = repositorio.get_veiculo()
            return jsonify({"veiculo": veiculo}), 200
    
    except Exception as e:
        return jsonify({"error": f"Um erro ocorreu: {e}"}), 500

@main_blueprint.route("/postVeiculo", methods=["POST"])
def insert_veiculo():
    try:
        # Obtém os dados enviados na requisição POST
        data = request.get_json()

        # Validação básica dos dados
        if "veiculo" not in data or "num_veiculo" not in data["veiculo"] or "placa" not in data["veiculo"]:
            raise ValueError("Dados incompletos. Certifique-se de incluir veiculo, num_veiculo e placa.")

        # Extrai os dados do veiculo
        veiculo_data = data["veiculo"]
        veiculo = Veiculo(num_veiculo=veiculo_data["num_veiculo"], placa=veiculo_data["placa"])

        # Cria uma instância do Repositorio e insere o veículo
        with Repositorio() as repositorio:
            repositorio.insert_veiculo(veiculo)

        # Retorna uma resposta de sucesso
        return jsonify({"message": "Veículo inserido com sucesso"}), 200

    except Exception as e:
        # Retorna uma resposta de erro em caso de exceção
        return jsonify({"error": f"Um erro ocorreu: {e}"}), 500