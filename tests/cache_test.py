import time

from infrastructure.cache.in_memory import InMemoryCache


def test_cache_set_and_get():
    cache = InMemoryCache()
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"


def test_cache_get_non_existent_key():
    cache = InMemoryCache()
    assert cache.get("non_existent") is None


def test_cache_ttl_expiration():
    cache = InMemoryCache()
    cache.set("temp_key", "temp_value", ttl_seconds=1)
    assert cache.get("temp_key") == "temp_value"

    # Simulate expiration by manipulating expiry time
    key_entry = cache._store.get("temp_key")
    assert key_entry is not None
    cache._store["temp_key"] = (key_entry[0], time.time() - 10)

    # Lazy expiration check
    assert cache.get("temp_key") is None
    assert "temp_key" not in cache._store


def test_cache_delete():
    cache = InMemoryCache()
    cache.set("to_delete", 123)
    assert cache.get("to_delete") == 123
    cache.delete("to_delete")
    assert cache.get("to_delete") is None
    # Deleting non-existent key should not raise
    cache.delete("non_existent")


def test_cache_clear():
    cache = InMemoryCache()
    cache.set("a", 1)
    cache.set("b", 2)
    cache.clear()
    assert cache.get("a") is None
    assert cache.get("b") is None
