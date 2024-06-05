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

master_server = MasterServer()

@app.route('/set', methods=['POST'])
def set_value():
    data = request.json
    result = master_server.set_value(data['key'], data['value'])
    return jsonify(result)

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    result = master_server.get_value(key)
    return jsonify(result)

@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify(master_server.edge_nodes)

@app.route('/nodes', methods=['POST'])
def add_node():
    node = request.json
    master_server.edge_nodes.append(node)
    return jsonify({"status": "node added"})

@app.route('/keys', methods=['GET'])
def get_all_keys():
    return jsonify(master_server.database)

if __name__ == '__main__':
    master_server.sync_with_master()
    app.run(host='0.0.0.0', port=5000)
