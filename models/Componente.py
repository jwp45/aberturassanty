class Componente:
    def __init__(self, codigo, descripcion, precio_unidad, unidad_medida):
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio_unidad = precio_unidad
        self.unidad_medida = unidad_medida  # "kg", "m2", "unidad"

    def calcular_costo(self, cantidad):
        return self.precio_unidad * cantidad