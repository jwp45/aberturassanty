import tkinter as tk
from tkinter import messagebox
from services.auth_service import validar_usuario

class LoginGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Santy Aberturas - Acceso")
        self.root.geometry("350x450")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        self.autenticado = False

        # Colores y Estilos (Consistentes con main.py)
        COLOR_FONDO = "#1e1e1e"
        COLOR_ORO = "#D4AF37"
        COLOR_BOTON = "#2d2d2d"
        COLOR_TEXTO = "#ffffff"

        # --- Interfaz ---
        tk.Label(self.root, text="SANTY", font=("Segoe UI", 24, "bold"), 
                 fg=COLOR_ORO, bg=COLOR_FONDO).pack(pady=(40, 0))
        tk.Label(self.root, text="SISTEMA DE GESTIÓN", font=("Segoe UI", 10), 
                 fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=(0, 20))

        # Contenedor de campos
        frame_campos = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_campos.pack(pady=20, padx=40, fill="x")

        tk.Label(frame_campos, text="Email", fg=COLOR_ORO, bg=COLOR_FONDO, 
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_email = tk.Entry(frame_campos, font=("Segoe UI", 11), bg="#2d2d2d", 
                                  fg="white", insertbackground="white", relief="flat")
        self.ent_email.pack(pady=(5, 15), fill="x")
        self.ent_email.insert(0, "admin@santy.com") # Ejemplo por defecto

        tk.Label(frame_campos, text="Contraseña", fg=COLOR_ORO, bg=COLOR_FONDO, 
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_pass = tk.Entry(frame_campos, font=("Segoe UI", 11), bg="#2d2d2d", 
                                 fg="white", insertbackground="white", relief="flat", show="*")
        self.ent_pass.pack(pady=(5, 5), fill="x")

        # Botón de ingreso
        self.btn_ingresar = tk.Button(self.root, text="INGRESAR", command=self.intentar_login,
                                     font=("Segoe UI", 11, "bold"), fg=COLOR_TEXTO, 
                                     bg=COLOR_BOTON, activebackground=COLOR_ORO, 
                                     relief="flat", cursor="hand2", height=2)
        self.btn_ingresar.pack(pady=30, padx=40, fill="x")

        # Vincular tecla Enter para loguear
        self.root.bind('<Return>', lambda event: self.intentar_login())

    def intentar_login(self):
        email = self.ent_email.get()
        password = self.ent_pass.get()

        if not email or not password:
            messagebox.showwarning("Atención", "Por favor complete todos los campos.")
            return

        if validar_usuario(email, password):
            self.autenticado = True
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Email o contraseña incorrectos.")

    def iniciar(self):
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()
        return self.autenticado
