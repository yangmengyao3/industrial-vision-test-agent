from pydantic import BaseModel, Field

from app.models.case import TestCase


class OptimizationResult(BaseModel):
    summary: str
    missing_items: list[str] = Field(default_factory=list)
    suggested_cases: list[TestCase] = Field(default_factory=list)


class OptimizationAgent:
    def optimize(self, raw_text: str, missing_types: list[str], tool_name: str) -> OptimizationResult:
        suggested_cases: list[TestCase] = []
        if "异常测试" in missing_types:
            suggested_cases.append(
                TestCase(
                    case_id="VIS-AREA-EXC-001",
                    name=f"验证{tool_name}在错误ROI配置下的异常处理",
                    test_type="异常测试",
                    priority="高",
                    severity="一般",
                    steps=["输入错误ROI", "执行检测"],
                    expected_results=["系统提示配置异常或返回受控错误"],
                )
            )
        if "参数测试" in missing_types:
            suggested_cases.append(
                TestCase(
                    case_id="VIS-AREA-PARAM-001",
                    name=f"验证{tool_name}关键参数边界值",
                    test_type="参数测试",
                    priority="高",
                    severity="一般",
                    steps=["设置最小值", "设置最大值", "执行检测"],
                    expected_results=["边界值输入可被正确处理"],
                )
            )
        summary = "；".join([f"补充{item}" for item in missing_types])
        return OptimizationResult(summary=summary, missing_items=missing_types, suggested_cases=suggested_cases)
