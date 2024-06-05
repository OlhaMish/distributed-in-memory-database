import requests
import time


class DatabaseClient:
    def __init__(self, master_url):
        self.master_url = master_url
        self.slave_nodes = self._get_slave_nodes()
        self.best_slave = self._get_best_slave()

    def _get_slave_nodes(self):
        response = requests.get(f"{self.master_url}/nodes")
        response.raise_for_status()
        return response.json()  # Assumes the response is a JSON list of slave IPs

    def _get_best_slave(self):
        best_latency = float('inf')
        best_slave = None
        for slave in self.slave_nodes:
            start_time = time.time()
            try:
                requests.get(f"http://{slave}/heartbeat", timeout=2)
                latency = time.time() - start_time
                if latency < best_latency:
                    best_latency = latency
                    best_slave = slave
            except requests.RequestException as e:
                print(f"Error contacting slave {slave}: {e}")
                continue
        if best_slave is None:
            raise Exception("No responsive slave nodes found")
        return best_slave

    def _switch_slave(self):
        self.best_slave = self._get_best_slave()

    def get(self, key):
        try:
            response = requests.get(f"http://{self.best_slave}/keys/{key}", timeout=2)
            response.raise_for_status()
            return response.json().get("value")
        except requests.RequestException:
            self._switch_slave()
            return self.get(key)

    def set(self, key, value):
        response = requests.post(f"{self.master_url}/keys", json={"key": key, "value": value})
        response.raise_for_status()
