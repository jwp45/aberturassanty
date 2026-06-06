import tkinter as tk
from tkinter import messagebox, ttk
from services.presupuesto_service import obtener_clientes_para_combo, calcular_y_guardar_presupuesto
from services.config_service import cargar_configuracion
from services.export_service import exportar_presupuesto_a_txt_local

"""
VISTA: Ventana para generar nuevos presupuestos.
Demuestra el uso de controles avanzados de Tkinter (Combobox, Text con Scroll).
"""

def abrir_nuevo_presupuesto():
    ventana = tk.Toplevel()
    ventana.title("Nuevo Presupuesto")
    ventana.geometry("600x800")
    
    # Variable para guardar el presupuesto actual una vez calculado
    presupuesto_actual = None

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
    # 2. ACCIONES DEL PRESUPUESTO
    # ==========================================
    def generar():
        nonlocal presupuesto_actual
        try:
            id_c = combo_cliente.get().split(":")[0]
            v_limpio = combo_vidrio.get().split(" ")[0].lower()
            t_limpio = combo_tipo.get().split("(")[0].strip()
            
            ticket, presupuesto_actual = calcular_y_guardar_presupuesto(id_c, ent_ancho.get(), ent_alto.get(), v_limpio, t_limpio, combo_color.get())
            
            txt_res.config(state="normal")
            txt_res.delete("1.0", tk.END)
            txt_res.insert(tk.END, ticket)
            txt_res.config(state="disabled")
            
            # Habilitar botones de acción posterior
            btn_imprimir.config(state="normal")
            btn_enviar.config(state="normal")
            
            messagebox.showinfo("Éxito", "Presupuesto calculado y guardado correctamente", parent=ventana)
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e), parent=ventana)
        except Exception as e: 
            messagebox.showerror("Error", str(e), parent=ventana)

    def imprimir():
        if presupuesto_actual:
            try:
                exportar_presupuesto_a_txt_local(presupuesto_actual)
            except Exception as e:
                messagebox.showerror("Error de Exportación", f"No se pudo generar la vista de impresión: {str(e)}", parent=ventana)
        else:
            messagebox.showwarning("Atención", "Debe calcular y guardar un presupuesto antes de imprimir.", parent=ventana)

    def enviar_email():
        dest = ent_email.get().strip()
        if not dest:
            messagebox.showwarning("Atención", "Debe ingresar una dirección de email.", parent=ventana)
            return
        if not presupuesto_actual:
            messagebox.showwarning("Atención", "Debe calcular y guardar un presupuesto antes de enviar.", parent=ventana)
            return
            
        btn_enviar.config(state="disabled", text="Enviando...")
        ventana.update()
        
        try:
            from services.export_service import enviar_presupuesto_por_email
            enviar_presupuesto_por_email(presupuesto_actual, dest)
            messagebox.showinfo("Éxito", f"Presupuesto enviado correctamente a {dest}", parent=ventana)
        except Exception as e:
            messagebox.showerror("Error de Envío", f"Ocurrió un error al enviar el email:\n{str(e)}", parent=ventana)
        finally:
            btn_enviar.config(state="normal", text="Enviar por Email")

    frame_acciones = tk.Frame(main_frame)
    frame_acciones.pack(fill="x", pady=10)

    btn_generar = tk.Button(frame_acciones, text="Calcular y Guardar", bg="#007bff", fg="white", font=("Arial", 10, "bold"), pady=8, command=generar)
    btn_generar.pack(side="left", fill="x", expand=True, padx=(0, 5))

    btn_imprimir = tk.Button(frame_acciones, text="Imprimir Presupuesto", bg="#28a745", fg="white", font=("Arial", 10, "bold"), pady=8, command=imprimir, state="disabled")
    btn_imprimir.pack(side="right", fill="x", expand=True, padx=(5, 0))

    # ==========================================
    # 3. SECCIÓN: ENVÍO POR EMAIL
    # ==========================================
    frame_email = tk.LabelFrame(main_frame, text=" Enviar Presupuesto por Email ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_email.pack(fill="x", pady=5)
    
    tk.Label(frame_email, text="Destinatario:").pack(side="left", padx=5)
    ent_email = tk.Entry(frame_email, font=("Arial", 10))
    ent_email.pack(side="left", fill="x", expand=True, padx=5)
    
    btn_enviar = tk.Button(frame_email, text="Enviar por Email", bg="#fd7e14", fg="white", font=("Arial", 9, "bold"), command=enviar_email, state="disabled")
    btn_enviar.pack(side="right", padx=5)

    # ==========================================
    # 4. SECCIÓN: DETALLE DEL PRESUPUESTO
    # ==========================================
    frame_resultado = tk.LabelFrame(main_frame, text=" Detalle del Presupuesto (Comprobante) ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_resultado.pack(fill="both", expand=True, pady=10)

    txt_res = tk.Text(frame_resultado, font=("Courier", 10), state="disabled", highlightthickness=0)
    txt_res.pack(fill="both", expand=True)

    # Botón de cierre
    btn_cerrar = tk.Button(main_frame, text="Cerrar Ventana", command=ventana.destroy, font=("Arial", 9))
    btn_cerrar.pack(pady=5)
