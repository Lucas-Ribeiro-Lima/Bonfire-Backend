from sqlalchemy.orm import Session

from domain.entities import RecursoPrimeiraInstancia, RecursoSegundaInstancia
from repositories.interfaces import IRecursoRepository
from repositories.models.recurso_model import (
    RecursoPrimeiraInstanciaModel,
    RecursoSegundaInstanciaModel,
)


class RecursoRepository(IRecursoRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_primeira(
        self, model: RecursoPrimeiraInstanciaModel
    ) -> RecursoPrimeiraInstancia:
        return RecursoPrimeiraInstancia(
            NUM_AI=str(model.NUM_AI),
            NUM_ATA=int(model.NUM_ATA),
            NUM_RECURSO=str(model.NUM_RECURSO or ""),
            NOM_CONC=str(model.NOM_CONC or ""),
            RESULTADO=bool(model.RESULTADO),
            DAT_PUBL=model.DAT_PUBL,  # type: ignore[arg-type]
        )

    def _to_model_primeira(
        self, entity: RecursoPrimeiraInstancia
    ) -> RecursoPrimeiraInstanciaModel:
        return RecursoPrimeiraInstanciaModel(**dict(entity))

    def _to_domain_segunda(
        self, model: RecursoSegundaInstanciaModel
    ) -> RecursoSegundaInstancia:
        return RecursoSegundaInstancia(
            NUM_AI=str(model.NUM_AI),
            NUM_RECURSO=str(model.NUM_RECURSO or ""),
            NOM_CONC=str(model.NOM_CONC or ""),
            RESULTADO=bool(model.RESULTADO),
            DAT_PUBL=model.DAT_PUBL,  # type: ignore[arg-type]
        )

    def _to_model_segunda(
        self, entity: RecursoSegundaInstancia
    ) -> RecursoSegundaInstanciaModel:
        return RecursoSegundaInstanciaModel(**dict(entity))

    def get_primeira_instancia(
        self, date: str | None = None, ata: int | str | None = None
    ) -> list[RecursoPrimeiraInstancia]:
        query = self.db.query(RecursoPrimeiraInstanciaModel)

        if ata is not None:
            query = query.filter(RecursoPrimeiraInstanciaModel.NUM_ATA == ata)
        if date is not None:
            query = query.filter(RecursoPrimeiraInstanciaModel.DAT_PUBL == date)

        results = query.limit(300).all()
        return [self._to_domain_primeira(r) for r in results]

    def get_segunda_instancia(
        self, date: str | None = None
    ) -> list[RecursoSegundaInstancia]:
        query = self.db.query(RecursoSegundaInstanciaModel)

        if date is not None:
            query = query.filter(RecursoSegundaInstanciaModel.DAT_PUBL == date)

        results = query.limit(300).all()
        return [self._to_domain_segunda(r) for r in results]

    def insert_primeira_instancia(self, rows: list[RecursoPrimeiraInstancia]) -> int:
        if not rows:
            return 0
        from sqlalchemy.dialects.mysql import insert as mysql_insert

        data = [dict(r) for r in rows]
        stmt = (
            mysql_insert(RecursoPrimeiraInstanciaModel)
            .values(data)
            .prefix_with("IGNORE")
        )
        result = self.db.execute(stmt)
        return getattr(result, "rowcount", 0)

    def insert_segunda_instancia(self, rows: list[RecursoSegundaInstancia]) -> int:
        if not rows:
            return 0
        from sqlalchemy.dialects.mysql import insert as mysql_insert

        data = [dict(r) for r in rows]
        stmt = (
            mysql_insert(RecursoSegundaInstanciaModel)
            .values(data)
            .prefix_with("IGNORE")
        )
        result = self.db.execute(stmt)
        return getattr(result, "rowcount", 0)
