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
