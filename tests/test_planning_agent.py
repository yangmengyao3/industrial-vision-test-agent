from app.agents.planning_agent import PlanningAgent
from app.models.task import GenerateTaskInput, ParameterInput


def test_planning_agent_generates_function_parameter_and_flow_points():
    task = GenerateTaskInput(
        task_name="面积检测标准测试",
        tool_name="面积检测工具",
        mode="generate",
        test_depth="标准",
        output_formats=["markdown"],
        feature_description="检测矩形 ROI 区域面积",
        parameters=[ParameterInput(name="面积阈值", range="1-100")],
        flow_steps=["创建方案", "添加工具", "执行检测"],
    )

    points = PlanningAgent().plan(task, [])

    assert any(point.test_type == "功能测试" for point in points)
    assert any(point.test_type == "参数测试" for point in points)
    assert any(point.test_type == "流程测试" for point in points)
