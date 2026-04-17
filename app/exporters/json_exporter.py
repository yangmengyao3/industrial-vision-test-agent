import json


class JsonExporter:
    def export(self, cases):
        return json.dumps([case.model_dump() for case in cases], ensure_ascii=False, indent=2)
