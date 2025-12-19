import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main_gui import App

class PedidoView(tk.Frame):
    def __init__(self, app: "App"):
        super().__init__(app.root)
        self.app: "App" = app
        self.system = app.system

        self.pack(fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self)
        container.grid(row=1, column=0)

        tk.Label(container, text="Crear Pedido", font=("Arial", 14)).pack(pady=10)

        # Selector cliente
        tk.Label(container, text="Cliente").pack()
        clientes = [(p.id, p.nombre, p.telefono) for p in self.system.listar_clientes()]
        self.combo_cliente = ttk.Combobox(container, values=[f"{c[2]} - {c[1]}" for c in clientes])
        self.combo_cliente.pack(pady=5)

        # Selector producto
        tk.Label(container, text="Productos").pack()
        productos = [(p.id, p.nombre, p.precio) for p in self.system.listar_productos()]
        self.combo = ttk.Combobox(container, values=[f"{p[1]} - S/.{p[2]}" for p in productos])
        self.combo.pack(pady=5)

        tk.Label(container, text="Cantidad").pack()
        self.cantidad = tk.Entry(container)
        self.cantidad.pack()

        tk.Button(container, text="Agregar al carrito", command=self.agregar).pack(pady=10)

        self.carrito = []
        self.lista = tk.Listbox(container)
        self.lista.pack(pady=5)

        tk.Button(container, text="Crear Pedido", command=self.crear_pedido).pack(pady=10)

        tk.Button(container, text="Regresar", command=self.app.show_menu).pack(pady=5)

    def agregar(self):
        sel = self.combo.get()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return

        cantidad = int(self.cantidad.get())
        nombre = sel.split(" - ")[0]

        producto = next((p for p in self.app.system.listar_productos() if p.nombre == nombre), None)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        self.carrito.append({"producto_id": producto.id, "cantidad": cantidad})
        self.lista.insert("end", f"{nombre} x {cantidad}")

    def crear_pedido(self):
        cli_sel = self.combo_cliente.get()
        if not cli_sel:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return

        if not self.carrito:
            messagebox.showerror("Error", "Carrito vacío")
            return

        telefono = cli_sel.split(" - ")[0]
        cliente = self.system.buscar_cliente_por_telefono(telefono)
        if not cliente:
            messagebox.showerror("Error", "No hay clientes registrados aún")
            return

        pedido = self.system.crear_pedido(cliente, self.carrito, "salon")
        messagebox.showinfo("Éxito", f"Pedido creado: {pedido.id[:8]}")
        self.app.show_menu()
