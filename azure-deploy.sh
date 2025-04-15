#!/bin/bash

# Ensure the script stops on error
set -e

# Variables
RESOURCE_GROUP="urban-copilot-rg"
APP_SERVICE_PLAN="urban-copilot-plan"
WEB_APP_NAME="urban-copilot-app"
REGION="eastus"
DOCKER_IMAGE="your-dockerhub-or-acr/urban-copilot:latest"  # Replace with your registry image

# Login to Azure if not already logged in
az login

# Optionally, login to container registry (if using Docker Hub or ACR)
# For Docker Hub:
# docker login --username <username> --password <password>

# For Azure Container Registry (ACR):
# az acr login --name <acr_name>

# Create a resource group
az group create --name $RESOURCE_GROUP --location $REGION

# Create an App Service plan
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# Create a Web App for Containers
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --name $WEB_APP_NAME --deployment-container-image-name $DOCKER_IMAGE

# Configure the Web App to use the container
az webapp config container set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name $DOCKER_IMAGE

# Optionally set environment variables (like secret keys or DB URLs)
# az webapp config appsettings set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --settings SECRET_KEY="your_secret_key"

# Output the Web App URL
WEB_APP_URL=$(az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)
echo "Web App deployed at: https://$WEB_APP_URL"

