from collections import defaultdict


class TreeExporter:
    def export(self, cases, title):
        groups = defaultdict(list)
        for case in cases:
            groups[case.test_type].append(case)

        lines = [title]
        group_items = list(groups.items())
        for index, (group_name, group_cases) in enumerate(group_items):
            prefix = "└──" if index == len(group_items) - 1 else "├──"
            lines.append(f"{prefix} {group_name}")
            for case in group_cases:
                lines.append(f"│   ├── {case.case_id} {case.name}")
        return "\n".join(lines)
