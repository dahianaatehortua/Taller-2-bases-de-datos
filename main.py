import os
import math
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import (
    create_engine, MetaData, Table, Column, 
    Integer, String, Date
)


# Modifica aquí la cantidad de registros que deseas insertar:
TOTAL_REGISTROS = 100_000   # <-- ¡CAMBIA ESTE NÚMERO AQUÍ! (ej: 500, 1000, 100000)
TAMAÑO_LOTE = 5_000         # Tamaño de cada bloque de inserción masiva


# 1. Cargar variables de entorno
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "taller_2")

MI_NOMBRE = "dahiana"
NOMBRE_TABLA = f"personas_{MI_NOMBRE}"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    """Conexión a MySQL con SQLAlchemy."""
    return create_engine(DATABASE_URL, echo=False)

def create_table_if_not_exists(engine, metadata):
    """Crea la tabla personas_dahiana si no existe con PK y 8 atributos."""
    tabla_personas = Table(
        NOMBRE_TABLA,
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("nombre", String(100), nullable=False),
        Column("apellido", String(100), nullable=False),
        Column("correo", String(150), nullable=False),
        Column("fecha_nacimiento", Date, nullable=False),
        Column("telefono", String(50), nullable=False),
        Column("direccion", String(200), nullable=False),
        Column("ciudad", String(100), nullable=False),
        Column("profesion", String(100), nullable=False)
    )
    metadata.create_all(engine)
    print(f"-> Tabla '{NOMBRE_TABLA}' lista en la base de datos.")
    return tabla_personas

def populate_database(engine, tabla_personas, total_records, batch_size=5_000):
    """Limpia registros previos e inserta exactamente la cantidad configurada."""
    
    fake = Faker("es_CO")
    
    # Ajusta el lote si la cantidad configurada es menor a 5.000
    batch_size = min(batch_size, total_records) if total_records > 0 else 1
    total_batches = math.ceil(total_records / batch_size)

    with engine.begin() as conn:
        # 1. Limpieza automática previa para no acumular datos viejos
        print(f"-> Limpiando registros anteriores en '{tabla_personas.name}'...")
        conn.execute(tabla_personas.delete())
        
        # 2. Inserción de los registros nuevos
        print(f"-> Iniciando inserción de {total_records:,} registros...")

        for i in range(total_batches):
            current_batch_size = min(batch_size, total_records - (i * batch_size))
            lote = []
            
            for _ in range(current_batch_size):
                lote.append({
                    "nombre": fake.first_name(),
                    "apellido": fake.last_name(),
                    "correo": fake.unique.email(),
                    "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=80),
                    "telefono": fake.phone_number(),
                    "direccion": fake.street_address(),
                    "ciudad": fake.city(),
                    "profesion": fake.job()
                })
            
            conn.execute(tabla_personas.insert(), lote)
            print(f"   Lote {i + 1}/{total_batches} insertado exitosamente.")

    print(f"-> ¡Éxito! Se insertaron exactamente los {total_records:,} registros.")

def main():
    engine = get_engine()
    metadata = MetaData()
    tabla = create_table_if_not_exists(engine, metadata)
    
    # Usa directamente la variable configurada arriba del archivo
    populate_database(engine, tabla, total_records=TOTAL_REGISTROS, batch_size=TAMAÑO_LOTE)

if __name__ == "__main__":
    main()