from sqlalchemy.orm import Session

from domain.entities import Operadora
from repositories.interfaces import IConsorcioRepository
from repositories.models.operadora_model import OperadoraModel


class ConsorcioRepository(IConsorcioRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: OperadoraModel) -> Operadora:
        return Operadora(
            ID=int(model.ID),
            NOME=str(model.NOME or ""),
            CONCESSIONARIA=str(model.CONCESSIONARIA or ""),
        )

    def _to_model(self, entity: Operadora) -> OperadoraModel:
        return OperadoraModel(
            ID=entity.ID,
            NOME=entity.NOME,
            CONCESSIONARIA=entity.CONCESSIONARIA,
        )

    def get_all(self) -> list[Operadora]:
        """Return all operator entities (consórcios)."""
        models = self.db.query(OperadoraModel).all()
        return [self._to_domain(m) for m in models]

    def get_by_id(self, id_consorcio: int) -> Operadora | None:
        """Find an operator by ID."""
        model = (
            self.db.query(OperadoraModel)
            .filter(OperadoraModel.ID == id_consorcio)
            .first()
        )
        return self._to_domain(model) if model is not None else None

    def get_by_ids(self, ids_consorcios: list[int]) -> list[Operadora]:
        """Find operators (consórcios) by a list of IDs."""
        if not ids_consorcios:
            return []
        models = (
            self.db.query(OperadoraModel)
            .filter(OperadoraModel.ID.in_(ids_consorcios))
            .all()
        )
        return [self._to_domain(m) for m in models]

    def insert_bulk(self, consorcios: list[Operadora]) -> int:
        """Insert or merge a list of consórcio entities into the database."""
        counter = 0
        for item in consorcios:
            model = self._to_model(item)
            self.db.merge(model)
            counter += 1
        return counter

    def update_bulk(self, consorcios: list[Operadora]) -> int:
        """Persist updated consórcio entities in the database."""
        counter = 0
        for item in consorcios:
            if item.id is not None:
                model = self._to_model(item)
                self.db.merge(model)
                counter += 1
        return counter

    def delete(self, id_consorcio: int) -> int:
        """Delete a consórcio by its ID."""
        deleted = (
            self.db.query(OperadoraModel)
            .filter(OperadoraModel.ID == id_consorcio)
            .delete()
        )
        return deleted
