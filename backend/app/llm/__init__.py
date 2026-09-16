"""
LLM 模块 - 大模型交互层

负责：
- 统一的 LLM 客户端管理（策略模式 + 工厂模式）
- 上下文管理器（对话历史管理）
- Embedding 服务（词嵌入服务）
- Prompt 模板管理
- LangChain chains 封装
- LangChain agents 封装
"""

from app.llm.base import BaseLLMClient
from app.llm.client import llm_client, get_llm_client, register_provider
from app.llm.openai_client import OpenAIClient
from app.llm.deepseek_client import DeepSeekClient
from app.llm.context import (
    BaseContextManager,
    SimpleContextManager,
    SummaryContextManager,
    HybridContextManager,
    get_context_manager,
    register_context_strategy,
)
from app.llm.embeddings import (
    BaseEmbeddingService,
    OpenAIEmbeddingService,
    get_embedding_service,
)

__all__ = [
    # 客户端
    "BaseLLMClient",
    "OpenAIClient",
    "DeepSeekClient",
    "llm_client",
    "get_llm_client",
    "register_provider",
    # 上下文管理器
    "BaseContextManager",
    "SimpleContextManager",
    "SummaryContextManager",
    "HybridContextManager",
    "get_context_manager",
    "register_context_strategy",
    # Embedding 服务
    "BaseEmbeddingService",
    "OpenAIEmbeddingService",
    "get_embedding_service",
]
