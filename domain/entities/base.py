from datetime import date, datetime
from typing import Any, Generator

from pydantic import BaseModel, ConfigDict


class DomainEntity(BaseModel):
    """Base domain entity supporting canonical Python naming and legacy database aliases."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="allow",
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if args:
            field_names = list(self.__class__.model_fields.keys())
            for idx, val in enumerate(args):
                if idx < len(field_names):
                    kwargs[field_names[idx]] = val
        super().__init__(**kwargs)

    def __getattr__(self, item: str) -> Any:
        for name, field_info in self.__class__.model_fields.items():
            if field_info.alias == item:
                return getattr(self, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )

    def __setattr__(self, item: str, value: Any) -> None:
        for name, field_info in self.__class__.model_fields.items():
            if field_info.alias == item:
                super().__setattr__(name, value)
                return
        super().__setattr__(item, value)

    def to_dict(self) -> dict[str, Any]:
        """Serialize entity to dictionary using database/alias column names."""
        data = self.model_dump(by_alias=True)
        for k, v in data.items():
            if isinstance(v, (datetime, date)):
                data[k] = v.isoformat()
        return data

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        yield from self.to_dict().items()
