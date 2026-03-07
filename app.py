from flask import Flask, Response, request
from flask_cors import CORS

from routes import autoinfracao, recursos, veiculos, linha, consorcio
from handlers.log import http_logger
from repositories.database import check_connection


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registra o blueprint 'main'
    logger.info("::Registering routes::")
    app.register_blueprint(autoinfracao.AutoInfracaoBlueprint)
    app.register_blueprint(recursos.RecursoPrimeiraInstanciaBlueprint)
    app.register_blueprint(veiculos.veiculoBlueprint) 
    app.register_blueprint(linha.linhaBlueprint)
    app.register_blueprint(consorcio.consorcioBlueprint)

    check_connection()

    @app.after_request
    def _(response: Response):
        http_logger.request(request, response.status_code)
        return response    

    return app
