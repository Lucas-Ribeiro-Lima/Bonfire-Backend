from domain.entities import Linha
from domain.exceptions import DuplicateEntityError, RelatedEntityNotFoundError
from repositories.interfaces import (
    IConsorcioRepository,
    ILinhaRepository,
    IRepositoryManager,
)
from services.commands import UpdateLinhaCommand


class LinhaService:
    """Domain service for Bus Line use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def _check_operadora_id_missing(
        self, items: list[Linha] | list[UpdateLinhaCommand], repo: IConsorcioRepository
    ) -> None:
        operadoras_ids = {
            item.operator_id for item in items if item.operator_id is not None
        }
        if operadoras_ids:
            existing_operadoras = repo.get_by_ids([op for op in operadoras_ids])
            existent_ids = {op.id for op in existing_operadoras}

            missing = operadoras_ids - existent_ids
            if missing:
                raise RelatedEntityNotFoundError("Consórcio", list(missing))

    def get_linha(self) -> list[Linha]:
        """Retrieve all bus lines from the repository."""
        with self._db_manager.session() as session:
            linha_repo = session.get_linha_repository()
            return linha_repo.get_all()

    def insert_linha(self, lines: list[Linha]) -> int:
        """Insert a batch of new lines into the repository after domain checks."""
        with self._db_manager.session() as session:
            line_repo: ILinhaRepository = session.get_linha_repository()
            cons_repo: IConsorcioRepository = session.get_consorcio_repository()

            self._check_operadora_id_missing(lines, cons_repo)

            cod_linhas = [item.line_code for item in lines]
            if cod_linhas:
                existing = line_repo.get_by_ids(cod_linhas)
                if existing:
                    existent_ids = [item.line_code for item in existing]
                    raise DuplicateEntityError("Linha", existent_ids)

            if not lines:
                return 0

            return line_repo.insert_bulk(lines)

    def update_linha(self, commands: list[UpdateLinhaCommand]) -> int:
        """Update bus lines based on a list of UpdateLinhaCommand."""
        if not commands:
            return 0

        with self._db_manager.session() as session:
            linha_repo = session.get_linha_repository()
            cons_repo = session.get_consorcio_repository()
            self._check_operadora_id_missing(commands, cons_repo)

            cod_linhas = [cmd.line_code for cmd in commands]
            if not cod_linhas:
                return 0

            existing = linha_repo.get_by_ids(cod_linhas)
            existing_map = {linha.line_code: linha for linha in existing}

            updated_codes = set()
            to_update: list[Linha] = []
            for cmd in commands:
                if cmd.line_code in existing_map:
                    linha = existing_map[cmd.line_code]
                    if cmd.shared is not None:
                        linha.shared = cmd.shared
                    if cmd.operator_id is not None:
                        linha.operator_id = cmd.operator_id
                    if cmd.active is not None:
                        if not cmd.active:
                            linha.deactivate(cmd.deregistration_date)
                        else:
                            linha.activate()
                    elif cmd.deregistration_date is not None:
                        linha.deregistration_date = cmd.deregistration_date

                    if cmd.line_code not in updated_codes:
                        to_update.append(linha)
                        updated_codes.add(cmd.line_code)

            if not to_update:
                return 0

            return linha_repo.update_bulk(to_update)

    def delete_linha(self, cod_linh: str) -> int:
        """Delete a line from the database by its line code."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.delete(cod_linh)
