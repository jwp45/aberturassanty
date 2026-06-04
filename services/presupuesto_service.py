from services.database import conectar
from models.Presupuesto import Presupuesto
from models.Cliente import Cliente

def obtener_clientes_para_combo():
    """Obtiene ID y Nombre de clientes para el selector de presupuestos."""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_cliente, nombre FROM clientes ORDER BY nombre")
        clientes = cursor.fetchall()
        conexion.close()
        return clientes
    except Exception as e:
        raise e

def calcular_y_guardar_presupuesto(id_cliente, ancho, alto, tipo_vidrio):
    """Realiza el cálculo y guarda en la DB."""
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        
        # 1. Obtenemos datos del cliente para el objeto
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
        res = cursor.fetchone()
        cliente_obj = Cliente(res[0], res[1], res[2], res[3])
        
        # 2. Usamos el modelo para calcular
        presu_temp = Presupuesto(0, cliente_obj, float(ancho), float(alto), tipo_vidrio)
        datos = presu_temp.procesar_presupuesto()
        precio_final = datos['total']
        
        # 3. Guardamos en la DB
        sql = """INSERT INTO presupuestos (id_cliente, ancho, alto, tipo_vidrio, precio_final) 
                 VALUES (%s, %s, %s, %s, %s) RETURNING id_presupuesto"""
        cursor.execute(sql, (id_cliente, float(ancho), float(alto), tipo_vidrio, precio_final))
        id_db = cursor.fetchone()[0]
        conexion.commit()
        conexion.close()
        
        # Devolvemos el comprobante generado
        presu_temp.id_presupuesto = id_db
        return presu_temp.generar_comprobante()
        
    except Exception as e:
        raise e
