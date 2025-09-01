import ttkbootstrap as tb
from ttkbootstrap.constants import *

def create_treeview(parent, columns):
    # ttkbootstrap Treeview
    tree = tb.Treeview(parent, columns=columns, show='headings', bootstyle="secondary")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    # Scrollbar
    scrollbar = tb.Scrollbar(parent, orient=VERTICAL, command=tree.yview, bootstyle="info")
    tree.configure(yscrollcommand=scrollbar.set)

    # Layout
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=LEFT, fill=Y)

    return tree