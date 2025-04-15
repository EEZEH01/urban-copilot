#!/usr/bin/env python3
"""
WSGI entry point for Urban Copilot application.
This file enables deployment to production WSGI servers like Gunicorn.
"""

from app.server import app

if __name__ == "__main__":
    # Run the application in development mode when executed directly
    app.run(host="0.0.0.0", port=5000, debug=True)
