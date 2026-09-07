from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from domain.entities import Linha, Operadora
from domain.exceptions import (
    DuplicateEntityError,
    EntityAlreadyDeactivatedError,
    RelatedEntityNotFoundError,
)
from repositories.linha_repository import LinhaRepository
from services.commands import UpdateLinhaCommand
from services.linha_service import LinhaService


def test_linha_model_without_dat_baix():
    linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    data = linha.to_dict()
    assert data == {
        "COD_LINH": "61",
        "ID_OPERADORA": 107,
        "COMPARTILHADA": True,
        "LINH_ATIV_EMPR": True,
        "DAT_BAIX": None,
    }


def test_linha_model_with_dat_baix():
    dt = datetime(2026, 8, 28, 10, 0, 0)
    linha = Linha(
        COD_LINH="62",
        ID_OPERADORA=108,
        COMPARTILHADA=False,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=dt,
    )
    data = linha.to_dict()
    assert data == {
        "COD_LINH": "62",
        "ID_OPERADORA": 108,
        "COMPARTILHADA": False,
        "LINH_ATIV_EMPR": False,
        "DAT_BAIX": "2026-08-28T10:00:00",
    }


def test_linha_repository_insert_bulk():
    mock_db = MagicMock()
    # Mock to ensure the exists check returns empty (no linhas found)
    mock_db.query.return_value.filter.return_value.all.side_effect = [
        [(107,), (108,)],
        [],
    ]
    repo = LinhaRepository(mock_db)

    payload = [
        Linha(
            COD_LINH="61",
            ID_OPERADORA=107,
            COMPARTILHADA=True,
            LINH_ATIV_EMPR=True,
        ),
        Linha(
            COD_LINH="62",
            ID_OPERADORA=108,
            COMPARTILHADA=False,
            LINH_ATIV_EMPR=False,
            DAT_BAIX="2026-08-28T10:00:00",
        ),
    ]

    count = repo.insert_bulk(payload)
    assert count == 2
    assert mock_db.add.call_count == 2


def test_linha_repository_get_by_ids():
    mock_db = MagicMock()
    repo = LinhaRepository(mock_db)

    existing_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_model = repo._to_model(existing_linha)
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_model]

    result = repo.get_by_ids(["61"])
    assert len(result) == 1
    assert result[0].line_code == "61"
    assert result[0].operator_id == 107


def test_linha_repository_update_bulk():
    mock_db = MagicMock()
    repo = LinhaRepository(mock_db)

    payload = [
        Linha(COD_LINH="61", ID_OPERADORA=107, COMPARTILHADA=True, LINH_ATIV_EMPR=True),
        Linha(
            COD_LINH="62", ID_OPERADORA=108, COMPARTILHADA=False, LINH_ATIV_EMPR=False
        ),
    ]

    count = repo.update_bulk(payload)
    assert count == 2
    assert mock_db.merge.call_count == 2


def test_linha_service_update_deactivate():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_linha_repo = mock_session.get_linha_repository.return_value

    existing_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_linha_repo.get_by_ids.return_value = [existing_linha]
    mock_linha_repo.update_bulk.side_effect = lambda linhas: len(linhas)

    service = LinhaService(mock_db_manager)
    payload = [UpdateLinhaCommand(line_code="61", active=False)]

    count = service.update_linha(payload)
    assert count == 1
    mock_linha_repo.get_by_ids.assert_called_once_with(["61"])
    mock_linha_repo.update_bulk.assert_called_once()
    updated_linha = mock_linha_repo.update_bulk.call_args[0][0][0]
    assert updated_linha.active is False
    assert updated_linha.deregistration_date is not None
    assert isinstance(updated_linha.deregistration_date, datetime)


def test_linha_service_update_already_deactivated_raises_error():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_linha_repo = mock_session.get_linha_repository.return_value

    existing_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_linha_repo.get_by_ids.return_value = [existing_linha]

    service = LinhaService(mock_db_manager)
    payload = [UpdateLinhaCommand(line_code="61", active=False)]

    with pytest.raises(EntityAlreadyDeactivatedError) as exc_info:
        service.update_linha(payload)
    assert "já se encontra baixada" in str(exc_info.value)


def test_linha_service_update_reactivate():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_linha_repo = mock_session.get_linha_repository.return_value

    existing_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_linha_repo.get_by_ids.return_value = [existing_linha]
    mock_linha_repo.update_bulk.side_effect = lambda linhas: len(linhas)

    service = LinhaService(mock_db_manager)
    payload = [UpdateLinhaCommand(line_code="61", active=True)]

    count = service.update_linha(payload)
    assert count == 1
    updated_linha = mock_linha_repo.update_bulk.call_args[0][0][0]
    assert updated_linha.active is True
    assert updated_linha.deregistration_date is None


def test_linha_service_update_operadora_not_found_raises_error():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_consorcio_repo = mock_session.get_consorcio_repository.return_value
    mock_consorcio_repo.get_by_ids.return_value = []

    service = LinhaService(mock_db_manager)
    payload = [UpdateLinhaCommand(line_code="61", operator_id=999)]

    with pytest.raises(RelatedEntityNotFoundError) as exc_info:
        service.update_linha(payload)
    assert "consórcios/operadoras" in str(exc_info.value)


def test_linha_service_update_empty_and_not_found():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_linha_repo = mock_session.get_linha_repository.return_value
    mock_linha_repo.get_by_ids.return_value = []

    service = LinhaService(mock_db_manager)
    assert service.update_linha([]) == 0
    assert service.update_linha([UpdateLinhaCommand(line_code="NONEXISTENT")]) == 0


def test_service_get_linha():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_linha_repository.return_value

    mock_linha = Linha(
        COD_LINH="61",
        ID_OPERADORA=107,
        COMPARTILHADA=True,
        LINH_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 8, 28, 12, 0, 0),
    )
    mock_repo.get_all.return_value = [mock_linha]

    service = LinhaService(mock_db_manager)
    res = service.get_linha()
    assert len(res) == 1
    assert res[0].line_code == "61"
    assert res[0].to_dict()["DAT_BAIX"] == "2026-08-28T12:00:00"


def test_linha_service_insert_already_exists():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_consorcio_repo = mock_session.get_consorcio_repository.return_value
    mock_linha_repo = mock_session.get_linha_repository.return_value

    mock_consorcio_repo.get_by_ids.return_value = [
        Operadora(107, "Teste", "Teste Concessionária"),
    ]

    mock_linha_repo.get_by_ids.return_value = [
        Linha("61", 107, COMPARTILHADA=False, LINH_ATIV_EMPR=True),
    ]

    service = LinhaService(mock_db_manager)

    payload = [
        Linha(
            COD_LINH="61",
            ID_OPERADORA=107,
            COMPARTILHADA=True,
            LINH_ATIV_EMPR=True,
        )
    ]

    with pytest.raises(DuplicateEntityError) as exc_info:
        service.insert_linha(payload)

    assert "já existem e não podem ser sobrescritas: 61" in str(exc_info.value)


@pytest.mark.usefixtures("app", "client", "database")
class TestLinha:
    @patch("services.linha_service.LinhaService.get_linha")
    def test_get_route(self, mock_get, client, database):
        """Test that GET /linha returns the correct list of lines."""
        mock_get.return_value = [
            {
                "COD_LINH": "61",
                "ID_OPERADORA": 107,
                "COMPARTILHADA": True,
                "LINH_ATIV_EMPR": True,
                "DAT_BAIX": None,
            }
        ]

        response = client.get("/linha")
        assert response.status_code == 200
        data = response.get_json()
        assert "linha" in data
        assert len(data["linha"]) == 1
        assert data["linha"][0]["COD_LINH"] == "61"
        assert data["linha"][0]["DAT_BAIX"] is None

    @patch("services.linha_service.LinhaService.get_linha")
    def test_get_route_with_data_baixa(self, mock_get, client, database):
        """Test that GET /linha returns list with DAT_BAIX populated."""
        mock_get.return_value = [
            {
                "COD_LINH": "62",
                "ID_OPERADORA": 108,
                "COMPARTILHADA": False,
                "LINH_ATIV_EMPR": False,
                "DAT_BAIX": "2026-08-28T11:00:00",
            }
        ]

        response = client.get("/linha")
        assert response.status_code == 200
        data = response.get_json()
        assert "linha" in data
        assert len(data["linha"]) == 1
        assert data["linha"][0]["COD_LINH"] == "62"
        assert data["linha"][0]["DAT_BAIX"] == "2026-08-28T11:00:00"

    @patch("services.linha_service.LinhaService.insert_linha")
    def test_insert_route(self, mock_insert, client, database):
        """Test that POST /linha inserts lines successfully."""
        mock_insert.return_value = 1

        payload = [
            {
                "COD_LINH": "61",
                "ID_OPERADORA": 107,
                "COMPARTILHADA": True,
                "LINH_ATIV_EMPR": True,
            }
        ]

        response = client.post("/linha", json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Linhas inseridas com sucesso"
        assert data["counter"] == 1

    @patch("services.linha_service.LinhaService.update_linha")
    def test_update_route(self, mock_update, client, database):
        """Test that PATCH /linha updates lines successfully."""
        mock_update.return_value = 1

        payload = [
            {
                "COD_LINH": "61",
                "ID_OPERADORA": 107,
                "COMPARTILHADA": False,
                "LINH_ATIV_EMPR": True,
            }
        ]

        response = client.patch("/linha", json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Linha atualizada com sucesso"
        assert data["counter"] == 1

    @patch("services.linha_service.LinhaService.delete_linha")
    def test_delete_route(self, mock_delete, client, database):
        """Test that DELETE /linha/<COD_LINH> deletes line successfully."""
        mock_delete.return_value = 1

        response = client.delete("/linha/61")
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Linha deletada com sucesso"
        assert data["counter"] == 1
