from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    model_validator,
)

from routes.v1.schemas.common import UploadFile, validate_required_file


class InfracaoCsvUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: UploadFile):
        return validate_required_file(
            data, "Arquivo CSV de infrações não está presente na requisição"
        )


class InfracaoXlsUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: UploadFile):
        return validate_required_file(
            data, "Arquivo XLS de infrações não está presente na requisição"
        )


class InfracaoCheckUploadDTO(BaseModel):
    file: UploadFile

    @model_validator(mode="before")
    @classmethod
    def check_file(cls, data: UploadFile):
        return validate_required_file(
            data, "Arquivo CSV de infrações não está presente na requisição"
        )


class InfracaoQueryDTO(BaseModel):
    date: str | None = Field(None, description="Data de ocorrência da infração")
    ai: str | None = Field(None, description="Número do Auto de Infração")


class InfracaoXlsQueryDTO(BaseModel):
    insert_ignore: bool | None = Field(
        True, description="Ignorar infrações duplicadas durante a inserção"
    )


class InfracaoItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    NUM_AI: str | None = Field(None, description="Número do Auto de Infração")
    NUM_NOTF: str | None = Field(None, description="Número da Notificação")
    TIP_PENL: str | None = Field(None, description="Tipo de Penalidade")
    NOM_CONC: str | None = Field(None, description="Nome da Concessionária")
    COD_LINH: str | None = Field(None, description="Código da Linha")
    NOM_LINH: str | None = Field(None, description="Nome da Linha")
    NUM_VEIC: int | None = Field(None, description="Número do Veículo")
    IDN_PLAC_VEIC: str | None = Field(None, description="Placa do Veículo")
    DAT_OCOR_INFR: datetime | str | None = Field(
        None, description="Data de ocorrência da infração"
    )
    DES_LOCA: str | None = Field(None, description="Descrição do Local")
    COD_IRRG_FISC: int | None = Field(
        None, description="Código da irregularidade fiscal"
    )
    ARTIGO: str | None = Field(None, description="Artigo infringido")
    DES_OBSE: str | None = Field(None, description="Observações")
    NUM_MATR_FISC: int | None = Field(None, description="Matrícula do Fiscal")
    QTE_PONT: int | None = Field(None, description="Quantidade de Pontos")
    DAT_EMIS_NOTF: datetime | str | None = Field(
        None, description="Data de emissão da notificação"
    )
    DAT_LIMT_RECU: datetime | str | None = Field(
        None, description="Data limite para recurso"
    )
    VAL_INFR: float | None = Field(None, description="Valor da infração")
    DAT_CANC: datetime | str | None = Field(None, description="Data de cancelamento")

    @field_serializer(
        "DAT_OCOR_INFR",
        "DAT_EMIS_NOTF",
        "DAT_LIMT_RECU",
        "DAT_CANC",
        when_used="json",
    )
    def serialize_dt(self, dt: datetime | str | None) -> str | None:
        return dt.isoformat() if isinstance(dt, datetime) else dt


class InfracaoListResponseDTO(BaseModel):
    autos: list[InfracaoItemDTO] = Field(..., description="Lista de autos de infração")


class InfracaoMessageResponseDTO(BaseModel):
    message: str = Field(
        ..., description="Mensagem descritiva do resultado da operação"
    )


class InfracaoCheckResponseDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    db_rows: str = Field(..., description="Registros encontrados no banco de dados")
    file_rows: str = Field(..., description="Linhas presentes no arquivo analisado")
    Not_Present: str = Field(
        ...,
        serialization_alias="Not Present",
        description="Linhas ausentes ou não encontradas",
    )
