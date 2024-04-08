import pytest
from unittest.mock import patch

@pytest.mark.usefixtures("app", "client", "database")
class TestVeiculos: 

  @patch('handlers.veiculos')
  def test_get_route(self, client, database):
    """Testa se a rota get"""

    veiculos.getVeiculos().return_value = [{"NUM_VEIC": "1111", "IDN_PLAC_VEIC": "OPC123", "VEIC_ATIV_EMPR": "false"}]
    res = client.get("/veiculos")
    

  def test_insert_route(self, client, database):
    """Testa a rota insert"""
    pass

  def test_update_route(self, client, database):
    """Testa a rota update"""
    pass