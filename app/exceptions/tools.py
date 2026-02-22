class ToolNotExists(Exception):
    def __init__(self):
        super().__init__("Tool not exists.")
