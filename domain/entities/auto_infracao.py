from datetime import datetime

from pydantic import Field

from domain.entities.base import DomainEntity


class AutoInfracao(DomainEntity):
    """Pure domain entity for Traffic Infraction Notice."""

    notice_number: str = Field(alias="NUM_AI")
    notification_number: str | int = Field(..., alias="NUM_NOTF")
    penalty_type: str = Field(..., alias="TIP_PENL")
    concessionaire_name: str = Field(..., alias="NOM_CONC")
    line_code: str | int = Field(..., alias="COD_LINH")
    line_name: str = Field(..., alias="NOM_LINH")
    vehicle_number: int | None = Field(default=None, alias="NUM_VEIC")
    license_plate: str | None = Field(default=None, alias="IDN_PLAC_VEIC")
    infraction_date: datetime | None = Field(default=None, alias="DAT_OCOR_INFR")
    location_description: str | None = Field(default=None, alias="DES_LOCA")
    irregularity_code: int = Field(..., alias="COD_IRRG_FISC")
    article: str = Field(..., alias="ARTIGO")
    observation: str | None = Field(default=None, alias="DES_OBSE")
    inspector_registration: int | None = Field(default=None, alias="NUM_MATR_FISC")
    points: int = Field(..., alias="QTE_PONT")
    notification_emission_date: datetime = Field(..., alias="DAT_EMIS_NOTF")
    appeal_limit_date: datetime = Field(..., alias="DAT_LIMT_RECU")
    infraction_value: float = Field(..., alias="VAL_INFR")
    cancellation_date: datetime | None = Field(default=None, alias="DAT_CANC")
