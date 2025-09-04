import os
import uuid
import sqlite3
from datetime import datetime
from config import DATA_DIR  

DB_PATH = os.path.join(DATA_DIR, "resultados.db")

def get_connection():
    """Devuelve una conexión a la base de datos SQLite."""
    return sqlite3.connect(DB_PATH)

def generate_unique_id():
    """Genera un ID único usando timestamp + sufijo aleatorio."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    return f"{timestamp}_{rand_suffix}"

# Inicialización DB
def init_db():
    """Crea la base de datos y tablas si no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = get_connection()
    c = conn.cursor()

    # Tabla de resultados RAW
    c.execute("""
    CREATE TABLE IF NOT EXISTS raw_results (
        unique_id TEXT PRIMARY KEY,
        format TEXT,
        test_id TEXT,
        date TEXT,
        time TEXT,
        temperature REAL,
        length REAL,
        width REAL,
        diameter REAL,
        height REAL,
        area REAL,
        weight REAL,
        density REAL,
        curing_days INTEGER,
        pace_rate REAL,
        max_load REAL,
        max_resistance REAL
    )
    """)

    # Tabla de meta
    c.execute("""
    CREATE TABLE IF NOT EXISTS meta_results (
        unique_id TEXT PRIMARY KEY,
        test_id TEXT,
        Name TEXT,
        Description TEXT,
        Moldeo TEXT,
        fck REAL
    )
    """)

    conn.commit()
    conn.close()

# Cargar datos
def load_raw(limit=100):
    """Carga los últimos 'limit' registros de raw_results."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT *
        FROM raw_results
        ORDER BY date DESC, time DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def load_meta():
    """Carga META como diccionario indexed by unique_id."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM meta_results")
    rows = {row["unique_id"]: dict(row) for row in c.fetchall()}
    conn.close()
    return rows

# Guardar datos
def save_meta(meta):
    """Guarda un diccionario meta (key = unique_id) en SQLite."""
    if not meta:
        return
    conn = get_connection()
    c = conn.cursor()
    for unique_id, row in meta.items():
        test_id = row.get("test_id", "")
        c.execute("""
        INSERT OR REPLACE INTO meta_results
        (unique_id, test_id, Name, Description, Moldeo, fck)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            unique_id,
            test_id,
            row.get("Name", ""),
            row.get("Description", ""),
            row.get("Moldeo", ""),
            row.get("fck", None)
        ))
    conn.commit()
    conn.close()

def save_raw(row):
    """Guarda un registro RAW en SQLite."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO raw_results (
        unique_id, format, test_id, date, time, temperature,
        length, width, diameter, height, area,
        weight, density, curing_days,
        pace_rate, max_load, max_resistance
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["unique_id"], row["format"], row["test_id"], row["date"], row["time"], row["temperature"],
        row["length"], row["width"], row["diameter"], row["height"], row["area"],
        row["weight"], row["density"], row["curing_days"],
        row["pace_rate"], row["max_load"], row["max_resistance"]
    ))
    conn.commit()
    conn.close()