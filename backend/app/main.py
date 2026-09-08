from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router

app = FastAPI(
    title="AI Agent Workflow Platform",
    description="基于工作流画布的 AI Agent 开发平台",
    version="0.1.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Agent Workflow Platform API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 注册 API 路由
app.include_router(api_router, prefix=settings.API_V1_STR)