from fastapi import Request, HTTPException, status
from app.core.redis import get_redis

# 限流配置
REGISTER_LIMIT_PER_HOUR = 5  # 每小时最多注册次数
LOGIN_LIMIT_PER_MINUTE = 5   # 每分钟最多登录尝试次数


def check_register_limit(ip: str) -> None:
    """
    检查注册频率限制
    - 同一 IP 每小时最多注册 5 次
    - 超限抛出 429 Too Many Requests
    """
    redis = get_redis()
    key = f"rate_limit:register:{ip}"
    
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 3600)  # 1小时过期
    
    if count > REGISTER_LIMIT_PER_HOUR:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"注册次数过多，请1小时后再试（当前：{count}/{REGISTER_LIMIT_PER_HOUR}）"
        )


def check_login_limit(ip: str) -> None:
    """
    检查登录频率限制
    - 同一 IP 每分钟最多尝试 5 次
    - 超限抛出 429 Too Many Requests
    """
    redis = get_redis()
    key = f"rate_limit:login:{ip}"
    
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)  # 1分钟过期
    
    if count > LOGIN_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"登录尝试过多，请1分钟后再试（当前：{count}/{LOGIN_LIMIT_PER_MINUTE}）"
        )


def get_client_ip(request: Request) -> str:
    """获取客户端真实 IP"""
    # 优先从 X-Forwarded-For 获取（如果有反向代理）
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
