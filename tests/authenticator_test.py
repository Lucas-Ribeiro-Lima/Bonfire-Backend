import json
import time
from unittest.mock import MagicMock, patch

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from infrastructure.auth.authenticator import KeyCloakAuthenticator
from infrastructure.cache.in_memory import InMemoryCache


@pytest.fixture(scope="module")
def rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    jwk_str = jwt.algorithms.RSAAlgorithm.to_jwk(public_key)
    jwk_dict = json.loads(jwk_str)
    jwk_dict["kid"] = "key-1"
    return private_key, public_key, jwk_dict


def test_authenticator_get_public_keys_cache_hit():
    cache = InMemoryCache()
    fake_jwks = {"keys": [{"kid": "cached-kid"}]}
    cache.set("keycloak_jwks", fake_jwks)

    auth = KeyCloakAuthenticator(cache)
    keys = auth._get_public_keys()
    assert keys == fake_jwks


def test_authenticator_get_public_keys_cache_miss_success(rsa_keys):
    _, _, jwk_dict = rsa_keys
    cache = InMemoryCache()
    auth = KeyCloakAuthenticator(cache)

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"keys": [jwk_dict]}
    mock_resp.raise_for_status = MagicMock()

    with patch("requests.get", return_value=mock_resp):
        keys = auth._get_public_keys()

    assert keys == {"keys": [jwk_dict]}
    assert cache.get("keycloak_jwks") == {"keys": [jwk_dict]}


def test_authenticator_get_public_keys_network_failure():
    cache = InMemoryCache()
    auth = KeyCloakAuthenticator(cache)

    with patch("requests.get", side_effect=Exception("Network error")):
        keys = auth._get_public_keys()

    assert keys == {}


def test_authenticator_get_timestamp():
    cache = InMemoryCache()
    auth = KeyCloakAuthenticator(cache)
    ts = auth.getTimestamp()
    assert isinstance(ts, float)
    assert ts > 0


def test_authenticator_is_authenticated_valid_token(rsa_keys):
    private_key, _, jwk_dict = rsa_keys
    cache = InMemoryCache()
    cache.set("keycloak_jwks", {"keys": [jwk_dict]})
    auth = KeyCloakAuthenticator(cache)

    token = jwt.encode(
        {"sub": "user-1", "exp": time.time() + 3600},
        private_key,
        algorithm="RS256",
        headers={"kid": "key-1"},
    )
    assert auth.isAuthenticated(token) is True


def test_authenticator_is_authenticated_expired_token(rsa_keys):
    private_key, _, jwk_dict = rsa_keys
    cache = InMemoryCache()
    cache.set("keycloak_jwks", {"keys": [jwk_dict]})
    auth = KeyCloakAuthenticator(cache)

    token = jwt.encode(
        {"sub": "user-1", "exp": time.time() - 100},
        private_key,
        algorithm="RS256",
        headers={"kid": "key-1"},
    )
    assert auth.isAuthenticated(token) is False


def test_authenticator_is_authenticated_missing_kid(rsa_keys):
    private_key, _, jwk_dict = rsa_keys
    cache = InMemoryCache()
    cache.set("keycloak_jwks", {"keys": [jwk_dict]})
    auth = KeyCloakAuthenticator(cache)

    # Token with header without kid
    token = jwt.encode(
        {"sub": "user-1"},
        private_key,
        algorithm="RS256",
        headers={},
    )
    assert auth.isAuthenticated(token) is False


def test_authenticator_is_authenticated_unknown_kid(rsa_keys):
    private_key, _, jwk_dict = rsa_keys
    cache = InMemoryCache()
    cache.set("keycloak_jwks", {"keys": [jwk_dict]})
    auth = KeyCloakAuthenticator(cache)

    token = jwt.encode(
        {"sub": "user-1"},
        private_key,
        algorithm="RS256",
        headers={"kid": "unknown-kid"},
    )
    assert auth.isAuthenticated(token) is False


def test_authenticator_check_connection_success(rsa_keys):
    from tests.conftest import patcher_kc_conn

    _, _, jwk_dict = rsa_keys
    cache = InMemoryCache()
    cache.set("keycloak_jwks", {"keys": [jwk_dict]})
    auth = KeyCloakAuthenticator(cache)
    patcher_kc_conn.temp_original(auth)  # Test real implementation


def test_authenticator_check_connection_failure():
    from tests.conftest import patcher_kc_conn

    cache = InMemoryCache()
    auth = KeyCloakAuthenticator(cache)
    with patch.object(auth, "_get_public_keys", return_value={}):
        with pytest.raises(ValueError, match="Could not retrieve JWKS"):
            patcher_kc_conn.temp_original(auth)
