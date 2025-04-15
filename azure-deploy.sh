#!/bin/bash

# Ensure the script stops on error
set -e

# Variables
RESOURCE_GROUP="urban-copilot-rg"
APP_SERVICE_PLAN="urban-copilot-plan-east"
WEB_APP_NAME="urban-copilot-app"
POSTGRES_SERVER="urban-copilot-db"
POSTGRES_ADMIN="pgadmin"
POSTGRES_PASSWORD="P@ssw0rd$(date +%s)"  # Generate a secure random password
POSTGRES_DB="urbancopilotdb"
REGION="eastus"  # Match existing resource group location
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

# Check if PostgreSQL server exists
echo "Checking if PostgreSQL server exists..."
PG_SERVER_EXISTS=$(az postgres server show \
  --resource-group $RESOURCE_GROUP \
  --name $POSTGRES_SERVER > /dev/null 2>&1 && echo "true" || echo "false")

if [[ "$PG_SERVER_EXISTS" == "true" ]]; then
  echo "PostgreSQL server '$POSTGRES_SERVER' already exists, retrieving connection info..."
  
  # Get the admin username from the existing server
  POSTGRES_ADMIN=$(az postgres server show \
    --resource-group $RESOURCE_GROUP \
    --name $POSTGRES_SERVER \
    --query administratorLogin \
    --output tsv)
    
  echo "Using existing PostgreSQL admin: $POSTGRES_ADMIN"
  
  # Get existing database or create if it doesn't exist
  echo "Checking if database '$POSTGRES_DB' exists..."
  DB_EXISTS=$(az postgres db show \
    --resource-group $RESOURCE_GROUP \
    --server-name $POSTGRES_SERVER \
    --name $POSTGRES_DB > /dev/null 2>&1 && echo "true" || echo "false")
    
  if [[ "$DB_EXISTS" == "false" ]]; then
    echo "Database '$POSTGRES_DB' doesn't exist, creating it..."
    az postgres db create \
      --name $POSTGRES_DB \
      --resource-group $RESOURCE_GROUP \
      --server-name $POSTGRES_SERVER
  else
    echo "Using existing database: $POSTGRES_DB"
  fi
else
  # Create Azure PostgreSQL server if it doesn't exist
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
fi

# Ensure firewall rule exists
echo "Ensuring firewall rule exists for Azure Services..."
az postgres server firewall-rule create \
  --name AllowAllAzureServices \
  --resource-group $RESOURCE_GROUP \
  --server-name $POSTGRES_SERVER \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0 \
  --output none 2>/dev/null || true

# Create App Service Plan
echo "Creating App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1 \
  --location brazilsouth  # Using brazilsouth specifically for App Service

# Create Web App with Container
echo "Creating Web App..."
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEB_APP_NAME \
  --deployment-container-image-name $ACR_LOGIN_SERVER/$DOCKER_IMAGE

# Configure Web App settings
echo "Configuring Web App settings..."
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --settings \
  DATABASE_URL="postgresql://$POSTGRES_ADMIN@$POSTGRES_SERVER:$POSTGRES_PASSWORD@$POSTGRES_SERVER.postgres.database.azure.com:5432/$POSTGRES_DB" \
  FLASK_APP="app.main" \
  FLASK_ENV="production"

# Create Azure Cognitive Services resource
echo "Creating Azure Cognitive Services resource..."
az cognitiveservices account create \
  --name $COGNITIVE_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --kind $COGNITIVE_SERVICE_KIND \
  --sku F0 \
  --location $REGION

# If the above command fails, try with a different kind or inform the user
if [ $? -ne 0 ]; then
  echo "Note: Failed to create Cognitive Services. You may need to:"
  echo "  1. Request quota increase for TextAnalytics"
  echo "  2. Set up Cognitive Services manually from the Azure Portal"
  echo "  3. Use a different Cognitive Service type"
  echo "Continuing with deployment without Cognitive Services..."
fi

# Restart the web app to apply settings
echo "Restarting Web App..."
az webapp restart --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

echo "======================================================================================="
echo "Deployment complete! Your Urban Copilot application is now running on Azure App Service."
echo "Web App URL: https://$WEB_APP_NAME.azurewebsites.net"
echo "======================================================================================="

# Display PostgreSQL connection string
echo "PostgreSQL Connection String:"
echo "postgresql://$POSTGRES_ADMIN@$POSTGRES_SERVER:$POSTGRES_PASSWORD@$POSTGRES_SERVER.postgres.database.azure.com:5432/$POSTGRES_DB"

