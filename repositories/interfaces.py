from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from domain.entities import (
        AutoInfracao,
        Linha,
        Operadora,
        RecursoPrimeiraInstancia,
        RecursoSegundaInstancia,
        Veiculo,
    )


class IAutoInfracaoRepository(ABC):
    @abstractmethod
    def get_infracoes(self, date: Any, ai: Any) -> list[AutoInfracao]:
        pass

    @abstractmethod
    def check_presence(self, values: list[str]) -> tuple[int, int, list[str]]:
        pass

    @abstractmethod
    def insert_bulk(self, values: list[AutoInfracao]) -> int:
        pass


class IVeiculoRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Veiculo]:
        pass

    @abstractmethod
    def get_by_id(self, num_veic: int) -> Any:
        pass

    @abstractmethod
    def get_by_ids(self, num_veics: list[int]) -> list[Veiculo]:
        pass

    @abstractmethod
    def insert(self, veiculo: Any) -> bool:
        pass

    @abstractmethod
    def insert_bulk(self, veiculos: list[Veiculo]) -> int:
        pass

    @abstractmethod
    def update_bulk(self, veiculos: list[Veiculo]) -> int:
        pass

    @abstractmethod
    def delete(self, num_veic: int) -> int:
        pass


class ILinhaRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Linha]:
        pass

    @abstractmethod
    def get_by_id(self, cod_linh: str) -> Any:
        pass

    @abstractmethod
    def get_by_ids(self, cod_linhas: list[str]) -> list[Linha]:
        pass

    @abstractmethod
    def insert_bulk(self, linhas: list[Linha]) -> int:
        pass

    @abstractmethod
    def update_bulk(self, linhas: list[Linha]) -> int:
        pass

    @abstractmethod
    def delete(self, cod_linh: str) -> int:
        pass


class IConsorcioRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Operadora]:
        pass

    @abstractmethod
    def get_by_id(self, id_consorcio: int) -> Any:
        pass

    @abstractmethod
    def get_by_ids(self, ids_consorcios: list[int]) -> list[Operadora]:
        pass

    @abstractmethod
    def insert_bulk(self, consorcios: list[Operadora]) -> int:
        pass

    @abstractmethod
    def update_bulk(self, consorcios: list[Operadora]) -> int:
        pass

    @abstractmethod
    def delete(self, id_consorcio: int) -> int:
        pass


class IRecursoRepository(ABC):
    @abstractmethod
    def get_primeira_instancia(
        self, date: Any, ata: Any
    ) -> list[RecursoPrimeiraInstancia]:
        pass

    @abstractmethod
    def get_segunda_instancia(self, date: Any) -> list[RecursoSegundaInstancia]:
        pass

    @abstractmethod
    def insert_primeira_instancia(self, rows: list[RecursoPrimeiraInstancia]) -> int:
        pass

    @abstractmethod
    def insert_segunda_instancia(self, rows: list[RecursoSegundaInstancia]) -> int:
        pass


class IRepositorySession(ABC):
    @abstractmethod
    def __enter__(self) -> "IRepositorySession":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def get_autoinfracao_repository(self) -> IAutoInfracaoRepository:
        pass

    @abstractmethod
    def get_veiculo_repository(self) -> IVeiculoRepository:
        pass

    @abstractmethod
    def get_linha_repository(self) -> ILinhaRepository:
        pass

    @abstractmethod
    def get_consorcio_repository(self) -> IConsorcioRepository:
        pass

    @abstractmethod
    def get_recurso_repository(self) -> IRecursoRepository:
        pass


class IRepositoryManager(ABC):
    @abstractmethod
    def session(self) -> AbstractContextManager[IRepositorySession]:
        pass

    @abstractmethod
    def check_connection(self) -> None:
        pass
