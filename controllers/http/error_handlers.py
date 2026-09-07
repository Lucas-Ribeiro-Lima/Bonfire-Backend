from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from domain.exceptions import (
    DomainException,
    DuplicateEntityError,
    EntityAlreadyDeactivatedError,
    InvalidIdentifierError,
    RelatedEntityNotFoundError,
)
from infrastructure.exceptions import (
    DatabaseConnectionError,
    InfrastructureException,
    InvalidDatabaseConfigError,
)
from infrastructure.parsers.exceptions import (
    DocumentParsingError,
    DocumentReadError,
    IncorrectInstanceError,
    InvalidDocumentDataError,
    NullExtractionError,
    ParserException,
    PublicationDateNotFoundError,
    QuantityOfAtasMismatchError,
    UnsupportedFormatError,
)
from utils.logger import logger


def register_error_handlers(app: Flask) -> None:
    """Register application-wide exception handlers on the Flask app."""

    # --- Domain Exception Handlers ---
    @app.errorhandler(DuplicateEntityError)
    def _handle_duplicate_entity(e: DuplicateEntityError):
        logger.systemLog(f"[DuplicateEntityError] {e}")
        return (
            jsonify(
                {
                    "error": "Conflict",
                    "message": str(e),
                    "status": 409,
                }
            ),
            409,
        )

    @app.errorhandler(RelatedEntityNotFoundError)
    def _handle_related_not_found(e: RelatedEntityNotFoundError):
        logger.systemLog(f"[RelatedEntityNotFoundError] {e}")
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(EntityAlreadyDeactivatedError)
    def _handle_already_deactivated(e: EntityAlreadyDeactivatedError):
        logger.systemLog(f"[EntityAlreadyDeactivatedError] {e}")
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(InvalidIdentifierError)
    def _handle_invalid_identifier(e: InvalidIdentifierError):
        logger.systemLog(f"[InvalidIdentifierError] {e}")
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(DomainException)
    def _handle_domain_exception(e: DomainException):
        logger.systemLog(f"[DomainException] {e}")
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    # --- Parser & Ingestion Exception Handlers ---
    @app.errorhandler(UnsupportedFormatError)
    def _handle_unsupported_format(e: UnsupportedFormatError):
        logger.systemLog(f"[UnsupportedFormatError] {e}")
        return (
            jsonify(
                {
                    "error": "Unsupported Format",
                    "message": str(e),
                    "status": 415,
                }
            ),
            415,
        )

    @app.errorhandler(DocumentParsingError)
    def _handle_document_parsing_error(e: DocumentParsingError):
        logger.systemLog(f"[DocumentParsingError] {e}")
        return (
            jsonify(
                {
                    "error": "Parsing Error",
                    "message": str(e),
                    "status": 422,
                }
            ),
            422,
        )

    @app.errorhandler(PublicationDateNotFoundError)
    def _handle_publi_date_not_found(e: PublicationDateNotFoundError):
        logger.systemLog(f"[PublicationDateNotFoundError] {e}")
        return (
            jsonify(
                {
                    "error": "DAT_PUBL Invalida",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(IncorrectInstanceError)
    def _handle_incorrect_instance(e: IncorrectInstanceError):
        logger.systemLog(f"[IncorrectInstanceError] {e}")
        return (
            jsonify(
                {
                    "error": "Incorrect Instance",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(QuantityOfAtasMismatchError)
    def _handle_atas_mismatch(e: QuantityOfAtasMismatchError):
        logger.systemLog(f"[QuantityOfAtasMismatchError] {e}")
        return (
            jsonify(
                {
                    "error": "Error extracting atas or tables",
                    "message": str(e),
                    "qtdAtas": e.qtd_atas,
                    "qtdTables": e.qtd_tables,
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(NullExtractionError)
    def _handle_null_extraction(e: NullExtractionError):
        logger.systemLog(f"[NullExtractionError] {e}")
        return (
            jsonify(
                {
                    "error": "autoSegundaInstanciaList NULL",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(InvalidDocumentDataError)
    def _handle_invalid_document_data(e: InvalidDocumentDataError):
        logger.systemLog(f"[InvalidDocumentDataError] {e}")
        return (
            jsonify(
                {
                    "error": "Invalid File Data",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    @app.errorhandler(DocumentReadError)
    def _handle_document_read_error(e: DocumentReadError):
        logger.systemLog(f"[DocumentReadError] {e}")
        return (
            jsonify(
                {
                    "error": "Error in file",
                    "message": str(e),
                    "status": 500,
                }
            ),
            500,
        )

    @app.errorhandler(ParserException)
    def _handle_parser_exception(e: ParserException):
        logger.systemLog(f"[ParserException] {e}")
        return (
            jsonify(
                {
                    "error": "Parsing Error",
                    "message": str(e),
                    "status": 400,
                }
            ),
            400,
        )

    # --- Infrastructure Exception Handlers ---
    @app.errorhandler(DatabaseConnectionError)
    def _handle_database_connection_error(e: DatabaseConnectionError):
        logger.systemLog(f"[DatabaseConnectionError] {e}")
        return (
            jsonify(
                {
                    "error": "Database Connection Error",
                    "message": str(e),
                    "status": 500,
                }
            ),
            500,
        )

    @app.errorhandler(InvalidDatabaseConfigError)
    def _handle_invalid_db_config(e: InvalidDatabaseConfigError):
        logger.systemLog(f"[InvalidDatabaseConfigError] {e}")
        return (
            jsonify(
                {
                    "error": "Invalid Database Configuration",
                    "message": str(e),
                    "status": 500,
                }
            ),
            500,
        )

    @app.errorhandler(InfrastructureException)
    def _handle_infrastructure_exception(e: InfrastructureException):
        logger.systemLog(f"[InfrastructureException] {e}")
        return (
            jsonify(
                {
                    "error": "Infrastructure Error",
                    "message": str(e),
                    "status": 500,
                }
            ),
            500,
        )

    # --- Standard HTTP / Unexpected Exception Handlers ---
    @app.errorhandler(HTTPException)
    def _handle_http_exception(e: HTTPException):
        code = e.code or 500
        return (
            jsonify(
                {
                    "error": e.name,
                    "message": e.description,
                    "status": code,
                }
            ),
            code,
        )

    @app.errorhandler(Exception)
    def _handle_generic_exception(e: Exception):
        logger.systemLog(e)
        status_code = getattr(e, "code", 500)
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "Ocorreu um erro interno no servidor.",
                }
            ),
            status_code,
        )
