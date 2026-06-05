import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "precios": {
        "aluminio_kg": 8500.0,
        "vidrio_4mm_m2": 18000.0,
        "vidrio_dvh_m2": 45000.0,
        "herrajes_kit": 35000.0
    },
    "perfiles": {
        "MO-101": {"nombre": "Marco ventana corrediza", "peso_kg_m": 1.2},
        "HO-203": {"nombre": "Hoja ventana corrediza", "peso_kg_m": 1.0},
        "PF-301": {"nombre": "Marco paño fijo", "peso_kg_m": 0.8},
        "PU-401": {"nombre": "Marco puerta", "peso_kg_m": 1.5},
        "PU-402": {"nombre": "Hoja puerta", "peso_kg_m": 1.4}
    },
    "tipos_abertura": {
        "Corrediza": {
            "perfiles_requeridos": [
                {"codigo": "MO-101", "cantidad_factor": 2.0}, # 2 * (Ancho + Alto)
                {"codigo": "HO-203", "cantidad_factor": 4.0}  # 2 * (Ancho + Alto) para 2 hojas
            ],
            "factor_herrajes": 1.0
        },
        "Paño Fijo": {
            "perfiles_requeridos": [
                {"codigo": "PF-301", "cantidad_factor": 2.0}
            ],
            "factor_herrajes": 0.2
        },
        "Puerta": {
            "perfiles_requeridos": [
                {"codigo": "PU-401", "cantidad_factor": 2.0},
                {"codigo": "PU-402", "cantidad_factor": 2.0}
            ],
            "factor_herrajes": 1.5
        }
    },
    "insumos_porcentaje": 0.07, # 7% para burletes, tornillos, etc.
    "colores_aluminio": {
        "Natural": 1.0,
        "Blanco": 1.15,
        "Negro": 1.20
    },
    "margen_ganancia": 1.6
}

def cargar_configuracion():
    if not os.path.exists(CONFIG_FILE):
        guardar_configuracion(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    with open(CONFIG_FILE, "r") as f:
        config_cargada = json.load(f)
    
    # Fusionar con DEFAULT_CONFIG para asegurar que no falten llaves nuevas
    # Esto evita errores cuando agregamos funcionalidades nuevas
    actualizada = False
    for key, value in DEFAULT_CONFIG.items():
        if key not in config_cargada:
            config_cargada[key] = value
            actualizada = True
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if sub_key not in config_cargada[key]:
                    config_cargada[key][sub_key] = sub_value
                    actualizada = True
                # Si el sub_valor es un dict (ej: "Corrediza"), verificar sus llaves (ej: "perfiles_requeridos")
                elif isinstance(sub_value, dict) and isinstance(config_cargada[key][sub_key], dict):
                    for sub_sub_key, sub_sub_value in sub_value.items():
                        if sub_sub_key not in config_cargada[key][sub_key]:
                            config_cargada[key][sub_key][sub_sub_key] = sub_sub_value
                            actualizada = True
    
    if actualizada:
        guardar_configuracion(config_cargada)
        
    return config_cargada

def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
