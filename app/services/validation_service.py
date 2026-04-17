class ValidationService:
    REQUIRED_GENERATE_FIELDS = ["task_name", "tool_name", "feature_description", "test_depth"]

    def validate_required(self, payload: dict, required_fields: list[str]) -> None:
        missing = [field for field in required_fields if not payload.get(field)]
        if missing:
            raise ValueError(f"缺少必填字段: {', '.join(missing)}")
