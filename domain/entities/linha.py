from datetime import datetime

from pydantic import Field

from domain.entities.base import DomainEntity
from domain.exceptions import EntityAlreadyDeactivatedError


class Linha(DomainEntity):
    """Pure domain entity for Bus Line."""

    line_code: str = Field(alias="COD_LINH")
    operator_id: int | None = Field(default=None, alias="ID_OPERADORA")
    shared: bool = Field(default=False, alias="COMPARTILHADA")
    active: bool = Field(default=True, alias="LINH_ATIV_EMPR")
    deregistration_date: datetime | None = Field(default=None, alias="DAT_BAIX")

    def get_line_code(self) -> str:
        return self.line_code

    def set_line_code(self, value: str) -> None:
        self.line_code = str(value)

    def get_operator_id(self) -> int | None:
        return self.operator_id

    def set_operator_id(self, value: int | str | None) -> None:
        self.operator_id = int(value) if value is not None else None

    def is_shared(self) -> bool:
        return self.shared

    def set_shared(self, value: bool) -> None:
        self.shared = bool(value)

    get_shared = is_shared

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> None:
        """Reactivate line and clear deregistration date."""
        self.active = True
        self.deregistration_date = None

    def deactivate(self, deregistration_date: datetime | str | None = None) -> None:
        """Deactivate line and record deregistration date."""
        if not self.active:
            raise EntityAlreadyDeactivatedError("Linha", self.line_code)
        self.active = False
        if isinstance(deregistration_date, str):
            try:
                self.deregistration_date = datetime.fromisoformat(deregistration_date)
            except ValueError:
                self.deregistration_date = datetime.now()
        elif isinstance(deregistration_date, datetime):
            self.deregistration_date = deregistration_date
        else:
            self.deregistration_date = datetime.now()

    def get_deregistration_date(self) -> datetime | None:
        return self.deregistration_date

    def set_deregistration_date(self, value: datetime | str | None) -> None:
        if isinstance(value, str):
            try:
                self.deregistration_date = datetime.fromisoformat(value)
            except ValueError:
                self.deregistration_date = None
        elif isinstance(value, datetime):
            self.deregistration_date = value
        else:
            self.deregistration_date = None
