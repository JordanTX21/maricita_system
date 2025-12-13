import tkinter as tk
from tkinter import ttk, messagebox

class ProductosView(tk.Frame):
    def __init__(self, app):
        super().__init__(app.content)
        self.app = app
        self.system = app.system

        tk.Label(self, text="Productos", font=("Arial", 18, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("precio", "stock"),
            show="headings"
        )
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_productos()

    def cargar_productos(self):
        self.tree.delete(*self.tree.get_children())

        if not self.system.productos:
            messagebox.showinfo("Productos", "No hay productos cargados")
            return

        for p in self.system.productos.values():
            self.tree.insert(
                "",
                "end",
                text=p.nombre,
                values=(f"S/. {p.precio}", p.stock)
            )
