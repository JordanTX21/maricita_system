import tkinter as tk
from gui.pedido_view import PedidoView

class MenuView(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        tk.Label(self, text="Menú Principal", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Crear Pedido", width=20,
                  command=lambda: self.app.show_frame(PedidoView)).pack(pady=5)

        tk.Button(self, text="Salir", width=20, command=app.root.quit).pack()
