# app/core/agent_base.py
class AgentBase:
    """
    A base class for agents. This class defines a contract that all agents must follow.
    The 'run' method must be implemented in any subclass.
    """
    def run(self, question: str) -> str:
        """
        Abstract method to process a question and return a response.
        This method must be implemented in any subclass.

        Parameters:
        - question (str): The question to be answered by the agent.

        Returns:
        - str: The response to the question.
        """
        raise NotImplementedError("This method should be implemented in subclasses")
