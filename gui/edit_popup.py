import tkinter as tk
from tkinter import messagebox
from file_manager import save_meta
from datetime import datetime

def open_edit_popup(parent, unique_id, meta, refresh_callback):
    popup = tk.Toplevel(parent)
    popup.title(f"Editar Test {unique_id}")
    popup.grab_set()

    tk.Label(popup, text="Nombre:").grid(row=0,column=0)
    name_entry = tk.Entry(popup, width=50)
    name_entry.grid(row=0,column=1)
    name_entry.insert(0, meta.get(unique_id, {}).get("Name",""))

    tk.Label(popup, text="Descripción:").grid(row=1,column=0)
    desc_entry = tk.Entry(popup, width=50)
    desc_entry.grid(row=1,column=1)
    desc_entry.insert(0, meta.get(unique_id, {}).get("Description",""))

    tk.Label(popup, text="Fecha de moldeo (dd/mm/yyyy):").grid(row=2, column=0)
    moldeo_entry = tk.Entry(popup, width=20)
    moldeo_entry.grid(row=2, column=1)
    moldeo_entry.insert(0, meta.get(unique_id, {}).get("Moldeo", ""))

    #codigo para el entry del fck
    tk.Label(popup, text="fck:").grid(row=3, column=0)
    fck_options = [21, 25, 30, 35, 40, 50, "Otro"]
    fck_var = tk.StringVar()
    fck_var.set(meta.get(unique_id, {}).get("fck", fck_options[0]))
    fck_menu = tk.OptionMenu(popup, fck_var, *fck_options)
    fck_menu.grid(row=3, column=1)
    fck_custom_entry = tk.Entry(popup, width=10)
    fck_custom_entry.grid(row=3, column=2)
    fck_custom_entry.grid_remove()  # Oculto al inicio

    def on_fck_change(*args):
        if fck_var.get() == "Otro":
            fck_custom_entry.grid()  # mostrar
        else:
            fck_custom_entry.grid_remove()  # ocultar

    fck_var.trace_add("write", on_fck_change)

    #código para guardar y cerrar el popup
    def save_and_close():
        # Validar fecha de moldeo
        fecha_str = moldeo_entry.get()
        try:
            _ = datetime.strptime(fecha_str, "%d/%m/%Y")  # Solo validar formato
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA")
            return  # No cerrar popup hasta que se corrija

        # Validar fck
        fck_val = fck_var.get()
        if fck_val == "Otro":
            try:
                fck_val = float(fck_custom_entry.get())
            except ValueError:
                messagebox.showerror("Error", "fck debe ser un número")
                return  # No cerrar popup hasta que se corrija

        # Crear entrada en meta si no existe
        if unique_id not in meta:
            meta[unique_id] = {}

        # Guardar datos en meta
        meta[unique_id] = {
            "test_id": meta[unique_id].get("test_id", ""),
            "Name": name_entry.get(),
            "Description": desc_entry.get(),
            "Moldeo": fecha_str,
            "fck": fck_val
        }

        # Guardar en CSV y refrescar Treeview
        save_meta(meta)
        refresh_callback()
        popup.destroy()


    tk.Button(popup, text="Guardar", command=save_and_close).grid(row=4,column=0)
    tk.Button(popup, text="Cancelar", command=popup.destroy).grid(row=4,column=1)