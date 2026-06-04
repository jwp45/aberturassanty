import tkinter as tk
from services.database import conectar
# Importamos las funciones desde nuestra nueva carpeta de módulos
from modulos.clientes_gui import abrir_gestion_clientes
from modulos.presupuestos_gui import abrir_nuevo_presupuesto

def crear_ventana_principal():
    root = tk.Tk()
    root.title("Santy Aberturas - Sistema Online")
    root.geometry("400x400")

    # Título Principal
    titulo = tk.Label(root, text="SANTY ABERTURAS", font=("Arial", 18, "bold"), fg="blue")
    titulo.pack(pady=30)

    # Botones del Menú que ahora llaman a las funciones importadas
    btn_clientes = tk.Button(root, text="Gestionar Clientes", width=25, height=2, command=abrir_gestion_clientes)
    btn_clientes.pack(pady=10)

    btn_presupuesto = tk.Button(root, text="Realizar Presupuesto", width=25, height=2, command=abrir_nuevo_presupuesto)
    btn_presupuesto.pack(pady=10)

    btn_salir = tk.Button(root, text="Salir", width=25, height=2, bg="red", fg="white", command=root.quit)
    btn_salir.pack(pady=10)

    # Pie de página para verificar conexión
    try:
        con = conectar()
        con.close()
        estado_db = tk.Label(root, text="● Base de Datos Conectada", fg="green", font=("Arial", 8))
    except:
        estado_db = tk.Label(root, text="○ Error de Conexión", fg="red", font=("Arial", 8))
    
    estado_db.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    crear_ventana_principal()
