# Use the official Python image as the base image
FROM python:3.12-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies in a virtual environment in a single step
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Final image (production-ready)
FROM python:3.12-slim

# Set the working directory before copying files
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the virtual environment path to use the correct pip
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.server:app

# Add health check for monitoring
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
CMD curl -f http://localhost:5000/ || exit 1

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.server:app"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
CMD curl -f http://localhost:5000/ || exit 1

# Set Python path and working directory
ENV PYTHONPATH=/app
WORKDIR /app

# Command to run the application using our startup script
COPY startup.sh /
RUN chmod +x /startup.sh
CMD ["/startup.sh"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
CMD curl -f http://localhost:5000/ || exit 1

# Command to run the application
CMD ["python", "app/server.py"]

