from flask import Flask
from Routes import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Registra o blueprint 'main'
app.register_blueprint(autoInfracaoPrimeiraInstancia.autoInfracaoPrimeiraInstanciaBlueprint)
app.register_blueprint(autoInfracaoSegundaInstancia.autoInfracaoSegundaInstanciaBlueprint)
app.register_blueprint(veiculos.veiculoBlueprint) 
app.register_blueprint(linha.linhaBlueprint)

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)