from datetime import datetime
from services.config_service import cargar_configuracion
from models.Componente import Componente, PerfilAluminio, Vidrio, Herraje

class Presupuesto:
    """
    MODELO: Contiene la lógica técnica y matemática del presupuesto.
    Calcula materiales, peso y precio final basándose en la configuración.
    Demuestra los conceptos de Composición/Agregación y Polimorfismo.
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
        2. Crea instancias de PerfilAluminio, Vidrio, Herraje e Insumos (Herencia).
        3. Calcula el total final iterando y sumando costos de forma polimórfica.
        """
        info_tipo = self.config["tipos_abertura"].get(self.tipo_abertura)
        if not info_tipo: raise ValueError("Tipo de abertura no configurado")
            
        # --- Relación de Agregación / Composición (OOP) ---
        # El presupuesto está compuesto de múltiples objetos derivados de Componente
        componentes = []
        perfiles_usados = []
        
        # 1. Perfiles de Aluminio
        precio_kg = self.config["precios"]["aluminio_kg"]
        factor_color = self.config["colores_aluminio"].get(self.color, 1.0)
        
        peso_total_al = 0
        costo_aluminio = 0
        for p in info_tipo["perfiles_requeridos"]:
            perfil_data = self.config["perfiles"][p["codigo"]]
            ml = (self.ancho + self.alto) * p["cantidad_factor"]
            
            # Instanciamos la subclase PerfilAluminio
            perfil_obj = PerfilAluminio(
                codigo=p["codigo"],
                descripcion=perfil_data["nombre"],
                precio_base_kg=precio_kg,
                peso_kg_m=perfil_data["peso_kg_m"],
                metros_lineales=ml,
                factor_color=factor_color
            )
            componentes.append(perfil_obj)
            costo_aluminio += perfil_obj.calcular_costo()
            peso_total_al += ml * perfil_data["peso_kg_m"]
            perfiles_usados.append(f"{p['codigo']} ({ml:.1f}m)")
        
        # 2. Vidrio
        m2 = self.ancho * self.alto
        v_precio = self.config["precios"]["vidrio_dvh_m2"] if self.tipo_vidrio == "dvh" else self.config["precios"]["vidrio_4mm_m2"]
        
        # Instanciamos la subclase Vidrio
        vidrio_obj = Vidrio(
            codigo=f"VID-{self.tipo_vidrio.upper()}",
            descripcion=f"Vidrio {self.tipo_vidrio.upper()}",
            precio_base_m2=v_precio,
            superficie_m2=m2
        )
        componentes.append(vidrio_obj)
        costo_vidrio = vidrio_obj.calcular_costo()
        
        # 3. Herrajes
        precio_herraje = self.config["precios"]["herrajes_kit"]
        factor_herrajes = info_tipo["factor_herrajes"]
        
        # Instanciamos la subclase Herraje
        herraje_obj = Herraje(
            codigo="HER-KIT",
            descripcion="Kit de herrajes",
            precio_base_unidad=precio_herraje,
            cantidad=factor_herrajes
        )
        componentes.append(herraje_obj)
        costo_herrajes = herraje_obj.calcular_costo()
        
        # 4. Insumos adicionales (burletes, tornillos - 7% sobre aluminio)
        costo_insumos = costo_aluminio * self.config.get("insumos_porcentaje", 0.07)
        insumos_obj = Componente(
            codigo="INSUMOS",
            descripcion="Tornillos y selladores",
            precio_base=costo_insumos
        )
        componentes.append(insumos_obj)
        
        # Polimorfismo en acción:
        # Sumamos el costo de todos los componentes llamando al método calcular_costo()
        # de cada objeto, independientemente de la subclase a la que pertenezcan.
        total_materiales = sum(comp.calcular_costo() for comp in componentes)
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
