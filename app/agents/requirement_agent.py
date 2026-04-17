from app.models.task import GenerateTaskInput, ParameterInput
from app.services.validation_service import ValidationService


class RequirementAgent:
    def __init__(self) -> None:
        self.validation_service = ValidationService()

    def parse_generate_payload(self, payload: dict) -> GenerateTaskInput:
        self.validation_service.validate_required(
            payload,
            ValidationService.REQUIRED_GENERATE_FIELDS,
        )
        return GenerateTaskInput(
            task_name=payload["task_name"],
            tool_name=payload["tool_name"],
            mode="generate",
            test_depth=payload["test_depth"],
            output_formats=payload.get("output_formats", ["markdown"]),
            feature_description=payload["feature_description"],
            parameters=[ParameterInput(**item) for item in payload.get("parameters", [])],
            flow_steps=payload.get("flow_steps", []),
            constraints=payload.get("constraints", []),
        )
