# Urban-copilot
AI Multi-Agent System for Smart Cities. Real-time Copilot for Urban Management.

UrbanCopilot is an AI-powered multi-agent system designed to assist citizens, operators, and municipalities with real-time information and actions for smart urban environments.

## Key Features
- AI Copilot with Chat & Visual UI
- Real-time insights: traffic, energy, reports, alerts
- No expensive infrastructure required
- Modular architecture using Azure AI Agents SDK
- Scalable and easy to deploy

## Architecture
Azure + Python + LLM + Vision + RAG + Multi-Agent Orchestration.

## Use Case
Solve daily city problems directly from a conversational interface.

## Demo video
(coming soon)

## Deployment

### Prerequisites
- Docker and Docker Compose installed
- Azure account with Web App service
- `.env` file configured with necessary environment variables

### Steps
1. Build and run locally:
   ```bash
   docker-compose up --build
   ```

2. Deploy to Azure:
   - Set up Azure credentials and publish profile as GitHub secrets.
   - Push changes to the `main` branch to trigger the GitHub Actions workflow.

3. Access the app at the Azure Web App URL.

## Azure Deployment

### Setting Up Azure Services
1. **Create a Resource Group**:
   ```bash
   az group create --name urban-copilot-rg --location eastus
   ```

2. **Create an Azure App Service**:
   ```bash
   az webapp create --resource-group urban-copilot-rg --plan urban-copilot-plan --name urban-copilot-app --runtime "PYTHON|3.10"
   ```

3. **Set Up a PostgreSQL Database**:
   ```bash
   az postgres flexible-server create --resource-group urban-copilot-rg --name urban-copilot-db --admin-user admin --admin-password <your-password>
   ```

4. **Configure App Service Environment Variables**:
   Use the `azure-config.sh` script to set environment variables in Azure App Service:
   ```bash
   ./azure-config.sh
   ```

### Configuring Environment Variables
- Create a `.env` file in the root directory with the following content:
  ```env
  FLASK_ENV=production
  FLASK_DEBUG=False
  SECRET_KEY=<your-secret-key>
  DB_USER=admin
  DB_PASSWORD=<your-password>
  DB_HOST=urban-copilot-db.postgres.database.azure.com
  DB_PORT=5432
  DB_NAME=urban_copilot
  AZURE_API_KEY=<your-azure-api-key>
  AZURE_ENDPOINT=<your-azure-endpoint>
  ```

### Health Check Endpoint

The application includes a health check endpoint at `/api/health` to monitor the application's status and its dependencies. This endpoint is used by the Dockerfile's `HEALTHCHECK` directive to ensure the application is running correctly.

#### Example Response
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "api": "up",
    "cognitive_services": "up"
  }
}
```

- **Status**: Indicates the overall health of the application (`healthy` or `degraded`).
- **Version**: The current version of the application.
- **Services**: The status of critical services, such as `cognitive_services`.

If any critical service is down, the `status` will be set to `degraded`.

### Troubleshooting
- **App Not Starting**:
  - Check the logs using:
    ```bash
    az webapp log tail --name urban-copilot-app --resource-group urban-copilot-rg
    ```

- **Database Connection Issues**:
  - Verify the database credentials and ensure the database is accessible from the App Service.

- **Environment Variables Not Set**:
  - Ensure the `azure-config.sh` script was executed successfully.

- **Docker Image Build Errors**:
  - Check the Dockerfile for syntax errors or missing dependencies.

- **GitHub Actions Failing**:
  - Review the workflow logs in the GitHub Actions tab for detailed error messages.
