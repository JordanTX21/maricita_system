import tkinter as tk
from gui.pedido_view import PedidoView

class MenuView(tk.Frame):
    def __init__(self, app):
        super().__init__(app.content)
        self.app = app

        self.pack(fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self, bg='white')
        container.grid(row=1, column=0)

        tk.Label(container, text="Menú Principal", font=("Arial", 18, "bold")).pack(pady=10)

        self._btn(container, "Crear Pedido", lambda: self.app.show_frame(PedidoView))

        tk.Button(
            container,
            text="Salir",
            width=30,
            command=self.app.root.quit,
            bg="#c0392b",
            fg="white"
        ).pack(pady=15)

    # ---------- helpers ----------
    def _btn(self, parent, text, command):
        tk.Button(
            parent,
            text=text,
            width=30,
            command=command
        ).pack(pady=4)