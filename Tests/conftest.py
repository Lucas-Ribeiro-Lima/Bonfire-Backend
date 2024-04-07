import pytest
from ..app import create_app

@pytest.fixture()
def app_flask(scope="module"):
  """Instance of Main app"""
  return create_app()
