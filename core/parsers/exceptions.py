class ParserException(Exception):
    """Base exception for all document parsing and ingestion failures."""

    def __init__(self, message: str = "Falha no processamento do documento.") -> None:
        self.message = message
        super().__init__(self.message)


class UnsupportedFormatError(ParserException):
    """Raised when the document format or extension is not supported."""

    def __init__(self, message: str = "Formato de arquivo não suportado pelo parser.") -> None:
        self.message = message
        super().__init__(self.message)


class DocumentReadError(ParserException):
    """Raised on low-level file reading or I/O failure."""

    def __init__(
        self,
        message: str = "Ocorreu um erro ao tentar ler ou processar o arquivo enviado.",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class PublicationDateNotFoundError(ParserException):
    """Raised when publication date (DAT_PUBL) is missing or cannot be parsed."""

    def __init__(
        self,
        message: str = "Data de publicação não encontrada ou formato inválido no arquivo.",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class IncorrectInstanceError(ParserException):
    """Raised when the document contains records of a different legal instance."""

    def __init__(
        self,
        message: str = "Instância incorreta. O arquivo contém registros de uma instância diferente da esperada.",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class QuantityOfAtasMismatchError(ParserException):
    """Raised when the number of meeting minutes does not match the number of tables."""

    def __init__(
        self,
        qtd_atas: int,
        qtd_tables: int,
        message: str = "A quantidade de Atas lidas não corresponde ao número de tabelas encontradas no documento.",
    ) -> None:
        self.qtd_atas = qtd_atas
        self.qtd_tables = qtd_tables
        self.message = message
        super().__init__(self.message)


class InvalidDocumentDataError(ParserException):
    """Raised when the document contains invalid internal structure or data."""

    def __init__(
        self,
        message: str = "O arquivo enviado possui formato estrutural inválido.",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class NullExtractionError(ParserException):
    """Raised when extraction yields null or empty data."""

    def __init__(
        self,
        message: str = "Nenhum dado válido extraído para inserção.",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class DocumentParsingError(ParserException):
    """General extraction pipeline execution error."""

    def __init__(
        self,
        message: str = "Falha ao processar o conteúdo do documento. Verifique se o formato interno e os dados estão legíveis.",
    ) -> None:
        self.message = message
        super().__init__(self.message)
