from pydantic import BaseModel, Field


class ParameterInput(BaseModel):
    name: str
    description: str = ""
    range: str = ""
    default: str = ""
    is_key: bool = False


class GenerateTaskInput(BaseModel):
    task_name: str
    tool_name: str
    mode: str
    test_depth: str
    output_formats: list[str] = Field(default_factory=list)
    feature_description: str
    parameters: list[ParameterInput] = Field(default_factory=list)
    flow_steps: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
