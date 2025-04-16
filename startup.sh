# Consolidated startup script for Urban Copilot
#!/bin/bash
set -e

# Determine environment (Docker or Azure)
if [ -d "/app" ]; then
    echo "Running in Docker environment"
    cd /app
    export PYTHONPATH=/app
else
    echo "Running in Azure environment"
    cd /home/site/wwwroot
    export PYTHONPATH=/home/site/wwwroot
fi

# Print environment info for debugging
echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Python version: $(python --version)"
echo "Directory listing:"
ls -la

# Load environment variables from .env file if present
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "WARNING: .env file not found!"
fi

# Ensure critical environment variables are set
: "${FLASK_APP:=app.main}"
: "${PORT:=80}"
export FLASK_APP PORT

# Validate critical files
if [ ! -f "wsgi.py" ]; then
    echo "ERROR: wsgi.py not found!"
    find . -name "wsgi.py"
    exit 1
fi

# Check module structure
if [ -d "app" ]; then
    echo "App directory found."
    find app -name "*.py" | sort
else
    echo "WARNING: app directory not found!"
fi

# Start the application
echo "Starting the application on port $PORT..."
gunicorn --bind 0.0.0.0:$PORT wsgi:app
