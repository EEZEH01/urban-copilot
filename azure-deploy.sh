#!/bin/bash

# Variables
RESOURCE_GROUP="urban-copilot-rg"
APP_SERVICE_PLAN="urban-copilot-plan"
WEB_APP_NAME="urban-copilot-app"
REGION="eastus"

# Create a resource group
az group create --name $RESOURCE_GROUP --location $REGION

# Create an App Service plan
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Create a Web App for Containers
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --name $WEB_APP_NAME --deployment-container-image-name urban-copilot:latest

# Configure the Web App to use the container
az webapp config container set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name urban-copilot:latest

# Output the Web App URL
WEB_APP_URL=$(az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)
echo "Web App deployed at: https://$WEB_APP_URL"
