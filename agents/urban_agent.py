from app.core.agent_base import AgentBase

class UrbanAgent(AgentBase):
    def run(self, question: str) -> str:
        return f"Urban Copilot Response to: {question}"
