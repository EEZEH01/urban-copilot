class AgentBase:
    def run(self, question: str) -> str:
        raise NotImplementedError("This method should be implemented in subclasses")
