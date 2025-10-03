import serial
import time
from config import SERIAL_PORT, BAUDRATE

def serial_tester():
    try:
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1
        )

        print(f"Escuchando en {SERIAL_PORT} @ {BAUDRATE} baud...")

        with open("raw_output1.txt", "ab") as f:  # binario, append
            while True:
                try:
                    byte = ser.read(1)
                    if not byte:
                        continue

                    # --- Guardar el byte crudo en archivo ---
                    f.write(byte)
                    f.flush()  # opcional, asegura que se escriba al instante

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