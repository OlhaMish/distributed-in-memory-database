import unittest
from master.master_server import MasterServer
from master.storage import save_to_persistent_storage, load_from_persistent_storage, LOG_FILE, PERSISTENT_STORAGE_FILE
import os
import time

class TestMasterServer(unittest.TestCase):
    def setUp(self):
        # Clear the persistent storage and log before each test
        if os.path.exists(PERSISTENT_STORAGE_FILE):
            os.remove(PERSISTENT_STORAGE_FILE)
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        self.master_server = MasterServer()

    def tearDown(self):
        # Clean up after tests
        if os.path.exists(PERSISTENT_STORAGE_FILE):
            os.remove(PERSISTENT_STORAGE_FILE)
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)

    def test_save_and_load_database(self):
        self.master_server.set_value("test_key", "test_value")
        time.sleep(2)  # Wait a bit for periodic save
        loaded_database = load_from_persistent_storage()
        self.assertIn("test_key", loaded_database)
        self.assertEqual(loaded_database["test_key"], "test_value")

    def test_load_database_on_startup(self):
        self.master_server.set_value("test_key", "test_value")
        time.sleep(2)  # Wait a bit for periodic save

        new_master_server = MasterServer()
        self.assertIn("test_key", new_master_server.database)
        self.assertEqual(new_master_server.database["test_key"], "test_value")

    def test_append_log(self):
        self.master_server.set_value("test_key1", "test_value1")
        self.master_server.set_value("test_key2", "test_value2")
        time.sleep(2)  # Wait a bit for periodic save

        self.master_server.save_database()  # Force save to ensure log compaction
        loaded_database = load_from_persistent_storage()
        self.assertIn("test_key1", loaded_database)
        self.assertIn("test_key2", loaded_database)
        self.assertEqual(loaded_database["test_key1"], "test_value1")
        self.assertEqual(loaded_database["test_key2"], "test_value2")

if __name__ == '__main__':
    unittest.main()
