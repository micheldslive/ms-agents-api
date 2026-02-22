class AgentNotFoundError(ValueError):
    def __init__(self, _id: str | None):
        super().__init__(f"Agent with _id {_id} not found.")


class AgentNotExists(ValueError):
    def __init__(self):
        super().__init__("The AI Agent not exists.")
