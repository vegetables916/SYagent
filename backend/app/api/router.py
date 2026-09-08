from fastapi import APIRouter
from app.api import workflows, executions, auth

api_router = APIRouter()

api_router.include_router(workflows.router, prefix="/workflows", tags=["工作流管理"])
api_router.include_router(executions.router, prefix="/executions", tags=["执行记录"])
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])