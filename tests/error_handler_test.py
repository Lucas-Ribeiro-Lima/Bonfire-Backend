from unittest.mock import patch

import pytest
from flask import Blueprint

from controllers.http.app import BonfireApp
from domain.exceptions import (
    DomainException,
    DuplicateEntityError,
    EntityAlreadyDeactivatedError,
    InvalidIdentifierError,
    RelatedEntityNotFoundError,
)
from infrastructure.exceptions import DatabaseConnectionError
from infrastructure.parsers.exceptions import (
    DocumentParsingError,
    DocumentReadError,
    InvalidDocumentDataError,
    NullExtractionError,
    PublicationDateNotFoundError,
    QuantityOfAtasMismatchError,
    UnsupportedFormatError,
)


@pytest.fixture
def error_app():
    with patch.object(BonfireApp, "check_auth", return_value=None):
        application = BonfireApp("test_bonfire_errors")
        application.config.update({"TESTING": True})

        # Register a test blueprint with routes that raise exceptions
        test_bp = Blueprint("test_errors", __name__)

        @test_bp.route("/test-database-connection-error")
        def _raise_database_connection_error():  # pyright: ignore [reportUnusedFunction]
            raise DatabaseConnectionError("Falha ao conectar no banco de dados")

        @test_bp.route("/test-duplicate-entity")
        def _raise_duplicate():  # pyright: ignore [reportUnusedFunction]
            raise DuplicateEntityError("Linha", ["61"])

        @test_bp.route("/test-already-deactivated")
        def _raise_already_deactivated():  # pyright: ignore [reportUnusedFunction]
            raise EntityAlreadyDeactivatedError("Linha", "61")

        @test_bp.route("/test-related-not-found")
        def _raise_related_not_found():  # pyright: ignore [reportUnusedFunction]
            raise RelatedEntityNotFoundError("Operadora", [999])

        @test_bp.route("/test-invalid-identifier")
        def _raise_invalid_identifier():  # pyright: ignore [reportUnusedFunction]
            raise InvalidIdentifierError("Veículo", "abc")

        @test_bp.route("/test-generic-domain-exception")
        def _raise_domain_exception():  # pyright: ignore [reportUnusedFunction]
            raise DomainException("Regra de domínio violada")

        @test_bp.route("/test-unsupported-format")
        def _raise_unsupported_format():  # pyright: ignore [reportUnusedFunction]
            raise UnsupportedFormatError(
                "Formato de arquivo não suportado pelo parser."
            )

        @test_bp.route("/test-document-parsing-error")
        def _raise_document_parsing_error():  # pyright: ignore [reportUnusedFunction]
            raise DocumentParsingError("Falha ao processar o conteúdo do documento.")

        @test_bp.route("/test-publi-date-not-found")
        def _raise_publi_date_not_found():  # pyright: ignore [reportUnusedFunction]
            raise PublicationDateNotFoundError(
                "Data de publicação não encontrada no documento"
            )

        @test_bp.route("/test-quantity-of-atas")
        def _raise_quantity_of_atas():  # pyright: ignore [reportUnusedFunction]
            raise QuantityOfAtasMismatchError(1, 2)

        @test_bp.route("/test-null-extraction")
        def _raise_null_extraction():  # pyright: ignore [reportUnusedFunction]
            raise NullExtractionError("Nenhum dado válido extraído para inserção.")

        @test_bp.route("/test-invalid-document-data")
        def _raise_invalid_document_data():  # pyright: ignore [reportUnusedFunction]
            raise InvalidDocumentDataError(
                "O arquivo enviado possui formato estrutural inválido."
            )

        @test_bp.route("/test-document-read-error")
        def _raise_document_read_error():  # pyright: ignore [reportUnusedFunction]
            raise DocumentReadError(
                "Ocorreu um erro ao tentar ler ou processar o arquivo enviado."
            )

        @test_bp.route("/test-generic-exception")
        def _raise_generic_exception():  # pyright: ignore [reportUnusedFunction]
            raise ValueError("Something unexpected went wrong")

        application.register_blueprint(test_bp)
        yield application


@pytest.fixture
def error_client(error_app):
    return error_app.test_client()


def test_database_connection_error_handling(error_client):
    response = error_client.get("/test-database-connection-error")
    assert response.status_code == 500
    data = response.get_json()
    assert data == {
        "error": "Database Connection Error",
        "message": "Falha ao conectar no banco de dados",
        "status": 500,
    }


def test_generic_exception_handling(error_client):
    response = error_client.get("/test-generic-exception")
    assert response.status_code == 500
    data = response.get_json()
    assert data == {
        "error": "Internal Server Error",
        "message": "Ocorreu um erro interno no servidor.",
    }


def test_duplicate_entity_handling(error_client):
    response = error_client.get("/test-duplicate-entity")
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Conflict"
    assert "já existem e não podem ser sobrescritas: 61" in data["message"]
    assert data["status"] == 409


def test_already_deactivated_handling(error_client):
    response = error_client.get("/test-already-deactivated")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"
    assert "já se encontra baixada" in data["message"]
    assert data["status"] == 400


def test_related_not_found_handling(error_client):
    response = error_client.get("/test-related-not-found")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"
    assert "não existem: 999" in data["message"]
    assert data["status"] == 400


def test_invalid_identifier_handling(error_client):
    response = error_client.get("/test-invalid-identifier")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"
    assert "Identificador de Veículo inválido: abc" in data["message"]
    assert data["status"] == 400


def test_domain_exception_fallback_handling(error_client):
    response = error_client.get("/test-generic-domain-exception")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Bad Request"
    assert data["message"] == "Regra de domínio violada"
    assert data["status"] == 400


def test_unsupported_format_handling(error_client):
    response = error_client.get("/test-unsupported-format")
    assert response.status_code == 415
    data = response.get_json()
    assert data["error"] == "Unsupported Format"
    assert data["status"] == 415


def test_document_parsing_error_handling(error_client):
    response = error_client.get("/test-document-parsing-error")
    assert response.status_code == 422
    data = response.get_json()
    assert data["error"] == "Parsing Error"
    assert data["status"] == 422


def test_publi_date_not_found_handling(error_client):
    response = error_client.get("/test-publi-date-not-found")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "DAT_PUBL Invalida"
    assert data["status"] == 400


def test_quantity_of_atas_handling(error_client):
    response = error_client.get("/test-quantity-of-atas")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Error extracting atas or tables"
    assert data["qtdAtas"] == 1
    assert data["qtdTables"] == 2
    assert data["status"] == 400


def test_null_extraction_handling(error_client):
    response = error_client.get("/test-null-extraction")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "autoSegundaInstanciaList NULL"
    assert data["status"] == 400


def test_invalid_document_data_handling(error_client):
    response = error_client.get("/test-invalid-document-data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid File Data"
    assert data["status"] == 400


def test_document_read_error_handling(error_client):
    response = error_client.get("/test-document-read-error")
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Error in file"
    assert data["status"] == 500
