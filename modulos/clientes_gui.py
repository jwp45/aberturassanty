import tkinter as tk
from tkinter import messagebox
# Importamos la LÓGICA desde el servicio
from services.cliente_service import (
    obtener_clientes, obtener_cliente_por_id, 
    guardar_nuevo_cliente, actualizar_cliente_db, eliminar_cliente_db
)

# --- FUNCIONES DE SOPORTE PARA LA GUI ---

def accion_guardar(ent_nom, ent_tel, ent_dir, ventana):
    try:
        guardar_nuevo_cliente(ent_nom.get(), ent_tel.get(), ent_dir.get())
        messagebox.showinfo("Éxito", "Cliente guardado")
        ventana.destroy()
        abrir_gestion_clientes()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def accion_eliminar(ent_id, ventana):
    id_c = ent_id.get()
    if not id_c: return
    if messagebox.askyesno("Confirmar", f"¿Eliminar ID {id_c}?"):
        try:
            eliminar_cliente_db(id_c)
            ventana.destroy()
            abrir_gestion_clientes()
        except Exception as e:
            messagebox.showerror("Error", str(e))

def accion_cargar_edicion(ent_id, ent_nom, ent_tel, ent_dir):
    try:
        res = obtener_cliente_por_id(ent_id.get())
        if res:
            ent_nom.delete(0, tk.END)
            ent_nom.insert(0, res[0])
            ent_tel.delete(0, tk.END)
            ent_tel.insert(0, res[1])
            ent_dir.delete(0, tk.END)
            ent_dir.insert(0, res[2])
        else:
            messagebox.showwarning("Error", "No se encontró el ID")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def accion_actualizar(ent_id, ent_nom, ent_tel, ent_dir, ventana):
    try:
        actualizar_cliente_db(ent_id.get(), ent_nom.get(), ent_tel.get(), ent_dir.get())
        messagebox.showinfo("Éxito", "Cliente actualizado")
        ventana.destroy()
        abrir_gestion_clientes()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- INTERFAZ GRÁFICA ---

def abrir_gestion_clientes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("550x700")
    
    # 1. FORMULARIO
    tk.Label(ventana, text="DATOS DEL CLIENTE", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(ventana, text="Nombre:").pack()
    ent_nombre = tk.Entry(ventana, width=40)
    ent_nombre.pack()

    tk.Label(ventana, text="Teléfono:").pack()
    ent_tel = tk.Entry(ventana, width=40)
    ent_tel.pack()

    tk.Label(ventana, text="Dirección:").pack()
    ent_dir = tk.Entry(ventana, width=40)
    ent_dir.pack()

    frame_btns = tk.Frame(ventana)
    frame_btns.pack(pady=10)
    
    tk.Button(frame_btns, text="Guardar Nuevo", bg="green", fg="white",
              command=lambda: accion_guardar(ent_nombre, ent_tel, ent_dir, ventana)).pack(side="left", padx=5)
    
    tk.Button(frame_btns, text="Actualizar Existente", bg="orange",
              command=lambda: accion_actualizar(ent_id_accion, ent_nombre, ent_tel, ent_dir, ventana)).pack(side="left", padx=5)

    tk.Label(ventana, text="--------------------------------------------------").pack()

    # 2. ACCIONES POR ID
    tk.Label(ventana, text="ACCIONES POR ID", font=("Arial", 10, "bold")).pack()
    frame_accion = tk.Frame(ventana)
    frame_accion.pack(pady=5)
    
    tk.Label(frame_accion, text="ID Cliente:").pack(side="left")
    ent_id_accion = tk.Entry(frame_accion, width=10)
    ent_id_accion.pack(side="left", padx=5)

    tk.Button(frame_accion, text="Cargar", command=lambda: accion_cargar_edicion(ent_id_accion, ent_nombre, ent_tel, ent_dir)).pack(side="left", padx=5)
    tk.Button(frame_accion, text="Eliminar", bg="red", fg="white", command=lambda: accion_eliminar(ent_id_accion, ventana)).pack(side="left", padx=5)

    tk.Label(ventana, text="--------------------------------------------------").pack()

    # 3. LISTADO
    tk.Label(ventana, text="LISTADO DE CLIENTES", font=("Arial", 12, "bold")).pack(pady=10)
    lista_frame = tk.Frame(ventana)
    lista_frame.pack(fill="both", expand=True, padx=20)

    try:
        clientes = obtener_clientes()
        for c in clientes:
            tk.Label(lista_frame, text=f"ID: {c[0]} | {c[1]} | Tel: {c[2]}").pack(anchor="w")
    except Exception as e:
        tk.Label(lista_frame, text=f"Error: {e}", fg="red").pack()

    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
