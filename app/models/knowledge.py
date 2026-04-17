from pydantic import BaseModel, Field


class KnowledgeParameter(BaseModel):
    name: str
    values: list[str] = Field(default_factory=list)


class KnowledgeItem(BaseModel):
    id: str
    title: str
    category: str
    applies_to: list[str] = Field(default_factory=list)
    summary: str = ""
    parameters: list[KnowledgeParameter] = Field(default_factory=list)
    test_focus: list[str] = Field(default_factory=list)
    common_risks: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    priority: str = "medium"
    enabled: bool = True
