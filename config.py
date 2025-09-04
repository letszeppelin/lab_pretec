import csv
import os

# Configuración general
SERIAL_PORT = "COM3"     # Ajustar al puerto real   
BAUDRATE = 9600
DISPLAY_LAST = 100
USE_SIMULATOR = True        # True = simulador, False = puerto real

# Carpeta data relativa al proyecto
BASE_DIR = os.path.dirname(__file__)  
DATA_DIR = os.path.join(BASE_DIR, "data")

# Crear la carpeta si no existe
os.makedirs(DATA_DIR, exist_ok=True)

# --- Archivos CSV ---
RAW_CSV = os.path.join(DATA_DIR, "resultados_raw.csv")
META_CSV = os.path.join(DATA_DIR, "resultados_meta.csv")