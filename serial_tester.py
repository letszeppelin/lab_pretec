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
            timeout=0.1  # pequeño timeout para no bloquear
        )

        print(f"Escuchando en {SERIAL_PORT} @ {BAUDRATE} baud...")

        buffer = b""  # acumulamos bytes recibidos

        while True:
            try:
                byte = ser.read(1)
                if not byte:
                    continue  # no llegó nada en este ciclo

                buffer += byte

                # Fin de línea detectado
                if byte in b"\r\n":
                    # Decodificamos línea completa
                    try:
                        line = buffer.decode("utf-8", errors="ignore").strip()
                    except Exception:
                        line = str(buffer)

                    # Mostrar con timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    if line:  # ignorar líneas vacías
                        print(f"[{line}")

                    # Reiniciamos buffer
                    buffer = b""

            except Exception as e:
                print("Error leyendo serial:", e)
                time.sleep(0.1)

    except Exception as e:
        print("No se pudo abrir el puerto:", e)


if __name__ == "__main__":
    serial_tester()