-- Estructura básica para el sistema de presupuestos
-- Puedes importar este archivo directamente en phpMyAdmin

CREATE DATABASE IF NOT EXISTS aberturas_santy;
USE aberturas_santy;

-- Tabla para Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(200)
) ENGINE=InnoDB;

-- Tabla para Presupuestos
CREATE TABLE IF NOT EXISTS presupuestos (
    id_presupuesto INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    ancho DECIMAL(10,2) NOT NULL,
    alto DECIMAL(10,2) NOT NULL,
    tipo_vidrio VARCHAR(10) DEFAULT 'dvh',
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
) ENGINE=InnoDB;
