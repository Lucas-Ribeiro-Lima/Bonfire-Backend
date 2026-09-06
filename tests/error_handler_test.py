from unittest.mock import patch

import pytest
from flask import Blueprint

from app import BonfireApp
from domain.exceptions import (
    DomainException,
    DuplicateEntityError,
    EntityAlreadyDeactivatedError,
    InvalidIdentifierError,
    RelatedEntityNotFoundError,
)
from exceptions.CustomExceptions import CustomException


@pytest.fixture
def error_app():
    with patch.object(BonfireApp, "checkAuth", return_value=None):
        application = BonfireApp("test_bonfire_errors")
        application.config.update({"TESTING": True})

        # Register a test blueprint with routes that raise exceptions
        test_bp = Blueprint("test_errors", __name__)

        @test_bp.route("/test-custom-exception")
        def _raise_custom_exception():  # pyright: ignore [reportUnusedFunction]
            raise CustomException(
                "Custom domain error occurred", status=418, error="TEAPOT_ERROR"
            )

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

        @test_bp.route("/test-generic-exception")
        def _raise_generic_exception():  # pyright: ignore [reportUnusedFunction]
            raise ValueError("Something unexpected went wrong")

        application.register_blueprint(test_bp)
        yield application


@pytest.fixture
def error_client(error_app):
    return error_app.test_client()


def test_custom_exception_handling(error_client):
    response = error_client.get("/test-custom-exception")
    assert response.status_code == 418
    data = response.get_json()
    assert data == {
        "error": "TEAPOT_ERROR",
        "message": "Um erro inesperado ocorreu.",
        "status": 418,
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

