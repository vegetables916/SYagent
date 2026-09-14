"""
LLM 模块 - 大模型交互层

负责：
- 统一的 LLM 客户端管理（策略模式 + 工厂模式）
- Prompt 模板管理
- LangChain chains 封装
- LangChain agents 封装
"""

from app.llm.base import BaseLLMClient
from app.llm.client import llm_client, get_llm_client, register_provider
from app.llm.openai_client import OpenAIClient
from app.llm.deepseek_client import DeepSeekClient

__all__ = [
    "BaseLLMClient",
    "OpenAIClient",
    "DeepSeekClient",
    "llm_client",
    "get_llm_client",
    "register_provider",
]
