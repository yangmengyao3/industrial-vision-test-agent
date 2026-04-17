from app.services.knowledge_service import KnowledgeService


class KnowledgeAgent:
    def __init__(self, knowledge_service: KnowledgeService | None = None) -> None:
        self.knowledge_service = knowledge_service or KnowledgeService()

    def collect(self, tool_name: str):
        return self.knowledge_service.search(tool_name.replace("工具", ""))
