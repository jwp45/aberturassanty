# Santy Aberturas - Sistema de Gestión y Presupuestos

Este proyecto es una aplicación de escritorio desarrollada en **Python** con **Tkinter** para la gestión de clientes y la realización automatizada de presupuestos técnicos de carpintería de aluminio para la empresa **Santy Aberturas**.

Este desarrollo forma parte del **Trabajo Práctico N.º 2** para la materia **Programación Avanzada** de la **Universidad Nacional Guillermo Brown (UNAB)**.

---

## 🚀 Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** Tkinter (Librería nativa de GUI en Python)
* **Persistencia en la Nube:** Supabase (Base de datos PostgreSQL en la nube)
* **Gestión de Configuración:** Archivos JSON local (`config.json` para almacenamiento parametrizable de costos)
* **Decoradores e Introspección:** Librerías nativas `functools` e `inspect` para validación dinámica de datos

---

## 🏗️ Estructura del Código (MVC)

El proyecto está organizado de manera modular según la separación de responsabilidades:

```text
AberturasSanty/
│
├── main.py                 # Punto de entrada de la aplicación
├── config.json             # Configuración persistente de costos (generada automáticamente)
├── README.md               # Documentación obligatoria del proyecto
├── consignas.pdf           # Consignas del trabajo práctico
│
├── models/                 # Lógica de Negocio (Modelado de datos)
│   ├── __init__.py         # Módulo y lógica de consola (para pruebas de terminal)
│   ├── Cliente.py          # Clase Cliente (Encapsulamiento)
│   ├── Presupuesto.py      # Clase Presupuesto (Composición y Relación)
│   └── Componente.py       # Clase Base y Derivadas (Herencia y Polimorfismo)
│
├── services/               # Capa de Servicios y Controladores
│   ├── database.py         # Conexión remota con Supabase
│   ├── cliente_service.py  # CRUD de Clientes en base de datos
│   ├── presupuesto_service.py # Lógica de cálculo y almacenamiento de presupuestos
│   ├── config_service.py   # Lectura y guardado de parámetros locales
│   └── decorators.py       # Decoradores para validación en tiempo de ejecución
│
└── views/                  # Interfaz Gráfica de Usuario (GUI)
    ├── clientes_gui.py     # Ventana ABM de Clientes
    ├── presupuestos_gui.py # Ventana para Generar Presupuestos
    └── configuracion_gui.py # Ventana de Configuración de precios
```

---

## 📐 Diagrama de Clases (UML)

El diseño del modelo de dominio sigue los principios de la Programación Orientada a Objetos:

```mermaid
classDiagram
    class Cliente {
        -int _id_cliente
        -str _nombre
        -str _telefono
        -str _direccion
        +id_cliente() int
        +nombre() str
        +nombre(valor: str) void
        +telefono() str
        +telefono(valor: str) void
        +direccion() str
        +direccion(valor: str) void
        +__str__() str
    }

    class Presupuesto {
        +int id_presupuesto
        +Cliente cliente
        +float ancho
        +float alto
        +str tipo_vidrio
        +str tipo_abertura
        +str color
        +str fecha
        +dict config
        +float MARGEN_GANANCIA
        +procesar_presupuesto() dict
        +generar_comprobante() str
    }

    class Componente {
        +str codigo
        +str descripcion
        +float precio_base
        +calcular_costo() float
    }

    class PerfilAluminio {
        +float peso_kg_m
        +float metros_lineales
        +float factor_color
        +calcular_costo() float
    }

    class Vidrio {
        +float superficie_m2
        +calcular_costo() float
    }

    class Herraje {
        +float cantidad
        +calcular_costo() float
    }

    %% Relaciones
    Presupuesto "1" --> "1" Cliente : Agrega / Pertenece a
    Presupuesto "1" *-- "many" Componente : Contiene (Composición)
    Componente <|-- PerfilAluminio : Hereda de
    Componente <|-- Vidrio : Hereda de
    Componente <|-- Herraje : Hereda de
```

---

## 💡 Conceptos de POO Aplicados

1. **Clases y Objetos:** Representación clara de las entidades del negocio: `Cliente`, `Presupuesto`, `Componente` (y sus derivados).
2. **Encapsulamiento:** En la clase `Cliente.py`, los atributos están protegidos con prefijo `_`. El acceso y modificación de los datos se hace a través de getters y setters utilizando `@property`, validando que el nombre no sea guardado con espacios vacíos o nulos.
3. **Herencia:** La clase `Componente` actúa como clase base de la cual heredan `PerfilAluminio`, `Vidrio` y `Herraje`, reutilizando el constructor base.
4. **Polimorfismo:** Cada subclase de `Componente` sobrescribe el método `calcular_costo()` de acuerdo a su propia lógica matemática (por peso de aluminio con factor de color, por metros cuadrados de vidrio, o por cantidad de kits de herrajes). En `Presupuesto.py` se calcula el costo total iterando de forma transparente sobre la lista genérica de componentes:
   ```python
   total_materiales = sum(comp.calcular_costo() for comp in componentes)
   ```
5. **Relaciones (Asociación y Composición):**
   - **Asociación:** Un `Presupuesto` se asocia a un `Cliente`.
   - **Composición:** Un `Presupuesto` está compuesto por múltiples objetos `Componente`.

---

## ⚙️ Instrucciones de Ejecución

### 1. Requisitos Previos
Asegúrate de tener instalado Python 3.10 o superior y las bibliotecas del sistema para Tcl/Tk (necesarias para Tkinter). En sistemas Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

### 2. Configurar Entorno Virtual
Crea y activa el entorno virtual en la carpeta del proyecto:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
Instala el conector de PostgreSQL necesario para Supabase:
```bash
pip install psycopg2-binary
```

### 4. Ejecutar la Aplicación
Corre el punto de entrada principal para iniciar la interfaz gráfica:
```bash
python main.py
```

*Nota:* Si deseas realizar pruebas rápidas directamente en la terminal de comandos (sin entorno gráfico), puedes ejecutar el módulo interactivo de consola:
```bash
python -m models
```

---

## 👥 Integrantes del Grupo
* **Nombre de Integrantes** johnny pintanel - santiago varela
