from pydantic import Field

from domain.entities.base import DomainEntity


class Operadora(DomainEntity):
    """Pure domain entity for Operadora (Consórcio)."""

    id: int = Field(alias="ID")
    name: str = Field(default="", alias="NOME")
    concessionaire: str = Field(default="", alias="CONCESSIONARIA")

    def get_id(self) -> int:
        return self.id

    def set_id(self, value: int | str) -> None:
        self.id = int(value)

    def get_name(self) -> str:
        return self.name

    def set_name(self, value: str) -> None:
        self.name = str(value)

    def get_concessionaire(self) -> str:
        return self.concessionaire

    def set_concessionaire(self, value: str) -> None:
        self.concessionaire = str(value)
