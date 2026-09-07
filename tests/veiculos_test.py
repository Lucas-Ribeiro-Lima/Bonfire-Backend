from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from domain.entities import Veiculo
from domain.exceptions import (
    DuplicateEntityError,
    EntityAlreadyDeactivatedError,
    InvalidIdentifierError,
)
from repositories.veiculo_repository import VeiculoRepository
from services.commands import UpdateVeiculoCommand
from services.veiculo_service import VeiculoService


def test_veiculo_model_without_dat_baix():
    veic = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    data = veic.to_dict()
    assert data == {
        "NUM_VEIC": 1111,
        "IDN_PLAC_VEIC": "OPC123",
        "VEIC_ATIV_EMPR": True,
        "DAT_BAIX": None,
    }


def test_veiculo_model_with_dat_baix():
    dt = datetime(2026, 8, 28, 10, 0, 0)
    veic = Veiculo(
        NUM_VEIC=2222,
        IDN_PLAC_VEIC="XYZ987",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=dt,
    )
    data = veic.to_dict()
    assert data == {
        "NUM_VEIC": 2222,
        "IDN_PLAC_VEIC": "XYZ987",
        "VEIC_ATIV_EMPR": False,
        "DAT_BAIX": "2026-08-28T10:00:00",
    }


def test_veiculo_repository_insert_bulk():
    mock_db = MagicMock()
    # Mock to ensure the exists check returns empty (no vehicles found)
    mock_db.query.return_value.filter.return_value.all.return_value = []
    repo = VeiculoRepository(mock_db)

    payload = [
        Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="OPC123", VEIC_ATIV_EMPR=True),
        Veiculo(
            NUM_VEIC=2222,
            IDN_PLAC_VEIC="XYZ987",
            VEIC_ATIV_EMPR=False,
            DAT_BAIX="2026-08-28T10:00:00",
        ),
    ]

    count = repo.insert_bulk(payload)
    assert count == 2
    assert mock_db.add.call_count == 2


def test_veiculo_repository_get_by_ids():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_model = repo._to_model(existing_veiculo)
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_model]

    result = repo.get_by_ids([1111])
    assert len(result) == 1
    assert result[0].vehicle_number == 1111
    assert result[0].license_plate == "OPC123"


def test_veiculo_repository_update_bulk():
    mock_db = MagicMock()
    repo = VeiculoRepository(mock_db)

    payload = [
        Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="OPC123", VEIC_ATIV_EMPR=True),
        Veiculo(NUM_VEIC=2222, IDN_PLAC_VEIC="XYZ987", VEIC_ATIV_EMPR=False),
    ]

    count = repo.update_bulk(payload)
    assert count == 2
    assert mock_db.merge.call_count == 2


def test_veiculo_service_update_deactivate():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_veiculo_repository.return_value

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_repo.get_by_ids.return_value = [existing_veiculo]
    mock_repo.update_bulk.side_effect = lambda veics: len(veics)

    service = VeiculoService(mock_db_manager)
    payload = [UpdateVeiculoCommand(vehicle_number=1111, active=False)]

    count = service.update_veiculos(payload)
    assert count == 1
    mock_repo.get_by_ids.assert_called_once_with([1111])
    mock_repo.update_bulk.assert_called_once()
    updated_veiculo = mock_repo.update_bulk.call_args[0][0][0]
    assert updated_veiculo.active is False
    assert updated_veiculo.deregistration_date is not None
    assert isinstance(updated_veiculo.deregistration_date, datetime)


def test_veiculo_service_update_already_deactivated_raises_error():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_veiculo_repository.return_value

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_repo.get_by_ids.return_value = [existing_veiculo]

    service = VeiculoService(mock_db_manager)
    payload = [UpdateVeiculoCommand(vehicle_number=1111, active=False)]

    with pytest.raises(EntityAlreadyDeactivatedError) as exc_info:
        service.update_veiculos(payload)
    assert "já se encontra baixado" in str(exc_info.value)


def test_veiculo_service_update_reactivate():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_veiculo_repository.return_value

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 1, 1),
    )
    mock_repo.get_by_ids.return_value = [existing_veiculo]
    mock_repo.update_bulk.side_effect = lambda veics: len(veics)

    service = VeiculoService(mock_db_manager)
    payload = [UpdateVeiculoCommand(vehicle_number=1111, active=True)]

    count = service.update_veiculos(payload)
    assert count == 1
    updated_veiculo = mock_repo.update_bulk.call_args[0][0][0]
    assert updated_veiculo.active is True
    assert updated_veiculo.deregistration_date is None


def test_veiculo_service_update_license_plate_and_empty():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_veiculo_repository.return_value

    existing_veiculo = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=True,
        DAT_BAIX=None,
    )
    mock_repo.get_by_ids.return_value = [existing_veiculo]
    mock_repo.update_bulk.side_effect = lambda veics: len(veics)

    service = VeiculoService(mock_db_manager)
    assert service.update_veiculos([]) == 0
    assert service.update_veiculos([UpdateVeiculoCommand(vehicle_number=9999)]) == 0

    count = service.update_veiculos(
        [
            UpdateVeiculoCommand(
                vehicle_number=1111,
                license_plate="XYZ9999",
                deregistration_date=datetime(2026, 5, 5),
            )
        ]
    )
    assert count == 1
    updated = mock_repo.update_bulk.call_args[0][0][0]
    assert updated.license_plate == "XYZ9999"
    assert updated.deregistration_date == datetime(2026, 5, 5)


def test_service_get_veiculos():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_veiculo_repository.return_value

    mock_veic = Veiculo(
        NUM_VEIC=1111,
        IDN_PLAC_VEIC="OPC123",
        VEIC_ATIV_EMPR=False,
        DAT_BAIX=datetime(2026, 8, 28, 12, 0, 0),
    )
    mock_repo.get_all.return_value = [mock_veic]

    service = VeiculoService(mock_db_manager)
    res = service.get_veiculos()
    assert len(res) == 1
    assert res[0].vehicle_number == 1111
    assert res[0].to_dict()["DAT_BAIX"] == "2026-08-28T12:00:00"


@pytest.mark.usefixtures("app", "client", "database")
class TestVeiculos:
    @patch("services.veiculo_service.VeiculoService.get_veiculos")
    def test_get_route(self, mock_get, client, database):
        """Test that GET /veiculos returns 200 and the correct list."""
        mock_get.return_value = [
            {
                "NUM_VEIC": 1111,
                "IDN_PLAC_VEIC": "OPC123",
                "VEIC_ATIV_EMPR": False,
                "DAT_BAIX": None,
            }
        ]

        response = client.get("/veiculos")

        assert response.status_code == 200
        data = response.get_json()
        assert "veiculos" in data
        assert len(data["veiculos"]) == 1
        assert data["veiculos"][0]["NUM_VEIC"] == 1111
        assert data["veiculos"][0]["DAT_BAIX"] is None

    @patch("services.veiculo_service.VeiculoService.get_veiculos")
    def test_get_route_with_data_baixa(self, mock_get, client, database):
        """Test that GET /veiculos returns 200 with DAT_BAIX populated."""
        mock_get.return_value = [
            {
                "NUM_VEIC": 2222,
                "IDN_PLAC_VEIC": "ABC1234",
                "VEIC_ATIV_EMPR": False,
                "DAT_BAIX": "2026-08-28T10:30:00",
            }
        ]

        response = client.get("/veiculos")

        assert response.status_code == 200
        data = response.get_json()
        assert "veiculos" in data
        assert len(data["veiculos"]) == 1
        assert data["veiculos"][0]["NUM_VEIC"] == 2222
        assert data["veiculos"][0]["DAT_BAIX"] == "2026-08-28T10:30:00"

    @patch("services.veiculo_service.VeiculoService.insert_veiculos")
    def test_insert_route(self, mock_insert, client, database):
        """Test POST /veiculos route."""
        mock_insert.return_value = 1

        payload = [
            {"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": True}
        ]

        response = client.post("/veiculos", json=payload)

        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "Veículos inseridos com sucesso"
        assert data["counter"] == 1

    @patch("services.veiculo_service.VeiculoService.update_veiculos")
    def test_update_route(self, mock_update, client, database):
        """Test PATCH /veiculos route."""
        mock_update.return_value = 1

        payload = [
            {"NUM_VEIC": 1111, "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": False}
        ]

        response = client.patch("/veiculos", json=payload)

        assert response.status_code == 202
        data = response.get_json()
        assert data["message"] == "Veículos atualizados com sucesso"
        assert data["counter"] == 1

    @patch("services.veiculo_service.VeiculoService.delete_veiculos")
    def test_delete_route(self, mock_delete, client, database):
        """Test DELETE /veiculos/<NUM_VEIC> route."""
        mock_delete.return_value = 1

        response = client.delete("/veiculos/1111")

        assert response.status_code == 202
        data = response.get_json()
        assert data["message"] == "Veículos deletados com sucesso"
        assert data["counter"] == 1


def test_veiculo_service_insert_bulk_already_exists():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_veiculo_repository.return_value
    mock_repo.get_by_ids.return_value = [
        Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="OPC123", VEIC_ATIV_EMPR=True)
    ]

    service = VeiculoService(mock_db_manager)
    payload = [Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="OPC123", VEIC_ATIV_EMPR=True)]

    with pytest.raises(DuplicateEntityError) as exc_info:
        service.insert_veiculos(payload)

    assert "já existem e não podem ser sobrescritos: 1111" in str(exc_info.value)


def test_veiculo_service_delete_invalid_id_raises_error():
    mock_db_manager = MagicMock()
    service = VeiculoService(mock_db_manager)

    with pytest.raises(InvalidIdentifierError) as exc_info:
        service.delete_veiculos("invalid_num")

    assert "Número do veículo inválido" in str(exc_info.value)
