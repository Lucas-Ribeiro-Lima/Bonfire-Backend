from controllers.http.app import BonfireApp, create_bonfire_app
from controllers.http.v1 import autoinfracao, consorcio, linha, recursos, veiculos

__all__ = [
    "BonfireApp",
    "create_bonfire_app",
    "autoinfracao",
    "recursos",
    "veiculos",
    "linha",
    "consorcio",
]
