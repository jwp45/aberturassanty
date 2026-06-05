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

    tk.Label(ventana, text="GENERAR PRESUPUESTO", font=("Arial", 14, "bold")).pack(pady=10)

    # --- SELECCIÓN DE CLIENTE ---
    tk.Label(ventana, text="Seleccione Cliente:").pack()
    clientes = obtener_clientes_para_combo()
    opciones_clientes = ["0: CONSUMIDOR FINAL"] + [f"{c[0]}: {c[1]}" for c in clientes]
    
    combo_cliente = ttk.Combobox(ventana, values=opciones_clientes, width=40, state="readonly")
    combo_cliente.set(opciones_clientes[0]); combo_cliente.pack(pady=5)

    # --- MEDIDAS ---
    frame_medidas = tk.Frame(ventana); frame_medidas.pack(pady=5)
    tk.Label(frame_medidas, text="Ancho (m):").grid(row=0, column=0)
    ent_ancho = tk.Entry(frame_medidas, width=10); ent_ancho.grid(row=0, column=1, padx=5)
    tk.Label(frame_medidas, text="Alto (m):").grid(row=0, column=2)
    ent_alto = tk.Entry(frame_medidas, width=10); ent_alto.grid(row=0, column=3, padx=5)

    # --- OPCIONES TÉCNICAS ---
    tk.Label(ventana, text="Tipo de Abertura:").pack()
    opciones_tipo = ["Corrediza (MO-101, HO-203)", "Paño Fijo (PF-301)", "Puerta (PU-401, PU-402)"]
    combo_tipo = ttk.Combobox(ventana, values=opciones_tipo, state="readonly", width=35)
    combo_tipo.set(opciones_tipo[0]); combo_tipo.pack(pady=5)

    config = cargar_configuracion()
    opciones_vidrio = [f"4mm (${config['precios']['vidrio_4mm_m2']:,.0f}/m²)", 
                       f"DVH (${config['precios']['vidrio_dvh_m2']:,.0f}/m²)"]
    tk.Label(ventana, text="Tipo de Vidrio:").pack()
    combo_vidrio = ttk.Combobox(ventana, values=opciones_vidrio, state="readonly", width=30)
    combo_vidrio.set(opciones_vidrio[0]); combo_vidrio.pack(pady=5)

    tk.Label(ventana, text="Color de Aluminio:").pack()
    combo_color = ttk.Combobox(ventana, values=["Natural", "Blanco", "Negro"], state="readonly")
    combo_color.set("Natural"); combo_color.pack(pady=5)

    # --- ACCIÓN ---
    def generar():
        try:
            id_c = combo_cliente.get().split(":")[0]
            v_limpio = combo_vidrio.get().split(" ")[0].lower()
            t_limpio = combo_tipo.get().split("(")[0].strip()
            
            ticket = calcular_y_guardar_presupuesto(id_c, ent_ancho.get(), ent_alto.get(), v_limpio, t_limpio, combo_color.get())
            
            txt_res.config(state="normal"); txt_res.delete("1.0", tk.END)
            txt_res.insert(tk.END, ticket); txt_res.config(state="disabled")
            messagebox.showinfo("Éxito", "Presupuesto guardado en la nube")
        except Exception as e: messagebox.showerror("Error", str(e))

    tk.Button(ventana, text="Calcular y Guardar", bg="blue", fg="white", font=("Arial", 10, "bold"), command=generar).pack(pady=20)

    # --- RESULTADO ---
    txt_res = tk.Text(ventana, height=15, width=65, state="disabled", font=("Courier", 10))
    txt_res.pack(pady=10, padx=20)
    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=5)
