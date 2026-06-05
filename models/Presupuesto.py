from datetime import datetime
from services.config_service import cargar_configuracion

class Presupuesto:
    """
    MODELO: Contiene la lógica técnica y matemática del presupuesto.
    Calcula materiales, peso y precio final basándose en la configuración.
    """
    def __init__(self, id_presupuesto, cliente, ancho, alto, tipo_vidrio="dvh", tipo_abertura="Corrediza", color="Natural"):
        self.id_presupuesto = id_presupuesto
        self.cliente = cliente
        self.ancho = ancho
        self.alto = alto
        self.tipo_vidrio = tipo_vidrio
        self.tipo_abertura = tipo_abertura
        self.color = color
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Carga precios y perfiles desde el archivo config.json
        self.config = cargar_configuracion()
        self.MARGEN_GANANCIA = self.config["margen_ganancia"]

    def procesar_presupuesto(self):
        """
        Lógica Principal:
        1. Identifica perfiles según tipo (MO-101, HO-203, etc.)
        2. Calcula KG de aluminio según metros lineales y peso por metro.
        3. Suma Vidrio, Herrajes e Insumos (7%).
        4. Aplica Coeficiente de Mano de Obra (Margen).
        """
        info_tipo = self.config["tipos_abertura"].get(self.tipo_abertura)
        if not info_tipo: raise ValueError("Tipo de abertura no configurado")
            
        # --- Cálculo de Aluminio ---
        peso_total_al = 0
        perfiles_usados = []
        precio_kg = self.config["precios"]["aluminio_kg"]
        factor_color = self.config["colores_aluminio"].get(self.color, 1.0)
        
        for p in info_tipo["perfiles_requeridos"]:
            perfil_data = self.config["perfiles"][p["codigo"]]
            ml = (self.ancho + self.alto) * p["cantidad_factor"]
            peso_total_al += ml * perfil_data["peso_kg_m"]
            perfiles_usados.append(f"{p['codigo']} ({ml:.1f}m)")

        costo_aluminio = peso_total_al * precio_kg * factor_color
        
        # --- Cálculo de Vidrio y Herrajes ---
        m2 = self.ancho * self.alto
        v_precio = self.config["precios"]["vidrio_dvh_m2"] if self.tipo_vidrio == "dvh" else self.config["precios"]["vidrio_4mm_m2"]
        costo_vidrio = m2 * v_precio
        costo_herrajes = self.config["precios"]["herrajes_kit"] * info_tipo["factor_herrajes"]
        costo_insumos = costo_aluminio * self.config.get("insumos_porcentaje", 0.07) # Burletes/Tornillos
        
        # --- Precio Final ---
        total_materiales = costo_aluminio + costo_vidrio + costo_herrajes + costo_insumos
        precio_final = total_materiales * self.MARGEN_GANANCIA
        
        return {
            "m2": round(m2, 2), "peso": round(peso_total_al, 2),
            "c_al": costo_aluminio, "c_vi": costo_vidrio, 
            "c_he": costo_herrajes + costo_insumos,
            "total": precio_final, "detalle_p": ", ".join(perfiles_usados)
        }

    def generar_comprobante(self):
        res = self.procesar_presupuesto()
        m = self.MARGEN_GANANCIA
        return (
            f"==================================================\n"
            f"          SANTY ABERTURAS - PRESUPUESTO           \n"
            f"==================================================\n"
            f"Cliente: {self.cliente.nombre} | Fecha: {self.fecha}\n"
            f"Detalle: {self.tipo_abertura} {self.color} ({self.ancho}x{self.alto})\n"
            f"Perfiles: {res['detalle_p']}\n"
            f"--------------------------------------------------\n"
            f"PRECIOS (Con Mano de Obra Incluida):\n"
            f" - Estructura Aluminio: ${res['c_al'] * m:,.2f}\n"
            f" - Vidrio / Paño:       ${res['c_vi'] * m:,.2f}\n"
            f" - Accesorios y Varios: ${res['c_he'] * m:,.2f}\n"
            f"--------------------------------------------------\n"
            f"TOTAL FINAL: ${res['total']:,.2f}\n"
            f"==================================================\n"
        )
