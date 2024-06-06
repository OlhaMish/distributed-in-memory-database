import json
import os

PERSISTENT_STORAGE_FILE = 'database.json'
LOG_FILE = 'database.log'

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

def append_to_log(key, value):
    with open(LOG_FILE, 'a') as log:
        log.write(json.dumps({key: value}) + '\n')

def compact_log():
    if not os.path.exists(LOG_FILE):
        return

    with open(PERSISTENT_STORAGE_FILE, 'r') as f:
        database = json.load(f)
        
    with open(LOG_FILE, 'r') as log:
        for line in log:
            update = json.loads(line.strip())
            database.update(update)

    save_to_persistent_storage(database)
    os.remove(LOG_FILE)
