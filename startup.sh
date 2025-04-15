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

gunicorn --bind=0.0.0.0:5000 --workers=4 app.server:app
