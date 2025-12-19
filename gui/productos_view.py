import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_gui import App

class ProductosView(tk.Frame):
    def __init__(self, app: "App"):
        super().__init__(app.root)
        self.app: "App" = app
        self.system = app.system

        tk.Label(self, text="Productos", font=("Arial", 18, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("nombre","precio", "stock"),
            show="headings"
        )
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_productos()
        
        tk.Button(self, text="Regresar", command=self.app.show_menu).pack(pady=5)

    def cargar_productos(self):
        self.tree.delete(*self.tree.get_children())

        if not self.system.listar_productos():
            messagebox.showinfo("Productos", "No hay productos cargados")
            return

        for p in self.system.listar_productos():
            self.tree.insert(
                "",
                "end",
                text=p.nombre,
                values=(p.nombre, f"S/. {p.precio}", p.stock)
            )
