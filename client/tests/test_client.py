import unittest
from unittest.mock import patch, Mock

from client.database_client import DatabaseClient


class TestDatabaseClient(unittest.TestCase):

    @patch('requests.get')
    def test_get_slave_nodes(self, mock_get):
        # Setup the mock to return a predefined response
        mock_response = Mock()
        mock_response.json.return_value = ["slave1", "slave2"]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = DatabaseClient("http://localhost:5000")
        self.assertEqual(client.slave_nodes, ["slave1", "slave2"])

    @patch('requests.get')
    def test_get_best_slave(self, mock_get):
        # Setup the mock to return a predefined response
        mock_get.side_effect = [
            Mock(status_code=200),  # Slave 1
            Mock(status_code=200),  # Slave 2
        ]

        with patch.object(DatabaseClient, '_get_slave_nodes', return_value=["slave1", "slave2"]):
            client = DatabaseClient("http://localhost:5000")
            self.assertIn(client.best_slave, ["slave1", "slave2"])

    @patch('requests.get')
    def test_get(self, mock_get):
        # Mock the slave node responses
        mock_response = Mock()
        mock_response.json.return_value = {"value": "test_value"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with patch.object(DatabaseClient, '_get_slave_nodes', return_value=["slave1"]), \
             patch.object(DatabaseClient, '_get_best_slave', return_value="slave1"):
            client = DatabaseClient("http://localhost:5000")
            value = client.get("test_key")
            self.assertEqual(value, "test_value")

    @patch('requests.post')
    def test_set(self, mock_post):
        # Mock the master node response
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = DatabaseClient("http://localhost:5000")
        client.set("test_key", "test_value")
        mock_post.assert_called_once_with("http://localhost:5000/keys",
                                          json={"key": "test_key", "value": "test_value"})


if __name__ == '__main__':
    unittest.main()
