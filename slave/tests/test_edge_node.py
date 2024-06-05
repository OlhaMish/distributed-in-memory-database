import unittest
from slave.edge_node import EdgeNode


class TestEdgeNode(unittest.TestCase):
    def setUp(self):
        self.edge_node = EdgeNode(master_url="http://localhost:5000")

    def test_set_and_get_value(self):
        self.edge_node.set_value("test_key", "test_value")
        result = self.edge_node.get_value("test_key")
        self.assertEqual(result['value'], "test_value")

    def test_get_nonexistent_key(self):
        result = self.edge_node.get_value("nonexistent_key")
        self.assertEqual(result['status'], "error")
        self.assertEqual(result['message'], "Key not found")


if __name__ == '__main__':
    unittest.main()
