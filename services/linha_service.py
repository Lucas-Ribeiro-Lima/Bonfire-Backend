from domain.entities import Linha
from domain.exceptions import DuplicateEntityError, RelatedEntityNotFoundError
from repositories.interfaces import (
    IConsorcioRepository,
    ILinhaRepository,
    IRepositoryManager,
)


class LinhaService:
    """Domain service for Bus Line use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def _check_operadora_id_missing(
        self, lines: list[Linha], repo: IConsorcioRepository
    ) -> None:
        operadoras_ids = {
            line.get_operator_id() for line in lines if line.operator_id is not None
        }
        if operadoras_ids:
            existing_operadoras = repo.get_by_ids(
                [op for op in operadoras_ids if op is not None]
            )
            existent_ids = {op.id for op in existing_operadoras if op.id is not None}

            missing = operadoras_ids - existent_ids
            if missing:
                missing_str = ", ".join(str(f) for f in missing)
                raise RelatedEntityNotFoundError(
                    "Operadora",
                    list(missing),
                    message=f"Não é possível prosseguir. Os seguintes consórcios/operadoras não existem: {missing_str}",
                )

    def _check_linha_does_not_exists(
        self, lines: list[Linha], repo: ILinhaRepository
    ) -> None:
        new_ids = [line.line_code for line in lines if line.line_code is not None]
        existents = repo.get_by_ids(new_ids)
        if existents:
            lines_existents = ", ".join(
                e.line_code for e in existents if e.line_code is not None
            )
            raise DuplicateEntityError(
                "Linha",
                [e.line_code for e in existents if e.line_code is not None],
                message=f"As seguintes linhas já existem e não podem ser sobrescritas: {lines_existents}",
            )

    def get_linha(self) -> list[Linha]:
        """Retrieve line data from the database as domain entities."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.get_all()

    def insert_linha(self, lines: list[Linha]) -> int:
        """Insert a list of line domain entities into the database."""
        with self._db_manager.session() as session:
            line_repo = session.get_linha_repository()
            cons_repo = session.get_consorcio_repository()
            self._check_operadora_id_missing(lines, cons_repo)
            self._check_linha_does_not_exists(lines, line_repo)

            if not lines:
                return 0

            return line_repo.insert_bulk(lines)

    def update_linha(self, lines: list[Linha]) -> int:
        """Update a list of line domain entities in the database."""
        with self._db_manager.session() as session:
            linha_repo = session.get_linha_repository()
            cons_repo = session.get_consorcio_repository()
            self._check_operadora_id_missing(lines, cons_repo)

            cod_linhas = [
                item.line_code for item in lines if isinstance(item.line_code, str)
            ]
            if not cod_linhas:
                return 0

            existing = linha_repo.get_by_ids(cod_linhas)
            existing_map = {
                linha.line_code: linha
                for linha in existing
                if linha.line_code is not None
            }

            updated_codes = set()
            to_update: list[Linha] = []
            for item in lines:
                if item.line_code is not None and item.line_code in existing_map:
                    linha = existing_map[item.line_code]
                    if item.shared is not None:
                        linha.set_shared(item.shared)
                    if item.operator_id is not None:
                        linha.set_operator_id(item.operator_id)
                    if item.active is not None:
                        if not item.active:
                            linha.deactivate(item.deregistration_date)
                        else:
                            linha.activate()
                    elif item.deregistration_date is not None:
                        linha.set_deregistration_date(item.deregistration_date)

                    if item.line_code not in updated_codes:
                        to_update.append(linha)
                        updated_codes.add(item.line_code)

            if not to_update:
                return 0

            return linha_repo.update_bulk(to_update)

    def delete_linha(self, cod_linh: str) -> int:
        """Delete a line from the database by its line code."""
        with self._db_manager.session() as session:
            repo = session.get_linha_repository()
            return repo.delete(cod_linh)
