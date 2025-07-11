from argparse import ArgumentParser
from waitress import serve
from flask import Flask
from flask_cors import CORS
from routes import autoInfracaoPrimeiraInstancia, autoInfracaoSegundaInstancia, veiculos, linha, consorcio

parser = ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--port", type=int, default=5000, help="Server port")

args = parser.parse_args()

app = Flask(__name__)
CORS(app)

# Registra o blueprint 'main'
app.register_blueprint(autoInfracaoPrimeiraInstancia.autoInfracaoPrimeiraInstanciaBlueprint)
app.register_blueprint(autoInfracaoSegundaInstancia.autoInfracaoSegundaInstanciaBlueprint)
app.register_blueprint(veiculos.veiculoBlueprint) 
app.register_blueprint(linha.linhaBlueprint)
app.register_blueprint(consorcio.consorcioBlueprint)

if args.debug:
    app.run(debug=True, port=args.port)
else:
    serve(app, host="0.0.0.0", port=args.port)