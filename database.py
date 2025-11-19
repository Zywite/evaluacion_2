import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Cargar variables de entorno desde .env
load_dotenv()

# --- PostgreSQL Connection Details (from environment variables) ---
DB_USER = os.getenv('DB_USER', 'joaquin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'saki7089')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'restaurant_proyect')

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Provides a new database session."""
    return SessionLocal()

def initialize_database():
    """Initializes the database and creates tables."""
    try:
        # The database itself should be created manually in PostgreSQL.
        # This function will create the tables.
        Base.metadata.create_all(bind=engine)
        print("Tablas de la base de datos aseguradas.")
    except Exception as e:
        print(f"Ocurrió un error durante la inicialización de la base de datos: {e}")
        # In a real application, you might want to handle this more gracefully.
        raise
