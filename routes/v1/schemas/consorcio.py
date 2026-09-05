from pydantic import BaseModel, ConfigDict, Field, RootModel


class ConsorcioItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int | str = Field(..., description="Identificador do consórcio / operadora")
    NOME: str = Field(..., description="Nome da operadora")
    CONCESSIONARIA: str = Field(..., description="Nome da concessionária")


class ConsorcioListResponseDTO(BaseModel):
    consorcios: list[ConsorcioItemDTO] = Field(
        ..., description="Lista de consórcios cadastrados"
    )


class ConsorcioRequestDTO(BaseModel):
    ID: int | str = Field(..., description="Identificador do consórcio / operadora")
    NOME: str = Field(..., description="Nome da operadora")
    CONCESSIONARIA: str = Field(..., description="Nome da concessionária")


class ConsorcioListRequestDTO(RootModel[list[ConsorcioRequestDTO]]):
    pass
