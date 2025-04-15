#!/bin/bash

# Ensure the script stops on error
set -e

# Variables
RESOURCE_GROUP="urban-copilot-rg"
APP_SERVICE_PLAN="urban-copilot-plan"
WEB_APP_NAME="urban-copilot-app"
POSTGRES_SERVER="urban-copilot-db"
POSTGRES_ADMIN="pgadmin"
POSTGRES_PASSWORD="P@ssw0rd$(date +%s)"  # Generate a secure random password
POSTGRES_DB="urbancopilotdb"
REGION="brazilsouth"
DOCKER_IMAGE="urban-copilot:latest"
COGNITIVE_SERVICE_NAME="urban-copilot-ai"
COGNITIVE_SERVICE_KIND="TextAnalytics"  # Options: TextAnalytics, ComputerVision, OpenAI, etc.

echo "=========================================="
echo "Urban Copilot Azure Deployment"
echo "=========================================="
echo "This script will deploy Urban Copilot to Azure App Service"
echo "Region: $REGION"
echo "Resource Group: $RESOURCE_GROUP"
echo "Web App: $WEB_APP_NAME"
echo "Database: $POSTGRES_SERVER"
echo "=========================================="

# Login to Azure if not already logged in
echo "Logging into Azure..."
az account show > /dev/null 2>&1 || az login

# Build and push your Docker image 
echo "Building Docker image..."
docker build -t $DOCKER_IMAGE .

# Tag image for Azure Container Registry
echo "Creating Azure Container Registry..."
ACR_NAME="${RESOURCE_GROUP//-/}acr"
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true || true
ACR_LOGIN_SERVER=$(az acr show --resource-group $RESOURCE_GROUP --name $ACR_NAME --query loginServer --output tsv)
ACR_USERNAME=$(az acr credential show --resource-group $RESOURCE_GROUP --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --resource-group $RESOURCE_GROUP --name $ACR_NAME --query passwords[0].value --output tsv)

echo "Tagging and pushing Docker image to ACR..."
docker tag $DOCKER_IMAGE $ACR_LOGIN_SERVER/$DOCKER_IMAGE
echo $ACR_PASSWORD | docker login $ACR_LOGIN_SERVER --username $ACR_USERNAME --password-stdin
docker push $ACR_LOGIN_SERVER/$DOCKER_IMAGE

# Create resource group if it doesn't exist
echo "Creating resource group if it doesn't exist..."
az group create --name $RESOURCE_GROUP --location $REGION

# Create Azure PostgreSQL server
echo "Creating Azure PostgreSQL server..."
az postgres server create \
  --name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP \
  --location $REGION \
  --admin-user $POSTGRES_ADMIN \
  --admin-password "$POSTGRES_PASSWORD" \
  --sku-name GP_Gen5_2 \
  --version 11

# Configure firewall rules for PostgreSQL
echo "Configuring PostgreSQL firewall rules..."
az postgres server firewall-rule create \
  --name AllowAllAzureServices \
  --resource-group $RESOURCE_GROUP \
  --server-name $POSTGRES_SERVER \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Create the database
echo "Creating database..."
az postgres db create \
  --name $POSTGRES_DB \
  --resource-group $RESOURCE_GROUP \
  --server-name $POSTGRES_SERVER

# Create App Service Plan
echo "Creating App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1

# Create Web App
echo "Creating Web App..."
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEB_APP_NAME \
  --deployment-container-image-name $ACR_LOGIN_SERVER/$DOCKER_IMAGE

# Create Cognitive Services resource
echo "Creating Azure Cognitive Services resource..."
az cognitiveservices account create \
  --name $COGNITIVE_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --kind $COGNITIVE_SERVICE_KIND \
  --sku S0 \
  --location $REGION \
  --yes

# Get Cognitive Services keys
echo "Retrieving Cognitive Services keys..."
COGNITIVE_KEY=$(az cognitiveservices account keys list \
  --name $COGNITIVE_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --query key1 \
  --output tsv)

COGNITIVE_ENDPOINT=$(az cognitiveservices account show \
  --name $COGNITIVE_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --query endpoint \
  --output tsv)

# Configure Web App settings
echo "Configuring Web App settings..."
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --settings \
  WEBSITES_PORT=5000 \
  SECRET_KEY="$(openssl rand -base64 24)" \
  FLASK_APP="app.server:app" \
  FLASK_ENV="production" \
  DB_USER="$POSTGRES_ADMIN@$POSTGRES_SERVER" \
  DB_PASSWORD="$POSTGRES_PASSWORD" \
  DB_HOST="$POSTGRES_SERVER.postgres.database.azure.com" \
  DB_PORT=5432 \
  DB_NAME="$POSTGRES_DB" \
  AZURE_API_KEY="$COGNITIVE_KEY" \
  AZURE_ENDPOINT="$COGNITIVE_ENDPOINT"

# Configure container settings for the Web App
echo "Configuring container settings..."
az webapp config container set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --docker-custom-image-name $ACR_LOGIN_SERVER/$DOCKER_IMAGE \
  --docker-registry-server-url https://$ACR_LOGIN_SERVER \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Enable logging
echo "Enabling logging..."
az webapp log config \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --docker-container-logging filesystem

# Restart the web app to apply changes
echo "Restarting the Web App..."
az webapp restart --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME

# Get the website URL
URL="https://$WEB_APP_NAME.azurewebsites.net"
echo "=========================================="
echo "Deployment completed successfully!"
echo "Your Urban Copilot application is now available at:"
echo "$URL"
echo ""
echo "PostgreSQL server: $POSTGRES_SERVER.postgres.database.azure.com"
echo "PostgreSQL admin: $POSTGRES_ADMIN@$POSTGRES_SERVER"
echo "PostgreSQL password: $POSTGRES_PASSWORD"
echo "PostgreSQL database: $POSTGRES_DB"
echo "=========================================="
echo "IMPORTANT: Save these database credentials in a secure location."
echo "=========================================="

# Use existing resource group and app service plan
echo "Using existing resource group: $RESOURCE_GROUP"

# Create a Web App for Containers
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --name $WEB_APP_NAME --deployment-container-image-name $DOCKER_IMAGE

# Configure the Web App to use the container
az webapp config container set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name $DOCKER_IMAGE

# Optionally set environment variables (like secret keys or DB URLs)
# az webapp config appsettings set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --settings SECRET_KEY="your_secret_key"

# Output the Web App URL
WEB_APP_URL=$(az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)
echo "Web App deployed at: https://$WEB_APP_URL"

