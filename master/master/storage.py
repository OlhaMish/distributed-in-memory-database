import json
import os

PERSISTENT_STORAGE_FILE = 'database.json'

def save_to_persistent_storage(database):
    with open(PERSISTENT_STORAGE_FILE, 'w') as f:
        json.dump(database, f)
    print(f"Database saved to {PERSISTENT_STORAGE_FILE}")

def load_from_persistent_storage():
    if not os.path.exists(PERSISTENT_STORAGE_FILE):
        return {}
    
    with open(PERSISTENT_STORAGE_FILE, 'r') as f:
        database = json.load(f)
    print(f"Database loaded from {PERSISTENT_STORAGE_FILE}")
    return database
