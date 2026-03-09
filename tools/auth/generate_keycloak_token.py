from keycloak import KeycloakOpenID
from classes.Config import config

from sys import argv, exit

usage_msg = '''usage: user password'''

keycloakOpenId = KeycloakOpenID(f"{config.envs["KEYCLOAK_ISSUER"]}/auth",
                                config.envs["KEYCLOAK_REALM_NAME"],
                                config.envs["KEYCLOAK_CLIENT_ID"],
                                config.envs["KEYCLOAK_CLIENT_SECRET"])

#Validate usage
if(len(argv) != 3):
    print("Incorrect usage")
    print(usage_msg)
    exit()

[ user, password ] = argv[1:]

token = keycloakOpenId.token(user, password)
print(token['access_token'])
