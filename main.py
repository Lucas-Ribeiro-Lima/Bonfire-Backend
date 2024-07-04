from flask import Flask
from routes import autoInfracaoPrimeiraInstancia, autoInfracaoSegundaInstancia, veiculos, linha, consorcio
from flask_cors import CORS

from routes import consorcio

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registra o blueprint 'main'
    app.register_blueprint(autoInfracaoPrimeiraInstancia.autoInfracaoPrimeiraInstanciaBlueprint)
    app.register_blueprint(autoInfracaoSegundaInstancia.autoInfracaoSegundaInstanciaBlueprint)
    app.register_blueprint(veiculos.veiculoBlueprint) 
    app.register_blueprint(linha.linhaBlueprint)
    app.register_blueprint(consorcio.consorcioBlueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    # serve(app, host="0.0.0.0", port=5000)