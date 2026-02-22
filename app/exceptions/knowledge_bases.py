class KnowledgeBaseNotExists(Exception):
    def __init__(self):
        super().__init__("Knowledge base not exists.")
