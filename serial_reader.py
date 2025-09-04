import serial
import time
import threading
from config import SERIAL_PORT, BAUDRATE, RAW_CSV
from file_manager import generate_unique_id, save_raw

serial_status = "Desconectado"
_last_data_time = None   # para controlar silencio en el puerto
SILENCE_TIMEOUT = 5      # segundos sin datos → estado vuelve a "Escuchando"


def serial_listener():
    global serial_status, _last_data_time
    try:
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

        serial_status = "Escuchando"
        print("Escuchando puerto serial...")

        while True:
            try:
                line = ser.readline().decode(errors="ignore").strip()

                # Detectar silencio en el puerto
                if not line:
                    if (
                        serial_status == "Recibiendo"
                        and _last_data_time
                        and (time.time() - _last_data_time > SILENCE_TIMEOUT)
                    ):
                        serial_status = "Escuchando"
                    continue

                # Si llega línea nueva → se actualiza timestamp
                _last_data_time = time.time()

                if line.startswith("$ALL"):
                    serial_status = "Recibiendo"
                    parts = line.split()
                    if len(parts) >= 4:
                        _, load, t_elapsed, _ = parts
                        print(f"Status: {load} kN @ {t_elapsed} s")
                    continue

                if line.startswith(("$C", "$$C", "$F", "$$F", "$B", "$$B")):
                    serial_status = "Recibiendo"
                    parts = line.split()
                    fmt = "2/3" if line.startswith("$$") else "1"
                    test_id = parts[2]
                    date = parts[3]
                    time_ = parts[4]

                    # Inicializamos vacíos
                    temp = length = width = diam = height = area = ""
                    weight = density = curing = pace = max_load = max_res = ""

                    if fmt == "1":
                        if parts[0].startswith("$C"):
                            length = parts[5]; width = parts[6]; area = parts[9]
                            pace = parts[10]; max_load = parts[11]; max_res = parts[12]
                        elif parts[0].startswith("$F"):
                            height = parts[5]; width = parts[6]; area = parts[9]
                            pace = parts[10]; max_load = parts[11]; max_res = parts[12]
                        elif parts[0].startswith("$B"):
                            length = parts[5]; width = parts[6]; area = parts[9]
                            pace = parts[10]; max_load = parts[11]; max_res = parts[12]

                    elif fmt == "2/3":
                        temp = parts[6]
                        if parts[0].startswith("$$C"):
                            length = parts[7]; width = parts[8]; area = parts[12]
                            weight = parts[13]; density = parts[14]; curing = parts[15]
                            pace = parts[16]; max_load = parts[17]; max_res = parts[18]
                        elif parts[0].startswith("$$F"):
                            height = parts[6]; width = parts[7]; area = parts[12]
                            weight = parts[13]; density = parts[14]; curing = parts[15]
                            pace = parts[16]; max_load = parts[17]; max_res = parts[18]
                        elif parts[0].startswith("$$B"):
                            length = parts[7]; width = parts[8]; area = parts[12]
                            weight = parts[13]; density = parts[14]; curing = parts[15]
                            pace = parts[16]; max_load = parts[17]; max_res = parts[18]

                    # Generamos un unique_id para cada registro
                    unique_id = generate_unique_id()

                    row = {
                        "unique_id": unique_id,
                        "format": fmt,
                        "test_id": test_id,
                        "date": date,
                        "time": time_,
                        "temperature": temp,
                        "length": length,
                        "width": width,
                        "diameter": diam,
                        "height": height,
                        "area": area,
                        "weight": weight,
                        "density": density,
                        "curing_days": curing,
                        "pace_rate": pace,
                        "max_load": max_load,
                        "max_resistance": max_res
                    }
                    save_raw(row)
                    print(f"Resultado: {test_id} | Max Load={max_load} | Max Res={max_res}")

            except (IndexError, ValueError) as e:
                # Error de parsing, no rompemos el bucle
                print("Error parseando línea:", line, "|", e)
                continue
            except Exception as e:
                print("Error leyendo serial:", e)
                serial_status = f"Error"

    except Exception as e:
        serial_status = f"No conectado"
        print("Error inicializando puerto:", e)


def start_serial_listener():
    t = threading.Thread(target=serial_listener, daemon=True)
    t.start()
