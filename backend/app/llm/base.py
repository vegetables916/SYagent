"""
LLM 基础客户端 - 抽象基类

定义统一的 LLM 接口，所有模型提供商必须实现该接口
"""

from abc import ABC, abstractmethod
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage


class BaseLLMClient(ABC):
    """LLM 客户端抽象基类"""

    @property
    @abstractmethod
    def provider(self) -> str:
        """模型提供商名称"""
        ...

    @abstractmethod
    def _create_client(self) -> BaseChatModel:
        """
        创建具体的 LangChain 模型客户端（内部使用）
        
        警告：此方法不应被直接调用，请使用 `client` 属性获取单例客户端。
        直接调用此方法会破坏单例模式。
        """
        ...

    @property
    def client(self) -> BaseChatModel:
        """获取模型客户端（懒加载单例）"""
        if not hasattr(self, "_client") or self._client is None:
            self._client = self._create_client()
        return self._client

    async def chat(self, message: str, system_prompt: str | None = None) -> str:
        """
        发送聊天消息

        Args:
            message: 用户消息
            system_prompt: 系统提示词（可选）

        Returns:
            模型回复内容
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=message))

        response = await self.client.ainvoke(messages)
        return response.content
