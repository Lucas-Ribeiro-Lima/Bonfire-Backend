from domain.entities import Operadora
from domain.exceptions import InvalidIdentifierError
from repositories.interfaces import IRepositoryManager
from services.commands import UpdateConsorcioCommand


class ConsorcioService:
    """Domain service for Consórcio / Operadora use cases."""

    def __init__(self, db_manager: IRepositoryManager):
        self._db_manager = db_manager

    def get_consorcios(self) -> list[Operadora]:
        """Return all registered consórcios as domain entities."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            return repo.get_all()

    def insert_consorcios(self, consorcios: list[Operadora]) -> int:
        """Insert or merge a list of consórcio domain entities in the database."""
        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            return repo.insert_bulk(consorcios)

    def update_consorcios(self, commands: list[UpdateConsorcioCommand]) -> int:
        """Update a list of consórcios in the database from update commands."""
        ids = [cmd.id for cmd in commands]
        if not ids:
            return 0

        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            existing = repo.get_by_ids(ids)
            existing_map = {op.id: op for op in existing}

            updated_ids = set()
            to_update: list[Operadora] = []
            for cmd in commands:
                if cmd.id in existing_map:
                    operadora = existing_map[cmd.id]
                    if cmd.name is not None:
                        operadora.name = cmd.name
                    if cmd.concessionaire is not None:
                        operadora.concessionaire = cmd.concessionaire

                    if cmd.id not in updated_ids:
                        to_update.append(operadora)
                        updated_ids.add(cmd.id)

            if not to_update:
                return 0

            return repo.update_bulk(to_update)

    def delete_consorcio(self, id_consorcio: str | int) -> int:
        """Delete a consórcio from the database by its ID."""
        try:
            id_consorcio_int = int(id_consorcio)
        except ValueError:
            raise InvalidIdentifierError(
                "Consórcio", id_consorcio, message="ID do consórcio inválido"
            )

        with self._db_manager.session() as session:
            repo = session.get_consorcio_repository()
            count = repo.delete(id_consorcio_int)
            return count
