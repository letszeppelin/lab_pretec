import serial
import csv
import os
import config
from datetime import datetime

# --- Carpeta donde se guardarán los archivos ---
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Variables de control ---
current_title = None
current_header = None
current_writer = None
current_file = None
blocks_saved = 0   # Contador de bloques guardados

print("Esperando transmisión de ensayos archivados... (CTRL+C para salir)")

try:
    if not config.USE_SIMULATOR:
        ser = serial.Serial(
            port=config.SERIAL_PORT,
            baudrate=config.BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
    else:
        ser = None

    while True:
        if config.USE_SIMULATOR:
            line = input()
        else:
            line = ser.readline().decode(errors="ignore").strip()

        if not line:
            continue

        # --- Detectar título de bloque ---
        if line.isupper() and not line.startswith("ID") and not line[0].isdigit():
            if current_file:
                current_file.close()
                blocks_saved += 1
                print(f"Bloques guardados: {blocks_saved}", end="\r")

            normalized_title = line.replace("(", "").replace(")", "").replace(" ", "_")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Historial_{normalized_title}_{timestamp}.csv"
            filepath = os.path.join(OUTPUT_DIR, filename)

            current_file = open(filepath, "w", newline="", encoding="utf-8")
            current_writer = csv.writer(current_file)
            current_title = line
            current_header = None
            continue

        # --- Encabezado ---
        if current_title and not current_header and "ID" in line:
            current_header = line.split()
            current_writer.writerow(current_header)
            continue

        # --- Fila de datos ---
        if current_header and (line[0].isdigit() or line.startswith("0")):
            parts = line.split()
            current_writer.writerow(parts)

except KeyboardInterrupt:
    print(f"\nFinalizado por el usuario. Total bloques guardados: {blocks_saved}")

finally:
    if current_file:
        current_file.close()
        blocks_saved += 1
        print(f"Bloques guardados: {blocks_saved}")
    if not config.USE_SIMULATOR and ser:
        ser.close()
    print("Todos los archivos guardados y puerto cerrado.")
