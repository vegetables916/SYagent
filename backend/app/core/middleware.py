from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def register_middlewares(app: FastAPI) -> None:
    """注册所有中间件"""
    
    # CORS 跨域中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 未来可以添加更多中间件：
    # - 请求日志中间件
    # - 限流中间件
    # - 认证中间件
    # - 压缩中间件
