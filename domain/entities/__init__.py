from domain.entities.auto_infracao import AutoInfracao
from domain.entities.base import DomainEntity
from domain.entities.linha import Linha
from domain.entities.operadora import Operadora
from domain.entities.recurso import (
    Recurso,
    RecursoPrimeiraInstancia,
    RecursoSegundaInstancia,
)
from domain.entities.veiculo import Veiculo

__all__ = [
    "DomainEntity",
    "AutoInfracao",
    "Linha",
    "Operadora",
    "Recurso",
    "RecursoPrimeiraInstancia",
    "RecursoSegundaInstancia",
    "Veiculo",
]
