from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UpdateLinhaCommand:
    """Application command for partial line updates."""

    line_code: str
    operator_id: int | None = None
    shared: bool | None = None
    active: bool | None = None
    deregistration_date: datetime | None = None


@dataclass(frozen=True)
class UpdateVeiculoCommand:
    """Application command for partial vehicle updates."""

    vehicle_number: int
    license_plate: str | None = None
    active: bool | None = None
    deregistration_date: datetime | None = None


@dataclass(frozen=True)
class UpdateConsorcioCommand:
    """Application command for partial consórcio (operadora) updates."""

    id: int
    name: str | None = None
    concessionaire: str | None = None
