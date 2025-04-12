import os

class Config:
    # General Flask Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # Clave secreta para la app (importante para sesiones)
    FLASK_APP = os.getenv("FLASK_APP", "main.py")  # Archivo principal para ejecutar Flask
    FLASK_ENV = os.getenv("FLASK_ENV", "development")  # Establecer si está en desarrollo o producción
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"  # Si debe estar en modo de depuración
    
    # Azure API Credentials
    AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")  # Clave API de Azure
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")  # Punto de conexión de Azure
    
    # Database Configuration (si usas base de datos)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db/development.db")  # Base de datos por defecto (puedes cambiar a PostgreSQL, etc.)
    
    # Optional: Other Configurations
    DEBUG = os.getenv("DEBUG", "True") == "True"  # Modo de depuración de la app (puedes ajustarlo)

config = Config()

