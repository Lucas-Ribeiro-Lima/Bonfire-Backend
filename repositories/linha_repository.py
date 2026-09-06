from sqlalchemy.orm import Session

from classes.Linha import Linha
from repositories.interfaces import ILinhaRepository
from repositories.models.linha_model import LinhaModel


class LinhaRepository(ILinhaRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: LinhaModel) -> Linha:
        return Linha(**model.__dict__)

    def _to_model(self, entity: Linha) -> LinhaModel:
        return LinhaModel(
            COD_LINH=entity.COD_LINH,
            ID_OPERADORA=entity.ID_OPERADORA,
            COMPARTILHADA=bool(
                entity.COMPARTILHADA if entity.COMPARTILHADA is not None else False
            ),
            LINH_ATIV_EMPR=bool(
                entity.LINH_ATIV_EMPR if entity.LINH_ATIV_EMPR is not None else True
            ),
            DAT_BAIX=entity.DAT_BAIX,
        )

    def get_all(self) -> list[Linha]:
        """Return all line entities."""
        models = self.db.query(LinhaModel).all()
        return [self._to_domain(m) for m in models]

    def get_by_id(self, cod_linh: str) -> Linha | None:
        """Find a line by its line code."""
        model = (
            self.db.query(LinhaModel).filter(LinhaModel.COD_LINH == cod_linh).first()
        )
        return self._to_domain(model) if model is not None else None

    def get_by_ids(self, cod_linhas: list[str]) -> list[Linha]:
        """Find lines by a list of line codes."""
        if not cod_linhas:
            return []
        models = (
            self.db.query(LinhaModel).filter(LinhaModel.COD_LINH.in_(cod_linhas)).all()
        )
        return [self._to_domain(m) for m in models]

    def insert_bulk(self, linhas: list[Linha]) -> int:
        """Insert a list of line domain entities into the database."""
        counter = 0
        for linha in linhas:
            model = self._to_model(linha)
            self.db.add(model)
            counter += 1
        return counter

    def update_bulk(self, linhas: list[Linha]) -> int:
        """Persist updated line domain entities to the database."""
        counter = 0
        for linha in linhas:
            if linha.line_code is not None:
                model = self._to_model(linha)
                self.db.merge(model)
                counter += 1
        return counter

    def delete(self, cod_linh: str) -> int:
        """Delete a line by its line code."""
        deleted = (
            self.db.query(LinhaModel).filter(LinhaModel.COD_LINH == cod_linh).delete()
        )
        return deleted
