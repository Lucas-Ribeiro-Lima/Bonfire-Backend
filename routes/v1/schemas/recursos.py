from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    model_serializer,
    model_validator,
)

from routes.v1.schemas.common import UploadFile, validate_required_file


class RecursoPrimeiraInstanciaUploadDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: UploadFile):
        return validate_required_file(
            data,
            "Arquivo de resultado de primeira instancia não está presente na requisição",
        )


class RecursoSegundaInstanciaUploadDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: UploadFile):
        return validate_required_file(
            data,
            "Arquivo de resultado de segunda instancia não está presente na requisição",
        )


class RecursoPrimeiraInstanciaQueryDTO(BaseModel):
    date: str | None = Field(None, description="Data de publicação do recurso")
    ata: str | None = Field(None, description="Número da ata da sessão")


class RecursoSegundaInstanciaQueryDTO(BaseModel):
    date: str | None = Field(None, description="Data de publicação do recurso")


class RecursoItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    NUM_AI: str | None = Field(None, description="Número do Auto de Infração")
    NUM_ATA: int | str | None = Field(None, description="Número da ata da sessão")
    NUM_RECURSO: str | None = Field(None, description="Número do recurso")
    NOM_CONC: str | None = Field(None, description="Nome da concessionária")
    RESULTADO: bool | None = Field(None, description="Resultado do recurso")
    DAT_PUBL: date | datetime | str | None = Field(
        None, description="Data de publicação do recurso"
    )
    COD_LINH: str | None = Field(None, description="Código da linha")
    NUM_VEIC: int | str | None = Field(None, description="Número do veículo")
    IDN_PLAC_VEIC: str | None = Field(None, description="Placa do veículo")

    @field_serializer("DAT_PUBL", when_used="json")
    def serialize_date(self, dt: date | datetime | str | None) -> str | None:
        return (
            dt.isoformat() if isinstance(dt, datetime) or isinstance(dt, date) else dt
        )

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        data = handler(self)
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if v is not None}
        return data


class RecursoListResponseDTO(BaseModel):
    recurses: list[RecursoItemDTO] = Field(
        ..., description="Lista de recursos encontrados"
    )
