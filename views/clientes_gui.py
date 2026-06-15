import tkinter as tk
from tkinter import messagebox, ttk
from services.cliente_service import (
    obtener_clientes, obtener_cliente_por_id, 
    guardar_nuevo_cliente, actualizar_cliente_db, eliminar_cliente_db
)

def configurar_estilos():
    """Configura los estilos de la tabla una sola vez."""
    style = ttk.Style()
    if style.theme_use() != "clam":
        style.theme_use("clam")
    
    style.configure("Treeview", 
                    background="#ffffff", 
                    foreground="#333333", 
                    rowheight=25, 
                    fieldbackground="#ffffff",
                    font=("Segoe UI", 9))
    
    style.configure("Treeview.Heading", 
                    background="#D4AF37", 
                    foreground="white", 
                    font=("Segoe UI", 10, "bold"))
    
    style.map("Treeview", background=[('selected', '#D4AF37')])

def abrir_gestion_clientes():
    configurar_estilos()
    ventana = tk.Toplevel()
    ventana.title("Gestión de Clientes")
    ventana.geometry("600x750")
    
    # Contenedor principal
    main_frame = tk.Frame(ventana, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

    # ==========================================
    # 1. SECCIÓN: FORMULARIO
    # ==========================================
    frame_formulario = tk.LabelFrame(main_frame, text=" Datos del Cliente ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_formulario.pack(fill="x", pady=10)
    frame_formulario.columnconfigure(1, weight=1)

    tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
    ent_nombre = tk.Entry(frame_formulario, font=("Arial", 10))
    ent_nombre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(frame_formulario, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=5)
    ent_tel = tk.Entry(frame_formulario, font=("Arial", 10))
    ent_tel.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(frame_formulario, text="Dirección:").grid(row=2, column=0, sticky="w", pady=5)
    ent_dir = tk.Entry(frame_formulario, font=("Arial", 10))
    ent_dir.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(frame_formulario, text="Email:").grid(row=3, column=0, sticky="w", pady=5)
    ent_email = tk.Entry(frame_formulario, font=("Arial", 10))
    ent_email.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

    frame_btns = tk.Frame(frame_formulario)
    frame_btns.grid(row=4, column=0, columnspan=2, pady=10)
    
    def guardar():
        try:
            guardar_nuevo_cliente(ent_nombre.get(), ent_tel.get(), ent_dir.get(), ent_email.get())
            messagebox.showinfo("Éxito", "Cliente guardado correctamente", parent=ventana)
            actualizar_lista()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    def actualizar():
        if not ent_id_accion.get(): 
            messagebox.showwarning("Atención", "Seleccione un cliente para actualizar", parent=ventana)
            return
        try:
            actualizar_cliente_db(ent_id_accion.get(), ent_nombre.get(), ent_tel.get(), ent_dir.get(), ent_email.get())
            messagebox.showinfo("Éxito", "Datos actualizados correctamente", parent=ventana)
            actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    def limpiar_campos():
        for e in [ent_id_accion, ent_nombre, ent_tel, ent_dir, ent_email]:
            e.delete(0, tk.END)

    tk.Button(frame_btns, text="Guardar Nuevo", bg="#28a745", fg="white", font=("Arial", 9, "bold"), command=guardar, padx=10).pack(side="left", padx=10)
    tk.Button(frame_btns, text="Actualizar", bg="#fd7e14", fg="white", font=("Arial", 9, "bold"), command=actualizar, padx=10).pack(side="left", padx=10)
    tk.Button(frame_btns, text="Limpiar", bg="#6c757d", fg="white", font=("Arial", 9, "bold"), command=limpiar_campos, padx=10).pack(side="left", padx=10)

    # ==========================================
    # 2. SECCIÓN: BÚSQUEDA / ELIMINACIÓN
    # ==========================================
    frame_busqueda = tk.LabelFrame(main_frame, text=" Acción por ID ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_busqueda.pack(fill="x", pady=10)

    tk.Label(frame_busqueda, text="ID Cliente:").pack(side="left", padx=5)
    ent_id_accion = tk.Entry(frame_busqueda, width=10, font=("Arial", 10))
    ent_id_accion.pack(side="left", padx=5)

    def eliminar():
        if not ent_id_accion.get(): return
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente permanentemente?", parent=ventana):
            eliminar_cliente_db(ent_id_accion.get())
            messagebox.showinfo("Éxito", "Cliente eliminado", parent=ventana)
            actualizar_lista()
            limpiar_campos()

    tk.Button(frame_busqueda, text="Eliminar Cliente", bg="#dc3545", fg="white", font=("Arial", 9, "bold"), command=eliminar).pack(side="right", padx=5)

    # ==========================================
    # 3. SECCIÓN: LISTADO (TABLA)
    # ==========================================
    frame_listado = tk.LabelFrame(main_frame, text=" Listado de Clientes ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_listado.pack(fill="both", expand=True, pady=10)

    # Buscador
    frame_search = tk.Frame(frame_listado)
    frame_search.pack(fill="x", pady=(0, 5))
    tk.Label(frame_search, text="🔍 Buscar:").pack(side="left", padx=5)
    ent_buscar = tk.Entry(frame_search, font=("Segoe UI", 10))
    ent_buscar.pack(side="left", fill="x", expand=True, padx=5)

    # Tabla
    columnas = ("ID", "Nombre", "Teléfono", "Dirección", "Email")
    tabla = ttk.Treeview(frame_listado, columns=columnas, show="headings", height=8)
    
    for col in columnas:
        tabla.heading(col, text=col)
    
    tabla.column("ID", width=40, anchor="center")
    tabla.column("Nombre", width=120)
    tabla.column("Teléfono", width=100)
    tabla.column("Dirección", width=120)
    tabla.column("Email", width=150)
    
    scroll = ttk.Scrollbar(frame_listado, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll.set)

    def actualizar_lista(event=None):
        for item in tabla.get_children(): tabla.delete(item)
        filtro = ent_buscar.get().lower()
        try:
            clientes = obtener_clientes()
            for c in clientes:
                if filtro in str(c[1]).lower():
                    tabla.insert("", tk.END, values=c)
        except Exception as e:
            print(f"Error al cargar lista: {e}")

    def al_seleccionar(event):
        seleccion = tabla.selection()
        if seleccion:
            v = tabla.item(seleccion[0])['values']
            limpiar_campos()
            for e, val in zip([ent_id_accion, ent_nombre, ent_tel, ent_dir, ent_email], v):
                e.insert(0, val)

    ent_buscar.bind("<KeyRelease>", actualizar_lista)
    tabla.bind("<<TreeviewSelect>>", al_seleccionar)

    # Carga inicial diferida
    ventana.after(100, actualizar_lista)

    tabla.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
