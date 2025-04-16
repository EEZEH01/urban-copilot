"""
Logging configuration for Urban Copilot application.
Centralizes logging setup for consistent logging across the application.
"""

import os
import logging
import logging.handlers
import time
from flask import request, g

def setup_logging(app):
    """
    Configure application logging.
    
    Args:
        app: The Flask application instance
    """
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # Get log level from environment or default to INFO
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if in production)
    if os.environ.get('FLASK_ENV') == 'production':
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'urban-copilot.log'),
            maxBytes=10485760,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Setup request logging
    @app.before_request
    def start_timer():
        g.start = time.time()
    
    @app.after_request
    def log_request(response):
        if request.path != '/api/health':  # Don't log health checks
            now = time.time()
            duration = round(now - g.start, 2)
            log_data = {
                'method': request.method,
                'path': request.path,
                'status': response.status_code,
                'duration': duration,
                'ip': request.remote_addr,
            }
            
            app.logger.info(f"Request: {log_data}")
        
        return response
    
    return root_logger
