#!/bin/bash

# Azure configuration script for Urban Copilot
# This script helps set up environment variables in Azure App Service

# Replace these variables with your actual Azure resources
RESOURCE_GROUP="urban-copilot-rg"
APP_SERVICE_NAME="urban-copilot-app"
POSTGRES_SERVER_NAME="urban-copilot-db"

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

# Log in to Azure (remove this if running in CI/CD pipeline with service principal)
echo "Logging in to Azure..."
az account show > /dev/null 2>&1 || az login

# Configure App Service environment variables
echo "Setting environment variables in Azure App Service..."
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_SERVICE_NAME --settings \
    SECRET_KEY="$SECRET_KEY" \
    FLASK_APP="$FLASK_APP" \
    FLASK_ENV="$FLASK_ENV" \
    DB_USER="$DB_USER@$POSTGRES_SERVER_NAME" \
    DB_PASSWORD="$DB_PASSWORD" \
    DB_HOST="$POSTGRES_SERVER_NAME.postgres.database.azure.com" \
    DB_PORT="$DB_PORT" \
    DB_NAME="$DB_NAME" \
    AZURE_API_KEY="$AZURE_API_KEY" \
    AZURE_ENDPOINT="$AZURE_ENDPOINT" \
    CACHE_TYPE="$CACHE_TYPE"

echo "Environment variables configured successfully!"
az login

# Configure App Service environment variables
echo "Setting environment variables in Azure App Service..."
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_SERVICE_NAME --settings \
    SECRET_KEY="$SECRET_KEY" \
    FLASK_APP="$FLASK_APP" \
    FLASK_ENV="$FLASK_ENV" \
    DB_USER="$DB_USER" \
    DB_PASSWORD="$DB_PASSWORD" \
    DB_HOST="$POSTGRES_SERVER_NAME.postgres.database.azure.com" \
    DB_PORT="$DB_PORT" \
    DB_NAME="$DB_NAME" \
    AZURE_API_KEY="$AZURE_API_KEY" \
    AZURE_ENDPOINT="$AZURE_ENDPOINT" \
    CACHE_TYPE="$CACHE_TYPE"

echo "Environment variables configured successfully!"
