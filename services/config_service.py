import json
import os

# --- Configuración de Rutas ---
# Obtenemos la ruta absoluta al directorio base del proyecto para asegurar que 
# el archivo config.json se encuentre correctamente sin importar desde dónde se ejecute el programa.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# --- Configuración por Defecto ---
# Este diccionario define los valores iniciales y la estructura necesaria para el sistema.
# Si el archivo config.json no existe o está incompleto, se utilizarán estos valores.
DEFAULT_CONFIG = {
    "precios": {
        "aluminio_kg": 8500.0,       # Precio base del aluminio por kilogramo
        "vidrio_4mm_m2": 18000.0,    # Precio del vidrio float de 4mm por m2
        "vidrio_dvh_m2": 45000.0,    # Precio del vidrio doble vidriado hermético por m2
        "herrajes_kit": 35000.0      # Precio estimado por kit de herrajes
    },
    "perfiles": {
        # Diccionario de perfiles técnicos con su peso teórico por metro lineal
        "MO-101": {"nombre": "Marco ventana corrediza", "peso_kg_m": 1.2},
        "HO-203": {"nombre": "Hoja ventana corrediza", "peso_kg_m": 1.0},
        "PF-301": {"nombre": "Marco paño fijo", "peso_kg_m": 0.8},
        "PU-401": {"nombre": "Marco puerta", "peso_kg_m": 1.5},
        "PU-402": {"nombre": "Hoja puerta", "peso_kg_m": 1.4}
    },
    "tipos_abertura": {
        # Define qué perfiles y factores de herraje se usan para cada tipo de abertura
        "Corrediza": {
            "perfiles_requeridos": [
                {"codigo": "MO-101", "cantidad_factor": 2.0}, # (Ancho + Alto) * 2
                {"codigo": "HO-203", "cantidad_factor": 4.0}  # (Ancho + Alto) * 2 * 2 hojas
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
    "insumos_porcentaje": 0.07, # 7% adicional para cubrir burletes, tornillos y selladores
    "colores_aluminio": {
        # Factores de incremento de precio según el tratamiento superficial
        "Natural": 1.0,
        "Blanco": 1.15,
        "Negro": 1.20
    },
    "margen_ganancia": 1.6, # Multiplicador para obtener el precio de venta final (Costo * 1.6)
    "resend_api_key": "re_b2AWas7o_8jmdMCsYSeSzVwPjAqa5gJWR", # Credenciales para envío de emails
    "resend_from_email": "Santy Aberturas <onboarding@resend.dev>"
}

def cargar_configuracion():
    """
    Carga la configuración desde el archivo JSON local.
    Si el archivo no existe, lo crea con los valores por defecto.
    También se encarga de 'reparar' archivos existentes si les faltan nuevas claves.
    """
    if not os.path.exists(CONFIG_FILE):
        # Si no hay archivo, creamos uno con la configuración base
        guardar_configuracion(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, "r") as f:
            config_cargada = json.load(f)
    except (json.JSONDecodeError, IOError):
        # En caso de error de lectura, devolvemos la configuración por defecto
        return DEFAULT_CONFIG
    
    # Lógica de Fusión:
    # Comparamos la configuración cargada con la DEFAULT para asegurar que
    # todas las llaves necesarias estén presentes. Útil para actualizaciones del sistema.
    actualizada = False
    for key, value in DEFAULT_CONFIG.items():
        if key not in config_cargada:
            config_cargada[key] = value
            actualizada = True
        elif isinstance(value, dict):
            # Verificación de segundo nivel para diccionarios anidados (ej: "precios")
            for sub_key, sub_value in value.items():
                if sub_key not in config_cargada[key]:
                    config_cargada[key][sub_key] = sub_value
                    actualizada = True
                # Verificación de tercer nivel (ej: llaves dentro de "tipos_abertura")
                elif isinstance(sub_value, dict) and isinstance(config_cargada[key][sub_key], dict):
                    for sub_sub_key, sub_sub_value in sub_value.items():
                        if sub_sub_key not in config_cargada[key][sub_key]:
                            config_cargada[key][sub_key][sub_sub_key] = sub_sub_value
                            actualizada = True
    
    # Si tuvimos que agregar alguna llave faltante, guardamos el archivo reparado
    if actualizada:
        guardar_configuracion(config_cargada)
        
    return config_cargada

def guardar_configuracion(config):
    """
    Persiste el diccionario de configuración en el archivo config.json con formato legible.
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
