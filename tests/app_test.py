from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from app import BonfireApp, create_bonfire_app


def test_app_init_db_connection_error_logs_warning():
    with patch(
        "repositories.manager.SQLAlchemyRepositoryManager.check_connection",
        side_effect=Exception("DB Connection Failed"),
    ):
        with patch(
            "infrastructure.auth.authenticator.KeyCloakAuthenticator.check_connection"
        ):
            with patch("utils.logger.logger.warn") as mock_warn:
                app_instance = BonfireApp("test_db_error_app")
                assert app_instance is not None
                mock_warn.assert_any_call(
                    "Database check on startup: DB Connection Failed"
                )


def test_app_init_auth_connection_error_logs_warning():
    with patch("repositories.manager.SQLAlchemyRepositoryManager.check_connection"):
        with patch(
            "infrastructure.auth.authenticator.KeyCloakAuthenticator.check_connection",
            side_effect=Exception("Keycloak Offline"),
        ):
            with patch("utils.logger.logger.warn") as mock_warn:
                app_instance = BonfireApp("test_auth_error_app")
                assert app_instance is not None
                mock_warn.assert_any_call("Keycloak check on startup: Keycloak Offline")


@pytest.fixture
def auth_app():
    with patch("repositories.manager.SQLAlchemyRepositoryManager.check_connection"):
        with patch(
            "infrastructure.auth.authenticator.KeyCloakAuthenticator.check_connection"
        ):
            application = BonfireApp("test_auth_app")
            application.config.update({"TESTING": True})
            return application


def test_check_auth_options_method(auth_app):
    with auth_app.test_request_context("/", method="OPTIONS"):
        assert auth_app.check_auth() is None


def test_check_auth_missing_header(auth_app):
    with auth_app.test_request_context("/", method="GET"):
        res = auth_app.check_auth()
        assert res is not None
        assert res.status_code == 401


def test_check_auth_malformed_header_not_bearer(auth_app):
    with auth_app.test_request_context(
        "/", method="GET", headers={"Authorization": "Basic 12345"}
    ):
        res = auth_app.check_auth()
        assert res is not None
        assert res.status_code == 401


def test_check_auth_malformed_header_single_part(auth_app):
    with auth_app.test_request_context(
        "/", method="GET", headers={"Authorization": "Bearer"}
    ):
        res = auth_app.check_auth()
        assert res is not None
        assert res.status_code == 401


def test_check_auth_token_unauthenticated(auth_app):
    auth_app._authController = MagicMock()
    auth_app._authController.is_authenticated.return_value = False
    with auth_app.test_request_context(
        "/", method="GET", headers={"Authorization": "Bearer invalid-token"}
    ):
        res = auth_app.check_auth()
        assert res is not None
        assert res.status_code == 401
        auth_app._authController.is_authenticated.assert_called_once_with(
            "invalid-token"
        )


def test_check_auth_token_authenticated(auth_app):
    auth_app._authController = MagicMock()
    auth_app._authController.is_authenticated.return_value = True
    with auth_app.test_request_context(
        "/", method="GET", headers={"Authorization": "Bearer valid-token"}
    ):
        assert auth_app.check_auth() is None
        auth_app._authController.is_authenticated.assert_called_once_with("valid-token")


def test_create_bonfire_app():
    with patch("repositories.manager.SQLAlchemyRepositoryManager.check_connection"):
        with patch(
            "infrastructure.auth.authenticator.KeyCloakAuthenticator.check_connection"
        ):
            app_instance = create_bonfire_app()
            assert isinstance(app_instance, BonfireApp)


def test_log_request(app):
    with app.test_request_context("/test-route", method="GET"):
        with patch("utils.logger.http_logger.request") as mock_http_req:
            resp = Response("OK", status=200)
            returned_resp = app.log_request(resp)
            assert returned_resp is resp
            mock_http_req.assert_called_once()
