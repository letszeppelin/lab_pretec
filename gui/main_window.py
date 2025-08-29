import tkinter as tk
from file_manager import load_meta, load_raw
from config import DISPLAY_LAST
from gui.treeview_widget import create_treeview
from gui.edit_popup import open_edit_popup

COLUMNS = ["ID","Fecha","Hora","Carga (kN)","Resistencia (MPa)","Nombre","Descripcion"]

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

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = create_treeview(frame, COLUMNS)

        self.edit_btn = tk.Button(self.root, text="Editar Seleccionado", command=self.edit_selected)
        self.edit_btn.pack(pady=5)

    def populate_treeview(self):
        # Guardar scroll y selección actuales
        top, bottom = self.tree.yview()
        selected_items = self.tree.selection()

        # Limpiar
        self.tree.delete(*self.tree.get_children())

        # Insertar datos
        for row in self.last_tests:
            unique_id = row.get("unique_id")
            meta_row = self.meta.get(unique_id, {})
            values = [
                #unique_id,
                row.get("test_id",""),
                row.get("date",""),
                row.get("time",""),
                row.get("max_load",""),
                row.get("max_resistance",""),
                meta_row.get("Name",""),
                meta_row.get("Description","")
            ]
            self.tree.insert("", tk.END, iid=unique_id, values=values)

        # Restaurar selección
        for iid in selected_items:
            if iid in self.tree.get_children():
                self.tree.selection_add(iid)

        # Smart scroll: mantener al final si antes estaba al final
        if bottom == 1.0:
            self.tree.yview_moveto(1.0)
        else:
            self.tree.yview_moveto(top)

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            tk.messagebox.showwarning("Sin Selección", "Seleccione un test para editar")
            return
        unique_id = selected[0]
        open_edit_popup(self.root, unique_id, self.meta, self.populate_treeview)

    def auto_refresh(self):
        self.raw_data = load_raw()
        self.last_tests = self.raw_data[-DISPLAY_LAST:]
        self.populate_treeview()
        self.root.after(5000, self.auto_refresh)
