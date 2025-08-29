import csv
import random
import time
from datetime import datetime
from config import RAW_CSV
from file_manager import generate_unique_id  

def simulator_thread():
    test_counter = 1
    while True:
        # Simula datos en tiempo real (ejemplo de carga)
        for t in range(1, 20):
            load = round(random.uniform(-5, 210), 3)
            t_elapsed = round(0.4 + t * 0.1, 3)
            time.sleep(0.05)

        now = datetime.now()
        date_str = now.strftime("%d/%m/%y")
        time_str = now.strftime("%H:%M")
        fmt = "2/3"
        test_id = f"{test_counter:04d}"
        unique_id = generate_unique_id()  # ahora creamos un ID único

        length = width = 150.0
        area = 22500.0
        weight = round(random.uniform(11, 12), 3)
        max_load = round(random.uniform(200, 220), 3)
        max_res = round(max_load * 0.045, 3)

        with open(RAW_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                unique_id, fmt, test_id, date_str, time_str, 25.0,
                length, width, "", "", area,
                weight, "", "", "", max_load, max_res
            ])

        print(f"Simulación Test {test_id}")
        test_counter += 1
        time.sleep(2)
