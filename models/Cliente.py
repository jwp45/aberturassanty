class Cliente:
    def __init__(self, id_cliente, nombre, telefono, direccion):
        self._id_cliente = id_cliente  # Encapsulamiento básico
        self._nombre = nombre
        self._telefono = telefono
        self._direccion = direccion

    # Getters y Setters para permitir la modificación (Parte del ABM)
    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre.strip():
            self._nombre = nuevo_nombre

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        self._telefono = nuevo_telefono

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, nueva_direccion):
        self._direccion = nueva_direccion

    def obtener_detalles(self):
        return f"ID: {self._id_cliente} | {self._nombre} | Tel: {self._telefono} | Dir: {self._direccion}"