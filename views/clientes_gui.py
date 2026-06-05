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
    
    # Contenedor principal con margen interno
    main_frame = tk.Frame(ventana, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

    # ==========================================
    # 1. SECCIÓN: FORMULARIO (Datos del Cliente)
    # ==========================================
    frame_formulario = tk.LabelFrame(main_frame, text=" Datos del Cliente ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_formulario.pack(fill="x", pady=10)
    frame_formulario.columnconfigure(1, weight=1) # Permite que los campos de texto se estiren

    # Etiquetas y Campos utilizando GRID para alineación perfecta
    tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
    ent_nombre = tk.Entry(frame_formulario, font=("Arial", 10))
    ent_nombre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(frame_formulario, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=5)
    ent_tel = tk.Entry(frame_formulario, font=("Arial", 10))
    ent_tel.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(frame_formulario, text="Dirección:").grid(row=2, column=0, sticky="w", pady=5)
    ent_dir = tk.Entry(frame_formulario, font=("Arial", 10))
    ent_dir.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    # Botones de Acción dentro del formulario
    frame_btns = tk.Frame(frame_formulario)
    frame_btns.grid(row=3, column=0, columnspan=2, pady=10)
    
    def guardar():
        try:
            guardar_nuevo_cliente(ent_nombre.get(), ent_tel.get(), ent_dir.get())
            messagebox.showinfo("Éxito", "Cliente guardado correctamente", parent=ventana)
            ventana.destroy()
            abrir_gestion_clientes()
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e), parent=ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}", parent=ventana)

    def actualizar():
        if not ent_id_accion.get():
            messagebox.showwarning("Atención", "Debe ingresar el ID del cliente para actualizar", parent=ventana)
            return
        try:
            actualizar_cliente_db(ent_id_accion.get(), ent_nombre.get(), ent_tel.get(), ent_dir.get())
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente", parent=ventana)
            ventana.destroy()
            abrir_gestion_clientes()
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e), parent=ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}", parent=ventana)

    btn_guardar = tk.Button(frame_btns, text="Guardar Nuevo", bg="#28a745", fg="white", font=("Arial", 9, "bold"), padx=10, command=guardar)
    btn_guardar.pack(side="left", padx=10)
    
    btn_actualizar = tk.Button(frame_btns, text="Actualizar", bg="#fd7e14", fg="white", font=("Arial", 9, "bold"), padx=10, command=actualizar)
    btn_actualizar.pack(side="left", padx=10)

    # ==========================================
    # 2. SECCIÓN: BÚSQUEDA Y ELIMINACIÓN
    # ==========================================
    frame_busqueda = tk.LabelFrame(main_frame, text=" Búsqueda y Eliminación ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_busqueda.pack(fill="x", pady=10)

    tk.Label(frame_busqueda, text="Buscar ID:").pack(side="left", padx=5)
    ent_id_accion = tk.Entry(frame_busqueda, width=10, font=("Arial", 10))
    ent_id_accion.pack(side="left", padx=5)

    def cargar():
        if not ent_id_accion.get():
            messagebox.showwarning("Atención", "Debe ingresar el ID del cliente para buscar", parent=ventana)
            return
        res = obtener_cliente_por_id(ent_id_accion.get())
        if res:
            for e, val in zip([ent_nombre, ent_tel, ent_dir], res):
                e.delete(0, tk.END)
                e.insert(0, val)
        else:
            messagebox.showwarning("Error", "Cliente no encontrado", parent=ventana)

    def eliminar():
        if not ent_id_accion.get():
            messagebox.showwarning("Atención", "Debe ingresar el ID del cliente para eliminar", parent=ventana)
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este cliente?", parent=ventana):
            eliminar_cliente_db(ent_id_accion.get())
            messagebox.showinfo("Éxito", "Cliente eliminado", parent=ventana)
            ventana.destroy()
            abrir_gestion_clientes()

    btn_cargar = tk.Button(frame_busqueda, text="Cargar Datos", font=("Arial", 9), command=cargar)
    btn_cargar.pack(side="left", padx=5)

    btn_eliminar = tk.Button(frame_busqueda, text="Eliminar Cliente", bg="#dc3545", fg="white", font=("Arial", 9, "bold"), command=eliminar)
    btn_eliminar.pack(side="left", padx=5)

    # ==========================================
    # 3. SECCIÓN: LISTADO ACTUAL
    # ==========================================
    frame_listado = tk.LabelFrame(main_frame, text=" Listado de Clientes ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_listado.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(frame_listado, highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_listado, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    clientes = obtener_clientes()
    for c in clientes:
        # Formato limpio para cada cliente de la lista
        texto_cliente = f"ID: {c[0]:<4} | Nombre: {c[1]:<20} | Tel: {c[2]}"
        lbl = tk.Label(scrollable_frame, text=texto_cliente, font=("Courier", 9), anchor="w")
        lbl.pack(anchor="w", fill="x", pady=2)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
