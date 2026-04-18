from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.knowledge_service import KnowledgeService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "pages/dashboard.html",
        {"page_title": "工业视觉测试用例 Agent 工作台"},
    )


@router.get("/generate", response_class=HTMLResponse)
def generate_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "pages/generate.html",
        {"page_title": "从零生成"},
    )


@router.get("/optimize", response_class=HTMLResponse)
def optimize_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "pages/optimize.html",
        {"page_title": "用例优化"},
    )


@router.get("/knowledge", response_class=HTMLResponse)
def knowledge_page(request: Request) -> HTMLResponse:
    knowledge_items = KnowledgeService().load_all()
    return templates.TemplateResponse(
        request,
        "pages/knowledge.html",
        {"page_title": "知识库管理", "knowledge_items": knowledge_items},
    )
