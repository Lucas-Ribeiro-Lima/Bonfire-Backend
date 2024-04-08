import pytest

@pytest.mark.usefixtures("app", "client", "database")
class TestLinha:
  def test_get_route(self, client, database):
    response = client.get("/linha")
    assert "200 OK" == response.status

  def test_insert_route(self):
    pass

  def test_update_route(self):
    pass