# app/agents/urban_agent.py
from app.core.agent_base import AgentBase

class UrbanAgent(AgentBase):
    """
    A specific agent for urban-related questions. Inherits from AgentBase and implements
    the 'run' method to provide specific responses related to urban topics.
    """
    def __init__(self):
        """
        Initialize the agent. You can load data, models, or any setup here if needed.
        """
        super().__init__()  # Call the parent constructor to ensure proper initialization

    def run(self, question: str) -> str:
        """
        Implement the logic for handling a question related to urban topics.

        Parameters:
        - question (str): The question to be answered by the agent.

        Returns:
        - str: The response to the question.
        """
        # Example logic: UrbanAgent returns a static response
        return f"Urban Copilot Response to: {question}"

