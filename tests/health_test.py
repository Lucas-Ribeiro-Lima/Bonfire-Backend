from unittest.mock import MagicMock


def test_healthz_liveness(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_readyz_readiness_all_up(client, app):
    mock_db = MagicMock()
    app.extensions["db_manager"] = mock_db
    app._authController = MagicMock()

    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ready"
    assert data["database"] == "up"
    assert data["auth"] == "up"


def test_readyz_readiness_database_down(client, app):
    mock_db = MagicMock()
    mock_db.check_connection.side_effect = Exception("DB Connection Refused")
    app.extensions["db_manager"] = mock_db
    app._authController = MagicMock()

    response = client.get("/readyz")
    assert response.status_code == 503
    data = response.get_json()
    assert data["status"] == "unhealthy"
    assert data["database"] == "down"
    assert data["auth"] == "up"


def test_readyz_readiness_auth_down(client, app):
    mock_db = MagicMock()
    app.extensions["db_manager"] = mock_db
    mock_auth = MagicMock()
    mock_auth.check_connection.side_effect = Exception("Keycloak Unreachable")
    app._authController = mock_auth

    response = client.get("/readyz")
    assert response.status_code == 503
    data = response.get_json()
    assert data["status"] == "unhealthy"
    assert data["database"] == "up"
    assert data["auth"] == "down"
