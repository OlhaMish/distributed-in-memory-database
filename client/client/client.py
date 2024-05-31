import requests
from client.geoip import get_client_ip, get_client_location

class DistributedDatabaseClient:
    def __init__(self, master_url):
        self.master_url = master_url
        self.edge_nodes = self.fetch_edge_nodes()
        self.client_location = self.get_client_location()

    def fetch_edge_nodes(self):
        response = requests.get(f"{self.master_url}/nodes")
        return response.json()

    def get_client_location(self):
        ip = get_client_ip()
        location = get_client_location(ip)
        return location

    def calculate_distance(self, loc1, loc2):
        from geopy.distance import geodesic
        return geodesic((loc1['latitude'], loc1['longitude']), (loc2['latitude'], (loc2['longitude']))).km

    def get_nearest_edge_node(self):
        nearest_node = min(self.edge_nodes, key=lambda node: self.calculate_distance(self.client_location, node['location']))
        return nearest_node

    def get(self, key):
        nearest_node = self.get_nearest_edge_node()
        response = requests.get(f"{nearest_node['url']}/keys/{key}")
        print(f"Response from {nearest_node['url']}/keys/{key}: {response.text}")  # Debugging line
        return response.json().get('value', '')

    def set(self, key, value):
        response = requests.post(f"{self.master_url}/keys/{key}", json={"value": value})
        return response.status_code == 200
