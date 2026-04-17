import json
from pathlib import Path


class TaskService:
    def __init__(self, base_path: str = "data/tasks") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, payload: dict) -> None:
        safe_name = name.replace("/", "-").replace("\\", "-").strip() or "task"
        (self.base_path / f"{safe_name}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
