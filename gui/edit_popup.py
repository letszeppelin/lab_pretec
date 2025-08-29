import tkinter as tk
from tkinter import messagebox
from file_manager import save_meta

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

    def save_and_close():
        meta[unique_id] = {"unique_id": unique_id,
                           "test_id": meta[unique_id].get("test_id",""),
                           "Name": name_entry.get(),
                           "Description": desc_entry.get()}
        save_meta(meta)
        refresh_callback()
        popup.destroy()

    tk.Button(popup, text="Guardar", command=save_and_close).grid(row=2,column=0)
    tk.Button(popup, text="Cancelar", command=popup.destroy).grid(row=2,column=1)