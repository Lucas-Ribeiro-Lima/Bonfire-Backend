from typing import Any, cast

from sqlalchemy import CursorResult, insert
from sqlalchemy.orm import Session

from domain.entities import AutoInfracao
from repositories.interfaces import IAutoInfracaoRepository
from repositories.models.autoinfracao_model import AutoInfracaoModel


class AutoInfracaoRepository(IAutoInfracaoRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: AutoInfracaoModel) -> AutoInfracao:
        return AutoInfracao(**model.__dict__)

    def _to_model(self, entity: AutoInfracao) -> AutoInfracaoModel:
        return AutoInfracaoModel(**dict(entity))

    def get_infracoes(self, date: Any, ai: Any) -> list[AutoInfracao]:
        query = self.db.query(AutoInfracaoModel)
        if ai is not None:
            query = query.filter(AutoInfracaoModel.NUM_AI.like(f"%{ai}%"))
        if date is not None:
            query = query.filter(AutoInfracaoModel.DAT_EMIS_NOTF >= date)
        models = query.limit(200).all()
        return [self._to_domain(m) for m in models]

    def check_presence(self, values: list[str]) -> tuple[int, int, list[str]]:
        existing = (
            self.db.query(AutoInfracaoModel.NUM_AI)
            .filter(AutoInfracaoModel.NUM_AI.in_(values))
            .all()
        )
        existing_set = {r[0] for r in existing}

        rows_counter = len(existing_set)
        counter = len(values)
        rows_not_present = [v for v in values if v not in existing_set]

        return rows_counter, counter, rows_not_present

    def insert_bulk(self, autos: list[AutoInfracao]) -> int:
        if not autos:
            return 0
        data = [dict(a) for a in autos]
        stmt = insert(AutoInfracaoModel).prefix_with("IGNORE").values(data)
        result = self.db.execute(stmt)
        return cast(CursorResult, result).rowcount
