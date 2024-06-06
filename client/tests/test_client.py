import pytest
import requests
from unittest.mock import patch, Mock
from client.database_client import DatabaseClient


# Mocking the requests.get and requests.post methods
@patch('client.database_client.requests.get')
@patch('client.database_client.requests.post')
def test_database_client_initialization(mock_post, mock_get):
    # Mock the response for _get_slave_nodes
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: ["192.168.1.2", "192.168.1.3"]),
        Mock(status_code=200),
        requests.RequestException
    ]

    client = DatabaseClient(master_url="http://master")

    assert client.master_url == "http://master"
    assert client.slave_nodes == ["192.168.1.2", "192.168.1.3"]
    assert client.best_slave == "192.168.1.2"


@patch('client.database_client.requests.get')
def test_get_best_slave(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: ["192.168.1.2", "192.168.1.3"]),
        Mock(status_code=200),
        Mock(status_code=200),
        Mock(status_code=200),
        requests.RequestException
    ]

    client = DatabaseClient(master_url="http://master")
    best_slave = client._get_best_slave()

    assert best_slave == "192.168.1.2"


@patch('client.database_client.requests.get')
def test_get_method(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: ["192.168.1.2"]),
        Mock(status_code=200, json=lambda: {"value": "test_value"}),
        Mock(status_code=200, json=lambda: {"value": "test_value"})  # Adding an extra response to cover all calls
    ]

    client = DatabaseClient(master_url="http://master")
    value = client.get("test_key")

    assert value == "test_value"


@patch('client.database_client.requests.get')
@patch('client.database_client.requests.post')
def test_set_method(mock_post, mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: ["192.168.1.2"])
    mock_post.return_value = Mock(status_code=200)

    client = DatabaseClient(master_url="http://master")
    client.set("test_key", "test_value")

    mock_post.assert_called_with("http://master/keys", json={"key": "test_key", "value": "test_value"})


@patch('client.database_client.requests.get')
def test_no_responsive_slaves(mock_get):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: ["192.168.1.2", "192.168.1.3"]),
        requests.RequestException,
        requests.RequestException
    ]

    with pytest.raises(Exception, match="No responsive slave nodes found"):
        DatabaseClient(master_url="http://master")

