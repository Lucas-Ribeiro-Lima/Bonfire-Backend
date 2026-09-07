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
