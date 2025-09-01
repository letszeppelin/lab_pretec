import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from file_manager import save_meta
from datetime import datetime
from ttkbootstrap.dialogs import Messagebox

def open_edit_popup(parent, unique_id, test_id, meta, refresh_callback):
    popup = tb.Toplevel(parent)
    popup.title(f"Editar Test {unique_id}")
    popup.grab_set()
    
    PAD_X = 5
    PAD_Y = 5

    # --- Nombre ---
    tb.Label(popup, text="Nombre:").grid(row=0, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    name_entry = tb.Entry(popup, width=50)
    name_entry.grid(row=0, column=1, columnspan=2, sticky=W, padx=PAD_X, pady=PAD_Y)
    name_entry.insert(0, meta.get(unique_id, {}).get("Name",""))

    # --- Descripción ---
    tb.Label(popup, text="Descripción:").grid(row=1, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    desc_entry = tb.Entry(popup, width=50)
    desc_entry.grid(row=1, column=1, columnspan=2, sticky=W, padx=PAD_X, pady=PAD_Y)
    desc_entry.insert(0, meta.get(unique_id, {}).get("Description",""))

    # --- Fecha de moldeo ---
    tb.Label(popup, text="Fecha de moldeo (dd/mm/yyyy):").grid(row=2, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    moldeo_entry = tb.Entry(popup, width=20)
    moldeo_entry.grid(row=2, column=1, columnspan=2, sticky=W, padx=PAD_X, pady=PAD_Y)
    moldeo_entry.insert(0, meta.get(unique_id, {}).get("Moldeo", ""))

    # --- fck ---
    tb.Label(popup, text="fck (MPa):").grid(row=3, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    fck_options = [21, 25, 30, 35, 40, 50, "Otro"]
    fck_var = tb.StringVar()
    fck_var.set(meta.get(unique_id, {}).get("fck", fck_options[0]))
    fck_menu = tb.OptionMenu(popup, fck_var, *fck_options, bootstyle="info")
    fck_menu.grid(row=3, column=1, sticky=W, padx=PAD_X, pady=PAD_Y)
   
    fck_custom_entry = tb.Entry(popup, width=10)
    fck_custom_entry.grid(row=3, column=2, sticky=W, padx=PAD_X, pady=PAD_Y)
    fck_custom_entry.grid_remove()

    def on_fck_change(*args):
        if fck_var.get() == "Otro":
            fck_custom_entry.grid()
        else:
            fck_custom_entry.grid_remove()

    fck_var.trace_add("write", on_fck_change)

    # --- Función Guardar y Cerrar ---
    def save_and_close():
        # Validar fecha de moldeo
        fecha_str = moldeo_entry.get()
        try:
            _ = datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            Messagebox.show_error("Formato de fecha inválido. Use DD/MM/AAAA", "Error", parent=popup)
            return

        # Validar fck
        fck_val = fck_var.get()
        if fck_val == "Otro":
            try:
                fck_val = float(fck_custom_entry.get())
            except ValueError:
                Messagebox.show_error("fck debe ser un número", "Error", parent=popup)
                return

        if unique_id not in meta:
            meta[unique_id] = {}

        meta[unique_id] = {
            "test_id": test_id,
            "Name": name_entry.get(),
            "Description": desc_entry.get(),
            "Moldeo": fecha_str,
            "fck": fck_val
        }

        save_meta(meta)
        refresh_callback()
        popup.destroy()

    # --- Botones centrados ---
    btn_frame = tb.Frame(popup)
    btn_frame.grid(row=4, column=0, columnspan=3, pady=15)
    tb.Button(btn_frame, text="Guardar", command=save_and_close, bootstyle="success").pack(side=LEFT, padx=10)
    tb.Button(btn_frame, text="Cancelar", command=popup.destroy, bootstyle="danger").pack(side=LEFT, padx=10)