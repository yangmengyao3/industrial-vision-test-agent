from pathlib import Path


class TemplateService:
    def __init__(self, base_path: str = "prompts") -> None:
        self.base_path = Path(base_path)

    def read(self, relative_path: str) -> str:
        return (self.base_path / relative_path).read_text(encoding="utf-8")
