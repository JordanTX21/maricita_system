import tkinter as tk
from gui.login_view import LoginView
from gui.menu_view import MenuView
from app.services.restaurante_service import RestauranteSystem
from app.services.auth_service import AuthService

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Maricita - Sistema de Pedidos")
        self.width = 800
        self.height = 600
        self.center_window()

        self.system = RestauranteSystem()
        self.auth = AuthService(self.system.db)

        self.frame = None
        self.show_login()

    # ---------- ventana ----------
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def show_frame(self, frame_class):
        if self.frame:
            self.frame.destroy()
        self.frame = frame_class(self)
        self.frame.pack(fill="both", expand=True)

    def show_login(self):
        self.show_frame(LoginView)

    def show_menu(self):
        self.show_frame(MenuView)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
