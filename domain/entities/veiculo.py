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

    def get_vehicle_number(self) -> int:
        return self.vehicle_number

    def set_vehicle_number(self, value: int | str) -> None:
        self.vehicle_number = int(value)

    def get_license_plate(self) -> str | None:
        return self.license_plate

    def set_license_plate(self, value: str | None) -> None:
        self.license_plate = str(value) if value is not None else None

    def is_active(self) -> bool:
        return self.active

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
