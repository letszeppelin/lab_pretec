import threading
import time
import random
from file_manager import generate_unique_id
from config import RAW_CSV
import csv
import serial_reader  

serial_status = "Desconectado"

def simulator_thread():
    serial_reader.serial_status = "Escuchando"
    test_counter = 1
    while True:
        try:
            serial_reader.serial_status = "Recibiendo"
            now = time.localtime()
            date_str = time.strftime("%d/%m/%y", now)
            time_str = time.strftime("%H:%M:%S", now)

            fmt = "2/3"
            test_id = f"{test_counter:04d}"
            length = width = 150.0
            area = 22500.0
            weight = round(random.uniform(11,12),3)
            max_load = round(random.uniform(200,220),3)
            max_res = round(max_load * 0.045,3)

            unique_id = generate_unique_id()

            with open(RAW_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    unique_id,
                    fmt, test_id, date_str, time_str, 25.0,
                    length, width, "", "", area,
                    weight, "", "", "", max_load, max_res
                ])

            print(f"Simulación Test {test_id}")
            test_counter += 1
            time.sleep(2)

        except Exception as e:
            serial_reader.serial_status = f"Error simulador: {e}"
            time.sleep(2)

def start_simulator():
    t = threading.Thread(target=simulator_thread, daemon=True)
    t.start()