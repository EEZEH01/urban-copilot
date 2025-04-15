#!/bin/bash
cd /home/site/wwwroot
export PYTHONPATH=/home/site/wwwroot
gunicorn --bind=0.0.0.0:5000 --workers=4 app.server:app
