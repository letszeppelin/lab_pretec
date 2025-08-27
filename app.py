import threading
import tkinter as tk
from config import USE_SIMULATOR
from simulator import simulator_thread
from serial_reader import serial_listener
from gui import ResultsApp
from file_manager import init_csvs

if __name__ == "__main__":
    init_csvs()

    if USE_SIMULATOR:
        t = threading.Thread(target=simulator_thread, daemon=True)
    else:
        t = threading.Thread(target=serial_listener, daemon=True)
    t.start()

    root = tk.Tk()
    app = ResultsApp(root)
    root.mainloop()