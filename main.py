import psycopg2
from models.Cliente import Cliente
from models.Presupuesto import Presupuesto


#Conectamos a la base de datos de Supabase usando psycopg2 

def conectar():
    return psycopg2.connect(
            host="aws-1-us-west-2.pooler.supabase.com",
            database="postgres",
            user="postgres.ervrzydvnspoyqmjzwok",
            password="Wolf@1109788",
            port="5432"
        )

def menu_abm_clientes():
    while True:
        print("\n--- GESTIÓN DE CLIENTES (ABM) ---")
        print("1. Dar de Alta Cliente")
        print("2. Dar de Baja Cliente")
        print("3. Modificar Cliente")
        print("4. Listar Todos los Clientes")
        print("5. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre y Apellido: ")
            tel = input("Teléfono: ")
            dir_cliente = input("Dirección: ")
            
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO clientes (nombre, telefono, direccion) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, tel, dir_cliente))
            conexion.commit()
            conexion.close()
            print(f"¡Cliente '{nombre}' guardado en Supabase!")

        elif opcion == "2":
            id_baja = int(input("Ingrese el ID del cliente a eliminar: "))
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "DELETE FROM clientes WHERE id_cliente = %s"
            cursor.execute(sql, (id_baja,))
            conexion.commit()
            if cursor.rowcount > 0:
                print("Cliente eliminado con éxito.")
            else:
                print("No se encontró el ID.")
            conexion.close()

        elif opcion == "3":
            id_mod = int(input("Ingrese el ID del cliente a modificar: "))
            conexion = conectar()
            cursor = conexion.cursor()
            # Primero buscamos los datos actuales
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_mod,))
            c = cursor.fetchone()
            
            if c:
                print(f"Modificando a: {c[1]}")
                nom = input(f"Nuevo Nombre [{c[1]}]: ") or c[1]
                tel = input(f"Nuevo Teléfono [{c[2]}]: ") or c[2]
                dir_c = input(f"Nueva Dirección [{c[3]}]: ") or c[3]
                
                sql = "UPDATE clientes SET nombre=%s, telefono=%s, direccion=%s WHERE id_cliente=%s"
                cursor.execute(sql, (nom, tel, dir_c, id_mod))
                conexion.commit()
                print("Datos actualizados en la nube.")
            else:
                print("Cliente no encontrado.")
            conexion.close()

        elif opcion == "4":
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes ORDER BY id_cliente")
            print("\n--- LISTADO DE CLIENTES (DESDE SUPABASE) ---")
            for (id_c, nom, tel, dire) in cursor:
                print(f"ID: {id_c} | {nom} | Tel: {tel} | Dir: {dire}")
            conexion.close()
        
        elif opcion == "5":
            break

def generar_presupuesto_menu():
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Obtenemos clientes para mostrar la lista de selección
    cursor.execute("SELECT id_cliente, nombre FROM clientes ORDER BY nombre")
    clientes = cursor.fetchall()
    
    if not clientes:
        print("\n[!] Error: No hay clientes en la base de datos.")
        conexion.close()
        return

    print("\n--- NUEVO PRESUPUESTO ONLINE ---")
    for c in clientes:
        print(f" [{c[0]}] - {c[1]}")
    
    try:
        id_sel = int(input("ID Cliente seleccionado: "))
        # Buscamos los datos completos del cliente seleccionado para crear el objeto
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_sel,))
        res = cursor.fetchone()
        
        if not res:
            print("ID inválido.")
            return

        # Creamos el objeto Cliente con los datos de la DB
        cliente_obj = Cliente(res[0], res[1], res[2], res[3])
        
        ancho = float(input("Ancho (metros): "))
        alto = float(input("Alto (metros): "))
        tipo_vidrio = input("Tipo de vidrio (4mm/dvh): ")

        # --- CAMBIO: Calculamos el precio antes de guardar ---
        # Usamos un ID temporal (0) porque aún no tenemos el de la DB
        presu_temp = Presupuesto(0, cliente_obj, ancho, alto, tipo_vidrio)
        datos_calculados = presu_temp.procesar_presupuesto()
        precio_total = datos_calculados['total']

        # Guardamos el presupuesto en la DB incluyendo el precio final
        sql = """INSERT INTO presupuestos (id_cliente, ancho, alto, tipo_vidrio, precio_final) 
                 VALUES (%s, %s, %s, %s, %s) RETURNING id_presupuesto"""
        cursor.execute(sql, (id_sel, ancho, alto, tipo_vidrio, precio_total))
        id_presu = cursor.fetchone()[0]
        conexion.commit()
        
        # Ahora sí, actualizamos el objeto con el ID real de la base de datos
        presu_temp.id_presupuesto = id_presu
        print(presu_temp.generar_comprobante())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()

def main():
    while True:
        print("\n========================================")
        print("  SISTEMA DE GESTIÓN (SUPABASE ONLINE)  ")
        print("========================================")
        print("1. Administrar Clientes")
        print("2. Realizar Presupuesto")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_abm_clientes()
        elif opcion == "2":
            generar_presupuesto_menu()
        elif opcion == "3":
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
