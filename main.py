from flask import Flask
from routes import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Registra o blueprint 'main'
app.register_blueprint(autoInfracaoPrimeiraInstancia.autoInfracaoPrimeiraInstanciaBlueprint)
app.register_blueprint(autoInfracaoSegundaInstancia.autoInfracaoSegundaInstanciaBlueprint)
app.register_blueprint(veiculo.veiculoBlueprint)

if __name__ == "__main__":
    app.run(debug=True)
