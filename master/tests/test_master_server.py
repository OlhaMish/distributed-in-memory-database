import pytest
from master.master_server import MasterServer
from master.storage import save_to_persistent_storage, load_from_persistent_storage, LOG_FILE, PERSISTENT_STORAGE_FILE
import os


@pytest.fixture(autouse=True)
def cleanup():
    # Clear the persistent storage and log before each test
    if os.path.exists(PERSISTENT_STORAGE_FILE):
        os.remove(PERSISTENT_STORAGE_FILE)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield
    # Clean up after tests
    if os.path.exists(PERSISTENT_STORAGE_FILE):
        os.remove(PERSISTENT_STORAGE_FILE)
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


@pytest.fixture
def master_server():
    return MasterServer(enable_periodic_save=False)


def test_save_and_load_database(master_server):
    master_server.set_value("test_key", "test_value")
    loaded_database = load_from_persistent_storage()
    assert "test_key" in loaded_database
    assert loaded_database["test_key"] == "test_value"


def test_load_database_on_startup(master_server):
    master_server.set_value("test_key", "test_value")

    new_master_server = MasterServer(enable_periodic_save=False)
    assert "test_key" in new_master_server.database
    assert new_master_server.database["test_key"] == "test_value"


def test_append_log(master_server):
    master_server.set_value("test_key1", "test_value1")
    master_server.set_value("test_key2", "test_value2")

    master_server.save_database()  # Force save to ensure log compaction
    loaded_database = load_from_persistent_storage()
    assert "test_key1" in loaded_database
    assert "test_key2" in loaded_database
    assert loaded_database["test_key1"] == "test_value1"
    assert loaded_database["test_key2"] == "test_value2"
