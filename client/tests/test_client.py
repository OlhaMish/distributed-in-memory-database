import unittest
from unittest.mock import patch, Mock
from client.client import DistributedDatabaseClient

class TestDistributedDatabaseClient(unittest.TestCase):
    def setUp(self):
        self.client = DistributedDatabaseClient(master_url="http://localhost:5000")

    @patch('client.client.requests.get')
    def test_fetch_edge_nodes(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{"url": "http://edge1", "location": {"latitude": 40.7128, "longitude": -74.0060}}]
        mock_get.return_value = mock_response

        edge_nodes = self.client.fetch_edge_nodes()
        self.assertIsInstance(edge_nodes, list)
        self.assertEqual(edge_nodes[0]['url'], "http://edge1")

    @patch('client.geoip.requests.get')
    @patch('client.geoip.get_client_ip')
    def test_get_client_location(self, mock_get_client_ip, mock_requests_get):
        ip = '8.8.8.8'  # Example IP address

        # Mock the response for get_client_ip
        mock_get_client_ip.return_value = ip

        # Mock the response for the first call to requests.get in get_client_ip
        mock_ip_response = Mock()
        mock_ip_response.json.return_value = {'origin': ip}

        # Mock the response for the second call to requests.get in get_client_location
        mock_location_response = Mock()
        mock_location_response.json.return_value = {'city': {'lat': 37.3861, 'lon': -122.0839}}

        # Set the side_effect of mock_requests_get to return the two responses in sequence
        mock_requests_get.side_effect = [mock_ip_response, mock_location_response]

        location = self.client.get_client_location()
        self.assertIn('latitude', location)
        self.assertIn('longitude', location)

    @patch('client.client.requests.get')
    def test_get_nearest_edge_node(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [{"url": "http://edge1", "location": {"latitude": 40.7128, "longitude": -74.0060}}]
        mock_get.return_value = mock_response

        self.client.edge_nodes = [
            {'url': 'http://edge1', 'location': {'latitude': 40.7128, 'longitude': -74.0060}},  # New York
            {'url': 'http://edge2', 'location': {'latitude': 34.0522, 'longitude': -118.2437}}  # Los Angeles
        ]
        self.client.client_location = {'latitude': 41.8781, 'longitude': -87.6298}  # Chicago
        nearest_node = self.client.get_nearest_edge_node()
        self.assertEqual(nearest_node['url'], 'http://edge1')

if __name__ == '__main__':
    unittest.main()
