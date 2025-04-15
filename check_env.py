#!/usr/bin/env python3
"""
Environment variable checker for Urban Copilot
This script validates that all required environment variables are set correctly.
"""

import os
import sys
import json
from dotenv import load_dotenv
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

# Define required and optional environment variables
REQUIRED_VARS = [
    "SECRET_KEY",
    "FLASK_APP",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST", 
    "DB_PORT",
    "DB_NAME"
]

OPTIONAL_VARS = [
    "FLASK_ENV",
    "FLASK_DEBUG",
    "AZURE_API_KEY",
    "AZURE_ENDPOINT",
    "LOG_LEVEL"
]

def print_status(message, status="ok", details=None):
    """Print a status message with appropriate coloring."""
    if status == "ok":
        color = Fore.GREEN
        symbol = "✓"
    elif status == "warning":
        color = Fore.YELLOW
        symbol = "!"
    elif status == "error":
        color = Fore.RED
        symbol = "✗"
    else:  # info
        color = Fore.BLUE
        symbol = "i"
    
    print(f"{color}{symbol} {message}{Style.RESET_ALL}")
    
    if details:
        print(f"  {details}")

def create_example_env():
    """Create an example .env file if none exists."""
    if Path(".env").exists():
        return False
        
    with open(".env.example", "w") as f:
        f.write("""# Urban Copilot Environment Variables
# Make a copy of this file named .env and fill in your values

# Flask settings
SECRET_KEY=your_secret_key_here
FLASK_APP=app.server:app
FLASK_ENV=development
FLASK_DEBUG=1

# Database settings
DB_USER=urban_copilot_user
DB_PASSWORD=your_password_here
DB_HOST=db
DB_PORT=5432
DB_NAME=urban_copilot

# Azure settings (if applicable)
# AZURE_API_KEY=your_azure_api_key
# AZURE_ENDPOINT=https://your-azure-endpoint.openai.azure.com

# Logging
LOG_LEVEL=INFO
""")
    return True

def check_env_variables():
    """Check if all required environment variables are set."""
    # Try to load variables from .env file
    env_file = Path(".env")
    if env_file.exists():
        print_status(f"Found .env file at {env_file.absolute()}", "info")
        load_dotenv(env_file)
    else:
        if create_example_env():
            print_status(f"Created example .env file (.env.example). Please configure it!", "warning")
        else:
            print_status("No .env file found. Checking environment variables directly.", "warning")
    
    # Check required variables
    missing = []
    for var in REQUIRED_VARS:
        if var in os.environ and os.environ[var]:
            masked_value = "***" if "PASSWORD" in var or "KEY" in var else os.environ[var]
            print_status(f"{var} = {masked_value}")
        else:
            print_status(f"{var} is not set", "error")
            missing.append(var)
    
    # Check optional variables
    for var in OPTIONAL_VARS:
        if var in os.environ and os.environ[var]:
            masked_value = "***" if "PASSWORD" in var or "KEY" in var else os.environ[var]
            print_status(f"{var} = {masked_value}")
        else:
            print_status(f"{var} is not set (optional)", "warning")
    
    # Generate database connection example
    db_vars = {var: os.environ.get(var, "") for var in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]}
    all_db_vars_set = all(db_vars.values())
    
    if all_db_vars_set:
        print_status("\nDatabase connection string:", "info")
        print(f"postgresql://{db_vars['DB_USER']}:***@{db_vars['DB_HOST']}:{db_vars['DB_PORT']}/{db_vars['DB_NAME']}")
        print("\nTo test the connection:")
        print(f"PGPASSWORD='{db_vars['DB_PASSWORD']}' psql -h {db_vars['DB_HOST']} -p {db_vars['DB_PORT']} -U {db_vars['DB_USER']} -d {db_vars['DB_NAME']} -c 'SELECT 1;'")
    
    # Summary
    if missing:
        print_status(f"\n{len(missing)} required environment variables are missing! Please set them in your .env file.", "error")
        return False
    else:
        print_status("\nAll required environment variables are set correctly!", "ok")
        return True

if __name__ == "__main__":
    print("===== Urban Copilot Environment Checker =====\n")
    result = check_env_variables()
    sys.exit(0 if result else 1)
