import tkinter as tk
from tkinter import ttk

class PagosView(tk.Frame):
    def __init__(self, app):
        super().__init__(app.content)
        self.app = app
        self.system = app.system

        tk.Label(self, text="Pagos", font=("Arial", 18, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("pedido", "metodo", "monto", "estado"),
            show="headings"
        )

        for col in ("pedido", "metodo", "monto", "estado"):
            self.tree.heading(col, text=col.capitalize())

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_pagos()

    def cargar_pagos(self):
        self.tree.delete(*self.tree.get_children())

        for p in self.system.pagos.values():
            self.tree.insert(
                "",
                "end",
                values=(
                    p.id,
                    p.metodo,
                    f"S/. {p.monto}",
                    p.confirmado
                )
            )
