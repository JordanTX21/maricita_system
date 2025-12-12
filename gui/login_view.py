import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app

        tk.Label(self, text="Usuario").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Contraseña").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Ingresar", command=self.login).pack(pady=10)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if self.app.auth.login(user, pwd):
            self.app.show_menu()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")
