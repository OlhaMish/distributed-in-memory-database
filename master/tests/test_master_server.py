import unittest
from master.master_server import MasterServer
from master.storage import save_to_persistent_storage, load_from_persistent_storage
import os

class TestMasterServer(unittest.TestCase):
    def setUp(self):
        # Clear the persistent storage before each test
        if os.path.exists('database.json'):
            os.remove('database.json')
        self.master_server = MasterServer()

    def tearDown(self):
        # Clean up after tests
        if os.path.exists('database.json'):
            os.remove('database.json')

    def test_save_and_load_database(self):
        self.master_server.set_value("test_key", "test_value")
        save_to_persistent_storage(self.master_server.database)
        loaded_database = load_from_persistent_storage()
        self.assertIn("test_key", loaded_database)
        self.assertEqual(loaded_database["test_key"], "test_value")

    def test_load_database_on_startup(self):
        self.master_server.set_value("test_key", "test_value")
        save_to_persistent_storage(self.master_server.database)

        new_master_server = MasterServer()
        self.assertIn("test_key", new_master_server.database)
        self.assertEqual(new_master_server.database["test_key"], "test_value")

if __name__ == '__main__':
    unittest.main()
