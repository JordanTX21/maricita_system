import tkinter as tk
from tkinter import messagebox

# --- Configuración de Colores y Fuentes (Simulación) ---
COLOR_ROJO_MARICITA = "#D62828" # Color rojo oscuro similar al botón
COLOR_GRIS_CLARO = "#f0f0f0"
FONT_PRINCIPAL = ("Arial", 12)
FONT_BOTON = ("Arial", 10, "bold")
FONT_ENLACE = ("Arial", 10, "underline")

class LoginView(tk.Frame):
    def __init__(self, app):
        # Usamos app.root (la ventana principal) como contenedor, no solo self
        super().__init__(app.root, bg="white")
        self.app = app
        
        # Centramos el contenido dentro del Frame principal usando 'grid'
        self.pack(fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        container = tk.Frame(self, bg='white')
        container.grid(row=1, column=0)
        
        # --- 1. Título Superior ---
        tk.Label(container, text="Maricita Restaurant", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=0, pady=(30, 10))

        tk.Label(container, text="Comida en un solo click", font=FONT_PRINCIPAL, bg="white").grid(row=2, column=0)

        frame_user = tk.Frame(container, bg="white")
        frame_user.grid(row=3, column=0, pady=10, padx=50, sticky="ew")
        frame_user.columnconfigure(1, weight=1) # El Entry tomará el espacio restante
        
        self.username = tk.Entry(frame_user, font=FONT_PRINCIPAL, relief="solid", bd=1)
        # Simular el texto "Usuario" dentro del campo si está vacío (placeholder)
        self.username.insert(0, "Usuario")
        self.username.bind('<FocusIn>', self.on_focus_in_user)
        self.username.bind('<FocusOut>', self.on_focus_out_user)
        self.username.grid(row=0, column=0, ipady=5, ipadx=5, sticky="ew") # ipady/ipadx para hacerlo más grande

        
        # Frame para Contraseña (Fila 4)
        frame_pwd = tk.Frame(container, bg="white")
        frame_pwd.grid(row=4, column=0, pady=10, padx=50, sticky="ew")
        frame_pwd.columnconfigure(1, weight=1)

        self.password = tk.Entry(frame_pwd, show="*", font=FONT_PRINCIPAL, relief="solid", bd=1)
        # Simular el texto "Contraseña" dentro del campo
        self.password.insert(0, "Contraseña")
        self.password.bind('<FocusIn>', self.on_focus_in_pwd)
        self.password.bind('<FocusOut>', self.on_focus_out_pwd)
        self.password.grid(row=0, column=0, ipady=5, ipadx=5, sticky="ew")
        
        # --- 5. Botón de Ingreso ---
        # El botón de la imagen es grande, rojo y tiene una flecha
        
        # Frame contenedor para el botón para mejor control de padding
        frame_button = tk.Frame(container, bg="white")
        frame_button.grid(row=5, column=0, pady=25, padx=50, sticky="ew")

        # El botón debe expandirse dentro de su frame
        btn_ingresar = tk.Button(
            frame_button, 
            text="➜ Ingresar", # Simular la flecha hacia la derecha
            command=self.login,
            bg=COLOR_ROJO_MARICITA,
            fg="white", # Texto blanco
            font=FONT_BOTON,
            relief="flat", # Para que se vea plano como en la imagen
            activebackground=COLOR_ROJO_MARICITA, # Mantener el color al hacer clic
            activeforeground="white",
            cursor="hand2" # Cambiar el cursor a una mano
        )
        # Usar place para simular que el botón tiene un ancho fijo o usar sticky="ew" en grid
        btn_ingresar.pack(fill="x", ipady=2) # Rellenar el ancho y darle padding interno

        # Enlace Registrarse como cliente
        btn_registro = tk.Button(
            container, 
            text="Registrarse como cliente", 
            command=self.register_client, 
            fg="blue", 
            bg="white", 
            font=FONT_ENLACE, 
            relief="flat",
            activebackground="white",
            cursor="hand2"
        )
        btn_registro.grid(row=7, column=0, pady=(5, 30))
        
    # --- Métodos de Interacción (Funciones Placeholder) ---
    
    # Placeholder: Simular el texto de ayuda ("placeholder") al entrar/salir del Entry
    def on_focus_in_user(self, event):
        if self.username.get() == "Usuario":
            self.username.delete(0, tk.END)
            
    def on_focus_out_user(self, event):
        if not self.username.get():
            self.username.insert(0, "Usuario")

    def on_focus_in_pwd(self, event):
        if self.password.get() == "Contraseña":
            self.password.delete(0, tk.END)
            self.password.config(show="*") # Mostrar asteriscos
            
    def on_focus_out_pwd(self, event):
        if not self.password.get():
            self.password.insert(0, "Contraseña")
            self.password.config(show="") # Ocultar asteriscos para mostrar el placeholder
            
    # Función de Login
    def login(self):
        # Limpiar el texto de ayuda antes de obtener el valor
        user = self.username.get()
        pwd = self.password.get()
        
        if user == "Usuario": user = ""
        if pwd == "Contraseña": pwd = "" # Omitir el placeholder
        
        if not user or not pwd:
            messagebox.showerror("Error", "Por favor, ingresa tu usuario y contraseña.")
            return

        # Lógica de autenticación real (asumiendo que 'self.app.auth.login' existe)
        if self.app.auth.login(user, pwd):
            # En una aplicación real:
            self.app.show_menu()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    # Función para "Registrarse como cliente"
    def register_client(self):
        messagebox.showinfo("Registro", "Redirigiendo a la pantalla de registro de cliente...")
        # Lógica para mostrar la vista de registro