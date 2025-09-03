import os, json

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

CACHE_FILE = os.path.join(DATA_DIR, "last_meta.json")

def save_last_meta(meta_dict):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(meta_dict, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Error guardando last_meta.json:", e)

def load_last_meta():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print("Error leyendo last_meta.json:", e)
        return {}
