import tkinter as tk
from tkinter import ttk, messagebox

class PedidoView(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.system = app.system

        tk.Label(self, text="Crear Pedido", font=("Arial", 14)).pack(pady=10)

        # Selector producto
        productos = [(p.id, p.nombre, p.precio) for p in self.system.productos.values()]
        self.combo = ttk.Combobox(self, values=[f"{p[1]} - S/.{p[2]}" for p in productos])
        self.combo.pack(pady=5)

        tk.Label(self, text="Cantidad").pack()
        self.cantidad = tk.Entry(self)
        self.cantidad.pack()

        tk.Button(self, text="Agregar al carrito", command=self.agregar).pack(pady=10)

        self.carrito = []
        self.lista = tk.Listbox(self)
        self.lista.pack(pady=5)

        tk.Button(self, text="Crear Pedido", command=self.crear_pedido).pack(pady=10)

    def agregar(self):
        sel = self.combo.get()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un producto")
            return

        cantidad = int(self.cantidad.get())
        nombre = sel.split(" - ")[0]

        producto = next((p for p in self.app.system.productos.values() if p.nombre == nombre), None)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        self.carrito.append({"producto_id": producto.id, "cantidad": cantidad})
        self.lista.insert("end", f"{nombre} x {cantidad}")

    def crear_pedido(self):
        if not self.carrito:
            messagebox.showerror("Error", "Carrito vacío")
            return

        cliente = next(iter(self.app.system.clientes.values()), None)
        if not cliente:
            messagebox.showerror("Error", "No hay clientes registrados aún")
            return

        pedido = self.app.system.crear_pedido(cliente, self.carrito, "salon")
        messagebox.showinfo("Éxito", f"Pedido creado: {pedido.id[:8]}")
        self.app.show_menu()
