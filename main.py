from flask import Flask
from routes import *

app = Flask(__name__)

# Registra o blueprint 'main'
app.register_blueprint(autoInfracaoPrimeiraInstancia.autoInfracaoPrimeiraInstanciaBlueprint)
app.register_blueprint(veiculo.veiculoBlueprint)

if __name__ == "__main__":
    app.run(debug=True)
