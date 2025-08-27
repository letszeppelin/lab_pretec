import serial
import csv
from config import SERIAL_PORT, BAUDRATE, RAW_CSV

def serial_listener():
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    print("Escuchando puerto serial...")
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue

            if line.startswith("$ALL"):
                parts = line.split()
                if len(parts) >= 4:
                    _, load, t_elapsed, _ = parts
                    print(f"Status: {load} kN @ {t_elapsed} s")
                continue

            if line.startswith(("$C","$$C","$F","$$F","$B","$$B")):
                parts = line.split()
                fmt = "2/3" if line.startswith("$$") else "1"
                test_id = parts[2]
                date = parts[3]
                time_ = parts[4]
                temp = length = width = diam = height = area = weight = density = curing = pace = max_load = max_res = ""

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

                with open(RAW_CSV, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        fmt, test_id, date, time_, temp,
                        length, width, diam, height, area,
                        weight, density, curing,
                        pace, max_load, max_res
                    ])
                print(f"Resultado: {test_id} | Max Load={max_load} | Max Res={max_res}")

        except Exception as e:
            print("Error leyendo serial:", e)
