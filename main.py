from argparse import ArgumentParser
from waitress import serve
from flask import Flask
from flask_cors import CORS
from routes import autoinfracao, recursos, veiculos, linha, consorcio
from repositories.database import check_connection
from handlers.log import logger

logger.info("::Initializing bonfire application::")

parser = ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--port", type=int, default=5000, help="Server port")

args = parser.parse_args()

app = Flask(__name__)
CORS(app)

# Registra o blueprint 'main'
logger.info("::Registering routes::")
app.register_blueprint(autoinfracao.AutoInfracaoBlueprint)
app.register_blueprint(recursos.RecursoPrimeiraInstanciaBlueprint)
app.register_blueprint(recursos.RecuroSegundaInstanciaBlueprint)
app.register_blueprint(veiculos.veiculoBlueprint) 
app.register_blueprint(linha.linhaBlueprint)
app.register_blueprint(consorcio.consorcioBlueprint)

check_connection()

logger.info(f"::Application listening on {args.port}::")
if args.debug:
    app.run(debug=True, port=args.port)
else:
    serve(app, host="0.0.0.0", port=args.port)

