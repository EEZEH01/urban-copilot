# Use the official Python image as the base image
FROM python:3.12-slim as builder

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

# Add health check for monitoring
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
CMD curl -f http://localhost:5000/ || exit 1

# Command to run the application
CMD ["python", "app/server.py"]

