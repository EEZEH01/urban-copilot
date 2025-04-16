# Consolidated Dockerfile for Urban Copilot
# Supports both local and Azure deployments using build arguments

# Base image
ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION} AS builder

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies in a virtual environment
COPY requirements.txt ./
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Final image
FROM python:${PYTHON_VERSION}

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the virtual environment path
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code and startup script
COPY . .
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Expose port (default to 80 for Azure)
ARG PORT=80
ENV PORT=${PORT}
EXPOSE ${PORT}

# Add health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen(f'http://localhost:{os.getenv('PORT', 80)}/')" || exit 1

# Command to run the application
CMD ["/startup.sh"]
