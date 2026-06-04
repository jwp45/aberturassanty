from datetime import datetime

class Presupuesto:
    def __init__(self, id_presupuesto, cliente, ancho, alto, tipo_vidrio="dvh"):
        self.id_presupuesto = id_presupuesto
        self.cliente = cliente  # Agregación: objeto de la clase Cliente
        self.ancho = ancho
        self.alto = alto
        self.tipo_vidrio = tipo_vidrio
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # LISTA DE PRECIOS (Valores actuales para el trabajo práctico)
        self.PRECIO_KG_ALUMINIO = 8500.0
        self.PRECIO_M2_VIDRIO_4MM = 18000.0
        self.PRECIO_M2_VIDRIO_DVH = 45000.0
        self.COSTO_HERRAJES_KIT = 35000.0 # Promedio entre 25k y 45k

    def calcular_m2(self):
        """Calcula la superficie de la abertura."""
        return self.ancho * self.alto

    def procesar_presupuesto(self):
        """
        Realiza el cálculo paso a paso siguiendo la lógica de carpintería:
        1. M2 y Metros Lineales
        2. Peso y Costo de Aluminio
        3. Costo de Vidrio y Herrajes
        4. Precio Final (Factor 1.6)
        """
        # 1. Superficie
        superficie_m2 = self.calcular_m2()
        
        # 2. Desarrollo Lineal (Fórmula simplificada: suma de perímetros de marco y hoja)
        # Usamos un factor de 5.5 para cubrir marco, hoja y desperdicios
        metros_lineales = (self.ancho + self.alto) * 5.5
        
        # 3. Peso y Costo Aluminio
        peso_aluminio = metros_lineales * 1.1  # Promedio kg/m de Línea Moderna
        costo_aluminio = peso_aluminio * self.PRECIO_KG_ALUMINIO
        
        # 4. Vidrio (4mm o DVH)
        precio_m2_v = self.PRECIO_M2_VIDRIO_DVH if self.tipo_vidrio == "dvh" else self.PRECIO_M2_VIDRIO_4MM
        costo_vidrio = superficie_m2 * precio_m2_v
        
        # 5. Herrajes
        costo_herrajes = self.COSTO_HERRAJES_KIT
        
        # 6. Cálculo Final con Coeficiente (1.6 = Materiales + Mano de Obra + Ganancia)
        costo_total_materiales = costo_aluminio + costo_vidrio + costo_herrajes
        precio_final = costo_total_materiales * 1.6
        
        return {
            "m2": round(superficie_m2, 2),
            "metros_lineales": round(metros_lineales, 2),
            "peso_al": round(peso_aluminio, 2),
            "c_aluminio": round(costo_aluminio, 2),
            "c_vidrio": round(costo_vidrio, 2),
            "c_herrajes": round(costo_herrajes, 2),
            "total": round(precio_final, 2)
        }

    def generar_comprobante(self):
        res = self.procesar_presupuesto()
        comprobante = (
            f"==================================================\n"
            f"          SANTY ABERTURAS - PRESUPUESTO           \n"
            f"==================================================\n"
            f"N°: {self.id_presupuesto} | Fecha: {self.fecha}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"--------------------------------------------------\n"
            f"DETALLE TÉCNICO:\n"
            f" - Medidas: {self.ancho}m x {self.alto}m\n"
            f" - Superficie: {res['m2']} m²\n"
            f" - Vidrio: {self.tipo_vidrio.upper()}\n"
            f" - Aluminio: {res['peso_al']} kg est.\n"
            f"--------------------------------------------------\n"
            f"DESGLOSE DE MATERIALES:\n"
            f" - Aluminio: ${res['c_aluminio']:,.2f}\n"
            f" - Vidrio:   ${res['c_vidrio']:,.2f}\n"
            f" - Herrajes: ${res['c_herrajes']:,.2f}\n"
            f"--------------------------------------------------\n"
            f"PRECIO FINAL (IVA INC.): ${res['total']:,.2f}\n"
            f"==================================================\n"
            f"Fórmula: (Materiales) x 1.6 Coef. Ganancia/MO\n"
        )
        return comprobante
