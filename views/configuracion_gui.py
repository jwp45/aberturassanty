import tkinter as tk
from tkinter import messagebox
from services.config_service import cargar_configuracion, guardar_configuracion

def abrir_configuracion():
    ventana = tk.Toplevel()
    ventana.title("Configuración de Costos y Parámetros")
    ventana.geometry("450x550")
    
    config = cargar_configuracion()
    
    # --- PRECIOS BASE ---
    tk.Label(ventana, text="Precios Base", font=("Arial", 12, "bold")).pack(pady=5)
    
    frame_precios = tk.Frame(ventana)
    frame_precios.pack(pady=5)
    
    entries = {}
    
    labels_precios = [
        ("Aluminio (kg):", "aluminio_kg"),
        ("Vidrio 4mm (m2):", "vidrio_4mm_m2"),
        ("Vidrio DVH (m2):", "vidrio_dvh_m2"),
        ("Kit Herrajes:", "herrajes_kit")
    ]
    
    for i, (label, key) in enumerate(labels_precios):
        tk.Label(frame_precios, text=label).grid(row=i, column=0, sticky="e", padx=5)
        entry = tk.Entry(frame_precios)
        entry.insert(0, str(config["precios"][key]))
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries[key] = entry

    # --- MARGEN GANANCIA ---
    tk.Label(ventana, text="Margen de Ganancia", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(ventana, text="Ej: 1.6 para 60% de ganancia").pack()
    entry_margen = tk.Entry(ventana)
    entry_margen.insert(0, str(config["margen_ganancia"]))
    entry_margen.pack(pady=5)
    
    def guardar():
        try:
            # Actualizar precios
            for key in entries:
                config["precios"][key] = float(entries[key].get())
            
            # Actualizar margen
            config["margen_ganancia"] = float(entry_margen.get())
            
            guardar_configuracion(config)
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
            ventana.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

    tk.Button(ventana, text="Guardar Configuración", bg="green", fg="white", command=guardar).pack(pady=20)
