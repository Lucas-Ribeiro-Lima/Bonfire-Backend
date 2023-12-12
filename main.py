from flask import Flask
from routes import *

app = Flask(__name__)

# Registra o blueprint 'main'
app.register_blueprint(autoInfracao.autoInfracao_blueprint)
app.register_blueprint(veiculo.veiculo_blueprint)
app.register

if __name__ == "__main__":
    app.run(debug=True)
