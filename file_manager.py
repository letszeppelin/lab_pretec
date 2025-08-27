import csv
import os
from config import RAW_CSV, META_CSV

def init_csvs():
    """Crea archivos CSV si no existen aún."""
    if not os.path.exists(RAW_CSV):
        with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "format","test_id","date","time","temperature",
                "length","width","diameter","height","area",
                "weight","density","curing_days",
                "pace_rate","max_load","max_resistance"
            ])

    if not os.path.exists(META_CSV):
        with open(META_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["test_id","Name","Description"])

def load_raw():
    data = []
    try:
        with open(RAW_CSV, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_id = row.get('test_id', '').strip()
                if not test_id:
                    continue
                data.append(row)
    except FileNotFoundError:
        pass
    return data

def load_meta():
    meta = {}
    try:
        with open(META_CSV, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_id = row.get('test_id', '').strip()
                if not test_id:
                    continue
                meta[test_id] = row
    except FileNotFoundError:
        pass
    return meta

def save_meta(meta):
    if not meta:
        return
    with open(META_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["test_id","Name","Description"])
        writer.writeheader()
        for row in meta.values():
            writer.writerow(row)
