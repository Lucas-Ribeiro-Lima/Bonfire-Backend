class InfrastructureException(Exception):
    """Base exception for infrastructure and persistence adapters."""

    pass


class MissingRequiredEnvError(InfrastructureException):
    """Raised during application bootstrap when a required environment variable is missing."""

    def __init__(self, env_name: str) -> None:
        self.env_name = env_name
        super().__init__(f"Missing required environment variable: {env_name}")


class DatabaseConnectionError(InfrastructureException):
    """Raised when establishing a connection to the database fails."""

    def __init__(
        self,
        message: str = "Não foi possível estabelecer conexão com o banco de dados.",
    ) -> None:
        super().__init__(message)


class InvalidDatabaseConfigError(InfrastructureException):
    """Raised when database configuration parameters are missing or invalid."""

    def __init__(self, message: str = "Erro interno de configuração do banco.") -> None:
        super().__init__(message)
