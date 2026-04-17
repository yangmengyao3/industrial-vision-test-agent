from app.models.task import GenerateTaskInput


def test_generate_task_input_parses_parameters_and_steps():
    task = GenerateTaskInput(
        task_name="面积检测测试",
        tool_name="面积检测工具",
        mode="generate",
        test_depth="标准",
        output_formats=["markdown"],
        feature_description="检测区域面积",
        parameters=[{"name": "面积阈值", "range": "1-100"}],
        flow_steps=["创建方案", "添加工具", "执行检测"],
    )

    assert task.parameters[0].name == "面积阈值"
    assert len(task.flow_steps) == 3
