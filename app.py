from flask import Flask
from routes import *
from flask_cors import CORS
from routes import autoinfracao, recursos, veiculos, linha

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registra o blueprint 'main'
    app.register_blueprint(autoinfracao.AutoInfracaoBlueprint)
    app.register_blueprint(recursos.RecursoPrimeiraInstanciaBlueprint)
    app.register_blueprint(veiculos.veiculoBlueprint) 
    app.register_blueprint(linha.linhaBlueprint)

    return app
