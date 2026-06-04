from models.Cliente import Cliente
from models.Presupuesto import Presupuesto

# Listas en memoria para actuar como almacenamiento temporario
base_clientes = []
contador_clientes = 1
contador_presupuestos = 100

def menu_abm_clientes():
    global contador_clientes
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
            nuevo = Cliente(contador_clientes, nombre, tel, dir_cliente)
            base_clientes.append(nuevo)
            print(f"¡Cliente '{nombre}' dado de alta con ID {contador_clientes}!")
            contador_clientes += 1

        elif opcion == "2":
            id_baja = int(input("Ingrese el ID del cliente a eliminar: "))
            cliente = next((c for c in base_clientes if c.id_cliente == id_baja), None)
            if cliente:
                base_clientes.remove(cliente)
                print("Cliente eliminado con éxito.")
            else:
                print("No se encontró ningún cliente con ese ID.")

        elif opcion == "3":
            id_mod = int(input("Ingrese el ID del cliente a modificar: "))
            cliente = next((c for c in base_clientes if c.id_cliente == id_mod), None)
            if cliente:
                print(f"Modificando a: {cliente.nombre}")
                cliente.nombre = input("Nuevo Nombre (dejar vacío para mantener): ") or cliente.nombre
                cliente.telefono = input("Nuevo Teléfono (dejar vacío para mantener): ") or cliente.telefono
                cliente.direccion = input("Nueva Dirección (dejar vacío para mantener): ") or cliente.direccion
                print("Datos actualizados correctamente.")
            else:
                print("Cliente no encontrado.")

        elif opcion == "4":
            print("\n--- LISTADO DE CLIENTES ---")
            if not base_clientes:
                print("No hay clientes registrados.")
            for c in base_clientes:
                print(c.obtener_detalles())
        
        elif opcion == "5":
            break

def generar_presupuesto_menu():
    global contador_presupuestos
    if not base_clientes:
        print("\n[!] Error: Debe cargar al menos un cliente antes de presupuestar.")
        return

    print("\n--- NUEVO PRESUPUESTO DE ABERTURA ---")
    print("Seleccione el cliente por su ID:")
    for c in base_clientes:
        print(f" [{c.id_cliente}] - {c.nombre}")
    
    try:
        id_sel = int(input("ID Cliente: "))
        cliente = next((c for c in base_clientes if c.id_cliente == id_sel), None)
        
        if not cliente:
            print("ID inválido.")
            return

        ancho = float(input("Ingrese ancho de la abertura (en metros): "))
        alto = float(input("Ingrese alto de la abertura (en metros): "))
        tipo_vidrio = input("Tipo de vidrio (escriba '4mm' o 'dvh'): ").strip().lower()
        if tipo_vidrio not in ["4mm", "dvh"]:
            tipo_vidrio = "dvh"  # Por defecto

        # Instanciación y relación de objetos (POO)
        presu = Presupuesto(contador_presupuestos, cliente, ancho, alto, tipo_vidrio)
        print(presu.generar_comprobante())
        contador_presupuestos += 1
        
    except ValueError:
        print("Error: Ingrese valores numéricos válidos.")

def main():
    # Carga inicial de datos de prueba para agilizar la corrección del profesor
    cliente_test = Cliente(99, "Carlos Carpintero", "2235123456", "Av. Acapulco 400")
    base_clientes.append(cliente_test)

    while True:
        print("\n========================================")
        print("  SISTEMA DE PRESUPUESTOS DE HERRERÍA   ")
        print("========================================")
        print("1. Administrar Clientes (ABM)")
        print("2. Realizar Presupuesto de Abertura")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_abm_clientes()
        elif opcion == "2":
            generar_presupuesto_menu()
        elif opcion == "3":
            print("Saliendo del sistema. ¡Buenas tareas!")
            break
        else:
            print("Opción incorrecta.")

if __name__ == "__main__":
    main()