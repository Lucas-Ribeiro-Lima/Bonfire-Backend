import os
from unittest.mock import patch

import pytest

from infrastructure.config import Config, load_config
from infrastructure.exceptions import MissingRequiredEnvError


def test_config_loads_with_required_values():
    cfg = Config(
        DB_PASSWORD="mypassword",
        KEYCLOAK_CLIENT_SECRET="mysecret",
        KEYCLOAK_REALM_NAME="myrealm",
    )
    assert cfg.DB_DRIVER == "mysql"
    assert cfg.DB_HOST in ("bonfire-db", "localhost")
    assert cfg.DB_PORT in (3306, "3306")
    assert cfg.DB_PASSWORD == "mypassword"
    assert cfg.KEYCLOAK_CLIENT_SECRET == "mysecret"
    assert cfg.KEYCLOAK_REALM_NAME == "myrealm"


def test_config_dict_access_and_mutation():
    cfg = Config(
        DB_PASSWORD="p",
        KEYCLOAK_CLIENT_SECRET="s",
        KEYCLOAK_REALM_NAME="r",
    )
    assert cfg["DB_USER"] == cfg.DB_USER
    cfg["DB_USER"] = "custom_user"
    assert cfg.DB_USER == "custom_user"

    with pytest.raises(KeyError):
        _ = cfg["NON_EXISTENT_KEY"]

    with pytest.raises(KeyError):
        cfg["NON_EXISTENT_KEY"] = "val"


def test_config_missing_required_env_raises():
    with patch.dict(os.environ, {}, clear=True):
        with patch.object(Config, "model_config", {"env_file": "non_existent.env"}):
            with pytest.raises(MissingRequiredEnvError):
                load_config()
