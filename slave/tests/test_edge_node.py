import pytest
from slave.edge_node import EdgeNode


@pytest.fixture
def edge_node():
    return EdgeNode(master_url="http://localhost:5000")


def test_set_and_get_value(edge_node):
    edge_node.set_value("test_key", "test_value")
    result = edge_node.get_value("test_key")
    assert result['value'] == "test_value"


def test_get_nonexistent_key(edge_node):
    result = edge_node.get_value("nonexistent_key")
    assert result['status'] == "error"
    assert result['message'] == "Key not found"