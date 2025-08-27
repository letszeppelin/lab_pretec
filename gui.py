import tkinter as tk
from tkinter import messagebox
from file_manager import load_meta, load_raw, save_meta
from config import DISPLAY_LAST

class ResultsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resultados Máquina de Compresión")
        self.meta = load_meta()
        self.raw_data = load_raw()
        self.last_tests = self.raw_data[-DISPLAY_LAST:]
        self.create_widgets()
        self.populate_listbox()
        self.auto_refresh()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10,pady=10)

        self.lb = tk.Listbox(frame, width=100, height=20)
        self.lb.pack(side=tk.LEFT)
        scrollbar = tk.Scrollbar(frame, command=self.lb.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.lb.config(yscrollcommand=scrollbar.set)

        self.edit_btn = tk.Button(self.root, text="Editar Seleccionado", command=self.open_edit_popup)
        self.edit_btn.pack(pady=5)

    def populate_listbox(self):
        # save current scroll position
        top, bottom = self.lb.yview()

        selection = self.lb.curselection()
        selected_id = None
        if selection and self.last_tests:
            selected_id = self.last_tests[selection[0]]['test_id']

        self.lb.delete(0, tk.END)
        for row in self.last_tests:
            meta = self.meta.get(row['test_id'], {})
            display = (
                f"{row['test_id']} | {row['date']} {row['time']} | "
                f"Carga Máx: {row.get('max_load','')} | Res Máx: {row.get('max_resistance','')} | "
                f"Nombre: {meta.get('Name','')} | Desc: {meta.get('Description','')}"
            )
            self.lb.insert(tk.END, display)

        # restore selection if any
        if selected_id:
            for i, row in enumerate(self.last_tests):
                if row['test_id'] == selected_id:
                    self.lb.select_set(i)
                    self.lb.see(i)
                    break

        # smart auto-scroll:
        if bottom == 1.0:  
            # user was at the bottom before refresh → keep at bottom
            self.lb.yview_moveto(1.0)
        else:
            # user was not at bottom → restore their scroll position
            self.lb.yview_moveto(top)

    
    def open_edit_popup(self):
        selection = self.lb.curselection()
        if not selection:
            messagebox.showwarning("Sin Selección","Seleccione un test para editar")
            return
        index = selection[0]
        row = self.last_tests[index]
        test_id = row['test_id']

        popup = tk.Toplevel(self.root)
        popup.title(f"Editar Test {test_id}")
        popup.grab_set()

        tk.Label(popup, text="Nombre/ID:").grid(row=0,column=0)
        name_entry = tk.Entry(popup,width=50)
        name_entry.grid(row=0,column=1)
        name_entry.insert(0, self.meta.get(test_id, {}).get("Name",""))

        tk.Label(popup, text="Descripción:").grid(row=1,column=0)
        desc_entry = tk.Entry(popup,width=50)
        desc_entry.grid(row=1,column=1)
        desc_entry.insert(0, self.meta.get(test_id, {}).get("Description",""))

        def save_and_close():
            self.meta[test_id] = {"test_id": test_id,
                                   "Name": name_entry.get(),
                                   "Description": desc_entry.get()}
            save_meta(self.meta)
            self.populate_listbox()
            popup.destroy()

        tk.Button(popup,text="Guardar",command=save_and_close).grid(row=2,column=0)
        tk.Button(popup,text="Cancelar",command=popup.destroy).grid(row=2,column=1)

    def auto_refresh(self):
        self.raw_data = load_raw()
        self.last_tests = self.raw_data[-DISPLAY_LAST:]
        self.populate_listbox()
        self.root.after(5000, self.auto_refresh)
