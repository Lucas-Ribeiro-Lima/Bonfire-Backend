import pytest
from app import create_app
from repositories.database import sqlite3Db

@pytest.fixture(scope="module")
def app():
  """Instance of Main app"""
  app = create_app()
  return app

@pytest.fixture(scope="module")
def database():
  """Instance of temporary database"""
  connection = sqlite3Db.create_temp_database()
  return connection


@pytest.fixture()
def client(app):
  client = app.test_client()
  return client

