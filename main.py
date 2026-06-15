import tkinter as tk
import sys
import os
from services.database import conectar
from views.clientes_gui import abrir_gestion_clientes
from views.presupuestos_gui import abrir_nuevo_presupuesto
from views.configuracion_gui import abrir_configuracion

# Configuración de Tcl/Tk (necesaria para tu entorno)
if sys.platform == "win32":
    tcl_path = r"C:\Users\santi\AppData\Local\Programs\Python\Python313\include\tcl\tcl8.6"
    tk_path = r"C:\Users\santi\AppData\Local\Programs\Python\Python313\include\tcl\tk8.6"
    if os.path.exists(tcl_path):
        os.environ["TCL_LIBRARY"] = tcl_path
    if os.path.exists(tk_path):
        os.environ["TK_LIBRARY"] = tk_path

def crear_ventana_principal():
    root = tk.Tk()
    root.title("Santy Aberturas")
    root.geometry("450x600")
    root.configure(bg="#1e1e1e")  # Fondo oscuro moderno (Dark Mode)
    root.resizable(False, False)

    # Colores
    COLOR_FONDO = "#1e1e1e"
    COLOR_ORO = "#D4AF37"
    COLOR_BOTON = "#2d2d2d"
    COLOR_TEXTO = "#ffffff"
    COLOR_HOVER = "#3d3d3d"

    # --- Header ---
    header_frame = tk.Frame(root, bg=COLOR_FONDO)
    header_frame.pack(pady=40)

    tk.Label(header_frame, text="SANTY", font=("Segoe UI", 28, "bold"), 
             fg=COLOR_ORO, bg=COLOR_FONDO).pack()
    tk.Label(header_frame, text="ABERTURAS", font=("Segoe UI", 18), 
             fg=COLOR_TEXTO, bg=COLOR_FONDO).pack()
    
    # Línea decorativa
    tk.Frame(root, bg=COLOR_ORO, height=2, width=100).pack(pady=10)

    # --- Botones Estilizados ---
    def on_enter(e):
        e.widget.config(bg=COLOR_HOVER, fg=COLOR_ORO)

    def on_leave(e):
        e.widget.config(bg=COLOR_BOTON, fg=COLOR_TEXTO)

    def crear_boton(texto, comando):
        btn = tk.Button(root, text=texto, command=comando,
                        font=("Segoe UI", 11, "bold"),
                        fg=COLOR_TEXTO, bg=COLOR_BOTON,
                        activeforeground=COLOR_ORO, activebackground=COLOR_HOVER,
                        relief="flat", width=30, height=2, cursor="hand2")
        btn.pack(pady=10)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    crear_boton("📂 GESTIONAR CLIENTES", abrir_gestion_clientes)
    crear_boton("📊 NUEVO PRESUPUESTO", abrir_nuevo_presupuesto)
    crear_boton("⚙️ CONFIGURACIÓN", abrir_configuracion)

    # Botón Salir (más pequeño y abajo)
    btn_salir = tk.Button(root, text="SALIR", command=root.quit,
                          font=("Segoe UI", 9, "bold"),
                          fg="#ff5555", bg=COLOR_FONDO,
                          activeforeground="#ff0000", activebackground=COLOR_FONDO,
                          relief="flat", cursor="hand2")
    btn_salir.pack(side="bottom", pady=40)

    # --- Estado de la Base de Datos ---
    try:
        con = conectar()
        con.close()
        estado_text = "● SISTEMA ONLINE"
        estado_color = "#44ff44"
    except:
        estado_text = "○ ERROR DE CONEXIÓN"
        estado_color = "#ff4444"

    tk.Label(root, text=estado_text, font=("Segoe UI", 8),
             fg=estado_color, bg=COLOR_FONDO).place(x=20, y=570)

    root.mainloop()

if __name__ == "__main__":
    crear_ventana_principal()
