from datetime import datetime

from pydantic import Field

from domain.entities.base import DomainEntity
from domain.exceptions import EntityAlreadyDeactivatedError


class Veiculo(DomainEntity):
    """Pure domain entity for Vehicle."""

    vehicle_number: int = Field(alias="NUM_VEIC")
    license_plate: str | None = Field(default=None, alias="IDN_PLAC_VEIC")
    active: bool = Field(default=True, alias="VEIC_ATIV_EMPR")
    deregistration_date: datetime | None = Field(default=None, alias="DAT_BAIX")

    def activate(self) -> None:
        """Reactivate vehicle and clear deregistration date."""
        self.active = True
        self.deregistration_date = None

    def deactivate(self, deregistration_date: datetime | str | None = None) -> None:
        """Deactivate vehicle and record deregistration date."""
        if not self.active:
            raise EntityAlreadyDeactivatedError("Veículo", self.vehicle_number)
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
