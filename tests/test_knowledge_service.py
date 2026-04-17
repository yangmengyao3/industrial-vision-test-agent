from app.services.knowledge_service import KnowledgeService


def test_knowledge_service_loads_tool_items():
    service = KnowledgeService(base_path="knowledge")

    items = service.load_all()

    assert any(item.title == "面积检测工具" for item in items)
