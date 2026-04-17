from fastapi.testclient import TestClient

from app.main import create_app


def test_dashboard_page_loads():
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert "工业视觉测试用例 Agent 工作台" in response.text


def test_generate_page_loads_form_sections():
    client = TestClient(create_app())

    response = client.get("/generate")

    assert response.status_code == 200
    assert "功能描述" in response.text
    assert "参数配置" in response.text


def test_generate_action_returns_result_panel_html():
    client = TestClient(create_app())

    response = client.post(
        "/actions/generate",
        json={
            "task_name": "面积检测标准测试",
            "tool_name": "面积检测工具",
            "test_depth": "标准",
            "output_formats": ["markdown"],
            "feature_description": "检测矩形 ROI 面积",
            "flow_steps": ["创建方案", "添加工具", "执行检测"],
            "parameters": [{"name": "面积阈值", "range": "1-100"}],
        },
    )

    assert response.status_code == 200
    assert "测试点" in response.text
    assert "覆盖分析" in response.text
