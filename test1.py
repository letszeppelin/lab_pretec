import time
from file_manager import generate_unique_id, save_raw

serial_status = "Desconectado"

def serial_listener_sim():
    global serial_status

    serial_status = "Escuchando"
    print("Simulador de puerto serial activo. Pega líneas y presiona Enter.")

    while True:
        try:
            line = input("> ").strip()  # ahora ves un prompt ">"
            if not line:
                continue  # ignorar líneas vacías

            # Actualizamos estado
            serial_status = "Recibiendo"

            if line.startswith("$ALL"):
                parts = line.split()
                if len(parts) >= 4:
                    _, load, t_elapsed, _ = parts
                    print(f"Status: {load} kN @ {t_elapsed} s")
                continue

            if line.startswith(("$C", "$$C", "$F", "$$F", "$B", "$$B")):
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
                    temp = parts[7]
                    if parts[0].startswith("$$C"):
                        length = parts[8]; width = parts[9]; area = parts[13]
                        weight = parts[14]; density = parts[15]; curing = parts[16]
                        pace = parts[17]; max_load = parts[18]; max_res = parts[19]
                    elif parts[0].startswith("$$F"):
                        height = parts[7]; width = parts[8]; area = parts[13]
                        weight = parts[14]; density = parts[15]; curing = parts[16]
                        pace = parts[17]; max_load = parts[18]; max_res = parts[19]
                    elif parts[0].startswith("$$B"):
                        length = parts[7]; width = parts[8]; area = parts[12]
                        weight = parts[13]; density = parts[14]; curing = parts[15]
                        pace = parts[16]; max_load = parts[17]; max_res = parts[18]

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
                print(f"Saverow: {row}")
                #save_raw(row)
                print(f"Resultado: {test_id} | Max Load={max_load} | Max Res={max_res}")

        except (IndexError, ValueError) as e:
            print("Error parseando línea:", line, "|", e)
        except Exception as e:
            print("Error en simulador:", e)

if __name__ == "__main__":
    serial_listener_sim()
    input("Presiona Enter para salir...")