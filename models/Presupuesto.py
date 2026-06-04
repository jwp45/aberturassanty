from datetime import datetime

class Presupuesto:
    def __init__(self, id_presupuesto, cliente, ancho, alto, tipo_vidrio="dvh"):
        self.id_presupuesto = id_presupuesto
        self.cliente = cliente  # Relación de agregación: la clase usa un objeto Cliente
        self.ancho = ancho
        self.alto = alto
        self.tipo_vidrio = tipo_vidrio
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Lista de precios fija para el entorno de simulación (simula la lista del taller)
        self.lista_precios = {
            "kg_aluminio": 8500.0,
            "vidrio_4mm": 18000.0,
            "vidrio_dvh": 45000.0,
            "herrajes_kit": 35000.0
        }

    def calcular_m2(self):
        return self.ancho * self.alto

    def procesar_presupuesto(self):
        m2 = self.calcular_m2()
        
        # Desarrollo lineal y peso (según tu receta de Línea Moderna)
        proporcion_desarrollo = 14.0 / 1.80  # metros de perfil por m²
        metros_lineales = m2 * proporcion_desarrollo
        peso_aluminio = metros_lineales * 1.1  # 1.1 kg por metro lineal promedio
        costo_aluminio = peso_aluminio * self.lista_precios["kg_aluminio"]
        
        # Cálculo de Vidrio
        precio_v = self.lista_precios["vidrio_dvh"] if self.tipo_vidrio == "dvh" else self.lista_precios["vidrio_4mm"]
        costo_vidrio = m2 * precio_v
        
        # Herrajes fijos por unidad de abertura
        costo_herrajes = self.lista_precios["herrajes_kit"]
        
        # Fórmula rápida con coeficiente de mano de obra/ganancia (x1.6)
        costo_materiales = costo_aluminio + costo_vidrio + costo_herrajes
        precio_final = costo_materiales * 1.6
        
        return {
            "m2": round(m2, 2),
            "peso_al": round(peso_aluminio, 2),
            "c_aluminio": round(costo_aluminio, 2),
            "c_vidrio": round(costo_vidrio, 2),
            "c_herrajes": round(costo_herrajes, 2),
            "total": round(precio_final, 2)
        }

    def generar_comprobante(self):
        res = self.procesar_presupuesto()
        comprobante = (
            f"\n==================================================\n"
            f"          PRESUPUESTO ABERTURA LÍNEA MODERNA       \n"
            f"==================================================\n"
            f"Presupuesto N°: {self.id_presupuesto} | Fecha: {self.fecha}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Dirección de Entrega: {self.cliente.direccion}\n"
            f"--------------------------------------------------\n"
            f"Medidas: {self.ancho}m x {self.alto}m ({res['m2']} m²)\n"
            f"Tipo de Vidrio: {self.tipo_vidrio.upper()}\n"
            f"--------------------------------------------------\n"
            f"Desglose Estimado de Materiales:\n"
            f" - Aluminio ({res['peso_al']} kg): ${res['c_aluminio']:,}\n"
            f" - Vidrio seleccionado: ${res['c_vidrio']:,}\n"
            f" - Kit Herrajes y accesorios: ${res['c_herrajes']:,}\n"
            f"--------------------------------------------------\n"
            f"PRECIO FINAL SUGERIDO (Mano de obra inc.): ${res['total']:,}\n"
            f"==================================================\n"
        )
        return comprobante