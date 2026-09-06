from typing import Any


class DomainException(Exception):
    """Base class for domain invariant violations."""

    def __init__(self, message: str = "Ocorreu um erro no domínio.") -> None:
        self.message = message
        super().__init__(self.message)


class EntityAlreadyDeactivatedError(DomainException):
    """Raised when attempting to deactivate an entity that is already inactive."""

    def __init__(
        self,
        entity_name: str,
        identifier: str | int | None = None,
        message: str | None = None,
    ) -> None:
        self.entity_name = entity_name
        self.identifier = identifier
        if message:
            self.message = message
        else:
            suffix = "baixada" if entity_name.lower().endswith("a") else "baixado"
            id_part = f" {identifier}" if identifier is not None else ""
            self.message = f"{entity_name}{id_part} já se encontra {suffix}"
        super().__init__(self.message)


class DuplicateEntityError(DomainException):
    """Raised when attempting to create or insert entities that already exist."""

    def __init__(
        self,
        entity_name: str,
        identifiers: list[Any] | None = None,
        message: str | None = None,
    ) -> None:
        self.entity_name = entity_name
        self.identifiers = identifiers or []
        if message:
            self.message = message
        else:
            ids_str = ", ".join(str(i) for i in self.identifiers)
            self.message = f"As seguintes entidades ({entity_name}) já existem e não podem ser sobrescritas: {ids_str}"
        super().__init__(self.message)


class RelatedEntityNotFoundError(DomainException):
    """Raised when a required related entity does not exist."""

    def __init__(
        self,
        entity_name: str,
        identifiers: list[Any] | None = None,
        message: str | None = None,
    ) -> None:
        self.entity_name = entity_name
        self.identifiers = identifiers or []
        if message:
            self.message = message
        else:
            ids_str = ", ".join(str(i) for i in self.identifiers)
            self.message = f"Não é possível prosseguir. Os seguintes consórcios/operadoras ({entity_name}) não existem: {ids_str}"
        super().__init__(self.message)


class InvalidIdentifierError(DomainException):
    """Raised when an identifier format or value is invalid."""

    def __init__(
        self,
        entity_name: str,
        value: Any = None,
        message: str | None = None,
    ) -> None:
        self.entity_name = entity_name
        self.value = value
        self.message = message or f"Identificador de {entity_name} inválido: {value}"
        super().__init__(self.message)
