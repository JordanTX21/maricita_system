import tkinter as tk

class Sidebar(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2c3e50", width=200)
        self.app = app
        self.pack_propagate(False)

        title = tk.Label(
            self,
            text="MARICITA",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)

        self._btn("Menú Principal", app.show_menu)
        self._btn("Clientes", lambda: app.show_frame_by_name("ClientesView"))
        self._btn("Productos", lambda: app.show_frame_by_name("ProductosView"))
        self._btn("Pagos", lambda: app.show_frame_by_name("PagosView"))
        self._btn("Pedidos", lambda: app.show_frame_by_name("PedidoView"))

        tk.Button(
            self,
            text="Salir",
            command=app.root.quit,
            bg="#c0392b",
            fg="white",
            relief="flat"
        ).pack(side="bottom", pady=20, fill="x")

    def _btn(self, text, command):
        tk.Button(
            self,
            text=text,
            command=command,
            bg="#34495e",
            fg="white",
            relief="flat",
            height=2
        ).pack(fill="x", padx=10, pady=5)
