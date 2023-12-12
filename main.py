from flask import Flask
from Blueprints.main_blueprint import main_blueprint

app = Flask(__name__)

# Registra o blueprint 'main'
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
