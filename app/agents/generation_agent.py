from app.models.case import TestCase


class GenerationAgent:
    TYPE_CODE = {
        "功能测试": "FUNC",
        "参数测试": "PARAM",
        "流程测试": "FLOW",
        "异常测试": "EXC",
    }
    TOOL_CODE = {
        "面积检测工具": "AREA",
        "瑕疵检测工具": "DEFECT",
    }

    def generate(self, tool_name, test_points):
        code = self.TOOL_CODE.get(tool_name, "GEN")
        return [
            TestCase(
                case_id=f"VIS-{code}-{self.TYPE_CODE.get(point.test_type, 'GEN')}-{index:03d}",
                name=point.title,
                test_type=point.test_type,
                priority=point.priority,
                severity="一般",
                preconditions=["已完成基础环境准备"],
                steps=["打开工作流", f"执行：{point.title}", "记录检测结果"],
                expected_results=["系统成功输出结果", point.reason],
            )
            for index, point in enumerate(test_points, start=1)
        ]
