"""
LLM 客户端工厂

根据配置创建对应的模型客户端，支持运行时切换
"""

from app.llm.base import BaseLLMClient
from app.llm.openai_client import OpenAIClient
from app.llm.deepseek_client import DeepSeekClient
from app.llm.config import llm_settings

# 提供商注册表
_PROVIDER_REGISTRY: dict[str, type[BaseLLMClient]] = {
    "openai": OpenAIClient,
    "deepseek": DeepSeekClient,
}

# 客户端实例缓存
_client_cache: dict[str, BaseLLMClient] = {}


def register_provider(name: str, client_cls: type[BaseLLMClient]) -> None:
    """注册新的模型提供商"""
    _PROVIDER_REGISTRY[name] = client_cls


def get_llm_client(provider: str | None = None) -> BaseLLMClient:
    """
    获取 LLM 客户端

    Args:
        provider: 提供商名称，为 None 时使用默认配置

    Returns:
        对应的 LLM 客户端实例
    """
    provider = provider or settings.DEFAULT_LLM_PROVIDER

    if provider not in _client_cache:
        if provider not in _PROVIDER_REGISTRY:
            available = ", ".join(_PROVIDER_REGISTRY.keys())
            raise ValueError(f"未知的模型提供商: {provider}，可选: {available}")
        _client_cache[provider] = _PROVIDER_REGISTRY[provider]()

    return _client_cache[provider]


# 默认客户端（使用配置的默认提供商）
llm_client = get_llm_client()
