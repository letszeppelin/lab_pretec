import csv
import os
import uuid
from datetime import datetime
from config import RAW_CSV, META_CSV


def generate_unique_id():
    """Genera un ID único usando timestamp + sufijo aleatorio."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    return f"{timestamp}_{rand_suffix}"


def init_csvs():
    """Crea archivos CSV si no existen aún, con columna unique_id."""
    if not os.path.exists(RAW_CSV):
        with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "unique_id", "format", "test_id", "date", "time", "temperature",
                "length", "width", "diameter", "height", "area",
                "weight", "density", "curing_days",
                "pace_rate", "max_load", "max_resistance"
            ])

    if not os.path.exists(META_CSV):
        with open(META_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["unique_id", "test_id", "Name", "Description"])


def load_raw():
    """Carga datos de RAW_CSV."""
    data = []
    try:
        with open(RAW_CSV, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('test_id', '').strip():
                    continue
                data.append(row)
    except FileNotFoundError:
        pass
    return data


def load_meta():
    """Carga datos de META_CSV como diccionario indexed by unique_id."""
    meta = {}
    try:
        with open(META_CSV, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                unique_id = row.get("unique_id", "").strip()
                if not unique_id:
                    continue
                meta[unique_id] = row
    except FileNotFoundError:
        pass
    return meta


def save_meta(meta):
    """Guarda el diccionario meta (key = unique_id)."""
    if not meta:
        return
    with open(META_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["unique_id", "test_id", "Name", "Description"])
        writer.writeheader()
        for row in meta.values():
            writer.writerow(row)
