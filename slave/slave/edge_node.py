import requests
from flask import Flask, request, jsonify
import os

PORT = 5001


class EdgeNode:
    def __init__(self, master_url):
        self.master_url = master_url
        self.database = {}

    def announce_to_master(self):
        requests.post(f"{self.master_url}/nodes", json={"port": PORT})

    def sync_with_master(self):
        try:
            response = requests.get(f"{self.master_url}/keys")
            if response.status_code == 200:
                self.database = response.json()
                print("Successfully synchronized with Master.")
            else:
                print(f"Failed to synchronize with Master: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error synchronizing with Master: {e}")

    def set_value(self, key, value):
        self.database[key] = value
        print(f"Set value: {key} -> {value}")  # Add this line
        return {"status": "success", "key": key, "value": value}

    def get_value(self, key):
        value = self.database.get(key)
        if value is not None:
            return {"status": "success", "key": key, "value": value}
        else:
            return {"status": "error", "message": "Key not found"}


app = Flask(__name__)
edge_node = EdgeNode(master_url=os.getenv("MASTER_URL", "http://localhost:5000"))


@app.route('/sync', methods=['POST'])
def sync():
    edge_node.sync_with_master()
    return jsonify({"status": "sync complete"})


@app.route('/keys/<key>', methods=['POST'])
def set_value(key):
    data = request.json
    result = edge_node.set_value(key, data['value'])
    return jsonify(result)


@app.route('/keys/<key>', methods=['GET'])
def get_value(key):
    result = edge_node.get_value(key)
    return jsonify(result)


def announce_self():
    requests.post()


if __name__ == '__main__':
    edge_node.announce_to_master()
    edge_node.sync_with_master()
    app.run(host='0.0.0.0', port=PORT)
