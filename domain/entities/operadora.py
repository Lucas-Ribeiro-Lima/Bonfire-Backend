from pydantic import Field

from domain.entities.base import DomainEntity


class Operadora(DomainEntity):
    """Pure domain entity for Operadora (Consórcio)."""

    id: int = Field(alias="ID")
    name: str = Field(default="", alias="NOME")
    concessionaire: str = Field(default="", alias="CONCESSIONARIA")
