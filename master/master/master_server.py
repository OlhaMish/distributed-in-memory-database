import requests
import grequests
from flask import Flask, request, jsonify
from master.storage import save_to_persistent_storage, load_from_persistent_storage

app = Flask(__name__)

class MasterServer:
    def __init__(self):
        self.database = load_from_persistent_storage()
        self.edge_nodes = []

    def save_database(self):
        save_to_persistent_storage(self.database)

    def set_value(self, key, value):
        self.database[key] = value
        self.broadcast_set(key, value)
        self.save_database()
        return {"status": "success", "key": key, "value": value}

    def get_value(self, key):
        value = self.database.get(key, None)
        return {"status": "success", "key": key, "value": value}

    def broadcast_set(self, key, value):
       requests = []
       for node in self.edge_nodes:
           url = f"{node['url']}/keys/{key}"
           data = {"value": value}
           requests.append(grequests.post(url, json=data))
       responses = grequests.map(requests)
       for response in responses:
           if response is not None and response.status_code != 200:
               print(f"Error broadcasting to {node['url']}: {response.status_code}")


    def sync_with_master(self):
        for node in self.edge_nodes:
            response = requests.get(f"{node['url']}/keys")
            if response.status_code == 200:
                node_data = response.json()
                self.database.update(node_data)
        self.save_database()
