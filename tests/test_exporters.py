from app.exporters.json_exporter import JsonExporter
from app.exporters.markdown_exporter import MarkdownExporter
from app.exporters.tree_exporter import TreeExporter
from app.models.case import TestCase


def test_markdown_exporter_includes_case_id():
    text = MarkdownExporter().export(
        [TestCase(case_id="VIS-AREA-FUNC-001", name="基本功能", test_type="功能测试", priority="高", severity="严重", steps=["添加工具"]) ]
    )

    assert "VIS-AREA-FUNC-001" in text


def test_tree_exporter_groups_cases_by_type():
    text = TreeExporter().export(
        [TestCase(case_id="VIS-AREA-FUNC-001", name="基本功能", test_type="功能测试", priority="高", severity="严重")],
        "面积检测工具测试用例",
    )

    assert "面积检测工具测试用例" in text
    assert "功能测试" in text


def test_json_exporter_outputs_case_id_field():
    text = JsonExporter().export(
        [TestCase(case_id="VIS-AREA-FUNC-001", name="基本功能", test_type="功能测试", priority="高", severity="严重")]
    )

    assert '"case_id": "VIS-AREA-FUNC-001"' in text
