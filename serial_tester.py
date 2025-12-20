import serial
import time
from datetime import datetime
from config import SERIAL_PORT, BAUDRATE

def serial_tester():
    try:
        ser = serial.Serial(
            port=SERIAL_PORT, # --- Si no reconoce el puerto, verificar en "adm de dispositivos" y corregir en config.py
            baudrate=BAUDRATE, #--- No se cambia, está especificado en el manual
            bytesize=serial.EIGHTBITS, #--- No se cambia, está especificado en el manual
            parity=serial.PARITY_NONE, #--- No se cambia, está especificado en el manual
            stopbits=serial.STOPBITS_ONE, #--- No se cambia, está especificado en el manual
            timeout=0.1
        )

        print(f"Escuchando en {SERIAL_PORT} @ {BAUDRATE} baud...")


        today = datetime.now().strftime("%Y.%m.%d") #--- Extrae fecha de hoy, para usar en el nombre del archivo
        filename = f"{today} - datos_extraidos.txt" # --- El nombre del archivo será igual a ej. "2025.11.24 - datos_extraidos.txt"

        with open(filename, "ab") as f:
            while True:
                try:
                    byte = ser.read(1)
                    if not byte:
                        continue

                    # --- Guardar el byte crudo en archivo ---
                    f.write(byte)
                    f.flush()  # asegura que se escriba al instante

                    # --- Mostrar en pantalla (solo para debug) ---
                    try:
                        ch = byte.decode("utf-8", errors="replace")
                    except Exception:
                        ch = str(byte)
                    print(repr(ch), end="")  # repr() para ver \r o \n explícito

                except Exception as e:
                    print("Error leyendo serial:", e)
                    time.sleep(0.1)

    except Exception as e:
        print("No se pudo abrir el puerto:", e)


if __name__ == "__main__":
    serial_tester()