import os

class Config:
    """
    Config class to manage Flask and Azure configuration settings.
    This class uses environment variables to configure the application.
    """
    # General Flask Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # Secret key used for sessions and cryptography
    FLASK_APP = os.getenv("FLASK_APP", "main.py")  # Main entry point file for the Flask app (can be overridden by environment)
    FLASK_ENV = os.getenv("FLASK_ENV", "development")  # Environment mode, can be "development" or "production"
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"  # Enables Flask debug mode if set to "True"
    
    # Azure API Credentials
    AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")  # Azure API key to interact with Azure services
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")  # Azure endpoint URL for accessing Azure services
    
    # Database Configuration
    DB_USER = os.getenv("DB_USER", "urban_copilot_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "urban_copilot")
    
    # Construct Database URL
    if not DB_PASSWORD:
        raise ValueError("Database password must be set in environment variables")
        
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Optional: Other Configurations
    DEBUG = os.getenv("DEBUG", "True") == "True"  # General debug mode for the application; can be controlled by environment

    # Optional: Cache configuration
    CACHE_TYPE = os.getenv("CACHE_TYPE", "simple")  # Default cache type is "simple"; change for production

# Instantiate the config class to be used later
config = Config()



