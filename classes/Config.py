from os import getenv 
from exceptions.CustomExceptions import ErrMissingRequiredEnv

env_default_variables = { 
    "DB_DRIVER": "mysql",
    "DB_HOST": "bonfire-db", 
    "DB_PORT": "3306",
    "DB_NAME": "bonfire",
    "DB_USER": "bonfire", 
    "DB_PASSWORD": None,

    # auth
    "KEYCLOAK_ISSUER": "http://keycloak:8080",
    "KEYCLOAK_CLIENT_ID": "bonfire",
    "KEYCLOAK_CLIENT_SECRET": None,
    "KEYCLOAK_REALM_NAME": None,
}

class Config:
    def __init__(self):
        self.envs: dict[str, str] = {}
        for env in env_default_variables:
            value = getenv(env, env_default_variables[env]) 
            if not value:
                raise ErrMissingRequiredEnv("ERROR::Missing required env: " + env)

            self.envs[env] = value

config = Config()

#  Example
#  
#  "driver": "mysql",
#  "host": "192.168.0.11",
#  "port": "3306",
#  "database": "bonfire",
#  "user": "bonfire",
#   "password": "strong-password"
#   
# 

