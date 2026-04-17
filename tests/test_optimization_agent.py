from app.agents.optimization_agent import OptimizationAgent


def test_optimization_agent_adds_missing_exception_case_suggestion():
    result = OptimizationAgent().optimize(
        raw_text="## 测试用例：VIS-AREA-FUNC-001\n仅包含基本功能测试",
        missing_types=["异常测试", "参数测试"],
        tool_name="面积检测工具",
    )

    assert "补充异常测试" in result.summary
    assert len(result.suggested_cases) >= 1
