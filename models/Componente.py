class Componente:
    """
    CLASE BASE: Representa un componente genérico del presupuesto.
    Demuestra los conceptos de Herencia y Polimorfismo.
    """
    def __init__(self, codigo, descripcion, precio_base):
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio_base = precio_base

    def calcular_costo(self):
        """
        Método polimórfico. Devuelve el costo calculado.
        Será sobrescrito por las clases derivadas.
        """
        return self.precio_base


class PerfilAluminio(Componente):
    """
    CLASE DERIVADA (Herencia): Representa un perfil de aluminio específico.
    Sobrescribe el cálculo del costo aplicando el peso y el factor de color.
    """
    def __init__(self, codigo, descripcion, precio_base_kg, peso_kg_m, metros_lineales, factor_color=1.0):
        super().__init__(codigo, descripcion, precio_base_kg)
        self.peso_kg_m = peso_kg_m
        self.metros_lineales = metros_lineales
        self.factor_color = factor_color

    def calcular_costo(self):
        # Peso total de aluminio = metros lineales * peso por metro
        peso_total = self.metros_lineales * self.peso_kg_m
        # Costo = peso total * precio por kg * recargo de color
        return peso_total * self.precio_base * self.factor_color


class Vidrio(Componente):
    """
    CLASE DERIVADA (Herencia): Representa un paño o tipo de vidrio.
    Sobrescribe el cálculo de costo multiplicando los m² por el precio base de ese vidrio.
    """
    def __init__(self, codigo, descripcion, precio_base_m2, superficie_m2):
        super().__init__(codigo, descripcion, precio_base_m2)
        self.superficie_m2 = superficie_m2

    def calcular_costo(self):
        return self.superficie_m2 * self.precio_base


class Herraje(Componente):
    """
    CLASE DERIVADA (Herencia): Representa los herrajes y accesorios.
    Sobrescribe el costo según la cantidad del kit necesaria para la abertura.
    """
    def __init__(self, codigo, descripcion, precio_base_unidad, cantidad=1.0):
        super().__init__(codigo, descripcion, precio_base_unidad)
        self.cantidad = cantidad

    def calcular_costo(self):
        return self.precio_base * self.cantidad