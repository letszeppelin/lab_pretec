# gui/styles.py
import ttkbootstrap as tb

def setup_styles(root):
    """
    Call this after creating the main window.
    Sets global styles for Treeview, Buttons, Labels, etc.
    """
    style = tb.Style(root)

    # Treeview style
    style.configure("Treeview",
                    rowheight=28,
                    font=("Arial", 11),
                    fieldbackground="#f5f5f5",
                    background="#f5f5f5",
                    foreground="black")
    style.map("Treeview",
              background=[("selected", "#0078d7")],
              foreground=[("selected", "white")])

    # Buttons (optional global look)
    style.configure("TButton", font=("Arial", 11))
    
    # Labels (optional global look)
    style.configure("TLabel", font=("Arial", 11))
    
    return style