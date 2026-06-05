import tkinter as tk
from tkinter import messagebox
from services.cliente_service import (
    obtener_clientes, obtener_cliente_por_id, 
    guardar_nuevo_cliente, actualizar_cliente_db, eliminar_cliente_db
)

"""
VISTA: Gestiona la interacción con el usuario para el ABM de Clientes.
Sigue el principio de separación de responsabilidades: la UI no conoce la DB,
solo llama a los servicios.
"""

def abrir_gestion_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("550x700")
    
    # --- FORMULARIO ---
    tk.Label(ventana, text="DATOS DEL CLIENTE", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(ventana, text="Nombre:").pack()
    ent_nombre = tk.Entry(ventana, width=40); ent_nombre.pack()

    tk.Label(ventana, text="Teléfono:").pack()
    ent_tel = tk.Entry(ventana, width=40); ent_tel.pack()

    tk.Label(ventana, text="Dirección:").pack()
    ent_dir = tk.Entry(ventana, width=40); ent_dir.pack()

    # --- BOTONES DE ACCIÓN ---
    frame_btns = tk.Frame(ventana)
    frame_btns.pack(pady=10)
    
    def guardar():
        guardar_nuevo_cliente(ent_nombre.get(), ent_tel.get(), ent_dir.get())
        messagebox.showinfo("Éxito", "Cliente guardado")
        ventana.destroy(); abrir_gestion_clientes()

    def actualizar():
        actualizar_cliente_db(ent_id_accion.get(), ent_nombre.get(), ent_tel.get(), ent_dir.get())
        messagebox.showinfo("Éxito", "Cliente actualizado")
        ventana.destroy(); abrir_gestion_clientes()

    tk.Button(frame_btns, text="Guardar Nuevo", bg="green", fg="white", command=guardar).pack(side="left", padx=5)
    tk.Button(frame_btns, text="Actualizar", bg="orange", command=actualizar).pack(side="left", padx=5)

    tk.Label(ventana, text="--------------------------------------------------").pack()

    # --- ACCIONES POR ID ---
    tk.Label(ventana, text="BÚSQUEDA Y ELIMINACIÓN", font=("Arial", 10, "bold")).pack()
    frame_accion = tk.Frame(ventana)
    frame_accion.pack(pady=5)
    
    ent_id_accion = tk.Entry(frame_accion, width=10); ent_id_accion.pack(side="left", padx=5)

    def cargar():
        res = obtener_cliente_por_id(ent_id_accion.get())
        if res:
            for e, val in zip([ent_nombre, ent_tel, ent_dir], res):
                e.delete(0, tk.END); e.insert(0, val)
        else: messagebox.showwarning("Error", "No encontrado")

    def eliminar():
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            eliminar_cliente_db(ent_id_accion.get())
            ventana.destroy(); abrir_gestion_clientes()

    tk.Button(frame_accion, text="Cargar", command=cargar).pack(side="left", padx=5)
    tk.Button(frame_accion, text="Eliminar", bg="red", fg="white", command=eliminar).pack(side="left", padx=5)

    # --- LISTADO ---
    tk.Label(ventana, text="LISTADO ACTUAL", font=("Arial", 12, "bold")).pack(pady=10)
    canvas = tk.Canvas(ventana); scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    clientes = obtener_clientes()
    for c in clientes:
        tk.Label(scrollable_frame, text=f"ID: {c[0]} | {c[1]} | Tel: {c[2]}", font=("Courier", 9)).pack(anchor="w")

    canvas.pack(side="left", fill="both", expand=True, padx=20); scrollbar.pack(side="right", fill="y")
