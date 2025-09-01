import threading
import ttkbootstrap as tb
from config import USE_SIMULATOR
from simulator import simulator_thread
from serial_reader import serial_listener
from gui.main_window import ResultsApp
from file_manager import init_csvs
#from gui.styles import setup_styles  # centralized styles

if __name__ == "__main__":
    init_csvs()

    if USE_SIMULATOR:
        t = threading.Thread(target=simulator_thread, daemon=True)
    else:
        t = threading.Thread(target=serial_listener, daemon=True)
    t.start()

    # Crear ttkbootstrap main window
    root = tb.Window(themename="cyborg")

    # Apply centralized styles
    #setup_styles(root)

    app = ResultsApp(root)

    root.mainloop()
