from abc import abstractmethod, ABC
from typing import override

from handlers.log import logger

class Authenticator(ABC):
    @abstractmethod
    def isAuthenticated(self, token: str) -> bool:
        pass

    @abstractmethod
    def checkConnection(self):
        pass


from classes.Config import config
from keycloak import KeycloakOpenID, KeycloakRPTNotFound

class KeyCloakAuthenticator(Authenticator):
    def __init__(self):
        logger.info("::Configuring Keycloak session::")
        self.keycloakOpenId = KeycloakOpenID(f"{config.envs["KEYCLOAK_ISSUER"]}/auth",
                                config.envs["KEYCLOAK_REALM_NAME"],
                                config.envs["KEYCLOAK_CLIENT_ID"],
                                config.envs["KEYCLOAK_CLIENT_SECRET"])
        logger.info("::Keycloak connection estabilished::")

    @override
    def isAuthenticated(self, token: str) -> bool:
        try:
            [ method, token ] = token.split(' ')
            if method != "Bearer":
                return False

            userInfo: dict[str, str | bool] = self.keycloakOpenId.introspect(token)
            return userInfo["active"] == True
        except:
            return False

    @override
    def checkConnection(self):
        try:
            logger.info("::Checking Keycloak connection::")
            #Try to get well-know form the server
            _ = self.keycloakOpenId.well_known()
        except KeycloakRPTNotFound as e:
            logger.error("::Keycloak connection failed::")
            logger.error(str(e.error_message))

            raise
        finally:
            return
