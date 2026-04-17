from app.models.case import TestPoint


class PlanningAgent:
    def plan(self, task, knowledge_items):
        points = [
            TestPoint(
                title=f"验证{task.tool_name}基本功能",
                test_type="功能测试",
                reason="主功能验证",
                priority="高",
            )
        ]
        for parameter in task.parameters:
            points.append(
                TestPoint(
                    title=f"验证参数 {parameter.name} 的边界与典型值",
                    test_type="参数测试",
                    reason="参数存在明确范围",
                    priority="高" if parameter.is_key else "中",
                )
            )
        if len(task.flow_steps) >= 3:
            points.append(
                TestPoint(
                    title=f"验证{task.tool_name}完整流程执行",
                    test_type="流程测试",
                    reason="需要验证端到端流程",
                    priority="高",
                )
            )
        for item in knowledge_items:
            for risk in item.common_risks:
                points.append(
                    TestPoint(
                        title=f"验证异常风险：{risk}",
                        test_type="异常测试",
                        reason="知识库风险补充",
                        priority="中",
                    )
                )
        return points
