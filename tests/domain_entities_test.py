from datetime import datetime

import pytest

from domain.entities import (
    AutoInfracao,
    Linha,
    Operadora,
    RecursoPrimeiraInstancia,
    Veiculo,
)
from domain.exceptions import EntityAlreadyDeactivatedError


def test_linha_domain_methods():
    linha = Linha(
        COD_LINH="61", ID_OPERADORA=107, COMPARTILHADA=False, LINH_ATIV_EMPR=True
    )
    assert linha.active is True
    assert linha.COD_LINH == "61"

    # Deactivation with datetime
    dt = datetime(2026, 8, 28, 12, 0, 0)
    linha.deactivate(dt)
    assert linha.active is False
    assert linha.DAT_BAIX == dt

    # Double deactivation should raise EntityAlreadyDeactivatedError
    with pytest.raises(EntityAlreadyDeactivatedError) as exc:
        linha.deactivate()
    assert "já se encontra baixada" in str(exc.value)

    # Reactivation
    linha.activate()
    assert linha.active is True
    assert linha.DAT_BAIX is None

    # Deactivation with ISO string
    linha.deactivate("2026-08-28T12:00:00")
    assert linha.active is False
    assert linha.deregistration_date == datetime(2026, 8, 28, 12, 0, 0)

    # Reactivation and deactivation with invalid date string fallback
    linha.activate()
    linha.deactivate("invalid-iso-date")
    assert linha.active is False
    assert isinstance(linha.deregistration_date, datetime)

    # Reactivation and deactivation with None (defaults to datetime.now)
    linha.activate()
    linha.deactivate(None)
    assert linha.active is False
    assert isinstance(linha.deregistration_date, datetime)

    # Direct attribute access and mutations
    linha.activate()
    assert linha.line_code == "61"
    assert linha.operator_id == 107
    assert linha.shared is False
    linha.shared = True
    assert linha.shared is True
    assert linha.COMPARTILHADA is True

    # Native Python serialization via dict()
    data = dict(linha)
    assert data["COD_LINH"] == "61"
    assert data["LINH_ATIV_EMPR"] is True
    assert data["DAT_BAIX"] is None
    assert data["COMPARTILHADA"] is True


def test_veiculo_domain_methods():
    veiculo = Veiculo(NUM_VEIC=1111, IDN_PLAC_VEIC="ABC1234", VEIC_ATIV_EMPR=True)
    assert veiculo.active is True

    # Deactivation with datetime
    dt = datetime(2026, 8, 28, 14, 0, 0)
    veiculo.deactivate(dt)
    assert veiculo.active is False
    assert veiculo.DAT_BAIX == dt

    # Double deactivation should raise EntityAlreadyDeactivatedError
    with pytest.raises(EntityAlreadyDeactivatedError) as exc:
        veiculo.deactivate()
    assert "já se encontra baixado" in str(exc.value)

    # Reactivation
    veiculo.activate()
    assert veiculo.active is True
    assert veiculo.DAT_BAIX is None

    # Deactivation with ISO string
    veiculo.deactivate("2026-08-28T14:00:00")
    assert veiculo.active is False
    assert veiculo.deregistration_date == datetime(2026, 8, 28, 14, 0, 0)

    # Reactivation and deactivation with invalid date string fallback
    veiculo.activate()
    veiculo.deactivate("invalid-iso-date")
    assert veiculo.active is False
    assert isinstance(veiculo.deregistration_date, datetime)

    # Reactivation and deactivation with None (defaults to datetime.now)
    veiculo.activate()
    veiculo.deactivate(None)
    assert veiculo.active is False
    assert isinstance(veiculo.deregistration_date, datetime)

    # Direct attribute access and mutations
    veiculo.activate()
    assert veiculo.vehicle_number == 1111
    assert veiculo.license_plate == "ABC1234"
    veiculo.license_plate = "XYZ9876"
    assert veiculo.license_plate == "XYZ9876"
    assert veiculo.IDN_PLAC_VEIC == "XYZ9876"

    # Native Python serialization via dict()
    data = dict(veiculo)
    assert data["NUM_VEIC"] == 1111
    assert data["IDN_PLAC_VEIC"] == "XYZ9876"
    assert data["VEIC_ATIV_EMPR"] is True


def test_operadora_domain_methods():
    operadora = Operadora(ID=107, NOME="Milenio", CONCESSIONARIA="Pampulha")
    data = dict(operadora)
    assert data == {"ID": 107, "NOME": "Milenio", "CONCESSIONARIA": "Pampulha"}

    # Direct field access
    assert operadora.id == 107
    assert operadora.name == "Milenio"
    assert operadora.concessionaire == "Pampulha"

    # Direct field mutations
    operadora.name = "Milenio Alterado"
    assert operadora.name == "Milenio Alterado"
    assert operadora.NOME == "Milenio Alterado"

    operadora.concessionaire = "Nova Concessionaria"
    assert operadora.concessionaire == "Nova Concessionaria"
    assert operadora.CONCESSIONARIA == "Nova Concessionaria"


def test_autoinfracao_and_recurso_serialization():
    ai = AutoInfracao(
        NUM_AI="12345-A", VAL_INFR=150.50, DAT_EMIS_NOTF="2026-08-28T10:00:00"
    )
    ai_dict = dict(ai)
    assert ai_dict["NUM_AI"] == "12345-A"
    assert ai_dict["VAL_INFR"] == 150.50
    assert ai_dict["DAT_EMIS_NOTF"] == "2026-08-28T10:00:00"

    rec1 = RecursoPrimeiraInstancia(
        NUM_AI="12345-A",
        NUM_ATA=5,
        NUM_RECURSO="123/2026",
        NOM_CONC="Consórcio BH Leste",
        RESULTADO=True,
        DAT_PUBL="2026-08-28",
    )
    rec1_dict = dict(rec1)
    assert rec1_dict["NUM_AI"] == "12345-A"
    assert rec1_dict["NUM_ATA"] == 5
    assert rec1_dict["RESULTADO"] is True
    assert rec1_dict["DAT_PUBL"] == "2026-08-28"
