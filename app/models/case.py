from pydantic import BaseModel, Field


class TestPoint(BaseModel):
    __test__ = False
    title: str
    test_type: str
    reason: str
    priority: str = "中"


class TestCase(BaseModel):
    __test__ = False
    case_id: str
    name: str
    test_type: str
    priority: str
    severity: str
    preconditions: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    expected_results: list[str] = Field(default_factory=list)
    remarks: str = ""


class CoverageReport(BaseModel):
    covered_types: list[str] = Field(default_factory=list)
    missing_types: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
