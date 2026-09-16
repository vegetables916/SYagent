"""上下文管理器工厂"""

from typing import Callable
from app.llm.context.base import BaseContextManager
from app.llm.context.simple import SimpleContextManager
from app.llm.context.summary import SummaryContextManager
from app.llm.context.embedding import EmbeddingContextManager
from app.llm.context.hybrid import HybridContextManager

# 策略注册表
_STRATEGY_REGISTRY: dict[str, Callable[..., BaseContextManager]] = {
    "simple": SimpleContextManager,
    "summary": SummaryContextManager,
    "embedding": EmbeddingContextManager,
    "hybrid": HybridContextManager,
}


def register_context_strategy(
    name: str, 
    factory: Callable[..., BaseContextManager]
) -> None:
    """注册新的上下文策略
    
    Args:
        name: 策略名称
        factory: 工厂函数/类
    """
    _STRATEGY_REGISTRY[name] = factory


def get_context_manager(
    strategy: str = "simple",
    **kwargs
) -> BaseContextManager:
    """获取上下文管理器
    
    Args:
        strategy: 策略名称
        **kwargs: 传递给策略的参数
    
    Returns:
        上下文管理器实例
    """
    if strategy not in _STRATEGY_REGISTRY:
        available = ", ".join(_STRATEGY_REGISTRY.keys())
        raise ValueError(f"未知的上下文策略: {strategy}，可选: {available}")
    
    return _STRATEGY_REGISTRY[strategy](**kwargs)
