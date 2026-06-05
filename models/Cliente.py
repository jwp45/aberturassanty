class Cliente:
    """
    Representa a un cliente en el sistema.
    Utiliza propiedades para demostrar el concepto de Encapsulamiento.
    """
    def __init__(self, id_cliente, nombre, telefono, direccion):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return f"Cliente: {self.nombre} (ID: {self.id_cliente})"
