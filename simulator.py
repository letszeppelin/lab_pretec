import threading
import time
import random
from file_manager import generate_unique_id, save_raw
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
            type = "Compresión (Cubo)"
            test_id = f"{test_counter:04d}"
            length = width = 150.0
            area = 22500.0
            weight = round(random.uniform(11, 12), 3)
            max_load = round(random.uniform(200, 220), 3)
            max_res = round(max_load * 0.045, 3)

            unique_id = generate_unique_id()

            row = {
                "unique_id": unique_id,
                "type": type,
                "format": fmt,
                "test_id": test_id,
                "date": date_str,
                "time": time_str,
                "temperature": 25.0,
                "length": length,
                "width": width,
                "diameter": "",
                "height": "",
                "area": area,
                "weight": weight,
                "density": "",
                "curing_days": "",
                "pace_rate": "",
                "max_load": max_load,
                "max_resistance": max_res,
            }

            save_raw(row)
            print(f"Simulación Test {test_id}")
            test_counter += 1
            time.sleep(2)

        except Exception as e:
            serial_reader.serial_status = f"Error simulador: {e}"
            time.sleep(2)


def start_simulator():
    t = threading.Thread(target=simulator_thread, daemon=True)
    t.start()