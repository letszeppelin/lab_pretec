import ttkbootstrap as tb
from ttkbootstrap.constants import *
from file_manager import save_meta
from datetime import datetime
from ttkbootstrap.dialogs import Messagebox
from utils.file_utils import save_last_meta, load_last_meta

def open_edit_popup(parent, unique_id, test_id, meta, refresh_callback):
    popup = tb.Toplevel(parent)
    popup.title(f"Editar Test {unique_id}")
    popup.grab_set()
    
    PAD_X = 5
    PAD_Y = 5

    # --- Cargar último meta guardado ---
    last_meta = load_last_meta()

    # --- Sección de copiar valores previos ---
    quick_frame = tb.LabelFrame(popup, text="Copiar datos previos")
    quick_frame.grid(row=0, column=0, columnspan=3, padx=PAD_X, pady=(PAD_Y, 15), sticky=EW)

    def copiar_fecha():
        if "Moldeo" in last_meta:
            moldeo_entry.delete(0, END)
            moldeo_entry.insert(0, last_meta["Moldeo"])

    def copiar_todo():
        if not last_meta:
            Messagebox.show_info("No hay datos previos guardados", "Aviso", parent=popup)
            return
        if "Name" in last_meta:
            name_entry.delete(0, END)
            name_entry.insert(0, last_meta["Name"])
        if "Description" in last_meta:
            desc_entry.delete(0, END)
            desc_entry.insert(0, last_meta["Description"])
        if "Moldeo" in last_meta:
            moldeo_entry.delete(0, END)
            moldeo_entry.insert(0, last_meta["Moldeo"])
        if "fck" in last_meta:
            fck_val = last_meta["fck"]
            if str(fck_val) in [str(x) for x in [21, 25, 30, 35, 40, 50]]:
                fck_var.set(fck_val)
                fck_custom_entry.grid_remove()
            else:
                fck_var.set("Otro")
                fck_custom_entry.grid()
                fck_custom_entry.delete(0, END)
                fck_custom_entry.insert(0, str(fck_val))

    def vaciar_todo():
        name_entry.delete(0, END)
        desc_entry.delete(0, END)
        moldeo_entry.delete(0, END)
        fck_var.set(21)  # Valor por defecto
        fck_custom_entry.delete(0, END)
        fck_custom_entry.grid_remove()

    tb.Button(quick_frame, text="Copiar fecha", bootstyle="secondary", command=copiar_fecha)\
        .grid(row=0, column=0, padx=PAD_X, pady=(PAD_Y, 15))
    tb.Button(quick_frame, text="Copiar todo", bootstyle="info", command=copiar_todo)\
        .grid(row=0, column=1, padx=PAD_X, pady=(PAD_Y, 15))
    tb.Button(quick_frame, text="Vaciar todo", bootstyle="danger", command=vaciar_todo)\
        .grid(row=0, column=2, padx=PAD_X, pady=(PAD_Y, 15))

    # Centrar los 3 botones en el frame
    quick_frame.grid_columnconfigure((0,1,2), weight=1)

    # --- Nombre ---
    tb.Label(popup, text="Nombre:").grid(row=1, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    name_entry = tb.Entry(popup, width=50)
    name_entry.grid(row=1, column=1, columnspan=2, sticky=W, padx=PAD_X, pady=PAD_Y)
    name_entry.insert(0, meta.get(unique_id, {}).get("Name",""))

    # --- Descripción ---
    tb.Label(popup, text="Descripción:").grid(row=2, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    desc_entry = tb.Entry(popup, width=50)
    desc_entry.grid(row=2, column=1, columnspan=2, sticky=W, padx=PAD_X, pady=PAD_Y)
    desc_entry.insert(0, meta.get(unique_id, {}).get("Description",""))

    # --- Fecha de moldeo ---
    tb.Label(popup, text="Fecha de moldeo (dd/mm/yyyy):").grid(row=3, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    moldeo_entry = tb.Entry(popup, width=20)
    moldeo_entry.grid(row=3, column=1, columnspan=2, sticky=W, padx=PAD_X, pady=PAD_Y)
    moldeo_entry.insert(0, meta.get(unique_id, {}).get("Moldeo", ""))

    # --- fck ---
    tb.Label(popup, text="fck (MPa):").grid(row=4, column=0, sticky=E, padx=PAD_X, pady=PAD_Y)
    fck_options = [21, 25, 30, 35, 40, 50, "Otro"]
    fck_var = tb.StringVar()

    # Tomar el valor guardado, si no hay usa el primero de la lista
    saved_fck = str(meta.get(unique_id, {}).get("fck", fck_options[0]))

    # Convertimos opciones a string para poder comparar fácilmente
    options_str = [str(x) for x in fck_options if x != "Otro"]

    if saved_fck in options_str:
        # Valor está dentro de las opciones predefinidas
        fck_var.set(saved_fck)
        show_custom = False
    else:
        # Valor no está en las opciones → se trata como "Otro"
        fck_var.set("Otro")
        show_custom = True

    fck_menu = tb.OptionMenu(popup, fck_var, *fck_options, bootstyle="info")
    fck_menu.grid(row=4, column=1, sticky=W, padx=PAD_X, pady=PAD_Y)

    fck_custom_entry = tb.Entry(popup, width=10)
    fck_custom_entry.grid(row=4, column=2, sticky=W, padx=PAD_X, pady=PAD_Y)

    if show_custom:
        fck_custom_entry.delete(0, END)
        fck_custom_entry.insert(0, saved_fck)
    else:
        fck_custom_entry.grid_remove()


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
            raw_val = fck_custom_entry.get().strip()
            try:
                # Primero intenta convertir a int
                fck_val = int(raw_val)
            except ValueError:
                try:
                    # Si falla, intenta como float
                    fck_val = float(raw_val)
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

        # Recopilar los valores actuales
        last_meta = {
            "Name": name_entry.get(),
            "Description": desc_entry.get(),
            "Moldeo": moldeo_entry.get(),
            "fck": fck_var.get() if fck_var.get() != "Otro" else fck_custom_entry.get()
            }

        # Guardar en el cache JSON
        save_last_meta(last_meta)

        refresh_callback()
        popup.destroy()

    # --- Botones centrados ---
    btn_frame = tb.Frame(popup)
    btn_frame.grid(row=5, column=0, columnspan=3, pady=15)
    tb.Button(btn_frame, text="Guardar", command=save_and_close, bootstyle="success").pack(side=LEFT, padx=10)
    tb.Button(btn_frame, text="Cancelar", command=popup.destroy, bootstyle="danger").pack(side=LEFT, padx=10)