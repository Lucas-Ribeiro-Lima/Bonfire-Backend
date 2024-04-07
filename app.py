from flask import Flask
from routes import *
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registra o blueprint 'main'
    app.register_blueprint(autoInfracaoPrimeiraInstancia.autoInfracaoPrimeiraInstanciaBlueprint)
    app.register_blueprint(autoInfracaoSegundaInstancia.autoInfracaoSegundaInstanciaBlueprint)
    app.register_blueprint(veiculos.veiculoBlueprint) 
    app.register_blueprint(linha.linhaBlueprint)

    return app
