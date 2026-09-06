from abc import ABC
from datetime import date, datetime
from typing import Iterator


class Recurso(ABC):
    def __init__(
        self,
        NUM_AI: str | None = None,
        NUM_RECURSO: str | None = None,
        NOM_CONC: str | None = None,
        RESULTADO: bool = False,
        DAT_PUBL: date | datetime | str | None = None,
        **kwargs: object,
    ):
        self.NUM_AI = NUM_AI
        self.NUM_RECURSO = NUM_RECURSO
        self.NOM_CONC = NOM_CONC
        self.RESULTADO = bool(RESULTADO)
        self.DAT_PUBL = self._parse_date(DAT_PUBL)

        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    @staticmethod
    def _parse_date(value: date | datetime | str | None) -> date | None:
        if isinstance(value, str):
            try:
                return (
                    datetime.fromisoformat(value).date()
                    if "T" in value or " " in value
                    else date.fromisoformat(value)
                )
            except ValueError:
                return None
        if isinstance(value, datetime):
            return value.date()
        return value

    def to_dict(self) -> dict[str, object]:
        """Convert entity attributes to a dictionary representation."""
        result: dict[str, object] = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if isinstance(value, (datetime, date)):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    def __iter__(self) -> Iterator[tuple[str, object]]:
        """Allow dict(instance) conversion."""
        yield from self.to_dict().items()


class RecursoPrimeiraInstancia(Recurso):
    """Pure domain entity for First Instance Appeal."""

    def __init__(
        self,
        NUM_AI: str | None = None,
        NUM_ATA: int | str | None = None,
        NUM_RECURSO: str | None = None,
        NOM_CONC: str | None = None,
        RESULTADO: bool = False,
        DAT_PUBL: date | datetime | str | None = None,
        **kwargs: object,
    ):
        self.NUM_ATA = int(NUM_ATA) if NUM_ATA is not None else None
        super().__init__(NUM_AI, NUM_RECURSO, NOM_CONC, RESULTADO, DAT_PUBL, **kwargs)


class RecursoSegundaInstancia(Recurso):
    """Pure domain entity for Second Instance Appeal."""
