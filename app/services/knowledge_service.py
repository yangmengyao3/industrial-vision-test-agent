from pathlib import Path

import yaml

from app.models.knowledge import KnowledgeItem


class KnowledgeService:
    def __init__(self, base_path: str = "knowledge") -> None:
        self.base_path = Path(base_path)

    def load_all(self) -> list[KnowledgeItem]:
        items: list[KnowledgeItem] = []
        for file_path in self.base_path.rglob("*.yaml"):
            data = yaml.safe_load(file_path.read_text(encoding="utf-8"))
            if data:
                items.append(KnowledgeItem(**data))
        return items

    def search(self, keyword: str) -> list[KnowledgeItem]:
        keyword = keyword.strip().lower()
        return [
            item
            for item in self.load_all()
            if keyword in item.title.lower() or keyword in item.summary.lower()
        ]
