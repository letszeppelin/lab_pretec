import serial
import time
from datetime import datetime

def serial_tester():
    try:
        ser = serial.Serial(
            port="COM5",
            baudrate=9600, 
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1
        )

        print("Escuchando...")

        today = datetime.now().strftime("%Y.%m.%d")
        filename = f"{today} - datos_extraidos.txt"

        recibiendo = False
        ultimo_byte = time.time()
        TIEMPO_FIN = 5.0 

        with open(filename, "ab") as f:
            while True:
                try:
                    byte = ser.read(1)

                    if byte:
                        if not recibiendo:
                            recibiendo = True

                        ultimo_byte = time.time()

                        # Guardar byte crudo
                        f.write(byte)
                        f.flush()

                        # Mostrar en pantalla
                        try:
                            ch = byte.decode("utf-8", errors="replace")
                        except Exception:
                            ch = str(byte)
                        print(ch) #print(repr(ch), end="")  para debug extra

                    else:
                        if recibiendo and (time.time() - ultimo_byte) >= TIEMPO_FIN:
                            print("\nEscuchando...")
                            recibiendo = False

                except Exception as e:
                    print("Error leyendo serial:", e)
                    time.sleep(0.1)

    except Exception as e:
        print("No se pudo abrir el puerto:", e)


if __name__ == "__main__":
    serial_tester()