from flask_cors import CORS
from flask import Flask, Response, request

from routes import autoinfracao, recursos, veiculos, linha, consorcio
from handlers.log import logger, http_logger

from handlers.authenticator import Authenticator, KeyCloakAuthenticator
from repositories.database import check_database_connection


class BonfireApp(Flask):
    _authController: Authenticator
    
    def __init__(self, name: str) -> None:
        logger.info("::Initializing bonfire application::")
        super().__init__(name)
        CORS(self)

        logger.info("::Registering routes::")
        self.register_blueprint(autoinfracao.AutoInfracaoBlueprint)
        self.register_blueprint(recursos.RecursoPrimeiraInstanciaBlueprint)
        self.register_blueprint(recursos.RecuroSegundaInstanciaBlueprint)
        self.register_blueprint(veiculos.veiculoBlueprint) 
        self.register_blueprint(linha.linhaBlueprint)
        self.register_blueprint(consorcio.consorcioBlueprint)

        check_database_connection()
        self._authController = KeyCloakAuthenticator()
        self._authController.checkConnection()

        @self.before_request
        def _():
            return self.checkAuth()

        @self.after_request
        def _(response: Response):
            return self.logRequest(response) 


    def logRequest(self, response: Response):
        http_logger.request(request, response.status_code)
        return response    

    def checkAuth(self):
        logged = self._authController.isAuthenticated(str(request.authorization))
        if not logged: 
            return Response("Unauthorized", status=401)
        pass

