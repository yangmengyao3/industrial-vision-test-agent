from app.models.case import CoverageReport


class CoverageAgent:
    EXPECTED_TYPES = ["功能测试", "参数测试", "流程测试", "异常测试"]

    def analyze(self, cases):
        covered = sorted({case.test_type for case in cases})
        missing = [test_type for test_type in self.EXPECTED_TYPES if test_type not in covered]
        risks = [f"缺少{test_type}" for test_type in missing]
        return CoverageReport(covered_types=covered, missing_types=missing, risks=risks)
