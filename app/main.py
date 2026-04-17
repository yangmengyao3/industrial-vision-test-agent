from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.actions import router as actions_router
from app.routes.pages import router as pages_router


def create_app() -> FastAPI:
    app = FastAPI(title="工业视觉测试用例 Agent 工作台")
    app.include_router(pages_router)
    app.include_router(actions_router, prefix="/actions")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


app = create_app()
