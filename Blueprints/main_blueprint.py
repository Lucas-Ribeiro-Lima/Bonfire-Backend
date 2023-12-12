from flask import Blueprint, jsonify, request
from Classes.Repositorio import Repositorio
from Classes.Extractor import Extractor

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def Bonfire():
    return "Bonfire - Autos de Infração"

@main_blueprint.route("/extract", methods=["POST"])
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
