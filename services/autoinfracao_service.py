from typing import Any

import pandas as pd

from classes.AutoInfracao import AutoInfracao
from exceptions.CustomExceptions import ErrReadingFile
from repositories.interfaces import IRepositoryManager


class AutoInfracaoService:
    """Domain service for Traffic Infraction Notice use cases."""

    def __init__(self, db_manager: IRepositoryManager, parser_factory=None):
        self._parser_factory = parser_factory
        self._db_manager = db_manager

    def get_infracoes(
        self, date: str | None = None, ai: str | None = None
    ) -> list[AutoInfracao]:
        """Retrieve infraction notices."""
        with self._db_manager.session() as session:
            repo = session.get_autoinfracao_repository()
            return repo.get_infracoes(date, ai)

    def check_infracoes(self, file_stream: Any) -> tuple[int, int, list[str]]:
        """Verify presence of infraction notices in database from a CSV file stream."""
        try:
            data_frame = pd.read_csv(file_stream, header=0, delimiter=";")
            values = data_frame["NUM_AI"].unique().tolist()
        except Exception as e:
            raise ErrReadingFile(f"Erro ao ler o arquivo CSV. {e}", 500)

        with self._db_manager.session() as session:
            repo = session.get_autoinfracao_repository()
            rows_counter, counter, rows_not_present = repo.check_presence(values)
            return rows_counter, counter, rows_not_present

    def extract_csv(self, file_stream: Any, ignore: bool = False) -> dict:
        if not self._parser_factory:
            raise RuntimeError("ParserFactory not injected")
        extractor = self._parser_factory.create_infracoes_csv_parser(ignore=ignore)
        return extractor.extract(file_stream)

    def extract_xls(self, file_stream: Any, ignore: bool = False) -> dict:
        if not self._parser_factory:
            raise RuntimeError("ParserFactory not injected")
        extractor = self._parser_factory.create_infracoes_xls_parser(ignore=ignore)
        return extractor.extract(file_stream)
