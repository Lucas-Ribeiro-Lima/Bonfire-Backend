from os import getenv 
from exceptions.CustomExceptions import ErrMissingRequiredEnv

env_variables = { 
    "DB_DRIVER": "mysql",
    "DB_HOST": "bonfire-db", 
    "DB_PORT": "3306",
    "DB_NAME": "bonfire",
    "DB_USER": "bonfire", 
    "DB_PASSWORD": None 
}

class Config:
    def __init__(self):
        self.envs = {}
        return

    @staticmethod
    def loadConfig():
        config = Config()

        for env in env_variables:
            value = getenv(env, env_variables[env]) 
            if not value:
                raise ErrMissingRequiredEnv("ERROR::Missing required env: " + env)

            config.envs[env] = value

        return config


config = Config.loadConfig()

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

