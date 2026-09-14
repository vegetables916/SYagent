"""
OpenAI 客户端

基于 BaseLLMClient 实现 OpenAI 模型调用
"""

from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from app.llm.base import BaseLLMClient
from app.llm.config import llm_settings


class OpenAIClient(BaseLLMClient):
    """OpenAI 模型客户端"""

    @property
    def provider(self) -> str:
        return "openai"

    def _create_client(self) -> BaseChatModel:
        return ChatOpenAI(
            model=llm_settings.OPENAI_MODEL,
            api_key=llm_settings.OPENAI_API_KEY,
            base_url=llm_settings.OPENAI_BASE_URL,
            temperature=0.7,
            max_tokens=2000,
        )
