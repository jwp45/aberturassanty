import tkinter as tk
from tkinter import messagebox, ttk
from services.presupuesto_service import obtener_clientes_para_combo, calcular_y_guardar_presupuesto

def accion_generar_presupuesto(combo_cliente, ent_ancho, ent_alto, ent_vidrio, txt_resultado):
    """Controlador para validar datos y llamar al servicio de cálculo."""
    seleccion = combo_cliente.get()
    if not seleccion:
        messagebox.showwarning("Atención", "Seleccione un cliente")
        return

    # Extraemos el ID del texto "ID: Nombre"
    id_cliente = seleccion.split(":")[0]
    
    try:
        comprobante = calcular_y_guardar_presupuesto(
            id_cliente, 
            ent_ancho.get(), 
            ent_alto.get(), 
            ent_vidrio.get()
        )
        
        # Mostramos el resultado en el área de texto
        txt_resultado.config(state="normal")
        txt_resultado.delete("1.0", tk.END)
        txt_resultado.insert(tk.END, comprobante)
        txt_resultado.config(state="disabled")
        
        messagebox.showinfo("Éxito", "Presupuesto generado y guardado")
        
    except ValueError:
        messagebox.showerror("Error", "Ancho y Alto deben ser números")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def abrir_nuevo_presupuesto():
    """Ventana de la interfaz para presupuestos."""
    ventana = tk.Toplevel()
    ventana.title("Nuevo Presupuesto")
    ventana.geometry("600x700")

    tk.Label(ventana, text="GENERAR PRESUPUESTO", font=("Arial", 14, "bold")).pack(pady=10)

    # 1. Selección de Cliente
    tk.Label(ventana, text="Seleccione Cliente:").pack()
    clientes = obtener_clientes_para_combo()
    opciones_clientes = [f"{c[0]}: {c[1]}" for c in clientes]
    
    combo_cliente = ttk.Combobox(ventana, values=opciones_clientes, width=40, state="readonly")
    combo_cliente.pack(pady=5)

    # 2. Datos de la abertura
    tk.Label(ventana, text="Ancho (mts):").pack()
    ent_ancho = tk.Entry(ventana, width=20)
    ent_ancho.pack()

    tk.Label(ventana, text="Alto (mts):").pack()
    ent_alto = tk.Entry(ventana, width=20)
    ent_alto.pack()

    tk.Label(ventana, text="Tipo de Vidrio (4mm/dvh):").pack()
    ent_vidrio = tk.Entry(ventana, width=20)
    ent_vidrio.insert(0, "4mm") # Valor por defecto
    ent_vidrio.pack()

    # 3. Botón de Acción
    tk.Button(ventana, text="Calcular y Guardar", bg="blue", fg="white", font=("Arial", 10, "bold"),
              command=lambda: accion_generar_presupuesto(combo_cliente, ent_ancho, ent_alto, ent_vidrio, txt_res)).pack(pady=20)

    # 4. Resultado (Comprobante) con Scrollbar
    tk.Label(ventana, text="RESULTADO / COMPROBANTE:").pack()
    
    # Creamos un frame para contener el texto y el scrollbar
    frame_txt = tk.Frame(ventana)
    frame_txt.pack(padx=10, pady=5, fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_txt)
    scrollbar.pack(side="right", fill="y")

    txt_res = tk.Text(frame_txt, height=18, width=65, state="disabled", font=("Courier", 10),
                      yscrollcommand=scrollbar.set)
    txt_res.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=txt_res.yview)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
