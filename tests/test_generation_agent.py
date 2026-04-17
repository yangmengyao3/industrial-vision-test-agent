from app.agents.generation_agent import GenerationAgent
from app.models.case import TestPoint


def test_generation_agent_turns_points_into_cases():
    cases = GenerationAgent().generate(
        "面积检测工具",
        [TestPoint(title="验证面积检测工具基本功能", test_type="功能测试", reason="主功能验证", priority="高")],
    )

    assert cases[0].case_id == "VIS-AREA-FUNC-001"
