import tkinter as tk
from tkinter import messagebox, ttk
from services.presupuesto_service import obtener_clientes_para_combo, calcular_y_guardar_presupuesto
from services.config_service import cargar_configuracion

"""
VISTA: Ventana para generar nuevos presupuestos.
Demuestra el uso de controles avanzados de Tkinter (Combobox, Text con Scroll).
"""

def abrir_nuevo_presupuesto():
    ventana = tk.Toplevel()
    ventana.title("Nuevo Presupuesto")
    ventana.geometry("600x800")

    # Contenedor principal con margen interno
    main_frame = tk.Frame(ventana, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

    # ==========================================
    # 1. SECCIÓN: CONFIGURACIÓN DEL PRESUPUESTO
    # ==========================================
    frame_datos = tk.LabelFrame(main_frame, text=" Configuración del Presupuesto ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_datos.pack(fill="x", pady=10)
    
    # Configuramos el estiramiento de las columnas del grid
    frame_datos.columnconfigure(1, weight=1)
    frame_datos.columnconfigure(3, weight=1)

    # Selector de Cliente
    tk.Label(frame_datos, text="Cliente:").grid(row=0, column=0, sticky="w", pady=5)
    clientes = obtener_clientes_para_combo()
    opciones_clientes = ["0: CONSUMIDOR FINAL"] + [f"{c[0]}: {c[1]}" for c in clientes]
    combo_cliente = ttk.Combobox(frame_datos, values=opciones_clientes, state="readonly", font=("Arial", 10))
    combo_cliente.set(opciones_clientes[0])
    combo_cliente.grid(row=0, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

    # Selector de Tipo de Abertura
    tk.Label(frame_datos, text="Tipo Abertura:").grid(row=1, column=0, sticky="w", pady=5)
    opciones_tipo = ["Corrediza (MO-101, HO-203)", "Paño Fijo (PF-301)", "Puerta (PU-401, PU-402)"]
    combo_tipo = ttk.Combobox(frame_datos, values=opciones_tipo, state="readonly", font=("Arial", 10))
    combo_tipo.set(opciones_tipo[0])
    combo_tipo.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

    # Selector de Tipo de Vidrio
    tk.Label(frame_datos, text="Tipo Vidrio:").grid(row=2, column=0, sticky="w", pady=5)
    config = cargar_configuracion()
    opciones_vidrio = [f"4mm (${config['precios']['vidrio_4mm_m2']:,.0f}/m²)", 
                       f"DVH (${config['precios']['vidrio_dvh_m2']:,.0f}/m²)"]
    combo_vidrio = ttk.Combobox(frame_datos, values=opciones_vidrio, state="readonly", font=("Arial", 10))
    combo_vidrio.set(opciones_vidrio[0])
    combo_vidrio.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

    # Selector de Color de Aluminio
    tk.Label(frame_datos, text="Color Aluminio:").grid(row=3, column=0, sticky="w", pady=5)
    combo_color = ttk.Combobox(frame_datos, values=["Natural", "Blanco", "Negro"], state="readonly", font=("Arial", 10))
    combo_color.set("Natural")
    combo_color.grid(row=3, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

    # Medidas de la abertura (Ancho y Alto en la misma fila)
    tk.Label(frame_datos, text="Ancho (m):").grid(row=4, column=0, sticky="w", pady=5)
    ent_ancho = tk.Entry(frame_datos, font=("Arial", 10))
    ent_ancho.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

    tk.Label(frame_datos, text="Alto (m):").grid(row=4, column=2, sticky="w", pady=5)
    ent_alto = tk.Entry(frame_datos, font=("Arial", 10))
    ent_alto.grid(row=4, column=3, sticky="ew", padx=5, pady=5)

    # ==========================================
    # 2. ACCIÓN: BOTÓN GENERAR
    # ==========================================
    def generar():
        try:
            id_c = combo_cliente.get().split(":")[0]
            v_limpio = combo_vidrio.get().split(" ")[0].lower()
            t_limpio = combo_tipo.get().split("(")[0].strip()
            
            ticket = calcular_y_guardar_presupuesto(id_c, ent_ancho.get(), ent_alto.get(), v_limpio, t_limpio, combo_color.get())
            
            txt_res.config(state="normal")
            txt_res.delete("1.0", tk.END)
            txt_res.insert(tk.END, ticket)
            txt_res.config(state="disabled")
            messagebox.showinfo("Éxito", "Presupuesto calculado y guardado correctamente", parent=ventana)
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e), parent=ventana)
        except Exception as e: 
            messagebox.showerror("Error", str(e), parent=ventana)

    btn_generar = tk.Button(main_frame, text="Calcular y Guardar Presupuesto", bg="#007bff", fg="white", font=("Arial", 10, "bold"), pady=8, command=generar)
    btn_generar.pack(fill="x", pady=10)

    # ==========================================
    # 3. SECCIÓN: DETALLE DEL PRESUPUESTO
    # ==========================================
    frame_resultado = tk.LabelFrame(main_frame, text=" Detalle del Presupuesto (Comprobante) ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_resultado.pack(fill="both", expand=True, pady=10)

    txt_res = tk.Text(frame_resultado, font=("Courier", 10), state="disabled", highlightthickness=0)
    txt_res.pack(fill="both", expand=True)

    # Botón de cierre
    btn_cerrar = tk.Button(main_frame, text="Cerrar Ventana", command=ventana.destroy, font=("Arial", 9))
    btn_cerrar.pack(pady=5)
