from app.agents.requirement_agent import RequirementAgent


def test_requirement_agent_parses_generate_payload():
    task = RequirementAgent().parse_generate_payload(
        {
            "task_name": "面积检测基础测试",
            "tool_name": "面积检测工具",
            "test_depth": "标准",
            "output_formats": ["markdown"],
            "feature_description": "检测矩形 ROI 面积",
        }
    )

    assert task.mode == "generate"
