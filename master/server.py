import logging

from gevent import monkey
monkey.patch_all()

from flask import Flask, request, jsonify
from master.master_server import MasterServer

app = Flask(__name__)


master_server = MasterServer()


@app.route('/nodes', methods=['GET'])
def get_nodes():
    return jsonify(master_server.edge_nodes)


@app.route('/nodes', methods=['POST'])
def add_node():
    node_ip = request.remote_addr
    port = request.json.get("port")

    master_server.edge_nodes.append(f"{node_ip}:{port}")
    logging.error(f"Added new EdgeNode {node_ip}")
    return jsonify({"status": "node added"})


@app.route('/keys', methods=['POST'])
def set_value():
    data = request.json
    logging.error(data)
    result = master_server.set_value(data['key'], data['value'])
    return jsonify(result)


@app.route('/keys', methods=['GET'])
def get_all_keys():
    return jsonify(master_server.database)


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({"status": "alive"})


if __name__ == '__main__':
    master_server.sync_with_master()
    app.run(host='0.0.0.0', port=5000)
