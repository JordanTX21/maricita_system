import tkinter as tk
from gui.pedido_view import PedidoView
from gui.productos_view import ProductosView
from gui.clientes_view import ClientesView
from gui.pagos_view import PagosView

class MenuView(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        tk.Label(self, text="Menú Principal", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Crear Pedido", width=20,
                  command=lambda: self.app.show_frame(PedidoView)).pack(pady=5)

        tk.Button(self, text="Productos", width=20,
                  command=lambda: self.app.show_frame(ProductosView)).pack(pady=5)

        tk.Button(self, text="Clientes", width=20,
                  command=lambda: self.app.show_frame(ClientesView)).pack(pady=5)

        tk.Button(self, text="Pagos", width=20,
                  command=lambda: self.app.show_frame(PagosView)).pack(pady=5)

        tk.Button(self, text="Salir", width=20, command=app.root.quit).pack()
