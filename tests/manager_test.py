from unittest.mock import MagicMock, patch

import pytest

from infrastructure.exceptions import (
    DatabaseConnectionError,
    InvalidDatabaseConfigError,
)
from repositories.autoinfracao_repository import AutoInfracaoRepository
from repositories.consorcio_repository import ConsorcioRepository
from repositories.linha_repository import LinhaRepository
from repositories.manager import SQLAlchemyRepositoryManager, SQLAlchemySession
from repositories.recurso_repository import RecursoRepository
from repositories.veiculo_repository import VeiculoRepository


def test_sqlalchemy_session_commit_on_success():
    mock_raw_session = MagicMock()
    session = SQLAlchemySession(mock_raw_session)

    with session as s:
        assert s == session

    mock_raw_session.commit.assert_called_once()
    mock_raw_session.rollback.assert_not_called()
    mock_raw_session.close.assert_called_once()


def test_sqlalchemy_session_rollback_on_error():
    mock_raw_session = MagicMock()
    session = SQLAlchemySession(mock_raw_session)

    with pytest.raises(ValueError):
        with session:
            raise ValueError("Test error")

    mock_raw_session.rollback.assert_called_once()
    mock_raw_session.commit.assert_not_called()
    mock_raw_session.close.assert_called_once()


def test_sqlalchemy_session_repository_getters():
    mock_raw_session = MagicMock()
    session = SQLAlchemySession(mock_raw_session)

    assert isinstance(session.get_veiculo_repository(), VeiculoRepository)
    assert isinstance(session.get_linha_repository(), LinhaRepository)
    assert isinstance(session.get_consorcio_repository(), ConsorcioRepository)
    assert isinstance(session.get_recurso_repository(), RecursoRepository)
    assert isinstance(session.get_autoinfracao_repository(), AutoInfracaoRepository)


def test_manager_get_engine_invalid_config():
    manager = SQLAlchemyRepositoryManager()
    with patch("repositories.manager.config") as mock_config:
        mock_config.DB_DRIVER = None
        with pytest.raises(InvalidDatabaseConfigError):
            manager._get_engine()


def test_manager_get_engine_success():
    manager = SQLAlchemyRepositoryManager()
    with patch("repositories.manager.create_engine") as mock_create:
        mock_create.return_value = MagicMock()
        engine = manager._get_engine()
        assert engine == mock_create.return_value
        # Second call returns cached engine
        assert manager._get_engine() == engine
        assert mock_create.call_count == 1


def test_manager_check_connection_success():
    from tests.conftest import patcher_db

    manager = SQLAlchemyRepositoryManager()
    mock_engine = MagicMock()
    manager._engine = mock_engine
    patcher_db.temp_original(manager)
    mock_engine.connect.assert_called_once()


def test_manager_check_connection_failure():
    from tests.conftest import patcher_db

    manager = SQLAlchemyRepositoryManager()
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception("DB unreachable")
    manager._engine = mock_engine
    with pytest.raises(DatabaseConnectionError):
        patcher_db.temp_original(manager)


def test_manager_session_context():
    manager = SQLAlchemyRepositoryManager()
    mock_factory = MagicMock()
    mock_raw_session = MagicMock()
    mock_factory.return_value = mock_raw_session
    manager._session_factory = mock_factory

    with manager.session() as s:
        assert isinstance(s, SQLAlchemySession)

    mock_factory.remove.assert_called_once()
