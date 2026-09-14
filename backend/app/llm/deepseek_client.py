"""
DeepSeek 客户端

基于 BaseLLMClient 实现 DeepSeek 模型调用
DeepSeek 兼容 OpenAI 接口，通过修改 base_url 即可接入
"""

from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from app.llm.base import BaseLLMClient
from app.llm.config import llm_settings


class DeepSeekClient(BaseLLMClient):
    """DeepSeek 模型客户端"""

    @property
    def provider(self) -> str:
        return "deepseek"

    def _create_client(self) -> BaseChatModel:
        return ChatOpenAI(
            model=llm_settings.DEEPSEEK_MODEL,
            api_key=llm_settings.DEEPSEEK_API_KEY,
            base_url=llm_settings.DEEPSEEK_BASE_URL,
            temperature=0.7,
            max_tokens=2000,
        )
