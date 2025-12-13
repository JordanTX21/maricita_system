import tkinter as tk

from gui.login_view import LoginView
from gui.menu_view import MenuView
from gui.clientes_view import ClientesView
from gui.productos_view import ProductosView
from gui.pedido_view import PedidoView

from app.services.restaurante_service import RestauranteSystem
from app.services.auth_service import AuthService


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Maricita - Sistema de Pedidos")

        self.width = 300
        self.height = 600
        self.center_window()

        self.system = RestauranteSystem()
        self.auth = AuthService(self.system)

        self.frame = None
        self.sidebar = None
        self.content = None
        self.frames = {}

        self.show_login()

    # ---------- ventana ----------
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    # ---------- navegación ----------
    def init_main_layout(self):
        # self.sidebar = Sidebar(self.root, self)
        # self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root)
        self.content.pack(side="right", fill="both", expand=True)

        self.frames = {
            "MenuView": MenuView(self),
            "ClientesView": ClientesView(self),
            "ProductosView": ProductosView(self),
            "PedidoView": PedidoView(self),
        }

    def show_frame_by_name(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    # ---------- vistas ----------
    def show_login(self):
        if self.sidebar:
            self.sidebar.pack_forget()
            self.content.pack_forget()

        self.frame = LoginView(self)
        self.frame.pack(fill="both", expand=True)

    def show_menu(self):
        if self.frame:
            self.frame.destroy()
            self.frame = None

        if not self.sidebar:
            self.init_main_layout()

        self.show_frame_by_name("MenuView")

    # ---------- run ----------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
