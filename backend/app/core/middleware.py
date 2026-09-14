from fastapi import FastAPI


def register_middlewares(app: FastAPI) -> None:
    """注册所有中间件"""

    # 未来可以添加更多中间件：
    # - 请求日志中间件
    # - 限流中间件
    # - 认证中间件
    # - 压缩中间件
