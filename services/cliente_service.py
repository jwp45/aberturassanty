from services.database import conectar
from services.decorators import validar_nombre_cliente

def obtener_clientes():
    """Devuelve la lista de todos los clientes."""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_cliente, nombre, telefono, direccion FROM clientes ORDER BY id_cliente DESC")
        clientes = cursor.fetchall()
        conexion.close()
        return clientes
    except Exception as e:
        raise e

def obtener_cliente_por_id(id_cliente):
    """Busca un cliente específico."""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, telefono, direccion FROM clientes WHERE id_cliente = %s", (id_cliente,))
        cliente = cursor.fetchone()
        conexion.close()
        return cliente
    except Exception as e:
        raise e

@validar_nombre_cliente
def guardar_nuevo_cliente(nombre, telefono, direccion):
    """Inserta un nuevo cliente en la DB."""
    
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO clientes (nombre, telefono, direccion) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, telefono, direccion))
        conexion.commit()
        conexion.close()
    except Exception as e:
        raise e

@validar_nombre_cliente
def actualizar_cliente_db(id_cliente, nombre, telefono, direccion):
    """Actualiza un cliente existente."""
    if not id_cliente:
        raise ValueError("ID es obligatorio")

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "UPDATE clientes SET nombre=%s, telefono=%s, direccion=%s WHERE id_cliente=%s"
        cursor.execute(sql, (nombre, telefono, direccion, id_cliente))
        conexion.commit()
        conexion.close()
    except Exception as e:
        raise e

def eliminar_cliente_db(id_cliente):
    """Elimina un cliente por ID."""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conexion.commit()
        conexion.close()
    except Exception as e:
        raise e
