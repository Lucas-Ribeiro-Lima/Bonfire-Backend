from contextlib import contextmanager
from typing import Any, Iterator

from repositories.interfaces import (
    IAutoInfracaoRepository,
    IConsorcioRepository,
    ILinhaRepository,
    IRecursoRepository,
    IRepositoryManager,
    IRepositorySession,
    IVeiculoRepository,
)


class FakeAutoInfracaoRepository(IAutoInfracaoRepository):
    def __init__(self):
        self.data: list[dict[str, Any]] = []

    def get_infracoes(self, date: Any, ai: Any) -> list[Any]:
        class FakeInfracao:
            def __init__(self, data):
                self._data = data

        return [FakeInfracao(d) for d in self.data]

    def check_presence(self, values: list[str]) -> tuple[int, int, list[str]]:
        existing = {d.get("NUM_AI") for d in self.data}
        rows_not_present = [v for v in values if v not in existing]
        return len(existing), len(values), rows_not_present

    def insert_bulk(self, records) -> int:
        self.data.extend(records)
        return len(records)

    def insert_bulk_rows(self, rows: list[dict[str, Any]], ignore: bool = False) -> int:
        self.data.extend(rows)
        return len(rows)


class FakeVeiculoRepository(IVeiculoRepository):
    def get_all(self):
        return []

    def get_by_id(self, num_veic):
        return None

    def get_by_ids(self, num_veics):
        return []

    def insert(self, veiculo):
        return True

    def insert_bulk(self, data):
        return len(data)

    def update_bulk(self, data):
        return len(data)

    def delete(self, num_veic):
        return 1


class FakeLinhaRepository(ILinhaRepository):
    def get_all(self):
        return []

    def get_by_id(self, cod_linh):
        return None

    def get_by_ids(self, cod_linhas):
        return []

    def insert_bulk(self, data):
        return len(data)

    def update_bulk(self, data):
        return len(data)

    def delete(self, cod_linh):
        return 1


class FakeConsorcioRepository(IConsorcioRepository):
    def get_all(self):
        return []

    def get_by_id(self, id_consorcio):
        return None

    def get_by_ids(self, ids_consorcios):
        return []

    def insert_bulk(self, data):
        return len(data)

    def update_bulk(self, data):
        return len(data)

    def delete(self, id_consorcio):
        return 1


class FakeRecursoRepository(IRecursoRepository):
    def get_primeira_instancia(self, date, ata):
        return []

    def get_segunda_instancia(self, date):
        return []

    def insert_primeira_instancia(self, rows):
        return len(rows)

    def insert_segunda_instancia(self, rows):
        return len(rows)


class FakeRepositorySession(IRepositorySession):
    def __init__(self):
        self.autoinfracao = FakeAutoInfracaoRepository()
        self.veiculo = FakeVeiculoRepository()
        self.linha = FakeLinhaRepository()
        self.consorcio = FakeConsorcioRepository()
        self.recurso = FakeRecursoRepository()

    def __enter__(self) -> "IRepositorySession":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_autoinfracao_repository(self) -> IAutoInfracaoRepository:
        return self.autoinfracao

    def get_veiculo_repository(self) -> IVeiculoRepository:
        return self.veiculo

    def get_linha_repository(self) -> ILinhaRepository:
        return self.linha

    def get_consorcio_repository(self) -> IConsorcioRepository:
        return self.consorcio

    def get_recurso_repository(self) -> IRecursoRepository:
        return self.recurso


class FakeRepositoryManager(IRepositoryManager):
    def __init__(self):
        self._session = FakeRepositorySession()

    @contextmanager
    def session(self) -> Iterator[IRepositorySession]:
        with self._session as s:
            yield s

    def check_connection(self) -> None:
        pass
