#!/bin/bash
set -e

# Check if we're in Docker or Azure environment
if [ -d "/app" ]; then
    # Docker environment
    echo "Running in Docker environment"
    cd /app
    export PYTHONPATH=/app
else
    # Azure environment
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

# Make sure critical files exist
if [ ! -f "wsgi.py" ]; then
    echo "ERROR: wsgi.py not found!"
    find . -name "wsgi.py"
    exit 1
fi

# Check module structure
echo "Checking Python modules:"
if [ -d "app" ]; then
    echo "App directory found."
    find app -name "*.py" | sort
else 
    echo "WARNING: app directory not found!"
fi

# Check if environment variables are loaded
echo "Checking environment variables:"
if [ -z "$FLASK_APP" ]; then
    echo "WARNING: FLASK_APP not set, setting to app.main"
    export FLASK_APP=app.main
fi

if [ -z "$PORT" ]; then
    echo "PORT not set, using default 80"
    export PORT=80
fi

echo "Starting Gunicorn with binding 0.0.0.0:$PORT"
echo "WSGI application: wsgi:app"

# Start the application with more detailed error logging
exec gunicorn --bind=0.0.0.0:$PORT --workers=2 --log-level debug --error-logfile - --access-logfile - wsgi:app
