from datetime import date

from pydantic import Field

from domain.entities.base import DomainEntity


class Recurso(DomainEntity):
    """Base domain entity for Appeals."""

    notice_number: str = Field(alias="NUM_AI")
    appeal_number: str = Field(alias="NUM_RECURSO")
    concessionaire_name: str = Field(alias="NOM_CONC")
    result: bool = Field(default=False, alias="RESULTADO")
    publication_date: date = Field(alias="DAT_PUBL")


class RecursoPrimeiraInstancia(Recurso):
    """Pure domain entity for First Instance Appeal."""

    meeting_minute_number: int = Field(alias="NUM_ATA")


class RecursoSegundaInstancia(Recurso):
    """Pure domain entity for Second Instance Appeal."""

    pass
