from fastapi.testclient import TestClient

from app.main import create_app



def test_dashboard_page_loads():
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert "工业视觉测试用例 Agent 工作台" in response.text
    assert "新建生成任务" in response.text



def test_generate_page_loads_form_sections():
    client = TestClient(create_app())

    response = client.get("/generate")

    assert response.status_code == 200
    assert "功能描述" in response.text
    assert "参数配置" in response.text
    assert "生成测试点" in response.text
    assert "生成完整测试用例" in response.text
    assert 'id="generate-form"' in response.text



def test_optimize_page_loads_targets_and_textarea():
    client = TestClient(create_app())

    response = client.get("/optimize")

    assert response.status_code == 200
    assert "优化目标" in response.text
    assert "补边界值测试" in response.text
    assert "开始优化" in response.text
    assert 'id="optimize-form"' in response.text



def test_knowledge_page_shows_seeded_knowledge_items():
    client = TestClient(create_app())

    response = client.get("/knowledge")

    assert response.status_code == 200
    assert "面积检测工具" in response.text
    assert "瑕疵检测工具" in response.text



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
    assert "功能测试" in response.text
    assert "导出结果" in response.text
    assert "Markdown" in response.text
    assert "JSON" in response.text
    assert "树形文本" in response.text



def test_optimize_action_returns_suggested_cases():
    client = TestClient(create_app())

    response = client.post(
        "/actions/optimize",
        json={
            "tool_name": "面积检测工具",
            "raw_text": "## 测试用例：VIS-AREA-FUNC-001\n仅包含基本功能测试",
        },
    )

    assert response.status_code == 200
    assert "异常测试" in response.text
    assert "参数测试" in response.text
    assert "导出结果" in response.text



def test_generate_action_accepts_form_payload():
    client = TestClient(create_app())

    response = client.post(
        "/actions/generate",
        data={
            "task_name": "面积检测表单测试",
            "tool_name": "面积检测工具",
            "test_depth": "标准",
            "output_formats": "markdown",
            "feature_description": "表单提交触发生成",
            "flow_steps": "创建方案\n添加工具\n执行检测",
            "parameter_names": ["面积阈值"],
            "parameter_ranges": ["1-100"],
            "parameter_descriptions": ["控制合格判定"],
        },
    )

    assert response.status_code == 200
    assert "VIS-AREA-FUNC-001" in response.text
    assert "copy-export" in response.text



def test_optimize_action_accepts_form_payload():
    client = TestClient(create_app())

    response = client.post(
        "/actions/optimize",
        data={
            "tool_name": "面积检测工具",
            "raw_text": "## 测试用例：VIS-AREA-FUNC-001\n仅包含基本功能测试",
        },
    )

    assert response.status_code == 200
    assert "VIS-AREA-EXC-001" in response.text



def test_export_result_endpoint_returns_markdown_text():
    client = TestClient(create_app())

    response = client.post(
        "/actions/export",
        json={
            "format": "markdown",
            "cases": [
                {
                    "case_id": "VIS-AREA-FUNC-001",
                    "name": "基本功能",
                    "test_type": "功能测试",
                    "priority": "高",
                    "severity": "严重",
                    "steps": ["添加工具"],
                }
            ],
            "title": "面积检测工具测试用例",
        },
    )

    assert response.status_code == 200
    assert "## 测试用例：VIS-AREA-FUNC-001" in response.text
