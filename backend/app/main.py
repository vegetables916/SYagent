from fastapi import FastAPI
from app.core.config import settings
from app.core.middleware import register_middlewares
from app.api.router import api_router

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# 注册中间件
register_middlewares(app)

@app.get("/")
async def root():
    return {"message": "AI Agent Workflow Platform API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 注册 API 路由
app.include_router(api_router, prefix=settings.API_V1_STR)