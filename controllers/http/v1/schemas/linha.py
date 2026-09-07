from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_serializer


class LinhaItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    COD_LINH: str = Field(..., description="Código identificador da linha")
    ID_OPERADORA: int | str | None = Field(
        None, description="Identificador da operadora associada"
    )
    COMPARTILHADA: bool | None = Field(
        False, description="Indica se a linha é compartilhada"
    )
    LINH_ATIV_EMPR: bool | None = Field(
        True, description="Indica se a linha está ativa na empresa"
    )
    DAT_BAIX: datetime | str | None = Field(None, description="Data de baixa da linha")

    @field_serializer("DAT_BAIX", when_used="json")
    def serialize_dt(self, dt: datetime | str | None) -> str | None:
        return dt.isoformat() if isinstance(dt, datetime) else dt


class LinhaListResponseDTO(BaseModel):
    linha: list[LinhaItemDTO] = Field(..., description="Lista de linhas")


class LinhaRequestDTO(BaseModel):
    COD_LINH: str = Field(..., description="Código identificador da linha")
    ID_OPERADORA: int | None = Field(
        None, description="Identificador da operadora associada"
    )
    COMPARTILHADA: bool | None = Field(
        None, description="Indica se a linha é compartilhada"
    )
    LINH_ATIV_EMPR: bool | None = Field(
        None, description="Indica se a linha está ativa na empresa"
    )
    DAT_BAIX: str | None = Field(None, description="Data de baixa da linha")


class LinhaListRequestDTO(RootModel[list[LinhaRequestDTO]]):
    pass
