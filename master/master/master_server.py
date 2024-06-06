import requests
import grequests
from master.storage import save_to_persistent_storage, load_from_persistent_storage, append_to_log, compact_log
from threading import Timer

class MasterServer:
    def __init__(self):
        self.database = load_from_persistent_storage()
        self.edge_nodes = []
        self.pending_updates = {}
        self.save_interval = 60  # Save changes every 60 seconds
        self.start_periodic_save()

    def start_periodic_save(self):
        def save_changes():
            if self.pending_updates:
                self.save_database()
                self.pending_updates = {}
            Timer(self.save_interval, save_changes).start()

        save_changes()

    def save_database(self):
        # Save only the pending updates
        for key, value in self.pending_updates.items():
            self.database[key] = value
        save_to_persistent_storage(self.database)
        compact_log()

    def set_value(self, key, value):
        self.pending_updates[key] = value
        append_to_log(key, value)
        self.broadcast_set(key, value)
        return {"status": "success", "key": key, "value": value}

    def get_value(self, key):
        value = self.database.get(key, None)
        return {"status": "success", "key": key, "value": value}

    def broadcast_set(self, key, value):
        requests = []
        for node in self.edge_nodes:
            url = f"http://{node}/keys/{key}"
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
