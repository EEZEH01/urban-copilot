import os

class Config:
    DEBUG = True
    AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")

config = Config()
