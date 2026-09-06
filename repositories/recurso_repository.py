from sqlalchemy.orm import Session

from domain.entities import RecursoPrimeiraInstancia, RecursoSegundaInstancia
from repositories.interfaces import IRecursoRepository
from repositories.models.autoinfracao_model import AutoInfracaoModel
from repositories.models.recurso_model import (
    RecursoPrimeiraInstanciaModel,
    RecursoSegundaInstanciaModel,
)


class RecursoRepository(IRecursoRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_primeira(
        self, model: RecursoPrimeiraInstanciaModel | None
    ) -> RecursoPrimeiraInstancia | None:
        if model is None:
            return None
        return RecursoPrimeiraInstancia(**model.__dict__)

    def _to_model_primeira(
        self, entity: RecursoPrimeiraInstancia
    ) -> RecursoPrimeiraInstanciaModel:
        return RecursoPrimeiraInstanciaModel(**dict(entity))

    def _to_domain_segunda(
        self, model: RecursoSegundaInstanciaModel | None
    ) -> RecursoSegundaInstancia | None:
        if model is None:
            return None
        return RecursoSegundaInstancia(**model.__dict__)

    def _to_model_segunda(
        self, entity: RecursoSegundaInstancia
    ) -> RecursoSegundaInstanciaModel:
        return RecursoSegundaInstanciaModel(**dict(entity))

    def get_primeira_instancia(
        self, date: str | None = None, ata: int | str | None = None
    ) -> list[RecursoPrimeiraInstancia]:
        query = self.db.query(
            RecursoPrimeiraInstanciaModel.NUM_AI,
            RecursoPrimeiraInstanciaModel.NUM_ATA,
            RecursoPrimeiraInstanciaModel.DAT_PUBL,
            AutoInfracaoModel.COD_LINH,
            AutoInfracaoModel.NUM_VEIC,
            AutoInfracaoModel.IDN_PLAC_VEIC,
        ).join(
            AutoInfracaoModel,
            RecursoPrimeiraInstanciaModel.NUM_AI == AutoInfracaoModel.NUM_AI,
        )

        if ata is not None:
            query = query.filter(RecursoPrimeiraInstanciaModel.NUM_ATA == ata)
        if date is not None:
            query = query.filter(RecursoPrimeiraInstanciaModel.DAT_PUBL == date)

        results = query.limit(300).all()
        return [
            RecursoPrimeiraInstancia(
                NUM_AI=r.NUM_AI,
                NUM_ATA=r.NUM_ATA,
                DAT_PUBL=r.DAT_PUBL,
                COD_LINH=r.COD_LINH,
                NUM_VEIC=r.NUM_VEIC,
                IDN_PLAC_VEIC=r.IDN_PLAC_VEIC,
            )
            for r in results
        ]

    def get_segunda_instancia(
        self, date: str | None = None
    ) -> list[RecursoSegundaInstancia]:
        query = self.db.query(
            RecursoSegundaInstanciaModel.NUM_AI,
            RecursoSegundaInstanciaModel.DAT_PUBL,
            AutoInfracaoModel.COD_LINH,
            AutoInfracaoModel.NUM_VEIC,
            AutoInfracaoModel.IDN_PLAC_VEIC,
        ).join(
            AutoInfracaoModel,
            RecursoSegundaInstanciaModel.NUM_AI == AutoInfracaoModel.NUM_AI,
        )

        if date is not None:
            query = query.filter(RecursoSegundaInstanciaModel.DAT_PUBL == date)

        results = query.limit(300).all()
        return [
            RecursoSegundaInstancia(
                NUM_AI=r.NUM_AI,
                DAT_PUBL=r.DAT_PUBL,
                COD_LINH=r.COD_LINH,
                NUM_VEIC=r.NUM_VEIC,
                IDN_PLAC_VEIC=r.IDN_PLAC_VEIC,
            )
            for r in results
        ]

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
