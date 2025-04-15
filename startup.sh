#!/bin/bash
# Check if we're in Docker or Azure environment
if [ -d "/app" ]; then
    # Docker environment
    cd /app
    export PYTHONPATH=/app
else
    # Azure environment
    cd /home/site/wwwroot
    export PYTHONPATH=/home/site/wwwroot
fi

# Print environment info for debugging
echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Directory listing:"
ls -la

# Use the correct WSGI application path (wsgi.py at the root)
gunicorn --bind=0.0.0.0:80 --workers=2 --log-level debug wsgi:app
