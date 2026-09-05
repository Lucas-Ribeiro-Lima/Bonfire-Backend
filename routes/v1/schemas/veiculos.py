from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_serializer


class VeiculoItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    NUM_VEIC: int | str = Field(..., description="Número do veículo")
    IDN_PLAC_VEIC: str = Field(..., description="Identificação da placa do veículo")
    VEIC_ATIV_EMPR: bool = Field(
        ..., description="Indica se o veículo está ativo na empresa"
    )
    DAT_BAIX: datetime | str | None = Field(
        None, description="Data de baixa do veículo, se baixado"
    )

    @field_serializer("DAT_BAIX", when_used="json")
    def serialize_dt(self, dt: [datetime | str]) -> str | None:
        return dt.isoformat() if isinstance(dt, datetime) else dt


class VeiculoListResponseDTO(BaseModel):
    veiculos: list[VeiculoItemDTO] = Field(..., description="Lista de veículos")


class VeiculoRequestDTO(BaseModel):
    NUM_VEIC: int | str = Field(..., description="Número do veículo")
    IDN_PLAC_VEIC: str | None = Field(
        None, description="Identificação da placa do veículo"
    )
    VEIC_ATIV_EMPR: bool | None = Field(
        None, description="Indica se o veículo está ativo na empresa"
    )
    DAT_BAIX: str | None = Field(None, description="Data de baixa do veículo")


class VeiculoListRequestDTO(RootModel[list[VeiculoRequestDTO]]):
    pass
