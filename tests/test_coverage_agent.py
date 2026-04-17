from app.agents.coverage_agent import CoverageAgent
from app.models.case import TestCase


def test_coverage_agent_reports_missing_exception_type():
    report = CoverageAgent().analyze(
        [TestCase(case_id="VIS-AREA-FUNC-001", name="基本功能", test_type="功能测试", priority="高", severity="严重")]
    )

    assert "异常测试" in report.missing_types
