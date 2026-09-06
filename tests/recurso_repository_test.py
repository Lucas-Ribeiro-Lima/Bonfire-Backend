from datetime import date
from unittest.mock import MagicMock

from domain.entities import RecursoPrimeiraInstancia, RecursoSegundaInstancia
from repositories.models.recurso_model import (
    RecursoPrimeiraInstanciaModel,
    RecursoSegundaInstanciaModel,
)
from repositories.recurso_repository import RecursoRepository


def test_recurso_to_model():
    mock_db = MagicMock()
    repo = RecursoRepository(mock_db)

    rec1 = RecursoPrimeiraInstancia(
        NUM_AI="AI-100",
        NUM_ATA=10,
        NUM_RECURSO="REC-1",
        NOM_CONC="CONC-A",
        RESULTADO=True,
        DAT_PUBL=date(2026, 1, 1),
    )
    model1 = repo._to_model_primeira(rec1)
    assert isinstance(model1, RecursoPrimeiraInstanciaModel)
    assert model1.NUM_AI == "AI-100"

    rec2 = RecursoSegundaInstancia(
        NUM_AI="AI-200",
        NUM_RECURSO="REC-2",
        NOM_CONC="CONC-B",
        RESULTADO=False,
        DAT_PUBL=date(2026, 2, 2),
    )
    model2 = repo._to_model_segunda(rec2)
    assert isinstance(model2, RecursoSegundaInstanciaModel)
    assert model2.NUM_AI == "AI-200"


def test_recurso_get_primeira_instancia():
    mock_db = MagicMock()
    repo = RecursoRepository(mock_db)

    fake_model = RecursoPrimeiraInstanciaModel(
        NUM_AI="AI-1",
        NUM_ATA=5,
        NUM_RECURSO="R-1",
        NOM_CONC="CONC",
        RESULTADO=True,
        DAT_PUBL=date(2026, 3, 3),
    )
    mock_db.query.return_value.filter.return_value.filter.return_value.limit.return_value.all.return_value = [
        fake_model
    ]

    res = repo.get_primeira_instancia(date="2026-03-03", ata=5)
    assert len(res) == 1
    assert res[0].notice_number == "AI-1"
    assert res[0].meeting_minute_number == 5


def test_recurso_get_segunda_instancia():
    mock_db = MagicMock()
    repo = RecursoRepository(mock_db)

    fake_model = RecursoSegundaInstanciaModel(
        NUM_AI="AI-2",
        NUM_RECURSO="R-2",
        NOM_CONC="CONC",
        RESULTADO=False,
        DAT_PUBL=date(2026, 4, 4),
    )
    mock_db.query.return_value.filter.return_value.limit.return_value.all.return_value = [
        fake_model
    ]

    res = repo.get_segunda_instancia(date="2026-04-04")
    assert len(res) == 1
    assert res[0].notice_number == "AI-2"


def test_recurso_insert_empty():
    mock_db = MagicMock()
    repo = RecursoRepository(mock_db)

    assert repo.insert_primeira_instancia([]) == 0
    assert repo.insert_segunda_instancia([]) == 0
    mock_db.execute.assert_not_called()


def test_recurso_insert_success():
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_db.execute.return_value = mock_result
    repo = RecursoRepository(mock_db)

    rec1 = RecursoPrimeiraInstancia(
        NUM_AI="AI-1",
        NUM_ATA=1,
        NUM_RECURSO="R-1",
        NOM_CONC="C",
        RESULTADO=True,
        DAT_PUBL=date(2026, 1, 1),
    )
    count1 = repo.insert_primeira_instancia([rec1])
    assert count1 == 1

    rec2 = RecursoSegundaInstancia(
        NUM_AI="AI-2",
        NUM_RECURSO="R-2",
        NOM_CONC="C",
        RESULTADO=False,
        DAT_PUBL=date(2026, 1, 1),
    )
    count2 = repo.insert_segunda_instancia([rec2])
    assert count2 == 1
