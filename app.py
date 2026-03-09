from flask_cors import CORS
from flask import Flask, Response, request
from keycloak import KeycloakOpenID

from routes import autoinfracao, recursos, veiculos, linha, consorcio
from handlers.log import logger, http_logger

from repositories.database import check_database_connection
from classes.Config import config

keycloakOpenId = KeycloakOpenID(f"{config.envs["KEYCLOAK_ISSUER"]}/auth",
                                config.envs["KEYCLOAK_REALM_NAME"],
                                config.envs["KEYCLOAK_CLIENT_ID"],
                                config.envs["KEYCLOAK_CLIENT_SECRET"])

class BonfireApp(Flask):
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
        [ method, token ] = str(request.authorization).split(' ')

        if method != "Bearer":
            return Response("Unauthorized", status=401)

        userInfo = keycloakOpenId.introspect(token)
        if not userInfo["active"]:
            return Response("Unauthorized", status=401)

        pass
