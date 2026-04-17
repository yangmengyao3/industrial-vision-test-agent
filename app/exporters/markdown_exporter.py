class MarkdownExporter:
    def export(self, cases):
        return "\n\n".join(
            [
                f"## 测试用例：{case.case_id}\n\n### 测试步骤\n"
                + "\n".join(f"{index}. {step}" for index, step in enumerate(case.steps, 1))
                for case in cases
            ]
        )
