import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_gui import App

class ClientesView(tk.Frame):
    def __init__(self, app: "App"):
        super().__init__(app.root)
        self.app: "App" = app
        self.system = app.system

        tk.Label(self, text="Clientes", font=("Arial", 18, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("telefono", "direccion"),
            show="headings"
        )
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("direccion", text="Dirección")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(
            self,
            text="Registrar Cliente",
            command=self.registrar_cliente
        ).pack(pady=10)

        tk.Button(self, text="Regresar", command=self.app.show_menu).pack(pady=5)

        self.cargar_clientes()

    def cargar_clientes(self):
        self.tree.delete(*self.tree.get_children())
        for c in self.system.listar_clientes():
            self.tree.insert(
                "",
                "end",
                text=c.nombre,
                values=(c.telefono, c.direccion)
            )

    def registrar_cliente(self):
        nombre = simpledialog.askstring("Cliente", "Nombre:")
        telefono = simpledialog.askstring("Cliente", "Teléfono:")
        direccion = simpledialog.askstring("Cliente", "Dirección:")

        if not nombre or not telefono:
            return

        self.system.crear_cliente(nombre, telefono, direccion)
        self.cargar_clientes()
        messagebox.showinfo("Éxito", "Cliente registrado")
