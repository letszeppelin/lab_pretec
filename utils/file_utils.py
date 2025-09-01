import json

CACHE_FILE = "last_meta.json"

def save_last_meta(meta_dict):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(meta_dict, f)
    except Exception as e:
        print("Error guardando last_meta.json:", e)

def load_last_meta():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print("Error leyendo last_meta.json:", e)
        return {}