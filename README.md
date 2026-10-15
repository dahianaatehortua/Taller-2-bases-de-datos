
## Descripción del Proyecto

Este proyecto automatiza la creación y el poblado masivo de una base de datos relacional **MySQL** local, de forma autónoma y reproducible. Utiliza **SQLAlchemy** para la conexión y la definición del esquema, y la librería **Faker**, configurada con localización colombiana (`es_CO`), para generar **100.000 registros** sintéticos coherentes (nombres, ubicaciones, teléfonos y ocupaciones).

El programa verifica si la tabla de destino existe en el servidor y, si no, la crea automáticamente, sin necesidad de ejecutar scripts SQL externos.

### Inserción por lotes (Batch Processing)

Realizar 100.000 `INSERT` individuales genera una sobrecarga enorme en el motor de base de datos y puede tardar más de 15 minutos. Para evitarlo, el script agrupa los registros en memoria en **lotes de 5.000** y los envía en bloques masivos con `conn.execute()`. Así, todo el proceso termina en cuestión de segundos.

---

## Estructura de la Tabla `personas_dahiana`

La tabla se crea en la base de datos `taller_2` y tiene una clave primaria autoincremental más **8 atributos**:

| Campo | Tipo SQL | Restricción | Generador de Faker |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PK, Auto_Increment | Gestionado por MySQL |
| `nombre` | VARCHAR(50) | Not Null | `fake.first_name()` |
| `apellido` | VARCHAR(50) | Not Null | `fake.last_name()` |
| `correo` | VARCHAR(100) | Unique, Not Null | `fake.unique.email()` |
| `fecha_nacimiento` | DATE | Not Null | `fake.date_of_birth(minimum_age=18, maximum_age=90)` |
| `telefono` | VARCHAR(30) | Not Null | `fake.phone_number()` |
| `direccion` | VARCHAR(150) | Not Null | `fake.street_address()` |
| `ciudad` | VARCHAR(50) | Not Null | `fake.city()` |
| `profesion` | VARCHAR(100) | Not Null | `fake.job()` |

---

## Prerrequisitos

* Python 3.10 o superior
* Servidor MySQL local activo
* Gestor de bases de datos DBeaver
* Git instalado

---

## Instalación y Configuración

1. **Clonar el repositorio:**
```bash
   git clone https://github.com/dahianaatehortua/Taller-2-bases-de-datos.git
   cd Taller-2-bases-de-datos
```

2. **Crear y activar el entorno virtual:**
```bash
   python -m venv .venv
```
   * Windows: `.venv\Scripts\activate`
   * macOS / Linux: `source .venv/bin/activate`

3. **Instalar las dependencias:**
```bash
   pip install -r requirements.txt
```

4. **Configurar las credenciales:** duplicar el archivo `.env.example`, nombrarlo `.env` y completar tus datos locales (ver la sección siguiente).

---

## Gestión Segura de Credenciales

Este proyecto no guarda usuarios ni contraseñas dentro del código fuente. La conexión se lee dinámicamente con `python-dotenv`:

* **`.env`**: almacena localmente los datos sensibles y está protegido por `.gitignore`, por lo que nunca se sube a GitHub.
* **`.env.example`**: plantilla pública que sirve de guía para que cualquier persona pueda clonar el proyecto y configurar sus propias credenciales.

```env
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
DB_HOST=localhost
DB_PORT=3306
DB_NAME=taller_2
```

| Variable | Descripción |
| :--- | :--- |
| `DB_USER` | Usuario de MySQL con permisos de administración |
| `DB_PASSWORD` | Contraseña local del servidor |
| `DB_HOST` | Host o IP del servidor (normalmente `localhost`) |
| `DB_PORT` | Puerto del servicio MySQL (por defecto `3306`) |
| `DB_NAME` | Base de datos de destino |

---

## Ejecución

Con el servicio MySQL iniciado y el entorno virtual activo, ejecutar desde la terminal:

```bash
python main.py
```

> **Nota:** si MySQL responde que la base de datos `taller_2` no existe, créala antes desde DBeaver con `CREATE DATABASE IF NOT EXISTS taller_2;` y vuelve a ejecutar.

---

## Verificación en DBeaver

1. Crear o abrir la conexión a MySQL con los mismos datos del `.env`.
2. Refrescar la conexión (`F5`) y abrir `taller_2` → `Tables` → `personas_dahiana`.
3. Ejecutar estas consultas de comprobación:

```sql
-- Debe devolver 100000
SELECT COUNT(*) FROM personas_dahiana;

-- Vista previa de los datos
SELECT * FROM personas_dahiana LIMIT 10;
```

---

## Organización del Repositorio

El proyecto sigue principios de modularidad y buenas prácticas de seguridad:

```text
Taller-2-bases-de-datos/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

* **`main.py`**: script principal. Contiene las funciones `get_engine` (conexión), `create_table_if_not_exists` (definición del esquema), `populate_database` (inserción masiva por lotes) y `main()` como orquestador, dentro del bloque `if __name__ == "__main__":`.
* **`requirements.txt`**: dependencias necesarias para reproducir el entorno (`SQLAlchemy`, `PyMySQL`, `Faker`, `python-dotenv`, `cryptography`).
* **`.gitignore`**: excluye el entorno virtual (`.venv/`), la caché de Python (`__pycache__/`) y el archivo de credenciales (`.env`).
* **`.env.example`**: plantilla pública de variables de entorno, sin contraseñas reales.
* **`README.md`**: este manual técnico con la descripción, instalación, ejecución y validación del proyecto.