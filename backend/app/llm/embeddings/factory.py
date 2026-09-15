"""Embedding 服务工厂"""

from typing import Callable, Dict
from app.llm.embeddings.base import BaseEmbeddingService
from app.llm.embeddings.openai_embedding import OpenAIEmbeddingService


# 服务注册表
_REGISTRY: Dict[str, Callable[..., BaseEmbeddingService]] = {
    "openai": OpenAIEmbeddingService,
}


def register_embedding_service(name: str, factory: Callable[..., BaseEmbeddingService]) -> None:
    """注册 Embedding 服务"""
    _REGISTRY[name] = factory


def get_embedding_service(provider: str = "openai", **kwargs) -> BaseEmbeddingService:
    """获取 Embedding 服务"""
    if provider not in _REGISTRY:
        available = ", ".join(_REGISTRY.keys())
        raise ValueError(f"未知的 Embedding 提供商: {provider}，可选: {available}")
    
    return _REGISTRY[provider](**kwargs)
