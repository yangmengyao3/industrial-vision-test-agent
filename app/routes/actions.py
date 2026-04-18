from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.agents.coverage_agent import CoverageAgent
from app.agents.generation_agent import GenerationAgent
from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.optimization_agent import OptimizationAgent
from app.agents.planning_agent import PlanningAgent
from app.agents.requirement_agent import RequirementAgent
from app.services.task_service import TaskService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _normalize_generate_payload(form_data) -> dict:
    parameter_names = form_data.getlist("parameter_names")
    parameter_ranges = form_data.getlist("parameter_ranges")
    parameter_descriptions = form_data.getlist("parameter_descriptions")
    parameters = []
    for index, name in enumerate(parameter_names):
        if not name.strip():
            continue
        parameters.append(
            {
                "name": name,
                "range": parameter_ranges[index] if index < len(parameter_ranges) else "",
                "description": parameter_descriptions[index] if index < len(parameter_descriptions) else "",
            }
        )
    flow_steps = [item.strip() for item in form_data.get("flow_steps", "").splitlines() if item.strip()]
    output_formats = form_data.getlist("output_formats") or [form_data.get("output_formats", "markdown")]
    return {
        "task_name": form_data.get("task_name", ""),
        "tool_name": form_data.get("tool_name", ""),
        "test_depth": form_data.get("test_depth", "标准"),
        "output_formats": output_formats,
        "feature_description": form_data.get("feature_description", ""),
        "flow_steps": flow_steps,
        "parameters": parameters,
    }


async def _get_payload(request: Request) -> dict:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        return await request.json()
    form_data = await request.form()
    return dict(form_data) if False else form_data


@router.post("/generate")
async def generate_action(request: Request):
    payload_source = await _get_payload(request)
    payload = payload_source if isinstance(payload_source, dict) else _normalize_generate_payload(payload_source)
    task = RequirementAgent().parse_generate_payload(payload)
    knowledge_items = KnowledgeAgent().collect(task.tool_name)
    test_points = PlanningAgent().plan(task, knowledge_items)
    test_cases = GenerationAgent().generate(task.tool_name, test_points)
    coverage = CoverageAgent().analyze(test_cases)
    TaskService().save(task.task_name, payload)
    context = {
        "request": request,
        "test_points": test_points,
        "test_cases": test_cases,
        "coverage": coverage,
    }
    return templates.TemplateResponse(request, "partials/result_panel.html", context)


@router.post("/optimize")
async def optimize_action(request: Request):
    payload_source = await _get_payload(request)
    if isinstance(payload_source, dict):
        payload = payload_source
    else:
        payload = {
            "tool_name": payload_source.get("tool_name", ""),
            "raw_text": payload_source.get("raw_text", ""),
        }
    result = OptimizationAgent().optimize(
        raw_text=payload["raw_text"],
        missing_types=["异常测试", "参数测试"],
        tool_name=payload["tool_name"],
    )
    context = {
        "request": request,
        "test_points": [],
        "test_cases": result.suggested_cases,
        "coverage": {"missing_types": result.missing_items, "risks": [result.summary]},
    }
    return templates.TemplateResponse(request, "partials/result_panel.html", context)
