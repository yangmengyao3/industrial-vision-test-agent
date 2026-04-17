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


@router.post("/generate")
async def generate_action(request: Request):
    payload = await request.json()
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
    payload = await request.json()
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
