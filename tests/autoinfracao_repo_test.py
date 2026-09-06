from io import BytesIO
from unittest.mock import MagicMock

import pytest

from domain.entities import AutoInfracao
from infrastructure.parsers.exceptions import DocumentReadError
from repositories.autoinfracao_repository import AutoInfracaoRepository
from repositories.models.autoinfracao_model import AutoInfracaoModel
from services.autoinfracao_service import AutoInfracaoService


def test_autoinfracao_repo_to_model():
    mock_db = MagicMock()
    repo = AutoInfracaoRepository(mock_db)

    entity = AutoInfracao(NUM_AI="AI-12345", NUM_NOTF="NOTF-1", TIP_PENL="MULTA")
    model = repo._to_model(entity)
    assert isinstance(model, AutoInfracaoModel)
    assert model.NUM_AI == "AI-12345"
    assert model.NUM_NOTF == "NOTF-1"


def test_autoinfracao_repo_get_infracoes():
    mock_db = MagicMock()
    repo = AutoInfracaoRepository(mock_db)

    fake_model = AutoInfracaoModel(NUM_AI="AI-999")
    mock_db.query.return_value.filter.return_value.filter.return_value.limit.return_value.all.return_value = [
        fake_model
    ]

    res = repo.get_infracoes(date="2026-01-01", ai="999")
    assert len(res) == 1
    assert res[0].notice_number == "AI-999"


def test_autoinfracao_repo_check_presence():
    mock_db = MagicMock()
    repo = AutoInfracaoRepository(mock_db)

    mock_db.query.return_value.filter.return_value.all.return_value = [
        ("AI-1",),
        ("AI-2",),
    ]

    present_count, total_count, not_present = repo.check_presence(
        ["AI-1", "AI-2", "AI-3"]
    )
    assert present_count == 2
    assert total_count == 3
    assert not_present == ["AI-3"]


def test_autoinfracao_repo_insert_bulk_empty():
    mock_db = MagicMock()
    repo = AutoInfracaoRepository(mock_db)

    assert repo.insert_bulk([]) == 0
    mock_db.execute.assert_not_called()


def test_autoinfracao_repo_insert_bulk_success():
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.rowcount = 2
    mock_db.execute.return_value = mock_result
    repo = AutoInfracaoRepository(mock_db)

    autos = [
        AutoInfracao(NUM_AI="AI-1"),
        AutoInfracao(NUM_AI="AI-2"),
    ]
    count = repo.insert_bulk(autos)
    assert count == 2
    mock_db.execute.assert_called_once()


def test_autoinfracao_service_get_infracoes():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_autoinfracao_repository.return_value
    mock_repo.get_infracoes.return_value = [AutoInfracao(NUM_AI="AI-1")]

    service = AutoInfracaoService(mock_db_manager)
    result = service.get_infracoes(date="2026-01-01", ai="AI-1")
    assert len(result) == 1
    mock_repo.get_infracoes.assert_called_once_with("2026-01-01", "AI-1")


def test_autoinfracao_service_check_infracoes_valid_csv():
    mock_db_manager = MagicMock()
    mock_session = mock_db_manager.session.return_value.__enter__.return_value
    mock_repo = mock_session.get_autoinfracao_repository.return_value
    mock_repo.check_presence.return_value = (1, 2, ["AI-2"])

    service = AutoInfracaoService(mock_db_manager)
    csv_content = b"NUM_AI;OUTRO\nAI-1;val\nAI-2;val\n"
    stream = BytesIO(csv_content)

    present, total, missing = service.check_infracoes(stream)
    assert present == 1
    assert total == 2
    assert missing == ["AI-2"]


def test_autoinfracao_service_check_infracoes_invalid_csv():
    mock_db_manager = MagicMock()
    service = AutoInfracaoService(mock_db_manager)

    invalid_stream = BytesIO(b"MALFORMED_HEADER_WITHOUT_NUM_AI\n123\n")
    with pytest.raises(DocumentReadError):
        service.check_infracoes(invalid_stream)


def test_autoinfracao_service_extract_without_factory():
    mock_db_manager = MagicMock()
    service = AutoInfracaoService(mock_db_manager, parser_factory=None)

    with pytest.raises(RuntimeError, match="ParserFactory not injected"):
        service.extract_csv(BytesIO(b"data"))

    with pytest.raises(RuntimeError, match="ParserFactory not injected"):
        service.extract_xls(BytesIO(b"data"))
