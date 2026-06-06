class Cliente:
    """
    Representa a un cliente en el sistema.
    Utiliza propiedades con decoradores @property para demostrar el concepto de Encapsulamiento.
    """
    def __init__(self, id_cliente, nombre, telefono, direccion):
        self._id_cliente = id_cliente
        self.nombre = nombre       # Invoca al setter de nombre para su validación
        self.telefono = telefono   # Invoca al setter de teléfono
        self.direccion = direccion # Invoca al setter de dirección

    @property
    def id_cliente(self):
        """Getter para obtener el ID de cliente (solo lectura)."""
        return self._id_cliente

    @property
    def nombre(self):
        """Getter para obtener el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Setter para el nombre, asegurando que no se guarden datos vacíos."""
        if not valor or not str(valor).strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = str(valor).strip()

    @property
    def telefono(self):
        """Getter para obtener el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        """Setter para el teléfono."""
        self._telefono = str(valor).strip() if valor else ""

    @property
    def direccion(self):
        """Getter para obtener la dirección del cliente."""
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        """Setter para la dirección."""
        self._direccion = str(valor).strip() if valor else ""

    def __str__(self):
        return f"Cliente: {self.nombre} (ID: {self.id_cliente})"
