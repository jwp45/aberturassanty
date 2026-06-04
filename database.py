import mariadb
import sys

def get_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="", # El usuario deberá completar esto o usar variables de entorno
            host="127.0.0.1",
            port=3306,
            database="aberturas_santy"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        sys.exit(1)

def init_db():
    # Esta función puede ejecutar el schema.sql o crear las tablas manualmente
    conn = get_connection()
    cur = conn.cursor()
    
    # Crear tabla clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            telefono VARCHAR(20),
            direccion VARCHAR(200)
        )
    """)
    
    # Crear tabla presupuestos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS presupuestos (
            id_presupuesto INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT,
            ancho FLOAT NOT NULL,
            alto FLOAT NOT NULL,
            tipo_vidrio VARCHAR(10) DEFAULT 'dvh',
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Base de datos inicializada correctamente.")
