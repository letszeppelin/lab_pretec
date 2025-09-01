import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from file_manager import load_meta, load_raw
from config import DISPLAY_LAST
from gui.treeview_widget import create_treeview
from gui.edit_popup import open_edit_popup
import serial_reader  
from ttkbootstrap.dialogs import Messagebox

COLUMNS = ["ID","Fecha","Hora","Carga (kN)","Resistencia (MPa)","Nombre","Descripcion","Fecha de Moldeo","fck"]

class ResultsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resultados Máquina de Compresión")
        self.meta = load_meta()
        self.raw_data = load_raw()
        self.last_tests = self.raw_data[-DISPLAY_LAST:]
        self.create_widgets()
        self.populate_treeview()
        self.auto_refresh()
        self.update_serial_status()

    def create_widgets(self):
        # Frame principal
        frame = tb.Frame(self.root)
        frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Label para mostrar estado del puerto serial
        self.status_label = tb.Label(self.root, text="Estado: Desconocido")
        self.status_label.pack(fill=X, padx=10, pady=(0, 5))

        # Treeview
        self.tree = create_treeview(frame, COLUMNS)

        # Botón editar
        self.edit_btn = tb.Button(self.root, text="Editar Seleccionado", command=self.edit_selected, bootstyle="info")
        self.edit_btn.pack(pady=5)

    def populate_treeview(self):
        top, bottom = self.tree.yview()
        selected_items = self.tree.selection()
        self.tree.delete(*self.tree.get_children())

        for row in self.last_tests:
            unique_id = row.get("unique_id")
            meta_row = self.meta.get(unique_id, {})
            values = [
                row.get("test_id",""),
                row.get("date",""),
                row.get("time",""),
                row.get("max_load",""),
                row.get("max_resistance",""),
                meta_row.get("Name",""),
                meta_row.get("Description",""),
                meta_row.get("Moldeo",""),
                meta_row.get("fck","")
            ]
            self.tree.insert("", "end", iid=unique_id, values=values)

        for iid in selected_items:
            if iid in self.tree.get_children():
                self.tree.selection_add(iid)

        if bottom == 1.0:
            self.tree.yview_moveto(1.0)
        else:
            self.tree.yview_moveto(top)

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            Messagebox.show_error("Seleccione un test para editar", "Sin Selección", parent=self.root)
            return
        unique_id = selected[0]
        # pasar test_id tambien
        row = next((r for r in self.last_tests if r["unique_id"] == unique_id), None)
        test_id = row.get("test_id") if row else ""

        open_edit_popup(self.root, unique_id, test_id, self.meta, self.populate_treeview)


    def auto_refresh(self):
        self.raw_data = load_raw()
        self.last_tests = self.raw_data[-DISPLAY_LAST:]
        self.populate_treeview()
        self.root.after(5000, self.auto_refresh)

    def update_serial_status(self):
        self.status_label.config(text=f"Estado: {serial_reader.serial_status}")

        # Estado del Serial
        status = serial_reader.serial_status
        if "Escuchando" in status:
            self.status_label.configure(foreground="#0078d7")
        elif "Recibiendo" in status:
            self.status_label.configure(foreground="green")
        elif "Error" in status or "No conectado" in status:
            self.status_label.configure(foreground="red")
        else:
            self.status_label.configure(foreground="black")

        self.root.after(2000, self.update_serial_status)